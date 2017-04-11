## Extra Mutable Linked List Questions ##

# Q6
def reverse(link):
    """Returns a Link that is the reverse of the original.

    >>> print_link(reverse(Link(1)))
    <1>
    >>> link = Link(1, Link(2, Link(3)))
    >>> new = reverse(link)
    >>> print_link(new)
    <3 2 1>
    >>> print_link(link)
    <1 2 3>
    """
    temp = Link(link.first)
    while link.rest is not Link.empty:
        link = link.rest
        temp = Link(link.first, temp)
    return temp


# Q7
def add_links(link1, link2):
    """Adds two Links, returning a new Link

    >>> l1 = Link(1, Link(2))
    >>> l2 = Link(3, Link(4, Link(5)))
    >>> new = add_links(l1,l2)
    >>> print_link(new)
    <1 2 3 4 5>
    """
    temp = Link.empty
    while link1 is not Link.empty:
        temp = Link(link1.first, temp)
        link1 = link1.rest
    while link2 is not Link.empty:
        temp = Link(link2.first, temp)
        link2 = link2.rest
    return reverse(temp)

# Q8
def slice_link(link, start, end):
    """Slices a Link from start to end (as with a normal Python list).

    >>> link = Link(3, Link(1, Link(4, Link(1, Link(5, Link(9))))))
    >>> new = slice_link(link, 1, 4)
    >>> print_link(new)
    <1 4 1>
    """
    if start > 0:
        return slice_link(link.rest, start-1, end-1)
    elif end > 0:
        return Link(link.first, slice_link(link.rest, start-1, end-1))
    else:
        return Link.empty


# Linked List Class
class Link:

    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest


def mygetitem(s,i):
    if isinstance(i, slice):
        return slice_link(s, i.start, i.stop)
    elif i == 0:
        return s.first
    else:
        return mygetitem(s.rest, i-1)



def mysetitem(s,i,x):
    if i == 0:
        s.first = x
    else:
        mysetitem(s.rest, i-1, x)

def print_link(link):
    """Print elements of a linked list link.

    >>> link = Link(1, Link(2, Link(3)))
    >>> print_link(link)
    <1 2 3>
    >>> link1 = Link(1, Link(Link(2), Link(3)))
    >>> print_link(link1)
    <1 <2> 3>
    >>> link1 = Link(3, Link(Link(4), Link(5, Link(6))))
    >>> print_link(link1)
    <3 <4> 5 6>
    """
    print('<' +helper(link).rstrip() +'>')

def print_link_str(link):
    return '< ' + helper(link).rstrip() + ' >'

def helper(link):
    if link == Link.empty:
        return ''
    elif isinstance(link.first, Link):
        return '<' +helper(link.first).rstrip() + '> '+ helper(link.rest)
    else:
        return str(link.first) +' '+  helper(link.rest)

Link.__getitem__ = mygetitem
Link.__setitem__ = mysetitem
Link.__add__ = add_links
Link.__repr__ = print_link_str
