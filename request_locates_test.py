import unittest
from unittest.mock import patch
from request_locates import (  # Replace 'your_module' with the actual module name where the original code resides
    ClientRequest,
    aggregate_requests_by_symbol,
    request_locates,
    distribute_locates
)


class TestClientRequest(unittest.TestCase):
    def test_init(self):
        client = ClientRequest("Client1", "ABC", 100)
        self.assertEqual(client.client_name, "Client1")
        self.assertEqual(client.symbol, "ABC")
        self.assertEqual(client.number_of_locates_requested, 100)
        self.assertEqual(client.number_of_locates_approved, 0)


class TestAggregateRequests(unittest.TestCase):
    def test_aggregate_requests(self):
        clients = [ClientRequest("Client1", "ABC", 100),
                   ClientRequest("Client1", "QQQ", 100),
                   ClientRequest("Client2", "ABC", 200)]
        result = aggregate_requests_by_symbol(clients)
        self.assertEqual(result, {"ABC": 300, "QQQ": 100})


class TestRequestLocates(unittest.TestCase):
    @patch('random.choice', return_value = True)
    @patch('random.uniform', return_value = 1)
    def test_request_locates(self, mock_uniform, mock_choice):
        result = request_locates({"ABC": 100})
        self.assertEqual(result, {"ABC": 100})


class TestDistributeLocates(unittest.TestCase):
    def test_distribute_locates_full_approval(self):
        clients = [ClientRequest("Client1", "ABC", 300),
                   ClientRequest("Client2", "QQQ", 100),
                   ClientRequest("Client2", "ABC", 200),
                   ClientRequest("Client3", "TTT", 100)]
        requested = {"ABC": 500, "QQQ": 100, "TTT": 100}
        approved = {"ABC": 500, "QQQ": 100, "TTT": 100}

        distribute_locates(clients, requested, approved)

        self.assertEqual(clients[0].number_of_locates_approved, 300)
        self.assertEqual(clients[1].number_of_locates_approved, 100)
        self.assertEqual(clients[2].number_of_locates_approved, 200)
        self.assertEqual(clients[3].number_of_locates_approved, 100)


    def test_distribute_locates_partial_approval(self):
        clients = [ClientRequest("Client1", "ABC", 300),
                   ClientRequest("Client2", "QQQ", 100),
                   ClientRequest("Client2", "ABC", 200),
                   ClientRequest("Client3", "TTT", 100)]
        requested = {"ABC": 500, "QQQ": 100, "TTT": 100}
        approved = {"ABC": 345, "QQQ": 65, "TTT": 100}

        distribute_locates(clients, requested, approved)

        self.assertEqual(clients[0].number_of_locates_approved, 200)
        self.assertEqual(clients[1].number_of_locates_approved, 65)
        self.assertEqual(clients[2].number_of_locates_approved, 145)
        self.assertEqual(clients[3].number_of_locates_approved, 100)

    def test_distribute_locates_partial_approval_small_first(self):
        clients = [ClientRequest("Client1", "ABC", 100),
                   ClientRequest("Client2", "ABC", 200)]
        requested = {"ABC": 300}
        approved = {"ABC": 150}

        distribute_locates(clients, requested, approved)

        self.assertEqual(clients[0].number_of_locates_approved, 50)
        self.assertEqual(clients[1].number_of_locates_approved, 100)

    def test_distribute_locates_partial_approval_big_first(self):
        clients = [ClientRequest("Client1", "ABC", 200),
                   ClientRequest("Client2", "ABC", 100)]
        requested = {"ABC": 300}
        approved = {"ABC": 200}

        distribute_locates(clients, requested, approved)

        self.assertEqual(clients[0].number_of_locates_approved, 100)
        self.assertEqual(clients[1].number_of_locates_approved, 100)

    def test_distribute_locates_no_approval(self):
        clients = [ClientRequest("Client1", "ABC", 100)]
        requested = {"ABC": 100}
        approved = {}

        distribute_locates(clients, requested, approved)

        self.assertEqual(clients[0].number_of_locates_approved, 0)

    def test_distribute_locates_multiple_symbols(self):
        clients = [
            ClientRequest("Client1", "ABC", 100),
            ClientRequest("Client2", "ABC", 200),
            ClientRequest("Client3", "QQQ", 200)
        ]
        requested = {"ABC": 300, "QQQ": 200}
        approved = {"ABC": 200, "QQQ": 150}

        distribute_locates(clients, requested, approved)

        self.assertEqual(clients[0].number_of_locates_approved, 100)  # Rounded to nearest 100
        self.assertEqual(clients[1].number_of_locates_approved, 100)  # Rounded to nearest 100
        self.assertEqual(clients[2].number_of_locates_approved, 150)


if __name__ == '__main__':
    unittest.main()
