import unittest
from unittest.mock import patch, MagicMock
from mysql_data_manager.modules.connection.objects.result import Result
from modules.user.data.status_data import StatusData
from modules.user.exceptions.user_status_fetch_exception import UserStatusFetchException
from modules.user.managers.status_manager import StatusManager


class StatusManagerTest(unittest.TestCase):

    @patch("modules.user.data.status_data.StatusData")
    def setUp(self, status_data: StatusData) -> None:
        self.status_data = StatusData
        self.status_manager: StatusManager = StatusManager(
            status_data=self.status_data
        )

    def test_get_all_fails_on_missing_statuses(self):
        self.status_data.load_all = MagicMock(return_value=Result(True))
        with self.assertRaises(UserStatusFetchException):
            self.status_manager.get_all()
            self.fail("Did not fail on missing user statuses")
        self.status_data.load_all.assert_called_once()
