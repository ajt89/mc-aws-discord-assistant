from unittest import TestCase, mock

from mcad.chat import ChatService
from mcad.constants import AUTHORIZED_CHANNEL, AUTHORIZED_ROLE

discord = mock.Mock()


class TestChatService(TestCase):
    @classmethod
    @mock.patch("mcad.chat.MCServerActions")
    def setUpClass(cls, mock_mcsa):
        cls.chat_service = ChatService()

    def setUp(self):
        self.message_mock = discord.message.Message()
        self.client_mock = discord.client.Client()
        author_mock = discord.abc.User()
        self.message_mock.author = author_mock

        self.client_mock.user.name = "bot"
        author_mock.name = "user"

        self.message_mock.channel.name = AUTHORIZED_CHANNEL

        minecraft_role_mock = discord.role.Role.MC()
        minecraft_role_mock.name = AUTHORIZED_ROLE
        self.everyone_role_mock = discord.role.Role.E()
        self.everyone_role_mock.name = "everyone"
        author_mock.roles = [minecraft_role_mock, self.everyone_role_mock]
        self.client_mock.roles = [minecraft_role_mock, self.everyone_role_mock]

        self.message_mock.content = "!mc "

    def test_filter_message_from_bot(self):
        self.message_mock = discord.client.Client()
        self.message_mock = self.client_mock

        message_filtered = self.chat_service.filter_message(self.message_mock, self.client_mock)

        self.assertTrue(message_filtered)

    def test_filter_message_from_wrong_channel(self):
        self.message_mock.channel.name = "general"

        message_filtered = self.chat_service.filter_message(self.message_mock, self.client_mock)

        self.assertTrue(message_filtered)

    def test_filter_message_from_user_wrong_role(self):
        self.message_mock.author.roles = [self.everyone_role_mock]

        message_filtered = self.chat_service.filter_message(self.message_mock, self.client_mock)

        self.assertTrue(message_filtered)

    def test_filter_message_from_user_incorrect_format(self):
        self.message_mock.content = "help"

        message_filtered = self.chat_service.filter_message(self.message_mock, self.client_mock)

        self.assertTrue(message_filtered)

    def test_filter_message_from_user_correct(self):
        message_filtered = self.chat_service.filter_message(self.message_mock, self.client_mock)

        self.assertFalse(message_filtered)

    def test_handle_message_help(self):
        self.message_mock.content = "!mc help"

        response = self.chat_service.handle_message(self.message_mock)

        self.assertEqual(self.chat_service._help_message(), response)

    def test_handle_default_message(self):
        self.message_mock.content = "!mc asdf"

        response = self.chat_service.handle_message(self.message_mock)

        self.assertEqual(self.chat_service._help_message(), response)

    def test_handle_server_status(self):
        self.message_mock.content = "!mc server status"

        response = self.chat_service.handle_message(self.message_mock)

        expected_response = "Server status:\n" + self.chat_service._server_status()

        self.assertEqual(expected_response, response)

    def test_handle_server_start_stopped(self):
        self.chat_service.mcsa.start_server.return_value = True
        self.message_mock.content = "!mc server start"

        response = self.chat_service.handle_message(self.message_mock)

        expected_response = "Instance Starting:\n" + self.chat_service._server_status(
            is_server_starting=True
        )

        self.assertEqual(expected_response, response)

    def test_handle_server_start_running(self):
        self.chat_service.mcsa.start_server.return_value = False
        self.message_mock.content = "!mc server start"

        response = self.chat_service.handle_message(self.message_mock)

        expected_response = "Instance Already Running:\n" + self.chat_service._server_status()

        self.assertEqual(expected_response, response)

    def test_handle_server_stop_running_inactive(self):
        self.chat_service.mcsa.shutdown_if_server_inactive.return_value = True
        self.message_mock.content = "!mc server stop"

        response = self.chat_service.handle_message(self.message_mock)

        expected_response = "Server Stopping:\n" + self.chat_service._server_status(
            is_server_stopping=True
        )

        self.assertEqual(expected_response, response)

    def test_handle_server_stop_running_active(self):
        self.chat_service.mcsa.shutdown_if_server_inactive.return_value = False
        self.message_mock.content = "!mc server stop"

        response = self.chat_service.handle_message(self.message_mock)

        expected_response = "Server Not Stopped:\n" + self.chat_service._server_status()

        self.assertEqual(expected_response, response)

    def test_handle_server_stop_force_running(self):
        self.chat_service.mcsa.shutdown_server.return_value = True
        self.message_mock.content = "!mc server stop force"

        response = self.chat_service.handle_message(self.message_mock)

        expected_response = "Server Stopping:\n" + self.chat_service._server_status(
            is_server_stopping=True
        )

        self.assertEqual(expected_response, response)

    def test_handle_server_stop_force_stopped(self):
        self.chat_service.mcsa.shutdown_server.return_value = False
        self.message_mock.content = "!mc server stop force"

        response = self.chat_service.handle_message(self.message_mock)

        expected_response = "Server Already Stopped:\n" + self.chat_service._server_status()

        self.assertEqual(expected_response, response)
