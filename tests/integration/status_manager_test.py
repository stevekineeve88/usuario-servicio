from modules.user.managers.status_manager import StatusManager
from tests.integration.setup.integration_setup import IntegrationSetup


class StatusManagerTest(IntegrationSetup):
    status_manager: StatusManager = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.status_manager = cls.service_locator.get(StatusManager.__name__)

    def test_get_all_gets_all_statuses(self):
        statuses = self.status_manager.get_all()

        expected = [
            "ACTIVE",
            "INACTIVE",
            "DELETED",
        ]

        self.assertEqual(3, len(statuses))
        for status in statuses:
            self.assertIn(status.get_const(), expected)

    def test_get_by_id_gets_status(self):
        statuses = self.status_manager.get_all()

        expected_status = statuses[0]
        actual_status = self.status_manager.get_by_id(expected_status.get_id())

        self.assertEqual(expected_status.get_id(), actual_status.get_id())
        self.assertEqual(expected_status.get_const(), actual_status.get_const())
        self.assertEqual(expected_status.get_description(), actual_status.get_description())

    def test_get_by_const_gets_status(self):
        statuses = self.status_manager.get_all()

        expected_status = statuses[0]
        actual_status = self.status_manager.get_by_const(expected_status.get_const())

        self.assertEqual(expected_status.get_id(), actual_status.get_id())
        self.assertEqual(expected_status.get_const(), actual_status.get_const())
        self.assertEqual(expected_status.get_description(), actual_status.get_description())
