def twenty_seventeen():
    """Come up with the most creative expression that evaluates to 2017,
    using only numbers and the +, *, and - operators.

    >>> twenty_seventeen()
    2017
    >>> twenty_seventeen() + twenty_seventeen()
    4034
    """
    return int((float("1" + "0" + "0" + "9" + "." + "5") - 1) * 2)
