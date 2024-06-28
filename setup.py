from setuptools import setup, find_packages

setup(
    name='ufu',
    version='1.0.0',
    packages=find_packages(),
    description='Classes comuns entre os repositórios começados com "cti", referentes ao meu TCC.',
    author='Mateus Herrera Gobetti Borges',
    author_email='mateusherreragb05@gmail.com',
    url='https://github.com/mateusherrera/cti_common',
    install_requires=['sqlalchemy', 'psycopg2', 'python-dotenv'],
)
