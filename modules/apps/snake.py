from modules.redis import RedisWrapper


class MonitorController:
    commands = {
        "snake": [
            dict(
                method="command",
                keywords=[
                    {
                        "temperature": {
                            "janet_input": False,
                            "thread_q": False,
                            "args": ["report_temp"],
                            "kwargs": {},
                        }
                    },
                    {
                        "humidity": {
                            "janet_input": False,
                            "thread_q": False,
                            "args": ["report_hum"],
                            "kwargs": {},
                        }
                    },
                ],
            )
        ]
    }

    def __init__(self, speech):
        self.redis = RedisWrapper().connect()

    def __str__(self):
        return "MonitorController"

    def command(self, command):
        value = ""
        if "temp" in command:
            temp = self.redis.get("temp").decode("utf-8")
            value = f"{temp} degrees celcius"
        elif "hum" in command:
            hum = self.redis.get("hum").decode("utf-8")
            value = f"{hum}% RH"

        return value
