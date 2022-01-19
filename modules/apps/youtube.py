from __future__ import unicode_literals
from youtube_search import YoutubeSearch
import webbrowser


class YTController:
    commands = {
        "youtube": [
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
        for_idx = janet_command.index("for")
        query = janet_command[for_idx + 1 :]
        youtube_results = self.search_youtube(" ".join(query))
        self.speech.speak(f"{len(youtube_results)} results found for {query}.")
        self.speech.speak("Would you like to hear the results or play the first song?")
        response = self.speech.listen()

        if self.speech.filter_response(response, keywords=["play", "first"]):
            result = youtube_results[0]
            webbrowser.open(result["link"])

        return

        # if filter_response(response, keywords=["hear the results"]):
        #     for result in youtube_results:
        #         self.speech.speak(result["title"])

    def search_youtube(self, query):
        results = YoutubeSearch(query, max_results=10).to_dict()
        lst_results = []
        for r in results:
            result = dict(
                title=r["title"],
                duration=r["duration"],
                link=f"https://youtube.com/{r['url_suffix']}",
            )
            lst_results.append(result)
        return lst_results
