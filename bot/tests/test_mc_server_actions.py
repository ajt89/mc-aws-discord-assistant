from unittest import TestCase, mock

from bot.mc_server_actions import MCServerActions

MOCK_INSTANCE_IP = "0.0.0.0"
ACTIVE_NUMBER_OF_USERS = 2
MAX_NUMBER_OF_USERS = 20
INACTIVE_NUMBER_OF_USERS = 0
INSTANCE_RUNNING_STATE = "running"
INSTANCE_STOPPED_STATE = "stopped"
ACTIVE_MC_USERNAMES = ["user0", "user1"]
INACTIVE_MC_USERNAMES = []


class TestMCServerActions(TestCase):
    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_update_mc_server_details_instance_stopped(self, aws_service_mock, mc_service_mock):
        aws_service_mock.return_value.is_instance_running = False

        mcsa = MCServerActions()

        aws_service_mock.return_value.update_instance_details.assert_called()
        mc_service_mock.assert_not_called()

    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_update_mc_server_details_instance_running(self, aws_service_mock, mc_service_mock):
        aws_service_mock.return_value.is_instance_running = True
        aws_service_mock.return_value.instance_ip = MOCK_INSTANCE_IP

        mcsa = MCServerActions()

        aws_service_mock.return_value.update_instance_details.assert_called_once()
        mc_service_mock.assert_called_once_with(MOCK_INSTANCE_IP)

    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_update_mc_server_details_instance_running_mc_connection(
        self, aws_service_mock, mc_service_mock
    ):
        aws_service_mock.return_value.is_instance_running = True
        aws_service_mock.return_value.instance_ip = MOCK_INSTANCE_IP

        mcsa = MCServerActions()
        mcsa._update_mc_server_details()

        self.assertEqual(aws_service_mock.return_value.update_instance_details.call_count, 2)
        mc_service_mock.assert_called_once_with(MOCK_INSTANCE_IP)
        mc_service_mock.return_value.update_server_details.assert_called_once()

    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_shutdown_server_instance_running_server_running(
        self, aws_service_mock, mc_service_mock
    ):
        aws_service_mock.return_value.is_instance_running = True
        aws_service_mock.return_value.instance_ip = MOCK_INSTANCE_IP

        mcsa = MCServerActions()
        shutdown_action = mcsa.shutdown_server()

        self.assertEqual(aws_service_mock.return_value.update_instance_details.call_count, 2)
        mc_service_mock.assert_called_once_with(MOCK_INSTANCE_IP)
        mc_service_mock.return_value.stop_server.assert_called_once()
        aws_service_mock.return_value.stop_instance.assert_called_once()
        self.assertTrue(shutdown_action)

    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_shutdown_server_instance_running_server_offline(
        self, aws_service_mock, mc_service_mock
    ):
        aws_service_mock.return_value.is_instance_running = True
        aws_service_mock.return_value.instance_ip = None

        mcsa = MCServerActions()
        shutdown_action = mcsa.shutdown_server()

        self.assertEqual(aws_service_mock.return_value.update_instance_details.call_count, 2)
        mc_service_mock.assert_not_called()
        mc_service_mock.return_value.stop_server.assert_not_called()
        aws_service_mock.return_value.stop_instance.assert_called_once()
        self.assertTrue(shutdown_action)

    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_shutdown_server_instance_stopped(self, aws_service_mock, mc_service_mock):
        aws_service_mock.return_value.is_instance_running = False
        aws_service_mock.return_value.instance_ip = None

        mcsa = MCServerActions()
        shutdown_action = mcsa.shutdown_server()

        self.assertEqual(aws_service_mock.return_value.update_instance_details.call_count, 2)
        mc_service_mock.assert_not_called()
        mc_service_mock.return_value.stop_server.assert_not_called()
        aws_service_mock.return_value.stop_instance.assert_not_called()
        self.assertFalse(shutdown_action)

    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_shutdown_if_server_inactive_instance_running_server_running_active(
        self, aws_service_mock, mc_service_mock
    ):
        aws_service_mock.return_value.is_instance_running = True
        aws_service_mock.return_value.instance_ip = MOCK_INSTANCE_IP
        mc_service_mock.return_value.number_of_users = ACTIVE_NUMBER_OF_USERS

        mcsa = MCServerActions()
        shutdown_action = mcsa.shutdown_if_server_inactive()

        self.assertEqual(aws_service_mock.return_value.update_instance_details.call_count, 2)
        mc_service_mock.assert_called_once_with(MOCK_INSTANCE_IP)
        mc_service_mock.return_value.stop_server.assert_not_called()
        aws_service_mock.return_value.stop_instance.assert_not_called()
        self.assertFalse(shutdown_action)

    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_shutdown_if_server_inactive_instance_running_server_running_inactive(
        self, aws_service_mock, mc_service_mock
    ):
        aws_service_mock.return_value.is_instance_running = True
        aws_service_mock.return_value.instance_ip = MOCK_INSTANCE_IP
        mc_service_mock.return_value.number_of_users = INACTIVE_NUMBER_OF_USERS

        mcsa = MCServerActions()
        shutdown_action = mcsa.shutdown_if_server_inactive()

        self.assertEqual(aws_service_mock.return_value.update_instance_details.call_count, 3)
        mc_service_mock.assert_called_once_with(MOCK_INSTANCE_IP)
        mc_service_mock.return_value.stop_server.assert_called_once()
        aws_service_mock.return_value.stop_instance.assert_called_once()
        self.assertTrue(shutdown_action)

    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_shutdown_if_server_inactive_instance_running_server_offline(
        self, aws_service_mock, mc_service_mock
    ):
        aws_service_mock.return_value.is_instance_running = True
        aws_service_mock.return_value.instance_ip = MOCK_INSTANCE_IP
        mc_service_mock.return_value = None

        mcsa = MCServerActions()
        shutdown_action = mcsa.shutdown_if_server_inactive()

        self.assertEqual(aws_service_mock.return_value.update_instance_details.call_count, 3)
        mc_service_mock.assert_called_with(MOCK_INSTANCE_IP)
        self.assertIsNone(mcsa.mc_service)
        aws_service_mock.return_value.stop_instance.assert_called_once()
        self.assertTrue(shutdown_action)

    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_shutdown_if_server_inactive_instance_stopped(self, aws_service_mock, mc_service_mock):
        aws_service_mock.return_value.is_instance_running = False

        mcsa = MCServerActions()
        shutdown_action = mcsa.shutdown_if_server_inactive()

        self.assertEqual(aws_service_mock.return_value.update_instance_details.call_count, 2)
        mc_service_mock.assert_not_called()
        self.assertIsNone(mcsa.mc_service)
        aws_service_mock.return_value.stop_instance.assert_not_called()
        self.assertFalse(shutdown_action)

    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_start_server_instance_stopped(self, aws_service_mock, mc_service_mock):
        aws_service_mock.return_value.is_instance_running = False

        mcsa = MCServerActions()
        start_action = mcsa.start_server()

        self.assertEqual(aws_service_mock.return_value.update_instance_details.call_count, 1)
        mc_service_mock.assert_not_called()
        self.assertIsNone(mcsa.mc_service)
        aws_service_mock.return_value.start_instance.assert_called_once()
        self.assertTrue(start_action)

    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_start_server_instance_running(self, aws_service_mock, mc_service_mock):
        aws_service_mock.return_value.is_instance_running = True
        aws_service_mock.return_value.instance_ip = MOCK_INSTANCE_IP
        aws_service_mock.return_value.start_instance.return_value = False

        mcsa = MCServerActions()
        start_action = mcsa.start_server()

        self.assertEqual(aws_service_mock.return_value.update_instance_details.call_count, 1)
        mc_service_mock.assert_called_with(MOCK_INSTANCE_IP)
        aws_service_mock.return_value.start_instance.assert_called_once()
        self.assertFalse(start_action)

    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_get_server_status_instance_running_server_running_active(
        self, aws_service_mock, mc_service_mock
    ):
        aws_service_mock.return_value.instance_state = INSTANCE_RUNNING_STATE
        aws_service_mock.return_value.instance_ip = MOCK_INSTANCE_IP
        aws_service_mock.return_value.is_instance_running = True
        mc_service_mock.return_value.number_of_users = ACTIVE_NUMBER_OF_USERS
        mc_service_mock.return_value.max_users = MAX_NUMBER_OF_USERS
        mc_service_mock.return_value.users = ACTIVE_MC_USERNAMES

        mcsa = MCServerActions()
        server_status = mcsa.get_server_status()
        aws_instance = server_status.get("aws_instance")
        mc_server = server_status.get("mc_server")

        self.assertEqual(aws_service_mock.return_value.update_instance_details.call_count, 2)
        mc_service_mock.assert_called_once()
        mc_service_mock.assert_called_with(MOCK_INSTANCE_IP)
        mc_service_mock.return_value.update_server_details.assert_called_once()
        self.assertEqual(aws_instance.get("state"), INSTANCE_RUNNING_STATE)
        self.assertEqual(aws_instance.get("ip"), MOCK_INSTANCE_IP)
        self.assertTrue(aws_instance.get("is_running"))
        self.assertTrue(mc_server.get("is_active"))
        self.assertTrue(mc_server.get("is_server_reachable"))
        self.assertEqual(mc_server.get("active_users"), ACTIVE_NUMBER_OF_USERS)
        self.assertEqual(mc_server.get("max_users"), MAX_NUMBER_OF_USERS)
        self.assertEqual(mc_server.get("users"), ACTIVE_MC_USERNAMES)

    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_get_server_status_instance_running_server_running_inactive(
        self, aws_service_mock, mc_service_mock
    ):
        aws_service_mock.return_value.instance_state = INSTANCE_RUNNING_STATE
        aws_service_mock.return_value.instance_ip = MOCK_INSTANCE_IP
        aws_service_mock.return_value.is_instance_running = True
        mc_service_mock.return_value.number_of_users = INACTIVE_NUMBER_OF_USERS
        mc_service_mock.return_value.max_users = MAX_NUMBER_OF_USERS
        mc_service_mock.return_value.users = INACTIVE_MC_USERNAMES

        mcsa = MCServerActions()
        server_status = mcsa.get_server_status()
        aws_instance = server_status.get("aws_instance")
        mc_server = server_status.get("mc_server")

        self.assertEqual(aws_service_mock.return_value.update_instance_details.call_count, 2)
        mc_service_mock.assert_called_once()
        mc_service_mock.assert_called_with(MOCK_INSTANCE_IP)
        mc_service_mock.return_value.update_server_details.assert_called_once()
        self.assertEqual(aws_instance.get("state"), INSTANCE_RUNNING_STATE)
        self.assertEqual(aws_instance.get("ip"), MOCK_INSTANCE_IP)
        self.assertTrue(aws_instance.get("is_running"))
        self.assertFalse(mc_server.get("is_active"))
        self.assertTrue(mc_server.get("is_server_reachable"))
        self.assertEqual(mc_server.get("active_users"), INACTIVE_NUMBER_OF_USERS)
        self.assertEqual(mc_server.get("max_users"), MAX_NUMBER_OF_USERS)
        self.assertEqual(mc_server.get("users"), INACTIVE_MC_USERNAMES)

    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_get_server_status_instance_running_server_stopped(
        self, aws_service_mock, mc_service_mock
    ):
        aws_service_mock.return_value.instance_state = INSTANCE_RUNNING_STATE
        aws_service_mock.return_value.instance_ip = MOCK_INSTANCE_IP
        aws_service_mock.return_value.is_instance_running = True
        mc_service_mock.return_value = None

        mcsa = MCServerActions()
        server_status = mcsa.get_server_status()
        aws_instance = server_status.get("aws_instance")
        mc_server = server_status.get("mc_server")

        self.assertEqual(aws_service_mock.return_value.update_instance_details.call_count, 2)
        self.assertEqual(mc_service_mock.call_count, 2)
        mc_service_mock.assert_called_with(MOCK_INSTANCE_IP)
        self.assertEqual(aws_instance.get("state"), INSTANCE_RUNNING_STATE)
        self.assertEqual(aws_instance.get("ip"), MOCK_INSTANCE_IP)
        self.assertTrue(aws_instance.get("is_running"))
        self.assertEqual(mc_server, {})

    @mock.patch("bot.mc_server_actions.MCService")
    @mock.patch("bot.mc_server_actions.AWSService")
    def test_get_server_status_instance_stopped(self, aws_service_mock, mc_service_mock):
        aws_service_mock.return_value.instance_state = INSTANCE_STOPPED_STATE
        aws_service_mock.return_value.instance_ip = None
        aws_service_mock.return_value.is_instance_running = False

        mcsa = MCServerActions()
        server_status = mcsa.get_server_status()
        aws_instance = server_status.get("aws_instance")
        mc_server = server_status.get("mc_server")

        self.assertEqual(aws_service_mock.return_value.update_instance_details.call_count, 2)
        mc_service_mock.assert_not_called()
        self.assertEqual(aws_instance.get("state"), INSTANCE_STOPPED_STATE)
        self.assertIsNone(aws_instance.get("ip"))
        self.assertFalse(aws_instance.get("is_running"))
        self.assertEqual(mc_server, {})
