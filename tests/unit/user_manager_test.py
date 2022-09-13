import unittest
from unittest.mock import patch, MagicMock
from mysql_data_manager.modules.connection.objects.result import Result
from modules.user.data.user_data import UserData
from modules.user.managers.status_manager import StatusManager
from modules.user.managers.user_manager import UserManager


class UserManagerTest(unittest.TestCase):

    @patch("modules.user.data.user_data.UserData")
    @patch("modules.user.managers.status_manager.StatusManager")
    def setUp(self, user_data: UserData, status_manager: StatusManager) -> None:
        self.user_data = user_data
        self.status_manager = status_manager
        self.user_manager: UserManager = UserManager(
            user_data=self.user_data,
            status_manager=self.status_manager
        )

    def test_search_defaults_limit_if_over_100(self):
        self.user_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": 101,
            "offset": 0
        }

        self.user_manager.search(**params)
        self.user_data.search.assert_called_once_with(
            search=params["search"],
            limit=10,
            offset=params["offset"]
        )

    def test_search_defaults_limit_if_under_0(self):
        self.user_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": -1,
            "offset": 0
        }

        self.user_manager.search(**params)
        self.user_data.search.assert_called_once_with(
            search=params["search"],
            limit=10,
            offset=params["offset"]
        )

    def test_search_defaults_offset_if_under_0(self):
        self.user_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": 20,
            "offset": -1
        }

        self.user_manager.search(**params)
        self.user_data.search.assert_called_once_with(
            search=params["search"],
            limit=params["limit"],
            offset=0
        )
