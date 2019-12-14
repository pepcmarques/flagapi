def line_breaker(sentence=""):
    if "\n" in sentence:
        return "\n"
    elif "\r\n" in sentence:
        return "\r\n"
    elif "\r" in sentence:
        return "\r"
    return ""
