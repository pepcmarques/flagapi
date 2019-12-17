def line_breaker(sentence=""):
    if "\r\n" in sentence:
        return "\r\n"
    elif "\n" in sentence:
        return "\n"
    elif "\r" in sentence:
        return "\r"
    return ""
