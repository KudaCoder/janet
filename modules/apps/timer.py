from modules.utils import duration

from word2number import w2n
from time import sleep
import threading


class TimeController:
    commands = {
        "reminder": [
            dict(
                method="build_timer",
                keywords=[
                    {
                        "set": {
                            "janet_input": True,
                            "thread_q": True,
                            "args": [],
                            "kwargs": {},
                        }
                    }
                ],
            )
        ]
    }

    def __init__(self, speech):
        self.speech = speech

    def timer(self, label, duration, thread_q):
        sleep(duration)
        thread_q.put(f"Hey, your timer for {label} has finished!")

    def build_timer(self, janet_command=None, thread_q=None):
        self.speech.speak("What would you like to call this timer?")
        label = self.speech.listen()

        duration_period = None
        if self.speech.filter_response(janet_command, keywords=["for"]):
            duration_period, duration_text = duration(janet_command)

        while not duration_period:
            self.speech.speak("How long would you like the timer for?")
            duration_text = self.speech.listen()
            duration_period = w2n.word_to_num(" ".join(duration_text))

        thread = threading.Thread(
            target=self.timer, args=(label, duration_period, thread_q)
        )
        thread.start()

        return f"Starting timer for {label} - I'll give you a shout in {duration_text}"
