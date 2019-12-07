const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;
const redirect = encodeURIComponent('http://localhost:3000/api/client/dashboard');

function login(req, res) {
    res.redirect(`https://discordapp.com/api/oauth2/authorize?client_id=323173717968683019&redirect_uri=${redirect}&response_type=code&scope=guilds`);
}

module.exports = {
    login: login
}
