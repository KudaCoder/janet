from word2number import w2n


def duration(text):
    """
    For converting written numbers detected from recognise_speech_input(),
    into integers used for time.sleep()
    Also returns duration as a string for janet_speak()
    TODO - Add filtering for complex times i.e. 1 hour & 15 minutes
    """
    duration_text = ""
    try:
        duration_text = text.split("for ")[1]
        if any(x in duration_text for x in ("seconds", "second")):
            duration = duration_text.split(" second")[0]
            duration = w2n.word_to_num(duration)
        elif any(x in duration_text for x in ("minutes", "minute")):
            duration = duration_text.split(" minute")[0]
            duration = w2n.word_to_num(duration) * 60
        elif any(x in duration_text for x in ("hours", "hour")):
            duration = duration_text.split(" hour")[0]
            duration = w2n.word_to_num(duration) * 3600
    except Exception:
        duration = None

    return duration, duration_text
