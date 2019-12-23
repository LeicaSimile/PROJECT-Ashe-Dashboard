import pytest
from status import CommandStatus
import helpers
import commands.Admin


class TestAdmin:
    def test_get_inactive_members(self):
        """
        MockMember
        MockGuild
        MockContext
        """
        context = helpers.MockContext()
        inactive_members = await commands.Admin.get_inactive_members(context)
        pass

    def test_purgelist(self):
        pass

    def test_purgenotify(self):
        pass

    def test_message(self):
        pass

    def test_edit(self):
        pass
