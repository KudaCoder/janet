from modules.comm.email import send_email
from .redis import RedisWrapper

import threading


def check_snake_temp():
    redis = RedisWrapper().connect()
    pre_temp = 0.0
    while True:
        temp = float(redis.get("temp").decode("utf-8"))
        if not pre_temp <= 16.5 and temp <= 16.0:
            send_email(
                "Low Snake Temp",
                f"The snake's habitat temperature is {temp}! Sort it out!!!",
            )
        pre_temp = temp
        break


def run():
    check_snake_temp()
    # check_thread = threading.Thread(target=check_snake_temp, daemon=True)
    # check_thread.start()
