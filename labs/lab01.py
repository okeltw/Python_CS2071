"""Required questions for lab 1"""
# Taylor Okel
# Lab 01
# 1/19/17 

## Boolean Operators ##

# Q4
def both_positive(x, y):
    """Returns True if both x and y are positive.

    >>> both_positive(-1, 1)
    False
    >>> both_positive(1, 1)
    True
    """
    "*** YOUR CODE HERE ***"
    return (x > 0) and (y > 0)


## while Loops ##

# Q7
def factors(n):
    """Prints out all of the numbers that divide `n` evenly.

    >>> factors(20)
    20
    10
    5
    4
    2
    1
    """
    "*** YOUR CODE HERE ***"
    x = n
    while (x > 0):
        if (n % x) == 0:
            print(x)
        x -= 1


# Q8
def fib(n):
    """Returns the nth Fibonacci number.

    >>> fib(0)
    0
    >>> fib(1)
    1
    >>> fib(2)
    1
    >>> fib(3)
    2
    >>> fib(4)
    3
    >>> fib(5)
    5
    >>> fib(6)
    8
    >>> fib(100)
    354224848179261915075
    """
    "*** YOUR CODE HERE ***"

    # Algorithm:
    # Fn = Fn-1 + Fn-2

    """ Recursive solution
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

    Cool to think about, but REALLY slow. Cannot efficiently compute fib(100),
    might actually stack overflow if left going long enough...
    """

    if n == 0:
        return 0
    elif n == 1:
        return 1
    elif n < 0:
        return None
    else:
        i = 2
        x = 0
        y = 1
        while i <= n:
            temp  = y
            y = y + x
            x = temp
            i+=1
        return y

"""************************"""
""" Lab 01 Extra Questions """
"""************************"""

def is_factor(x, y):
    """ Returns True if x is a factor of y, False otherwise.

    >>> is_factor(3, 6)
    True
    >>> is_factor(4, 10)
    False
    >>> is_factor(0, 5)
    False
    >>> is_factor(0, 0)
    False
    """
    return (x!=0) and (y%x == 0)

def gets_discount(x, y):
    """ Returns True if this is a combination of a senior citizen
    and a child, False otherwise.

    >>> gets_discount(65, 12)
    True
    >>> gets_discount(9, 70)
    True
    >>> gets_discount(40, 45)
    False
    >>> gets_discount(40, 75)
    False
    >>> gets_discount(65, 13)
    False
    >>> gets_discount(7, 9)
    False
    >>> gets_discount(73, 77)
    False
    >>> gets_discount(70, 31)
    False
    >>> gets_discount(10, 25)
    False
    """

    return (x <= 12 or y <= 12) and (x >= 65 or y >= 65)

def falling(n, k):
    """Compute the falling factorial of n to depth k.

    >>> falling(6, 3)  # 6 * 5 * 4
    120
    >>> falling(4, 0)
    1
    >>> falling(4, 3)  # 4 * 3 * 2
    24
    >>> falling(4, 1)  # 4
    4
    """

    """ Recursive approach
    if k > n:
        return None
    elif n == 1 or k == 1:
        return n
    elif k == 0:
        return 1
    else:
        return n*falling(n-1, k-1)
    """

    result, x = 1, n-k
    while n > x:
        result, n = result*n, n-1
    return result
