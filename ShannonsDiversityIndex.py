#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emartin
#
# Created:     16/10/2020
# Copyright:   (c) emartin 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#!/usr/bin/env python

# Shannon Diversity Index
# http://en.wikipedia.org/wiki/Shannon_index

import sys

def sdi(data):
    """ Given a hash { 'species': count } , returns the SDI

    >>> sdi({'a': 10, 'b': 20, 'c': 30,})
    1.0114042647073518"""

    from math import log as ln

    def p(n, N):
        """ Relative abundance """
        if n is  0:
            return 0
        else:
            return (float(n)/N) * ln(float(n)/N)

    N = sum(data.values())

    return -sum(p(n, N) for n in data.values() if n is not 0)

if __name__ == '__main__':
    import doctest
    doctest.testmod()

def main():
    vals ={
        "1a" : 25,
        "1b" : 20,
        "2" : 15,
        "3a" : 14   }
    print("Shannon's = {}".format(sdi(vals)))

if __name__ == '__main__':
    main()
