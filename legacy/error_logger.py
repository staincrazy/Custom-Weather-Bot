from datetime import datetime

_time_now = datetime.now()


def logEvent(event=None, function=None, user_input=None):
    with open("legacy_error.logs", "a") as f:
        f.write("\n" + f"At {_time_now}: this event occurred "
                + str(event) + f" while calling {str(function)} with the input {str(user_input)}" + "\n")
