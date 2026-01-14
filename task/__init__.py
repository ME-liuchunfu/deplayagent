import logging
import threading
import time

import schedule


logger = logging.getLogger(__name__)


class ScheduleTask:

    def __init__(self):
        self._thread = None  # 后台线程对象

    def add_task(self, func, *args, **kwargs):
        """添加定时任务，直接调用schedule的语法即可"""
        return schedule.every(*args, **kwargs).do(func)

    def clear(self):
        schedule.clear()
        logger.info(f'定时任务清空')

    def get_jobs(self):
        task_list = [str(job) for job in schedule.jobs]
        logger.info(f"当前共{len(task_list)}个定时任务")
        return task_list

    def _run_loop(self):
        """内部循环方法，不对外暴露"""
        while True:
            schedule.run_pending()
            time.sleep(1)

    def start(self):
        """启动后台线程"""
        if self._thread:
            return
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info("✅ 定时任务工具类初始化完成，后台线程已启动")


schedule_task = ScheduleTask()
