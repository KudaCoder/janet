from nltk.tokenize import word_tokenize
import nltk

from pattern.text.en import singularize
import speech_recognition as sr
from gtts import gTTS
import os

nltk.download("all")


class Speech:
    def listen(self):
        """
        Used to recognise and record speech input from the microphone then
        convert that audio into a string
        """
        audio_text = ""

        if not os.environ.get("DEBUG"):
            with sr.Microphone() as source:
                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source, duration=0.2)
                r.energy_threshold = 775
                # r.non_speaking_duration = 0.2
                # r.dynamic_energy_threshold = True

                audio = r.listen(source)
                try:
                    audio_text = r.recognize_google(audio)
                    print(audio_text)
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    self.speak(
                        "Uh oh! Couldn't request results from Google Speech Recognition"
                        f" service; {e}"
                    )

        else:
            audio_text = input("Please type command correctly: \n")

        return self.recognise(audio_text)

    def recognise(self, audio_text):
        audio_text = audio_text.lower()
        if audio_text == "manual input":
            self.speak("Please enter the value")
            audio_text = input(": ").lower()
        word_tokens = word_tokenize(audio_text)

        # # This is taking too many words out and changing the meaning of the sentence
        # tagged = nltk.pos_tag(word_tokens)
        # stop_words = set(stopwords.words('english'))
        # clean_tokens = [w for w in tagged if w[0].lower() not in stop_words]

        singulars = [singularize(w) for w in word_tokens]

        return singulars

    def speak(self, output):
        print(output)
        tts = gTTS(output, slow=False)
        janet_audio = "janet_audio.mp3"
        tts.save(janet_audio)
        os.system(f"play {janet_audio} tempo 1.25")
        os.remove(janet_audio)

    @staticmethod
    def filter_response(response, keywords: list = None):
        if any(entry in response for entry in keywords):
            return True
        return False
