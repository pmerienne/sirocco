import pytest
from dotenv import load_dotenv, find_dotenv


@pytest.fixture(scope='session', autouse=True)
def load_env():
    env_file = find_dotenv('.env.test')
    load_dotenv(env_file)
