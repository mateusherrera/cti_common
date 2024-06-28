"""
Classe para criar conexões com o banco de dados (Postgres).

:author: Mateus Herrera Gobetti Borges
:github: mateusherrera
:date: 2024-06-27
"""

from sqlalchemy import create_engine, Connection, Engine, NullPool
from dotenv import load_dotenv
from os import getenv


class DBConnection:
    """ Classe para criar conexões com o banco de dados (Postgres). """

    # ini: Attributes

    dict_credencials: dict

    # end: Attributes

    # ini: Constructor

    def __init__(self, dict_credencials: dict=None) -> None:
        """
        Construtor da classe DBConnection.

        :param dict_credencials: Dicionário com as credenciais para conexão com o banco de dados.
            - Opcional: Caso opte por não usar o arquivo .env.
            - Estrutura: {
                'driver': 'driver_name',
                'username': 'username',
                'password': 'password',
                'host': 'host',
                'port': 'port',
                'database': 'database',
            }
        """

        if dict_credencials is not None:
            self.dict_credencials = dict_credencials
        else:
            load_dotenv(override=True)
            self.dict_credencials = {
                'driver': getenv('PS_DRIVER'),
                'username': getenv('PS_USER'),
                'password': getenv('PS_PASSWORD'),
                'host': getenv('PS_HOST'),
                'port': getenv('PS_PORT'),
                'database': getenv('PS_DB'),
            }
        pass

    # end: Constructor

    # ini: Methods

    def get_connection(self) -> tuple[Connection, Engine]:
        """
        Método para criar e retornar uma conexão com o banco de dados.

        :return: Conexão com o banco de dados.
        """

        url = (
            f'{self.dict_credencials["driver"]}://{self.dict_credencials["username"]}:'
            f'{self.dict_credencials["password"]}@{self.dict_credencials["host"]}:{self.dict_credencials["port"]}/'
            f'{self.dict_credencials["database"]}'
        )

        engine = create_engine(url, poolclass=NullPool)
        return engine.connect(), engine

    # end: Methods

    # end: DBConnection
    pass
