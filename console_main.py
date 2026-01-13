"""
gui程序入口
"""
import os.path

from logconfig import setup_rotating_log
from console_gui import app_run as console_run

log_dir = "../deplayagent-logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

setup_rotating_log(log_file="../deplayagent-logs/app.log")


def main():
    console_run()


if __name__ == '__main__':
    main()