import socket
from unittest import TestCase
from client_python.client import Client
from classes.pokemons import *
from classes.agents import *


class TestClasses(TestCase):

    def setUp(self) -> None:
        ip = '127.0.0.1'
        port = 6666
        # start connection
        self.client = Client()
        self.client.start_connection(ip, port)

    def test_Pokemons(self):
        sstr = self.client.get_pokemons()
        print(Pokemons(sstr))
        self.client.stop_connection()

    def test_Agents(self):
        self.client.add_agent("{\"id\":0}")
        sstr = self.client.get_agents()
        print(Agents(sstr))
        self.client.stop_connection()

