"""
Classe para enviar e-mails.

:author: Mateus Herrera Gobetti Borges
:github: mateusherrera
:date: 2024-06-27.
"""

from email.message import EmailMessage
from dotenv import load_dotenv
from smtplib import SMTP
from os import getenv


class EmailSender:
    """ Classe para enviar e-mails. """

    # ini: Attributes

    smtp_server: str
    smtp_port: str
    smtp_user: str
    smtp_password: str

    sender: str
    body: str

    # end: Attributes

    # ini: Constructor

    def __init__(self, dict_config: dict=None) -> None:
        """
        Construtor da classe EmailSender.

        :param dict_config: Dicionário com as configurações para envio de e-mails.
            - Opcional: Caso opte por não usar o arquivo .env.
            - Estrutura: {
                'smtp_server': 'smtp_server',
                'smtp_port': 'smtp_port',
                'smtp_user': 'smtp_user',
                'smtp_password': 'smtp_password',
                'sender': 'sender_email',
            }
        """

        if dict_config is not None:
            if not self._is_structure_correct(dict_config):
                raise ValueError('A estrutura do dicionário não está correta.')

            else:
                self.dict_config = dict_config

                self.smtp_server = dict_config['smtp_server']
                self.smtp_port = dict_config['smtp_port']
                self.smtp_user = dict_config['smtp_user']
                self.smtp_password = dict_config['smtp_password']

                self.sender = dict_config['sender']

        else:
            load_dotenv(override=True)
            is_env_set, missing_env_variables = self._verify_env_variables()

            if not is_env_set:
                raise ValueError(
                    f'As seguintes variáveis de ambiente não foram carregadas: {', '.join(missing_env_variables)}.'
                )

            else:
                self.smtp_server = getenv('SMTP_SERVER')
                self.smtp_port = getenv('SMTP_PORT')
                self.smtp_user = getenv('SMTP_USER')
                self.smtp_password = getenv('SMTP_PASSWORD')

                self.sender = getenv('SENDER')

        self.body = None
        pass

    # end: Constructor

    # ini: Methods

    def _is_structure_correct(self, dict_config) -> bool:
        """
        Método para verificar a estrutura do dicionário de configurações.

        :param dict_config: Dicionário com as configurações para envio de e-mails.

        :return: True se a estrutura estiver correta, False caso contrário.
        """

        expected_keys = ['smtp_server', 'smtp_port', 'smtp_user', 'smtp_password', 'sender']
        return sorted(expected_keys) == sorted(dict_config.keys())

    def _verify_env_variables(self) -> tuple[bool, list]:
        """
        Método para verificar se as variáveis de ambiente necessárias foram carregadas.

        :return: Bool com o indicativo se estão ou não corretas as variáveis de ambiente; Lista de variáveis faltantes.
        """

        env_variables = ['SMTP_SERVER', 'SMTP_PORT', 'SMTP_USER', 'SMTP_PASSWORD', 'SENDER']
        missing_env_variables = list()

        for env_variable in env_variables:
            if getenv(env_variable) is None:
                missing_env_variables.append(env_variable)

        return len(missing_env_variables) == 0, missing_env_variables

    def add_line(self, line: str) -> None:
        """
        Método para adicionar uma linha ao corpo do e-mail.

        :param line: Linha a ser adicionada ao corpo do e-mail.
        """

        if self.body is None:
            self.body = line
        else:
            self.body += '\n' + line

    def send_email(self, subject: str, receivers: str) -> bool:
        """
        Método para enviar e-mail.

        :param subject: Assunto do e-mail.
        :param receivers: Lista de e-mails dos destinatários (separados com ',').

        :return: True se o e-mail foi enviado com sucesso, False caso contrário.
        """

        msg = EmailMessage()

        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = receivers

        msg.set_content(self.body)

        try:
            with SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            return True

        except:
            return False

    # end: Methods

    # end: EmailSender
    pass
