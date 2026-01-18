import logging
import requests
import schedule
from application_config import app_port, random_token

logger = logging.getLogger(__name__)


def sync_qagent_container():

    def wrapper():
        response = requests.post(f'http://localhost:{app_port}/api/qagent/server_container/sync?token={random_token}')
        logger.info(f'response==>{response.text}')
    schedule.every(60).seconds.do(wrapper)
