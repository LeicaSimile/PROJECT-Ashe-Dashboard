import logging
import logging.config
import os.path
import random
import re
import sqlite3

FILE_DATABASE = "database/project-ashe.db"


## === Functions === ##
def clean(line):
    """ Strip a string of non-alphanumerics (except underscores).
    Can use to clean strings before using them in a database query.

    Args:
        line(unicode): String to clean.

    Returns:
        line(unicode): A string safe to use in a database query.

    Examples:
        >>> clean("Robert'); DROP TABLE Students;")
        RobertDROPTABLEStudents
    """
    return "".join(char for char in line if (char.isalnum() or "_" == char))

def parse_cases(text):
    """ Changes substring's letter case (uppercase, lowercase, start case, sentence case).

    Args:
        text(unicode): String to parse.
    """
    markersUpper = (re.escape(get_setting("Variables", "open_upper")),
                    re.escape(get_setting("Variables", "close_upper"))
                    )
    markersLower = (re.escape(get_setting("Variables", "open_lower")),
                    re.escape(get_setting("Variables", "close_lower"))
                    )
    markersStart = (re.escape(get_setting("Variables", "open_startcase")),
                    re.escape(get_setting("Variables", "close_startcase"))
                    )
    markersSentence = (re.escape(get_setting("Variables", "open_sentence")),
                       re.escape(get_setting("Variables", "close_sentence"))
                       )
    
    for result in re.finditer(r"{}(.*?){}".format(markersUpper[0], markersUpper[1]), text):
        ## Uppercase -> "ALL MY LIFE HAS BEEN A SERIES OF DOORS IN MY FACE."
        text = text.replace(result.group(), result.group(1).upper())

    for result in re.finditer(r"{}(.*?){}".format(markersLower[0], markersLower[1]), text):
        ## Lowercase -> "all my life has been a series of doors in my face."
        text = text.replace(result.group(), result.group(1).lower())

    for result in re.finditer(r"{}(.*?){}".format(markersStart[0], markersStart[1]), text):
        text = text.replace(result.group(), titlecase(result.group(1)))

    for result in re.finditer(r"{}(.*?){}".format(markersSentence[0], markersSentence[1]), text):
        ## Sentence case -> "All my life has been a series of doors in my face."
        newCase = result.group(1)
        
        for index, character in enumerate(newCase):
            if character.isalpha():
                text = text.replace(result.group(), newCase[:index] + newCase[index:].capitalize())
                break
        
        
    return text

def parse_choices(text):
    """ Chooses a random option in a given set.

    Args:
        text(unicode): String to parse. Options are enclosed in angle brackets, separated by a pipeline.

    Yields:
        newString(unicode): An option from the leftmost set of options is chosen for the string and updates accordingly.

    Raises:
        StopIteration: text's options are all chosen.

    Examples:
        >>> next(parse_choices("<Chocolates|Sandwiches> are the best!"))
        "Chocolates are the best!"

        >>> result = parse_choices("I would like some <cupcakes|ice cream>, <please|thanks>.")
        >>> for _ in result: print(next(result))
        I would like some <cupcakes|ice cream>, thanks.
        I would like some cupcakes, thanks.
    """

    OPEN_CHAR = get_setting("Variables", "open_choose")
    CLOSE_CHAR = get_setting("Variables", "close_choose")
    ESCAPE_CHAR = get_setting("Variables", "escape")
    SPLITTER = get_setting("Variables", "parse_choose")
    done = False

    while not done:
        if OPEN_CHAR not in text or CLOSE_CHAR not in text:
            done = True
            
        level = 0
        escapeNum = 0
        openIndex = 0
        closeIndex = 0
        optionNum = 0
        options = []
        
        for index, char in enumerate(text):
            if OPEN_CHAR == char and not escapeNum % 2:
                level += 1
                if 1 == level:
                    openIndex = index
                    options.append([])
                elif level:
                    options[optionNum].append(char)
            elif CLOSE_CHAR == char and not escapeNum % 2:
                level -= 1
                if 0 == level:
                    ## First and outermost level gathered.
                    closeIndex = index
                    break
                elif level:
                    options[optionNum].append(char)
            elif SPLITTER == char and not escapeNum % 2:
                if 1 == level:
                    optionNum += 1
                    options.append([])
                elif level:
                    options[optionNum].append(char)
            elif ESCAPE_CHAR == char:
                escapeNum += 1
                if level:
                    options[optionNum].append(char)
            else:
                escapeNum = 0
                if level:
                    options[optionNum].append(char)
                
        tmpBlock = text[openIndex:closeIndex + 1]
        
        if 1 < len(tmpBlock):
            text = text.replace(tmpBlock, "".join(random.choice(options)))
        else:
            done = True
            
        yield text
    
def parse_optional(text):
    """ Chooses whether to omit a substring or not.

    Args:
        text(unicode): String to parse. Substring to be reviewed is enclosed in braces.

    Yields:
        text(unicode): The string with or without the leftmost substring, stripped of the braces.

    Raises:
        StopIteration: text's braces are fully parsed.

    Examples:
        >>> next(parse_optional("You're mean{ingful}."))
        "You're meaningful."

        >>> result = parse_optional("You're pretty{{ darn} awful}.")
        >>> for _ in result: print(next(result))
        You're pretty{ darn} awful.
        You're pretty awful.
    """
    
    OPEN_CHAR = get_setting("Variables", "open_omit")
    CLOSE_CHAR = get_setting("Variables", "close_omit")
    ESCAPE_CHAR = get_setting("Variables", "escape")
    done = False

    while not done:
        if OPEN_CHAR not in text or CLOSE_CHAR not in text:
            done = True
            
        level = 0
        escapeNum = 0
        openIndex = 0
        closeIndex = 0
        
        for index, char in enumerate(text):
            if OPEN_CHAR == char and not escapeNum % 2:
                level += 1
                if 1 == level:
                    openIndex = index
            elif CLOSE_CHAR == char and not escapeNum % 2:
                level -= 1
                if 0 == level:
                    ## First and outermost level gathered.
                    closeIndex = index
                    break
            elif ESCAPE_CHAR == char:
                escapeNum += 1
            else:
                escapeNum = 0
                
        tmpBlock = text[openIndex:closeIndex + 1]
        
        if 1 < len(tmpBlock):
            if random.getrandbits(1):
                text = "".join([text[:openIndex], text[closeIndex + 1:]])
            else:
                text = "".join([text[:openIndex], text[openIndex + 1:closeIndex], text[closeIndex + 1:]])
        else:
            done = True
            
        yield text

def parse_all(text):
    """ Parses special blocks of text and takes care of escape characters.
      - Makes a choice between multiple phrases (parse_choices)
      - Chooses whether to omit a phrase or not (parse_optional)
      - Changes the letter case of a phrase (parse_cases)

    Args:
        text(unicode): String to parse.

    Returns:
        text(unicode): Updated string.

    Examples:
        >>> parse_all("I'm {b}eating you{r <cake|homework>}.")
        I'm eating your homework.
    """

    if (get_setting("Variables", "open_omit") in text
    and get_setting("Variables", "close_omit") in text):
        for result in parse_optional(text):
            text = result

    if (get_setting("Variables", "open_choose") in text
    and get_setting("Variables", "open_choose") in text):
        for result in parse_choices(text):
            text = result

    text = parse_cases(text)

    ## Parse escape characters.
    text = text.replace("{e}{e}".format(e=get_setting("Variables", "escape")), get_setting("Variables", "sentinel"))
    text = text.replace(get_setting("Variables", "escape"), "")
    text = text.replace(get_setting("Variables", "sentinel"), get_setting("Variables", "escape"))

    return text

def regexp(expression, line):
    reg = re.compile(expression)

    if line:
        return reg.search(line) is not None

def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                  lambda mo: mo.group(0)[0].upper() +
                             mo.group(0)[1:].lower(),
                  s)


## === Classes === ##
class Database(object):
    """ For reading and parsing lines in a SQLite database.

    Args:
        dbFile(unicode): The filepath of the database.
    """
    
    def __init__(self, dbFile):
        self.db = dbFile

    def get_column(self, header, table, maximum=None):
        """ Gets fields under a column header.

        Args:
            header(unicode): Name of column's header.
            table(unicode): Name of table.
            maximum(int, optional): Maximum amount of fields to fetch.

        Returns:
            fields(list): List of fields under header.
        """
        fields = []
        table = clean(table)
        connection = sqlite3.connect(self.db)
        connection.row_factory = lambda cursor, row: row[0]
        c = connection.cursor()
        if maximum:
            c.execute("SELECT {} FROM {} LIMIT ?".format(header, table), [maximum])
        else:
            c.execute("SELECT {} FROM {}".format(header, table))
        fields = c.fetchall()
        c.close()
        
        return fields

    def get_field(self, fieldId, header, table):
        """ Gets the field under the specified header, identified by its primary key value.

        Args:
            fieldId(int, str): Unique ID of line the field is in.
            header(unicode): Header of the field to fetch.
            table(unicode): Name of table to look into.

        Returns:
            The desired field, or None if the lookup failed.

        Raises:
            TypeError: If fieldId doesn't exist in the table.
        
        Examples:
            >>> get_field(123, "firstname", "kings")
            Adgar
        """
        header = clean(header)
        table = clean(table)
        field = None
        
        connection = sqlite3.connect(self.db)
        c = connection.cursor()

        statement = "SELECT {} FROM {} WHERE id=?".format(header, table)
        logger.debug(statement)
        c.execute(statement, [fieldId])

        try:
            field = c.fetchone()[0]
        except TypeError:
            logger.exception("ID \"{}\" was not in table \"{}\"".format(fieldId, table))
        
        c.close()
        
        return field

    def get_ids(self, table, conditions=None, splitter=","):
        """ Gets the IDs that fit within the specified categories. Gets all IDs if category is None.

        Args:
            table(unicode): Name of table to look into.
            conditions(list, optional): Categories you want to filter the line by.
                [("header of categories 1", "=", "category1",) "header of category 2": "category3"]
                Multiple categories under a single header are separated with a comma.
                If categories are provided, the line must match at least one category in each header.
            searchMode(unicode, optional): Determines the method of searching for matches.
                Database.SEARCH_SIMPLE ("simple) uses match_dumbsimple function.
                Database.SEARCH_REGEX ("regex") uses regexp function.
                Database.SEARCH_DUMBREGEX ("dumbregex") uses match_dumbregex function.
                Any other value uses a strict search.

        Returns:
            ids(list): List of IDs that match the categories.

        Raises:
            OperationalError: If table or header doesn't exist.
            TypeError: If category is neither None nor a dictionary.

        Examples:
            >>> get_ids({"type": "greeting"})
            [1, 2, 3, 5, 9, 15]  # Any row that has the type "greeting".

            >>> get_ids({"type": "nickname,quip", "by": "Varric"})
            [23, 24, 25, 34, 37, 41, 42, 43]  # Any row by "Varric" that has the type "nickname" or "quip".
        """
        ids = []
        table = clean(table)
        clause = ""
        
        connection = sqlite3.connect(self.db)
        connection.row_factory = lambda cursor, row: row[0]  # Outputs first element of tuple for fetchall()

        c = connection.cursor()

        if conditions:
            clause = "WHERE ("
            clauseList = [clause,]
            substitutes = []
            catCount = 1
            headerCount = 1

            ## TODO: Add ability to specify comparison operator (e.g. =, <, LIKE, etc.)
            for con in conditions:
                if 1 < headerCount:
                    clauseList.append(" AND (")

                
                    
                clauseList.append(")")
                headerCount += 2
                catCount = 1

            clause = "".join(clauseList)

            statement = "SELECT id FROM {} {}".format(table, clause)
            logger.debug("(get_ids) Substitutes: {}".format(substitutes))
            logger.debug("(get_ids) SQLite statement: {}".format(statement))

            c.execute(statement, substitutes)
        else:
            c.execute("SELECT id FROM {}".format(table))

        ids = c.fetchall()

        return ids

    def random_line(self, header, table, category=None, splitter=","):
        """ Chooses a random line from the table under the header.

        Args:
            header(unicode): The header of the column where you want a random line from.
            table(unicode): Name of the table to look into.
            category(dict, optional): Categories you want to filter the line by, formatted like so:
                {"header of categories 1": "category1,category2", "header of category 2": "category3"}
                Multiple categories under a single header are separated with a comma.
            splitter(unicode, optional): What separates multiple categories (default is a comma).

        Returns:
            line(unicode): A random line from the database.

        Raises:
            OperationalError: If header or table doesn't exist.
            TypeError: If category is neither None nor a dictionary.

        Examples:
            >>> random_line("line", {"type": "greeting"})
            Hello.
        """
        header = clean(header)
        table = clean(table)
        line = ""
        
        connection = sqlite3.connect(self.db)
        c = connection.cursor()

        if category:
            ids = self.get_ids(table, category, splitter)
            if ids:
                line = random.choice(ids)
                line = self.get_field(line, header, table)
            else:
                line = ""
        else:
            c.execute("SELECT {} FROM {} ORDER BY Random() LIMIT 1".format(header, table))  # TODO: Take categories into account.
            line = c.fetchone()[0]

        return line


def test():
    d = Database(FILE_DATABASE)
    print(d.random_line("phrase", "phrases"))
    print(d.get_ids("phrases"))

if "__main__" == __name__:
    test()
