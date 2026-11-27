#!/usr/bin/env python3
"""t/1810 to t/1814, and the faults from t/1820: references to arrays and
hashes, and elements through them (step 13a; D107, D112, D114).

The definition, which is all this file knows of the language:

  [ LIST ]  { LIST }  \\@a  \\%h          a reference to a new container, or
                                       to the variable's own
  EXPR->[I]  EXPR->{K}                 the element, the arrow left out
  $a[0][1]  $h{a}{b}  $r->[0]{k}       between two subscripts

**A reference is the container itself**, as a Python list or dict is:
copies of a list hold the same references (shallow), and two references
are `==` when they are one container. Reading through undef, or through
an element or a key that is not there, is a fault, `undef where a
reference is wanted`, and through anything else that is not the
reference wanted `not a reference to an array` (or `to a hash`). Storing
through undef makes it: every hop that is undef or not there becomes a
new array or hash, by the subscript after it, the variable at the head
too; an array grows to hold an index. A store through a loop's variable
that holds undef is the fault, since perl's lands in the list (T250).
A reference is true and defined, `ref` is ARRAY or HASH, and anywhere
else a number or a string is wanted it is a fault: `a reference where a
number is wanted`, `a reference where a string is wanted`.

The model is Python, whose lists and dicts are references already. perl
is the second derivation: t/checks.py oracle holds every .expected of a
test without a `kind:` to what perl 5.42 prints, and each fault test's
output to the start of it.

1810 reads, 1811 stores and what they make, 1812 the assigning operators
and steps through a chain, 1813 references as values (identity, `ref`,
truth, shallow copies, cycles, `exists` and `delete`), 1814 references in
loops, sorts, maps and subs. 1820 on each fault once.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/ref.py --program 1810 > t/1810-ref-reads.pl
    python3 t/models/ref.py 1810 > t/1810-ref-reads.expected
    python3 t/models/ref.py --program 1811 > t/1811-ref-stores.pl
    python3 t/models/ref.py 1811 > t/1811-ref-stores.expected
    python3 t/models/ref.py --program 1812 > t/1812-ref-assigning-operators-and-steps.pl
    python3 t/models/ref.py 1812 > t/1812-ref-assigning-operators-and-steps.expected
    python3 t/models/ref.py --program 1813 > t/1813-ref-as-values.pl
    python3 t/models/ref.py 1813 > t/1813-ref-as-values.expected
    python3 t/models/ref.py --program 1814 > t/1814-ref-in-loops-and-subs.pl
    python3 t/models/ref.py 1814 > t/1814-ref-in-loops-and-subs.expected
    python3 t/models/ref.py --program 1820 > t/1820-fault-read-undef.pl
    python3 t/models/ref.py 1820 > t/1820-fault-read-undef.expected
    python3 t/models/ref.py --program 1821 > t/1821-fault-read-undef-hash.pl
    python3 t/models/ref.py 1821 > t/1821-fault-read-undef-hash.expected
    python3 t/models/ref.py --program 1822 > t/1822-fault-read-through-missing-index.pl
    python3 t/models/ref.py 1822 > t/1822-fault-read-through-missing-index.expected
    python3 t/models/ref.py --program 1823 > t/1823-fault-read-through-missing-key.pl
    python3 t/models/ref.py 1823 > t/1823-fault-read-through-missing-key.expected
    python3 t/models/ref.py --program 1824 > t/1824-fault-read-through-undef-element.pl
    python3 t/models/ref.py 1824 > t/1824-fault-read-through-undef-element.expected
    python3 t/models/ref.py --program 1825 > t/1825-fault-read-named-hash-through-missing.pl
    python3 t/models/ref.py 1825 > t/1825-fault-read-named-hash-through-missing.expected
    python3 t/models/ref.py --program 1826 > t/1826-fault-read-named-array-through-missing.pl
    python3 t/models/ref.py 1826 > t/1826-fault-read-named-array-through-missing.expected
    python3 t/models/ref.py --program 1827 > t/1827-fault-read-a-number.pl
    python3 t/models/ref.py 1827 > t/1827-fault-read-a-number.expected
    python3 t/models/ref.py --program 1828 > t/1828-fault-read-a-string.pl
    python3 t/models/ref.py 1828 > t/1828-fault-read-a-string.expected
    python3 t/models/ref.py --program 1829 > t/1829-fault-read-a-hash-as-an-array.pl
    python3 t/models/ref.py 1829 > t/1829-fault-read-a-hash-as-an-array.expected
    python3 t/models/ref.py --program 1830 > t/1830-fault-read-an-array-as-a-hash.pl
    python3 t/models/ref.py 1830 > t/1830-fault-read-an-array-as-a-hash.expected
    python3 t/models/ref.py --program 1831 > t/1831-fault-read-deep-wrong-kind.pl
    python3 t/models/ref.py 1831 > t/1831-fault-read-deep-wrong-kind.expected
    python3 t/models/ref.py --program 1832 > t/1832-fault-read-through-a-number-element.pl
    python3 t/models/ref.py 1832 > t/1832-fault-read-through-a-number-element.expected
    python3 t/models/ref.py --program 1833 > t/1833-fault-read-a-literal.pl
    python3 t/models/ref.py 1833 > t/1833-fault-read-a-literal.expected
    python3 t/models/ref.py --program 1834 > t/1834-fault-exists-through-undef.pl
    python3 t/models/ref.py 1834 > t/1834-fault-exists-through-undef.expected
    python3 t/models/ref.py --program 1835 > t/1835-fault-exists-through-missing.pl
    python3 t/models/ref.py 1835 > t/1835-fault-exists-through-missing.expected
    python3 t/models/ref.py --program 1836 > t/1836-fault-delete-through-undef.pl
    python3 t/models/ref.py 1836 > t/1836-fault-delete-through-undef.expected
    python3 t/models/ref.py --program 1837 > t/1837-fault-delete-through-an-array.pl
    python3 t/models/ref.py 1837 > t/1837-fault-delete-through-an-array.expected
    python3 t/models/ref.py --program 1838 > t/1838-fault-call-gives-undef-read.pl
    python3 t/models/ref.py 1838 > t/1838-fault-call-gives-undef-read.expected
    python3 t/models/ref.py --program 1839 > t/1839-fault-store-through-empty-string.pl
    python3 t/models/ref.py 1839 > t/1839-fault-store-through-empty-string.expected
    python3 t/models/ref.py --program 1840 > t/1840-fault-store-through-false.pl
    python3 t/models/ref.py 1840 > t/1840-fault-store-through-false.expected
    python3 t/models/ref.py --program 1841 > t/1841-fault-store-through-a-number.pl
    python3 t/models/ref.py 1841 > t/1841-fault-store-through-a-number.expected
    python3 t/models/ref.py --program 1842 > t/1842-fault-store-through-the-other-kind.pl
    python3 t/models/ref.py 1842 > t/1842-fault-store-through-the-other-kind.expected
    python3 t/models/ref.py --program 1843 > t/1843-fault-step-through-a-hash-as-an-array.pl
    python3 t/models/ref.py 1843 > t/1843-fault-step-through-a-hash-as-an-array.expected
    python3 t/models/ref.py --program 1844 > t/1844-fault-store-before-the-start.pl
    python3 t/models/ref.py 1844 > t/1844-fault-store-before-the-start.expected
    python3 t/models/ref.py --program 1845 > t/1845-fault-store-hop-before-the-start.pl
    python3 t/models/ref.py 1845 > t/1845-fault-store-hop-before-the-start.expected
    python3 t/models/ref.py --program 1846 > t/1846-fault-store-through-a-call.pl
    python3 t/models/ref.py 1846 > t/1846-fault-store-through-a-call.expected
    python3 t/models/ref.py --program 1847 > t/1847-fault-store-through-or.pl
    python3 t/models/ref.py 1847 > t/1847-fault-store-through-or.expected
    python3 t/models/ref.py --program 1848 > t/1848-fault-store-through-a-choice.pl
    python3 t/models/ref.py 1848 > t/1848-fault-store-through-a-choice.expected
    python3 t/models/ref.py --program 1849 > t/1849-fault-store-through-loop-variable.pl
    python3 t/models/ref.py 1849 > t/1849-fault-store-through-loop-variable.expected
    python3 t/models/ref.py --program 1850 > t/1850-fault-store-through-it.pl
    python3 t/models/ref.py 1850 > t/1850-fault-store-through-it.expected
    python3 t/models/ref.py --program 1851 > t/1851-fault-step-through-it-in-a-map.pl
    python3 t/models/ref.py 1851 > t/1851-fault-step-through-it-in-a-map.expected
    python3 t/models/ref.py --program 1852 > t/1852-fault-odd-new-hash.pl
    python3 t/models/ref.py 1852 > t/1852-fault-odd-new-hash.expected
    python3 t/models/ref.py --program 1853 > t/1853-fault-odd-new-hash-assigned.pl
    python3 t/models/ref.py 1853 > t/1853-fault-odd-new-hash-assigned.expected
    python3 t/models/ref.py --program 1854 > t/1854-fault-reference-as-a-number-add.pl
    python3 t/models/ref.py 1854 > t/1854-fault-reference-as-a-number-add.expected
    python3 t/models/ref.py --program 1855 > t/1855-fault-reference-as-a-number-add-right.pl
    python3 t/models/ref.py 1855 > t/1855-fault-reference-as-a-number-add-right.expected
    python3 t/models/ref.py --program 1856 > t/1856-fault-reference-as-a-number-subtract.pl
    python3 t/models/ref.py 1856 > t/1856-fault-reference-as-a-number-subtract.expected
    python3 t/models/ref.py --program 1857 > t/1857-fault-reference-as-a-number-multiply.pl
    python3 t/models/ref.py 1857 > t/1857-fault-reference-as-a-number-multiply.expected
    python3 t/models/ref.py --program 1858 > t/1858-fault-reference-as-a-number-divide.pl
    python3 t/models/ref.py 1858 > t/1858-fault-reference-as-a-number-divide.expected
    python3 t/models/ref.py --program 1859 > t/1859-fault-reference-as-a-number-modulus.pl
    python3 t/models/ref.py 1859 > t/1859-fault-reference-as-a-number-modulus.expected
    python3 t/models/ref.py --program 1860 > t/1860-fault-reference-as-a-number-power.pl
    python3 t/models/ref.py 1860 > t/1860-fault-reference-as-a-number-power.expected
    python3 t/models/ref.py --program 1861 > t/1861-fault-reference-as-a-number-negate.pl
    python3 t/models/ref.py 1861 > t/1861-fault-reference-as-a-number-negate.expected
    python3 t/models/ref.py --program 1862 > t/1862-fault-reference-as-a-number-increment.pl
    python3 t/models/ref.py 1862 > t/1862-fault-reference-as-a-number-increment.expected
    python3 t/models/ref.py --program 1863 > t/1863-fault-reference-as-a-number-decrement.pl
    python3 t/models/ref.py 1863 > t/1863-fault-reference-as-a-number-decrement.expected
    python3 t/models/ref.py --program 1864 > t/1864-fault-reference-as-a-number-add-to.pl
    python3 t/models/ref.py 1864 > t/1864-fault-reference-as-a-number-add-to.expected
    python3 t/models/ref.py --program 1865 > t/1865-fault-reference-as-a-number-less.pl
    python3 t/models/ref.py 1865 > t/1865-fault-reference-as-a-number-less.expected
    python3 t/models/ref.py --program 1866 > t/1866-fault-reference-as-a-number-compare.pl
    python3 t/models/ref.py 1866 > t/1866-fault-reference-as-a-number-compare.expected
    python3 t/models/ref.py --program 1867 > t/1867-fault-reference-as-a-number-equal-to-a-number.pl
    python3 t/models/ref.py 1867 > t/1867-fault-reference-as-a-number-equal-to-a-number.expected
    python3 t/models/ref.py --program 1868 > t/1868-fault-reference-as-a-number-number-equal-to.pl
    python3 t/models/ref.py 1868 > t/1868-fault-reference-as-a-number-number-equal-to.expected
    python3 t/models/ref.py --program 1869 > t/1869-fault-reference-as-a-number-not-equal-to-undef.pl
    python3 t/models/ref.py 1869 > t/1869-fault-reference-as-a-number-not-equal-to-undef.expected
    python3 t/models/ref.py --program 1870 > t/1870-fault-reference-as-a-number-index.pl
    python3 t/models/ref.py 1870 > t/1870-fault-reference-as-a-number-index.expected
    python3 t/models/ref.py --program 1871 > t/1871-fault-reference-as-a-number-chr.pl
    python3 t/models/ref.py 1871 > t/1871-fault-reference-as-a-number-chr.expected
    python3 t/models/ref.py --program 1872 > t/1872-fault-reference-as-a-number-repeat-count.pl
    python3 t/models/ref.py 1872 > t/1872-fault-reference-as-a-number-repeat-count.expected
    python3 t/models/ref.py --program 1873 > t/1873-fault-reference-as-a-number-substr-position.pl
    python3 t/models/ref.py 1873 > t/1873-fault-reference-as-a-number-substr-position.expected
    python3 t/models/ref.py --program 1874 > t/1874-fault-reference-as-a-number-range.pl
    python3 t/models/ref.py 1874 > t/1874-fault-reference-as-a-number-range.expected
    python3 t/models/ref.py --program 1875 > t/1875-fault-reference-as-a-number-range-loop.pl
    python3 t/models/ref.py 1875 > t/1875-fault-reference-as-a-number-range-loop.expected
    python3 t/models/ref.py --program 1876 > t/1876-fault-reference-as-a-number-sort-block.pl
    python3 t/models/ref.py 1876 > t/1876-fault-reference-as-a-number-sort-block.expected
    python3 t/models/ref.py --program 1877 > t/1877-fault-reference-as-a-string-say.pl
    python3 t/models/ref.py 1877 > t/1877-fault-reference-as-a-string-say.expected
    python3 t/models/ref.py --program 1878 > t/1878-fault-reference-as-a-string-print.pl
    python3 t/models/ref.py 1878 > t/1878-fault-reference-as-a-string-print.expected
    python3 t/models/ref.py --program 1879 > t/1879-fault-reference-as-a-string-in-a-list.pl
    python3 t/models/ref.py 1879 > t/1879-fault-reference-as-a-string-in-a-list.expected
    python3 t/models/ref.py --program 1880 > t/1880-fault-reference-as-a-string-concat.pl
    python3 t/models/ref.py 1880 > t/1880-fault-reference-as-a-string-concat.expected
    python3 t/models/ref.py --program 1881 > t/1881-fault-reference-as-a-string-concat-to.pl
    python3 t/models/ref.py 1881 > t/1881-fault-reference-as-a-string-concat-to.expected
    python3 t/models/ref.py --program 1882 > t/1882-fault-reference-as-a-string-interpolated.pl
    python3 t/models/ref.py 1882 > t/1882-fault-reference-as-a-string-interpolated.expected
    python3 t/models/ref.py --program 1883 > t/1883-fault-reference-as-a-string-equal.pl
    python3 t/models/ref.py 1883 > t/1883-fault-reference-as-a-string-equal.expected
    python3 t/models/ref.py --program 1884 > t/1884-fault-reference-as-a-string-compare-strings.pl
    python3 t/models/ref.py 1884 > t/1884-fault-reference-as-a-string-compare-strings.expected
    python3 t/models/ref.py --program 1885 > t/1885-fault-reference-as-a-string-less-string.pl
    python3 t/models/ref.py 1885 > t/1885-fault-reference-as-a-string-less-string.expected
    python3 t/models/ref.py --program 1886 > t/1886-fault-reference-as-a-string-repeat.pl
    python3 t/models/ref.py 1886 > t/1886-fault-reference-as-a-string-repeat.expected
    python3 t/models/ref.py --program 1887 > t/1887-fault-reference-as-a-string-length.pl
    python3 t/models/ref.py 1887 > t/1887-fault-reference-as-a-string-length.expected
    python3 t/models/ref.py --program 1888 > t/1888-fault-reference-as-a-string-uc.pl
    python3 t/models/ref.py 1888 > t/1888-fault-reference-as-a-string-uc.expected
    python3 t/models/ref.py --program 1889 > t/1889-fault-reference-as-a-string-lc.pl
    python3 t/models/ref.py 1889 > t/1889-fault-reference-as-a-string-lc.expected
    python3 t/models/ref.py --program 1890 > t/1890-fault-reference-as-a-string-ord.pl
    python3 t/models/ref.py 1890 > t/1890-fault-reference-as-a-string-ord.expected
    python3 t/models/ref.py --program 1891 > t/1891-fault-reference-as-a-string-substr.pl
    python3 t/models/ref.py 1891 > t/1891-fault-reference-as-a-string-substr.expected
    python3 t/models/ref.py --program 1892 > t/1892-fault-reference-as-a-string-index-of.pl
    python3 t/models/ref.py 1892 > t/1892-fault-reference-as-a-string-index-of.expected
    python3 t/models/ref.py --program 1893 > t/1893-fault-reference-as-a-string-key.pl
    python3 t/models/ref.py 1893 > t/1893-fault-reference-as-a-string-key.expected
    python3 t/models/ref.py --program 1894 > t/1894-fault-reference-as-a-string-key-read.pl
    python3 t/models/ref.py 1894 > t/1894-fault-reference-as-a-string-key-read.expected
    python3 t/models/ref.py --program 1895 > t/1895-fault-reference-as-a-string-join.pl
    python3 t/models/ref.py 1895 > t/1895-fault-reference-as-a-string-join.expected
    python3 t/models/ref.py --program 1896 > t/1896-fault-reference-as-a-string-join-separator.pl
    python3 t/models/ref.py 1896 > t/1896-fault-reference-as-a-string-join-separator.expected
    python3 t/models/ref.py --program 1897 > t/1897-fault-reference-as-a-string-sort.pl
    python3 t/models/ref.py 1897 > t/1897-fault-reference-as-a-string-sort.expected
    python3 t/models/ref.py --program 1898 > t/1898-fault-reference-as-a-string-hash-list.pl
    python3 t/models/ref.py 1898 > t/1898-fault-reference-as-a-string-hash-list.expected
    python3 t/models/ref.py --program 1899 > t/1899-fault-frozen-through-a-reference.pl
    python3 t/models/ref.py 1899 > t/1899-fault-frozen-through-a-reference.expected
    python3 t/models/ref.py --program 1900 > t/1900-fault-frozen-hash-through-a-reference.pl
    python3 t/models/ref.py 1900 > t/1900-fault-frozen-hash-through-a-reference.expected
    python3 t/models/ref.py --program 1901 > t/1901-fault-frozen-by-a-chain-in-the-list.pl
    python3 t/models/ref.py 1901 > t/1901-fault-frozen-by-a-chain-in-the-list.expected
    python3 t/models/ref.py --program 1902 > t/1902-fault-frozen-inner-by-a-chain.pl
    python3 t/models/ref.py 1902 > t/1902-fault-frozen-inner-by-a-chain.expected
    python3 t/models/ref.py --program 1903 > t/1903-fault-frozen-hash-by-a-chain-in-a-map.pl
    python3 t/models/ref.py 1903 > t/1903-fault-frozen-hash-by-a-chain-in-a-map.expected
    python3 t/models/ref.py --program 1904 > t/1904-fault-frozen-by-a-chain-in-a-sort.pl
    python3 t/models/ref.py 1904 > t/1904-fault-frozen-by-a-chain-in-a-sort.expected
    python3 t/models/ref.py --program 1905 > t/1905-fault-frozen-made-in.pl
    python3 t/models/ref.py 1905 > t/1905-fault-frozen-made-in.expected
    python3 t/models/ref.py --program 1906 > t/1906-fault-frozen-from-a-sub.pl
    python3 t/models/ref.py 1906 > t/1906-fault-frozen-from-a-sub.expected
    python3 t/models/ref.py --program 1907 > t/1907-fault-past-the-end-in-a-loop.pl
    python3 t/models/ref.py 1907 > t/1907-fault-past-the-end-in-a-loop.expected
    python3 t/models/ref.py --program 1908 > t/1908-fault-no-key-in-a-loop.pl
    python3 t/models/ref.py 1908 > t/1908-fault-no-key-in-a-loop.expected
    python3 t/models/ref.py --program 1909 > t/1909-fault-past-the-end-in-a-grep.pl
    python3 t/models/ref.py 1909 > t/1909-fault-past-the-end-in-a-grep.expected
"""

import sys

UNDEF_REF = 'undef where a reference is wanted'
NOT_ARRAY = 'not a reference to an array'
NOT_HASH = 'not a reference to a hash'
NUMBER = 'a reference where a number is wanted'
STRING = 'a reference where a string is wanted'
BEFORE = 'an element before the start of the array'
FROZEN = 'an array was changed while a foreach is over it'
HFROZEN = 'a hash was changed while a foreach is over it'
ODD = 'an odd number of values for a hash'
PAST = 'an element past the end of the array in a foreach, where perl would make it'
KEY_PAST = 'a key that is not there in a foreach, where perl would make it'

class Fault(Exception):
    pass

# ---- values: an int, a str, None for undef, a list or a dict (a
# reference to one), True and False never.

def lit(v):
    if v is None:
        return 'undef'
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return f'"{v}"'
    if isinstance(v, list):
        return '[' + ', '.join(lit(x) for x in v) + ']'
    return '{' + ', '.join(f'{k} => {lit(x)}' for k, x in v.items()) + '}'

def fresh(v):
    """A literal, worked out: every container in it new."""
    if isinstance(v, list):
        return [fresh(x) for x in v]
    if isinstance(v, dict):
        return {k: fresh(x) for k, x in v.items()}
    return v

def shown(v):
    if v is None:
        return 'u'
    if isinstance(v, list):
        return 'ARRAY'
    if isinstance(v, dict):
        return 'HASH'
    return str(v)

def true(v):
    return not (v is None or v == 0 or v == '' or v == '0')

def get(c, k):
    if isinstance(c, list):
        return c[k] if -len(c) <= k < len(c) else None
    return c.get(k)

def through(v, k):
    """What a hop reads through, for subscript k (D107)."""
    if v is None:
        raise Fault(UNDEF_REF)
    if isinstance(k, int) and not isinstance(v, list):
        raise Fault(NOT_ARRAY)
    if isinstance(k, str) and not isinstance(v, dict):
        raise Fault(NOT_HASH)
    return v

def empty(k):
    return [] if isinstance(k, int) else {}

def put(c, k, v):
    if isinstance(c, list):
        if k < -len(c):
            raise Fault(BEFORE)
        if k < 0:
            k += len(c)
        while len(c) <= k:
            c.append(None)
    c[k] = v

# ---- a program and what it prints

class Prog:
    def __init__(self):
        self.lines = []
        self.out = []
        self.env = {}
        self.arrows = 0
        self.readonly = set()
        # The subs, which stand at the top of the file (D72).
        self.subs = []

    def say(self, text, printed):
        self.lines.append(text)
        self.out.append(printed)

    # A path: a base, ('$', name) a scalar, ('@', name) an element of a
    # named array, ('%', name) of a named hash; and its subscripts.
    def text(self, base, subs):
        def sub(k):
            return f'[{k}]' if isinstance(k, int) else f'{{{k}}}'
        kind, name = base
        if kind == '$':
            head, rest = f'${name}->' + sub(subs[0]), subs[1:]
        else:
            head, rest = f'${name}' + sub(subs[0]), subs[1:]
        # The arrow between two subscripts is written now and then, and
        # left out the rest of the time: perl has them the same.
        for k in rest:
            self.arrows += 1
            head += ('->' if self.arrows % 3 == 0 else '') + sub(k)
        return head

    def start(self, base, subs):
        """The container the first subscript is of, read through."""
        kind, name = base
        if kind == '$':
            return through(self.env['$' + name], subs[0])
        return self.env[kind + name]

    def read(self, base, subs):
        c = self.start(base, subs)
        for k, after in zip(subs, subs[1:]):
            c = through(get(c, k), after)
        return get(c, subs[-1])

    def made(self, base, subs):
        """The container the last subscript is of, every hop made (T248)."""
        kind, name = base
        if kind == '$':
            v = self.env['$' + name]
            if v is None:
                if name in self.readonly:
                    raise Fault(UNDEF_REF)
                v = self.env['$' + name] = empty(subs[0])
            c = through(v, subs[0])
        else:
            c = self.env[kind + name]
        for k, after in zip(subs, subs[1:]):
            v = get(c, k)
            if v is None:
                v = empty(after)
                put(c, k, v)
            c = through(v, after)
        return c

    def show(self, base, subs):
        t = self.text(base, subs)
        v = self.read(base, subs)
        if isinstance(v, (list, dict)):
            self.say(f'say(ref({t}));', shown(v))
        else:
            self.say(f'say(defined({t}) ? {t} : "u");', shown(v))

    def my(self, name, v):
        self.lines.append(f'my ${name} = {lit(v)};')
        self.env['$' + name] = fresh(v)

    def mya(self, name, *vs):
        self.lines.append(f'my @{name} = ({", ".join(lit(v) for v in vs)});')
        self.env['@' + name] = [fresh(v) for v in vs]

    def myh(self, name, **kv):
        self.lines.append(f'my %{name} = ({", ".join(f"{k} => {lit(v)}" for k, v in kv.items())});')
        self.env['%' + name] = {k: fresh(v) for k, v in kv.items()}

    def store(self, base, subs, op, value):
        t = self.text(base, subs)
        self.lines.append(f'{t} {op} {lit(value)};')
        c = self.made(base, subs)
        k = subs[-1]
        if isinstance(c, list) and k < -len(c):
            raise Fault(BEFORE)
        was = get(c, k)
        value = fresh(value)
        now = {'=': lambda: value, '+=': lambda: (was or 0) + value, '-=': lambda: (was or 0) - value,
               '*=': lambda: was * value, '.=': lambda: ('' if was is None else str(was)) + str(value), '//=': lambda: value if was is None else was,
               '||=': lambda: was if true(was) else value, '&&=': lambda: value if true(was) else was}[op]()
        if op in ('//=', '||=', '&&=') and now is was and (isinstance(c, dict) and k in c or isinstance(c, list) and -len(c) <= k < len(c)):
            return
        put(c, k, now)

    def step(self, base, subs, op, before):
        t = self.text(base, subs)
        c = self.made(base, subs)
        k = subs[-1]
        if isinstance(c, list) and k < -len(c):
            raise Fault(BEFORE)
        was = get(c, k)
        now = (was or 0) + (1 if op == '++' else -1)
        put(c, k, now)
        value = now if before else (0 if was is None and op == '++' else was)
        e = f'{op}{t}' if before else f'{t}{op}'
        self.steps = getattr(self, 'steps', 0) + 1
        v = f'$v{self.steps}'
        self.lines.append(f'my {v} = {e};')
        self.say(f'say(defined({v}) ? {v} : "u");', shown(value))

    def count(self, name):
        self.say(f'say(scalar(@{name}));', str(len(self.env['@' + name])))

    def keys(self, name):
        self.say(f'say(join(",", sort keys(%{name})));', ','.join(sorted(self.env['%' + name])))

    def block(self, f):
        """A case in a block of its own, its variables its own."""
        outer = self.env
        self.env = dict(outer)
        self.lines.append('{')
        f(self)
        self.lines.append('}')
        self.env = outer

# ---- the structures, and every path into them and just off their edges

STRUCTURES = [
    [1, [2, 3], {'k': 'v', 'n': [4, None]}, None, 'end'],
    {'a': {'b': {'c': 5}}, 'list': [[6, 7], [8]], 'u': None, 'z': 0},
    [[[[9]]]],
    {'x': [{'y': [10, 11]}]},
]

def paths(v, depth=0):
    """The paths into v, and one past each edge: a key or an index that is
    not there, and an index from the end."""
    if isinstance(v, list):
        keys = list(range(len(v))) + [len(v), -1] + ([-len(v)] if len(v) > 1 else [])
    elif isinstance(v, dict):
        keys = list(v) + ['nope']
    else:
        return []
    found = []
    for k in keys:
        found.append([k])
        inner = get(v, k)
        for rest in paths(inner, depth + 1):
            found.append([k] + rest)
    return found

def case_read(p):
    for n, s in enumerate(STRUCTURES):
        def one(p, s=s):
            p.my('r', s)
            for path in paths(s):
                try:
                    p.read(('$', 'r'), path)
                except Fault:
                    continue
                p.show(('$', 'r'), path)
        p.block(one)
    def named(p):
        p.mya('a', [1, 2], {'k': 3}, None, [[4]])
        p.myh('h', x=[5, 6], y={'z': 7}, u=None)
        for path in [[0, 0], [0, 1], [0, 2], [1, 'k'], [1, 'q'], [3, 0, 0], [3, 0], [-1, 0, 0], [0, -1]]:
            p.show(('@', 'a'), path)
        for path in [['x', 0], ['x', 1], ['x', -2], ['x', 5], ['y', 'z'], ['y', 'w']]:
            p.show(('%', 'h'), path)
    p.block(named)
    def literal(p):
        p.say('say([1, 2, 3]->[1]);', '2')
        p.say('say(+{a => 1, b => [2, 3]}->{b}[1]);', '3')
        p.say('say([[4, 5], [6]]->[0]->[1]);', '5')
        p.say('say(({a => 7})->{a});', '7')
    p.block(literal)

STORES = [
    ('$', 'r', None, [[0], [2], ['a'] and [5]]),
]

def case_store(p):
    def from_undef(p):
        p.lines.append('my $r;')
        p.env['$r'] = None
        p.store(('$', 'r'), ['a', 'b', 2], '=', 1)
        p.say('say(ref($r));', 'HASH')
        for path in (['a', 'b', 2], ['a', 'b', 0], ['a', 'b', 3]):
            p.show(('$', 'r'), path)
        p.show(('$', 'r'), ['a', 'b'])
        p.store(('$', 'r'), ['a', 'c'], '=', 'x')
        p.store(('$', 'r'), ['list', 3, 'k'], '=', 2)
        for path in (['a', 'c'], ['list', 0], ['list', 3], ['list', 3, 'k'], ['list', -1, 'k']):
            p.show(('$', 'r'), path)
    p.block(from_undef)
    def array_from_undef(p):
        p.lines.append('my $q;')
        p.env['$q'] = None
        p.store(('$', 'q'), [1, 0, 'x'], '=', 7)
        for path in ([1, 0, 'x'], [0], [1, 1], [-1, 0, 'x']):
            p.show(('$', 'q'), path)
        p.store(('$', 'q'), [-2], '=', 'first')
        p.store(('$', 'q'), [1, 0, 'y'], '=', [8, 9])
        for path in ([0], [1, 0, 'y', 1], [1, 0, 'y']):
            p.show(('$', 'q'), path)
    p.block(array_from_undef)
    def into_structures(p):
        for name, s in zip('stuv', STRUCTURES):
            p.my(name, s)
        p.store(('$', 's'), [1, 5], '=', 12)
        p.store(('$', 's'), [2, 'n', 1], '=', 'set')
        p.store(('$', 's'), [3, 'made'], '=', 13)
        p.store(('$', 's'), [2, 'new', 0], '=', 14)
        for path in ([1, 5], [1, 4], [1, 2], [2, 'n', 1], [3, 'made'], [2, 'new', 0], [4]):
            p.show(('$', 's'), path)
        p.store(('$', 't'), ['a', 'b', 'd'], '=', 15)
        p.store(('$', 't'), ['u', 0], '=', 16)
        p.store(('$', 't'), ['list', 1, 1], '=', 17)
        for path in (['a', 'b', 'd'], ['a', 'b', 'c'], ['u', 0], ['list', 1, 0], ['list', 1, 1]):
            p.show(('$', 't'), path)
        p.store(('$', 'u'), [0, 0, 0, 1], '=', 18)
        p.store(('$', 'u'), [0, 1, 0, 0], '=', 19)
        for path in ([0, 0, 0, 0], [0, 0, 0, 1], [0, 1, 0, 0], [0, 1, 0]):
            p.show(('$', 'u'), path)
        p.store(('$', 'v'), ['x', 0, 'y', 2], '=', 20)
        p.store(('$', 'v'), ['x', 1, 'y', 0], '=', 21)
        for path in (['x', 0, 'y', 2], ['x', 0, 'y', 1], ['x', 1, 'y', 0], ['x', 1, 'y']):
            p.show(('$', 'v'), path)
    p.block(into_structures)
    def named(p):
        p.lines.append('my @a;')
        p.env['@a'] = []
        p.lines.append('my %h;')
        p.env['%h'] = {}
        p.store(('@', 'a'), [3, 0], '=', 1)
        p.count('a')
        p.store(('@', 'a'), [0, 'k'], '=', 2)
        p.store(('@', 'a'), [-1, 1], '=', 3)
        p.count('a')
        for path in ([3, 0], [3, 1], [0, 'k'], [1], [-4, 'k']):
            p.show(('@', 'a'), path)
        p.store(('%', 'h'), ['x', 'y', 'z'], '=', 4)
        p.store(('%', 'h'), ['w', 2], '=', 5)
        p.store(('%', 'h'), ['x', 'v'], '=', 6)
        p.keys('h')
        for path in (['x', 'y', 'z'], ['x', 'v'], ['w', 2], ['w', 0], ['x', 'y']):
            p.show(('%', 'h'), path)
    p.block(named)

def case_ops(p):
    def ops(p):
        p.lines.append('my $r;')
        p.env['$r'] = None
        p.store(('$', 'r'), ['n'], '+=', 3)
        p.store(('$', 'r'), ['n'], '+=', 4)
        p.store(('$', 'r'), ['m', 0], '-=', 2)
        p.store(('$', 'r'), ['s', 'a'], '.=', 'x')
        p.store(('$', 's', 'a') and ('$', 'r'), ['s', 'a'], '.=', 'y')
        p.store(('$', 'r'), ['d', 'e'], '//=', 4)
        p.store(('$', 'r'), ['d', 'e'], '//=', 5)
        p.store(('$', 'r'), ['o', 1], '||=', 6)
        p.store(('$', 'r'), ['o', 1], '||=', 7)
        p.store(('$', 'r'), ['o', 0], '&&=', 8)
        p.store(('$', 'r'), ['o', 1], '&&=', 9)
        p.store(('$', 'r'), ['y', 'z'], '&&=', 10)
        p.store(('$', 'r'), ['n'], '*=', 3)
        for path in (['n'], ['m', 0], ['s', 'a'], ['d', 'e'], ['o', 0], ['o', 1], ['y', 'z']):
            p.show(('$', 'r'), path)
        p.say('say(exists($r->{y}{z}) ? 1 : 0);', '1' if 'z' in p.env['$r']['y'] else '0')
        for op, before in (('++', False), ('++', True), ('--', False), ('--', True)):
            p.step(('$', 'r'), ['c', 0], op, before)
        p.step(('$', 'r'), ['new', 'x'], '++', False)
        p.step(('$', 'r'), ['new', 'y'], '--', False)
        p.step(('$', 'r'), ['new2', 3], '++', True)
        p.step(('$', 'r'), ['new2', 2], '--', True)
        for path in (['c', 0], ['new', 'x'], ['new', 'y'], ['new2', 3], ['new2', 2], ['new2', 0]):
            p.show(('$', 'r'), path)
    p.block(ops)
    def named(p):
        p.lines.append('my @a;')
        p.env['@a'] = []
        p.lines.append('my %h;')
        p.env['%h'] = {}
        p.step(('@', 'a'), [2, 'n'], '++', False)
        p.step(('@', 'a'), [2, 'n'], '++', True)
        p.store(('%', 'h'), ['x', 1], '+=', 5)
        p.store(('%', 'h'), ['x', 1], '.=', 'z')
        p.step(('%', 'h'), ['y', 'k'], '--', True)
        p.count('a')
        p.keys('h')
        for path in ([2, 'n'], [0]):
            p.show(('@', 'a'), path)
        for path in (['x', 1], ['x', 0], ['y', 'k']):
            p.show(('%', 'h'), path)
    p.block(named)

def case_values(p):
    # Each is short, and what it prints is worked out here by hand, from
    # the definition: a reference is the container itself.
    def identity(p):
        p.lines += ['my $r = [1, 2];', 'my $s = $r;', 'my $t = [1, 2];']
        p.say('say($r == $s ? 1 : 0);', '1')
        p.say('say($r == $t ? 1 : 0);', '0')
        p.say('say($r != $t ? 1 : 0);', '1')
        p.say('say([] == [] ? 1 : 0);', '0')
        p.lines += ['my @a = (5);', 'my %h = (k => 6);', 'my $ra = \\@a;', 'my $rh = \\%h;']
        p.say('say($ra == \\@a ? 1 : 0);', '1')
        p.say('say(\\@a == \\@a ? 1 : 0);', '1')
        p.say('say($rh == \\%h ? 1 : 0);', '1')
        p.lines.append('$a[1] = 7;')
        p.say('say($ra->[1]);', '7')
        p.lines.append('$ra->[2] = 8;')
        p.say('say(scalar(@a));', '3')
        p.lines.append('$rh->{j} = 9;')
        p.say('say(join(",", sort keys(%h)));', 'j,k')
        p.say('say($h{j});', '9')
    p.block(identity)
    def kinds(p):
        p.lines += ['my $r = [1];', 'my $h = {};', 'my $u;', 'my $n = 3;', 'my $s = "ARRAY";']
        for e, v in (('$r', 'ARRAY'), ('$h', 'HASH'), ('$u', ''), ('$n', ''), ('$s', ''), ('[]', 'ARRAY'), ('{}', 'HASH')):
            p.say(f'say("[", ref({e}), "]");', f'[{v}]')
        p.say('say(ref $r eq "ARRAY" ? 1 : 0);', '1')
        p.say('say(ref($h) eq "HASH" ? 1 : 0);', '1')
        p.say('say($r ? "t" : "f", $h ? "t" : "f", !$r ? "t" : "f");', 'ttf')
        p.say('say(defined($r) ? 1 : 0, defined($u) ? 1 : 0);', '10')
        p.say('say($u // $r == $r ? 1 : 0);', '1')
        p.say('say(($r || 0) == $r ? 1 : 0);', '1')
        p.say('say(!!$h ? "t" : "f");', 't')
    p.block(kinds)
    def copies(p):
        p.lines += ['my @rows = ([1, 2], [3, 4]);', 'my @c = @rows;', '$c[0][0] = 9;', '$c[1] = [5];']
        p.say('say($rows[0][0], $rows[1][0], $c[1][0]);', '935')
        p.lines += ['my @d = ([0]) x 2;', '$d[0][0] = 5;']
        p.say('say($d[1][0], $d[0] == $d[1] ? 1 : 0);', '51')
        p.lines += ['my @a = (1, 2);', 'my $c = [@a];', '$a[0] = 7;']
        p.say('say($c->[0], $a[0]);', '17')
        p.lines += ['my @one = [1, 2, 3];']
        p.say('say(scalar(@one), $one[0][2]);', '13')
        p.say('say(+{a => 1, a => 2}->{a});', '2')
        p.lines += ['my %g = (x => [1]);', 'my %f = %g;', '$f{x}[0] = 2;']
        p.say('say($g{x}[0]);', '2')
        p.lines += ['my $deep = {a => [1, {b => 2}]};', 'my $copy = $deep->{a};', '$copy->[1]{b} = 3;']
        p.say('say($deep->{a}[1]{b});', '3')
    p.block(copies)
    def cycles(p):
        p.lines += ['my $q = {n => 1};', '$q->{self} = $q;']
        p.say('say($q->{self}{self}{n}, $q->{self} == $q ? 1 : 0);', '11')
        p.lines += ['my $x = [1];', 'my $y = [$x];', '$x->[1] = $y;']
        p.say('say($x->[1][0][1][0][0]);', '1')
        p.lines += ['for my $k (1 .. 3) {', '    my $c = {k => $k};', '    $c->{me} = $c;', '}', 'my $z;', '$z->[0] = $z;']
        p.say('say($z->[0][0] == $z ? 1 : 0);', '1')
    p.block(cycles)
    def exists_delete(p):
        p.lines += ['my $r = {a => {b => 1, c => undef}, l => [{k => 2}]};', 'my %h = (x => {y => 3});']
        p.say('say(exists($r->{a}{b}) ? 1 : 0, exists($r->{a}{c}) ? 1 : 0, exists($r->{a}{d}) ? 1 : 0);', '110')
        p.say('say(exists $r->{l}[0]{k} ? 1 : 0, exists($h{x}{y}) ? 1 : 0, exists $h{x}->{z} ? 1 : 0);', '110')
        p.say('say(delete($r->{a}{b}), exists($r->{a}{b}) ? 1 : 0);', '10')
        p.lines.append('my $d = delete $h{x}{y};')
        p.say('say($d, exists($h{x}{y}) ? 1 : 0, exists($h{x}) ? 1 : 0);', '301')
        p.say('say(defined(delete($r->{a}{nope})) ? 1 : 0);', '0')
        p.lines.append('delete $r->{l}[0]{k};')
        p.say('say(exists($r->{l}[0]{k}) ? 1 : 0);', '0')
    p.block(exists_delete)
    def a_my_again(p):
        p.lines += ['my @r;', 'for my $i (1 .. 3) {', '    my @a = ($i);', '    push @r, \\@a;', '}']
        p.say('say($r[0][0], $r[1][0], $r[2][0]);', '123')
        p.subs += ['sub fresh() {', '    my %h = (n => 1);', '    return \\%h;', '}']
        p.lines += ['my $f = fresh();', 'my $g = fresh();', '$f->{n} = 2;']
        p.say('say($g->{n}, $f == $g ? 1 : 0);', '10')
    p.block(a_my_again)

def case_loops(p):
    def loops(p):
        p.lines += ['my @rows = ([1, "a"], [2, "b"], [3, "c"]);', 'for my $row (@rows) {', '    say($row->[0], $row->[1]);', '}']
        p.out += ['1a', '2b', '3c']
        p.lines += ['for (@rows) {', '    $_->[0] *= 10;', '}']
        p.say('say($rows[0][0], $rows[2][0]);', '1030')
        p.lines += ['my @recs = ({n => 3, name => "c"}, {n => 1, name => "a"}, {n => 2, name => "b"});']
        p.say('say(join(",", map { $_->{name} } sort { $a->{n} <=> $b->{n} } @recs));', 'a,b,c')
        p.say('say(join(",", map { $_->{n} } grep { $_->{name} ne "b" } @recs));', '3,1')
        p.say('say(join(",", map { $_->[0] } sort { $b->[0] <=> $a->[0] } @rows));', '30,20,10')
        p.lines += ['my $r = [7, 8, 9];', 'for my $x ($r->[0], $r->[2]) {', '    say($x);', '}']
        p.out += ['7', '9']
        p.lines += ['my %by = (a => [1, 2], b => [3]);', 'for my $k (sort keys(%by)) {', '    say($k, $by{$k}[0], defined($by{$k}[1]) ? $by{$k}[1] : "u");', '}']
        p.out += ['a12', 'b3u']
        p.say('say(join(",", map { $_ * 2 } ($r->[0], $r->[1])));', '14,16')
        p.lines += ['my $total = 0;', '$total += $_->[0] for @rows;']
        p.say('say($total);', '60')
    p.block(loops)
    def subs(p):
        p.subs += ['sub total($t) {', '    return $t->[0] + $t->[1];', '}', 'sub make($n) {', '    return { n => $n, l => [$n, $n * 2] };', '}',
                    'sub mark($p) {', '    $p->[0] = 1;', '    return ref($p);', '}']
        p.say('say(total([3, 4]));', '7')
        p.say('say(make(5)->{l}[1], make(6)->{n});', '106')
        p.lines += ['my $m = make(2);', '$m->{l}[0] = 9;']
        p.say('say($m->{l}[0], make(2)->{l}[0]);', '92')
        p.lines += ['my $u;']
        p.say('say(mark($u), defined($u) ? 1 : 0);', 'ARRAY0')
        p.lines += ['my $w = [0];', 'mark($w);']
        p.say('say($w->[0]);', '1')
        p.subs += ['sub pair() {', '    return ([1], {k => 2});', '}']
        p.lines += ['my @p = pair();']
        p.say('say($p[0][0], $p[1]{k});', '12')
        p.subs += ['sub add_to($l, $v) {', '    $l->[0] += $v;', '    return;', '}']
        p.lines += ['my $acc = [1];', 'add_to($acc, 4);']
        p.say('say($acc->[0]);', '5')
    p.block(subs)

SAME = {
    '1810': ('ref-reads', case_read),
    '1811': ('ref-stores', case_store),
    '1812': ('ref-assigning-operators-and-steps', case_ops),
    '1813': ('ref-as-values', case_values),
    '1814': ('ref-in-loops-and-subs', case_loops),
}

# ---- the faults: each program says 1, does the one thing, and says 2.
# What the thing is, and its fault, is the definition's; the path cases are
# worked out by the simulation above, which must fault where the table says.

def path_fault(setup, base, subs, store=None):
    def check():
        p = Prog()
        for name, v in setup.items():
            p.env[name] = fresh(v)
        try:
            if store is None:
                p.read(base, subs)
            else:
                p.made(base, subs)
                c = p.made(base, subs)
                if isinstance(c, list) and subs[-1] < -len(c):
                    raise Fault(BEFORE)
        except Fault as f:
            return str(f)
        return None
    return check

FAULTS = []

def fault(name, lines, message, check=None):
    FAULTS.append((name, lines, message, check))

R = ('$', 'r')
# Reading through what is not a reference (D107).
fault('read-undef', ['my $r;', 'say($r->[0]);'], UNDEF_REF, path_fault({'$r': None}, R, [0]))
fault('read-undef-hash', ['my $r;', 'my $x = $r->{a};'], UNDEF_REF, path_fault({'$r': None}, R, ['a']))
fault('read-through-missing-index', ['my $r = [];', 'say(defined($r->[0][1]) ? 1 : 0);'], UNDEF_REF, path_fault({'$r': []}, R, [0, 1]))
fault('read-through-missing-key', ['my $h = {};', 'my $x = $h->{a}{b};'], UNDEF_REF, path_fault({'$h': {}}, ('$', 'h'), ['a', 'b']))
fault('read-through-undef-element', ['my $r = [1, undef];', 'say($r->[1]{k});'], UNDEF_REF, path_fault({'$r': [1, None]}, R, [1, 'k']))
fault('read-named-hash-through-missing', ['my %h;', 'say(defined($h{a}{b}) ? 1 : 0);'], UNDEF_REF, path_fault({'%h': {}}, ('%', 'h'), ['a', 'b']))
fault('read-named-array-through-missing', ['my @a;', 'my $t = $a[3][0];'], UNDEF_REF, path_fault({'@a': []}, ('@', 'a'), [3, 0]))
fault('read-a-number', ['my $x = 5;', 'say($x->[0]);'], NOT_ARRAY, path_fault({'$x': 5}, ('$', 'x'), [0]))
fault('read-a-string', ['my $x = "k";', 'say($x->{k});'], NOT_HASH, path_fault({'$x': 'k'}, ('$', 'x'), ['k']))
fault('read-a-hash-as-an-array', ['my $x = {};', 'say(defined($x->[0]) ? 1 : 0);'], NOT_ARRAY, path_fault({'$x': {}}, ('$', 'x'), [0]))
fault('read-an-array-as-a-hash', ['my $x = [1];', 'say(defined($x->{a}) ? 1 : 0);'], NOT_HASH, path_fault({'$x': [1]}, ('$', 'x'), ['a']))
fault('read-deep-wrong-kind', ['my $x = {a => [1, {b => 2}]};', 'say($x->{a}[1][0]);'], NOT_ARRAY, path_fault({'$x': {'a': [1, {'b': 2}]}}, ('$', 'x'), ['a', 1, 0]))
fault('read-through-a-number-element', ['my $x = [5];', 'say($x->[0][0]);'], NOT_ARRAY, path_fault({'$x': [5]}, ('$', 'x'), [0, 0]))
fault('read-a-literal', ['say([1]->{a});'], NOT_HASH)
fault('exists-through-undef', ['my $r;', 'say(exists($r->{a}) ? 1 : 0);'], UNDEF_REF)
fault('exists-through-missing', ['my %h;', 'say(exists($h{a}{b}) ? 1 : 0);'], UNDEF_REF)
fault('delete-through-undef', ['my $r;', 'delete $r->{a};'], UNDEF_REF)
fault('delete-through-an-array', ['my $r = [1];', 'delete $r->{a};'], NOT_HASH)
fault('call-gives-undef-read', ['sub f() {', '    return undef;', '}', 'say(f()->[0]);'], UNDEF_REF)
# Storing through what is defined and not the reference wanted (T234).
fault('store-through-empty-string', ['my $x = "";', '$x->{a} = 1;'], NOT_HASH, path_fault({'$x': ''}, ('$', 'x'), ['a'], store=True))
fault('store-through-false', ['my $x = false;', '$x->[0] = 1;'], NOT_ARRAY)
fault('store-through-a-number', ['my $x = [5];', '$x->[0][1] = 1;'], NOT_ARRAY, path_fault({'$x': [5]}, ('$', 'x'), [0, 1], store=True))
fault('store-through-the-other-kind', ['my %h = (a => [1]);', '$h{a}{b} = 2;'], NOT_HASH, path_fault({'%h': {'a': [1]}}, ('%', 'h'), ['a', 'b'], store=True))
fault('step-through-a-hash-as-an-array', ['my $x = {};', '$x->[0]++;'], NOT_ARRAY)
fault('store-before-the-start', ['my $r = [1];', '$r->[-3] = 1;'], BEFORE, path_fault({'$r': [1]}, R, [-3], store=True))
fault('store-hop-before-the-start', ['my $r = [1];', '$r->[-3]{a} = 1;'], BEFORE)
# Only a variable or an element is made (T252); a read-only one holding
# undef is not made either (T250).
fault('store-through-a-call', ['sub f() {', '    return undef;', '}', 'f()->[0] = 5;'], UNDEF_REF)
fault('store-through-or', ['my ($r, $s);', '($r || $s)->[0] = 5;'], UNDEF_REF)
fault('store-through-a-choice', ['my ($r, $s);', 'my $c = 1;', '($c ? $r : $s)->[0] = 5;'], UNDEF_REF)
fault('store-through-loop-variable', ['my @l = (undef, undef);', 'for my $x (@l) {', '    $x->[0] = 1;', '}'], UNDEF_REF)
fault('store-through-it', ['my @m = (undef);', '$_->{n} = 1 for @m;'], UNDEF_REF)
fault('step-through-it-in-a-map', ['my @m = (undef);', 'my @n = map { $_->[0]++ } @m;'], UNDEF_REF)
# A new hash's odd list (T244).
fault('odd-new-hash', ['my $h = {a => 1, "b"};'], ODD)
fault('odd-new-hash-assigned', ['my %h = {a => 1};'], ODD)
# A reference where a number or a string is wanted (D112).
NUMS = [('add', 'my $x = $r + 1;'), ('add-right', 'my $x = 1 + $r;'), ('subtract', 'my $x = $r - 1;'), ('multiply', 'my $x = $r * 2;'),
        ('divide', 'my $x = $r / 2;'), ('modulus', 'my $x = $r % 2;'), ('power', 'my $x = $r ** 2;'), ('negate', 'my $x = -$r;'),
        ('increment', '$r++;'), ('decrement', '--$r;'), ('add-to', '$r += 1;'), ('less', 'say($r < 1 ? 1 : 0);'),
        ('compare', 'say($r <=> $r);'), ('equal-to-a-number', 'say($r == 0 ? 1 : 0);'), ('number-equal-to', 'say(0 == $r ? 1 : 0);'),
        ('not-equal-to-undef', 'my $u = 1;\nsay($r != $u ? 1 : 0);'), ('index', 'my @a = (1);\nsay($a[$r]);'), ('chr', 'say(chr($r));'),
        ('repeat-count', 'say("a" x $r);'), ('substr-position', 'say(substr("abc", $r));'), ('range', 'my @l = (1 .. $r);'),
        ('range-loop', 'for my $i ($r .. 2) {\n}'), ('sort-block', 'my @s = sort { $r } (1, 2);')]
STRS = [('say', 'say($r);'), ('print', 'print($r);'), ('in-a-list', 'say("a", $r);'), ('concat', 'my $x = $r . "";'),
        ('concat-to', 'my $s = "";\n$s .= $r;'), ('interpolated', 'my $x = "$r";'), ('equal', 'say($r eq $r ? 1 : 0);'),
        ('compare-strings', 'say($r cmp "a");'), ('less-string', 'say("a" lt $r ? 1 : 0);'), ('repeat', 'my $x = $r x 2;'),
        ('length', 'say(length($r));'), ('uc', 'say(uc($r));'), ('lc', 'say(lc $r);'), ('ord', 'say(ord($r));'),
        ('substr', 'say(substr($r, 0, 1));'), ('index-of', 'say(index("abc", $r));'), ('key', 'my %h;\n$h{$r} = 1;'),
        ('key-read', 'my %h;\nsay(defined($h{$r}) ? 1 : 0);'), ('join', 'say(join(",", $r));'), ('join-separator', 'say(join($r, 1, 2));'),
        ('sort', 'my @l = ($r, [2]);\nmy @s = sort @l;'), ('hash-list', 'my %h = ($r, 1);')]
for name, code in NUMS:
    fault(f'reference-as-a-number-{name}', ['my $r = [1];'] + code.split('\n'), NUMBER)
for name, code in STRS:
    fault(f'reference-as-a-string-{name}', ['my $r = [1];'] + code.split('\n'), STRING)
# The freeze is the container's, whatever reaches it (T237, D114, T251).
fault('frozen-through-a-reference', ['my @a = (1, 2);', 'my $r = \\@a;', 'for my $x (@a) {', '    $r->[0] = 5;', '    last;', '}'], FROZEN)
fault('frozen-hash-through-a-reference', ['my %h = (a => 1);', 'my $r = \\%h;', 'for my $v (values(%h)) {', '    $r->{b} = 5;', '    last;', '}'], HFROZEN)
fault('frozen-by-a-chain-in-the-list', ['my $r = [7, 8];', 'for my $x ($r->[0], $r->[1]) {', '    my $s = $r;', '    $s->[0] = 9;', '    last;', '}'], FROZEN)
fault('frozen-inner-by-a-chain', ['my @a = ([1, 2]);', 'for my $x ($a[0][0], $a[0][1]) {', '    my $in = $a[0];', '    $in->[1] = 3;', '    last;', '}'], FROZEN)
fault('frozen-hash-by-a-chain-in-a-map', ['my $r = {a => 1};', 'my $s = $r;', 'my @l = map { $s->{b} = 2 } ($r->{a});'], HFROZEN)
fault('frozen-by-a-chain-in-a-sort', ['my $r = [2, 1];', 'my $s = $r;', 'my @l = sort { $s->[0] = 3; $a <=> $b } ($r->[0], $r->[1]);'], FROZEN)
fault('frozen-made-in', ['my @a = (undef, 1);', 'for my $x (@a) {', '    $a[0][0] = 1;', '    last;', '}'], FROZEN)
fault('frozen-from-a-sub', ['my $r = [1, 2];', 'sub poke($s) {', '    $s->[1] = 0;', '    return;', '}', 'for my $x ($r->[0]) {', '    poke($r);', '}'], FROZEN)
fault('past-the-end-in-a-loop', ['my $r = [1];', 'for my $x ($r->[3]) {', '}'], PAST)
fault('no-key-in-a-loop', ['my $r = {a => 1};', 'for my $x ($r->{b}) {', '}'], KEY_PAST)
fault('past-the-end-in-a-grep', ['my $r = [1];', 'my @g = grep { 1 } ($r->[0], $a[0][5]);'.replace(', $a[0][5]', ', $r->[2]')], PAST)

def commands():
    out = []
    for number, (name, _) in SAME.items():
        out.append(f'    python3 t/models/ref.py --program {number} > t/{number}-{name}.pl')
        out.append(f'    python3 t/models/ref.py {number} > t/{number}-{name}.expected')
    for n, (name, _, _, _) in enumerate(FAULTS):
        number = 1820 + n
        out.append(f'    python3 t/models/ref.py --program {number} > t/{number}-fault-{name}.pl')
        out.append(f'    python3 t/models/ref.py {number} > t/{number}-fault-{name}.expected')
    return '\n'.join(out) + '\n'

HEAD = '# model: t/models/ref.py\nuse v5.42;\n'

def main(argv):
    if argv == ['--commands']:
        sys.stdout.write(commands())
        return
    assert commands() in __doc__, 'the commands in the docstring are not the tests: python3 t/models/ref.py --commands'
    want_program = argv[0] == '--program'
    number = argv[-1]
    if number in SAME:
        name, case = SAME[number]
        p = Prog()
        case(p)
        indent = 0
        body = []
        for line in p.lines:
            for l in line.split('\n'):
                if l == '}':
                    indent -= 1
                body.append('    ' * indent + l)
                if l == '{':
                    indent += 1
        sys.stdout.write(HEAD + ''.join(l + '\n' for l in p.subs) + '\n'.join(body) + '\n' if want_program else '\n'.join(p.out) + '\n')
        return
    n = int(number) - 1820
    name, lines, message, check = FAULTS[n]
    if check is not None:
        assert check() == message, (name, check(), message)
    program = '# kind: fault\n' + HEAD + 'say(1);\n' + '\n'.join(lines) + '\nsay(2);\n'
    if want_program:
        sys.stdout.write(program)
        return
    # The line of the statement that faults: the last of `lines` that is a
    # statement begun on its own line, or the loop round it.
    at = FAULT_LINE.get(name)
    line = 5 + (at if at is not None else len(lines) - 1)
    sys.stdout.write(f'1\nfault: {message} at t/{number}-fault-{name}.pl line {line}.\nexit: 1\n')

# Where a fault is not on the last line of its lines: the index of its line.
FAULT_LINE = {
    'store-through-loop-variable': 2, 'frozen-through-a-reference': 3, 'frozen-hash-through-a-reference': 3,
    'frozen-by-a-chain-in-the-list': 3, 'frozen-inner-by-a-chain': 3, 'frozen-made-in': 2, 'frozen-from-a-sub': 2,
    'past-the-end-in-a-loop': 1, 'no-key-in-a-loop': 1, 'range-loop': 1,
    'reference-as-a-number-range-loop': 1,
}

if __name__ == '__main__':
    main(sys.argv[1:])
