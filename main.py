from time import sleep

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler

from event_handlers import OnFailureEvent, OnSuccessEvent
from monitors import init_monitors
from register import GetAllRegisteredFuncs
from utils.log import run_logger
from utils_old import CronToKwargs

init_monitors()  # 运行相关模块，继而对监控任务进行注册操作

scheduler = BackgroundScheduler()
run_logger.info("成功初始化调度器")

funcs = GetAllRegisteredFuncs()
run_logger.info(f"获取到 {len(funcs)} 个监控函数")

for service_name, module_name, cron, func in funcs:
    scheduler.add_job(func, "cron", **CronToKwargs(cron),
                      id=f"{service_name}|{module_name}")
run_logger.info("已将监控函数加入调度")

scheduler.add_listener(OnSuccessEvent, EVENT_JOB_EXECUTED)
scheduler.add_listener(OnFailureEvent, EVENT_JOB_ERROR)
run_logger.info("成功注册事件回调")

scheduler.start()
run_logger.info("调度器已启动")

while True:
    sleep(10)
