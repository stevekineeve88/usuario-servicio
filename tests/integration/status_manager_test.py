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
