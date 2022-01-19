import webbrowser


class WebController:
    commands = {
        "google": [
            dict(
                method="search",
                keywords=[
                    {
                        "search": {
                            "janet_input": True,
                            "thread_q": False,
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

    def search(self, janet_command=None):
        # TODO: Have tried several google search APIs but they are not
        #       returning the data i'm looking for. Consider making own
        if self.speech.filter_response(janet_command, keywords=["for"]):
            webSearch_text = janet_command.split("for ")[1]
            webbrowser.open(f"http://google.com/search?q={webSearch_text}")
