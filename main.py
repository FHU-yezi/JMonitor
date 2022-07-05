from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep

from event_handlers import OnFailureEvent, OnSuccessEvent
from monitors import init_monitors
from register import GetAllRegisteredFuncs
from utils import CronToKwargs

init_monitors()  # 运行相关模块，继而对监控任务进行注册操作

scheduler = BackgroundScheduler()

funcs = GetAllRegisteredFuncs()

for service_name, module_name, cron, func in funcs:
    scheduler.add_job(func, "cron", **CronToKwargs(cron), id=f"{service_name}_{module_name}")

scheduler.add_listener(OnSuccessEvent, EVENT_JOB_EXECUTED)
scheduler.add_listener(OnFailureEvent, EVENT_JOB_ERROR)

scheduler.start()

while True:
    sleep(10)
