from frontend.blueprints.utils import APITools


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
        self.speech = speech
        self.api_tools = APITools()

    def __str__(self):
        return "MonitorController"

    def command(self, command):
        value = ""
        if "temp" in command:
            reading = self.api_tools.current_reading()
            value = f"{reading['temp']} degrees celcius"
        elif "hum" in command:
            reading = self.api_tools.current_reading()
            value = f"{reading['hum']}% RH"

        return value
