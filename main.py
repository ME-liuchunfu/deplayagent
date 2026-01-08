"""
gui程序入口
"""

from logconfig import setup_rotating_log
from console_gui import app_run as console_run

setup_rotating_log(log_file="logs/app.log")

def main():
    console_run()

if __name__ == '__main__':
    main()