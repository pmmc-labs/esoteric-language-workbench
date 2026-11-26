#!/usr/bin/env python3
"""t/1500 to t/1530: hashes (step 12a; D27, D98, D102).

The definition, which is all this file knows of the language beyond
t/models/interp.py.

  my %h;  my %h = LIST;  %h = LIST;
  $h{KEY}                      the element
  $h{KEY} = V   OP=   ++  --   stored, and worked on, as an array's is
  exists($h{KEY})  delete($h{KEY})
  keys(%h)  values(%h)  %h     lists; where one value is wanted, a count

**A hash is an array whose indexes are strings.** A key is made a string
as `.` makes one (a number as it prints, a boolean `1` or the empty
string), and an undef key is a fault. One word alone in the braces, and a
word before `=>`, is that string, whatever the word.

A list for a hash is keys and values by turns: a key given twice keeps its
last value and its first place, and **an odd number of values is a
fault**. Reading a key that is not there gives undef and makes nothing;
storing makes it; an operator that reads and stores (`+=`, `//=`, `++`)
makes it first. The orders are an array's (D80): `$h{K} = V` is V, then K,
then the store; `$h{K} OP= V` is K, the element made, then V.

`delete` gives the value that was there, or undef. Where one value is
wanted, `%h`, `keys(%h)` and `values(%h)` are how many keys there are.
After `return`, each is list-shaped (D18).

**The order** (D27) is the order keys were first stored in; a key deleted
and stored again is last. perl's is another every run, so every test here
sorts what it shows, and t/checks.py refuses one that does not: the order
itself has a test of its own kind, by hand.

This model works a program out; it does not refuse one: where a word may
stand, D76, and what `exists` may be followed by are the compiler's.

The model is Python, whose dict keeps the order of first storing. perl is
the second derivation: t/checks.py oracle holds every .expected of a test
without a `kind:` to what perl 5.42 prints, and each fault test's output
to the start of it.

1500 is the literal and its keys, 1501 elements, 1502 exists, delete, the
counts and copies. 1510 on each fault once.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/hash.py --program 1500 > t/1500-hash-literals-and-keys.pl
    python3 t/models/hash.py 1500 > t/1500-hash-literals-and-keys.expected
    python3 t/models/hash.py --program 1501 > t/1501-hash-elements.pl
    python3 t/models/hash.py 1501 > t/1501-hash-elements.expected
    python3 t/models/hash.py --program 1502 > t/1502-hash-exists-delete-counts.pl
    python3 t/models/hash.py 1502 > t/1502-hash-exists-delete-counts.expected
    python3 t/models/hash.py --program 1503 > t/1503-hash-order-by-the-model.pl
    python3 t/models/hash.py 1503 > t/1503-hash-order-by-the-model.expected
    python3 t/models/hash.py --program 1510 > t/1510-fault-hash-odd-list.pl
    python3 t/models/hash.py 1510 > t/1510-fault-hash-odd-list.expected
    python3 t/models/hash.py --program 1511 > t/1511-fault-hash-odd-list-assigned.pl
    python3 t/models/hash.py 1511 > t/1511-fault-hash-odd-list-assigned.expected
    python3 t/models/hash.py --program 1512 > t/1512-fault-hash-odd-list-of-one.pl
    python3 t/models/hash.py 1512 > t/1512-fault-hash-odd-list-of-one.expected
    python3 t/models/hash.py --program 1513 > t/1513-fault-hash-odd-list-from-an-array.pl
    python3 t/models/hash.py 1513 > t/1513-fault-hash-odd-list-from-an-array.expected
    python3 t/models/hash.py --program 1514 > t/1514-fault-hash-odd-list-from-a-hash-and-one.pl
    python3 t/models/hash.py 1514 > t/1514-fault-hash-odd-list-from-a-hash-and-one.expected
    python3 t/models/hash.py --program 1515 > t/1515-fault-hash-undef-key-read.pl
    python3 t/models/hash.py 1515 > t/1515-fault-hash-undef-key-read.expected
    python3 t/models/hash.py --program 1516 > t/1516-fault-hash-undef-key-stored.pl
    python3 t/models/hash.py 1516 > t/1516-fault-hash-undef-key-stored.expected
    python3 t/models/hash.py --program 1517 > t/1517-fault-hash-undef-key-worked-on.pl
    python3 t/models/hash.py 1517 > t/1517-fault-hash-undef-key-worked-on.expected
    python3 t/models/hash.py --program 1518 > t/1518-fault-hash-undef-key-stepped.pl
    python3 t/models/hash.py 1518 > t/1518-fault-hash-undef-key-stepped.expected
    python3 t/models/hash.py --program 1519 > t/1519-fault-hash-undef-key-exists.pl
    python3 t/models/hash.py 1519 > t/1519-fault-hash-undef-key-exists.expected
    python3 t/models/hash.py --program 1520 > t/1520-fault-hash-undef-key-deleted.pl
    python3 t/models/hash.py 1520 > t/1520-fault-hash-undef-key-deleted.expected
    python3 t/models/hash.py --program 1521 > t/1521-fault-hash-undef-key-in-a-list.pl
    python3 t/models/hash.py 1521 > t/1521-fault-hash-undef-key-in-a-list.expected
    python3 t/models/hash.py --program 1522 > t/1522-fault-hash-whole-num-key.pl
    python3 t/models/hash.py 1522 > t/1522-fault-hash-whole-num-key.expected
    python3 t/models/hash.py --program 1523 > t/1523-fault-hash-whole-num-key-read.pl
    python3 t/models/hash.py 1523 > t/1523-fault-hash-whole-num-key-read.expected
    python3 t/models/hash.py --program 1524 > t/1524-fault-hash-whole-num-key-in-a-list.pl
    python3 t/models/hash.py 1524 > t/1524-fault-hash-whole-num-key-in-a-list.expected
    python3 t/models/hash.py --program 1525 > t/1525-fault-hash-missing-as-a-number.pl
    python3 t/models/hash.py 1525 > t/1525-fault-hash-missing-as-a-number.expected
    python3 t/models/hash.py --program 1526 > t/1526-fault-hash-missing-as-a-string.pl
    python3 t/models/hash.py 1526 > t/1526-fault-hash-missing-as-a-string.expected
    python3 t/models/hash.py --program 1527 > t/1527-fault-hash-deleted-as-a-string.pl
    python3 t/models/hash.py 1527 > t/1527-fault-hash-deleted-as-a-string.expected
    python3 t/models/hash.py --program 1528 > t/1528-fault-hash-string-stepped.pl
    python3 t/models/hash.py 1528 > t/1528-fault-hash-string-stepped.expected
    python3 t/models/hash.py --program 1529 > t/1529-fault-hash-returned-for-one-value.pl
    python3 t/models/hash.py 1529 > t/1529-fault-hash-returned-for-one-value.expected
    python3 t/models/hash.py --program 1530 > t/1530-fault-hash-keys-returned-for-one-value.pl
    python3 t/models/hash.py 1530 > t/1530-fault-hash-keys-returned-for-one-value.expected
    python3 t/models/hash.py --program 1620 > t/1620-hash-in-loops.pl
    python3 t/models/hash.py 1620 > t/1620-hash-in-loops.expected
    python3 t/models/hash.py --program 1621 > t/1621-hash-loops-order-by-the-model.pl
    python3 t/models/hash.py 1621 > t/1621-hash-loops-order-by-the-model.expected
    python3 t/models/hash.py --program 1622 > t/1622-hash-slices.pl
    python3 t/models/hash.py 1622 > t/1622-hash-slices.expected
    python3 t/models/hash.py --program 1623 > t/1623-hash-parameter.pl
    python3 t/models/hash.py 1623 > t/1623-hash-parameter.expected
    python3 t/models/hash.py --program 1624 > t/1624-hash-in-strings.pl
    python3 t/models/hash.py 1624 > t/1624-hash-in-strings.expected
    python3 t/models/hash.py --program 1640 > t/1640-fault-hash-frozen-for-over-values.pl
    python3 t/models/hash.py 1640 > t/1640-fault-hash-frozen-for-over-values.expected
    python3 t/models/hash.py --program 1641 > t/1641-fault-hash-frozen-for-over-the-hash.pl
    python3 t/models/hash.py 1641 > t/1641-fault-hash-frozen-for-over-the-hash.expected
    python3 t/models/hash.py --program 1642 > t/1642-fault-hash-frozen-for-over-a-slice.pl
    python3 t/models/hash.py 1642 > t/1642-fault-hash-frozen-for-over-a-slice.expected
    python3 t/models/hash.py --program 1643 > t/1643-fault-hash-frozen-for-over-an-element.pl
    python3 t/models/hash.py 1643 > t/1643-fault-hash-frozen-for-over-an-element.expected
    python3 t/models/hash.py --program 1644 > t/1644-fault-hash-frozen-for-it-over-values.pl
    python3 t/models/hash.py 1644 > t/1644-fault-hash-frozen-for-it-over-values.expected
    python3 t/models/hash.py --program 1645 > t/1645-fault-hash-frozen-for-it-over-the-hash.pl
    python3 t/models/hash.py 1645 > t/1645-fault-hash-frozen-for-it-over-the-hash.expected
    python3 t/models/hash.py --program 1646 > t/1646-fault-hash-frozen-for-it-over-a-slice.pl
    python3 t/models/hash.py 1646 > t/1646-fault-hash-frozen-for-it-over-a-slice.expected
    python3 t/models/hash.py --program 1647 > t/1647-fault-hash-frozen-for-it-over-an-element.pl
    python3 t/models/hash.py 1647 > t/1647-fault-hash-frozen-for-it-over-an-element.expected
    python3 t/models/hash.py --program 1648 > t/1648-fault-hash-frozen-for-modifier-over-values.pl
    python3 t/models/hash.py 1648 > t/1648-fault-hash-frozen-for-modifier-over-values.expected
    python3 t/models/hash.py --program 1649 > t/1649-fault-hash-frozen-for-modifier-over-the-hash.pl
    python3 t/models/hash.py 1649 > t/1649-fault-hash-frozen-for-modifier-over-the-hash.expected
    python3 t/models/hash.py --program 1650 > t/1650-fault-hash-frozen-for-modifier-over-a-slice.pl
    python3 t/models/hash.py 1650 > t/1650-fault-hash-frozen-for-modifier-over-a-slice.expected
    python3 t/models/hash.py --program 1651 > t/1651-fault-hash-frozen-for-modifier-over-an-element.pl
    python3 t/models/hash.py 1651 > t/1651-fault-hash-frozen-for-modifier-over-an-element.expected
    python3 t/models/hash.py --program 1652 > t/1652-fault-hash-frozen-map-over-values.pl
    python3 t/models/hash.py 1652 > t/1652-fault-hash-frozen-map-over-values.expected
    python3 t/models/hash.py --program 1653 > t/1653-fault-hash-frozen-map-over-the-hash.pl
    python3 t/models/hash.py 1653 > t/1653-fault-hash-frozen-map-over-the-hash.expected
    python3 t/models/hash.py --program 1654 > t/1654-fault-hash-frozen-map-over-a-slice.pl
    python3 t/models/hash.py 1654 > t/1654-fault-hash-frozen-map-over-a-slice.expected
    python3 t/models/hash.py --program 1655 > t/1655-fault-hash-frozen-map-over-an-element.pl
    python3 t/models/hash.py 1655 > t/1655-fault-hash-frozen-map-over-an-element.expected
    python3 t/models/hash.py --program 1656 > t/1656-fault-hash-frozen-grep-over-values.pl
    python3 t/models/hash.py 1656 > t/1656-fault-hash-frozen-grep-over-values.expected
    python3 t/models/hash.py --program 1657 > t/1657-fault-hash-frozen-grep-over-the-hash.pl
    python3 t/models/hash.py 1657 > t/1657-fault-hash-frozen-grep-over-the-hash.expected
    python3 t/models/hash.py --program 1658 > t/1658-fault-hash-frozen-grep-over-a-slice.pl
    python3 t/models/hash.py 1658 > t/1658-fault-hash-frozen-grep-over-a-slice.expected
    python3 t/models/hash.py --program 1659 > t/1659-fault-hash-frozen-grep-over-an-element.pl
    python3 t/models/hash.py 1659 > t/1659-fault-hash-frozen-grep-over-an-element.expected
    python3 t/models/hash.py --program 1660 > t/1660-fault-hash-frozen-sort-over-values.pl
    python3 t/models/hash.py 1660 > t/1660-fault-hash-frozen-sort-over-values.expected
    python3 t/models/hash.py --program 1661 > t/1661-fault-hash-frozen-sort-over-the-hash.pl
    python3 t/models/hash.py 1661 > t/1661-fault-hash-frozen-sort-over-the-hash.expected
    python3 t/models/hash.py --program 1662 > t/1662-fault-hash-frozen-sort-over-a-slice.pl
    python3 t/models/hash.py 1662 > t/1662-fault-hash-frozen-sort-over-a-slice.expected
    python3 t/models/hash.py --program 1663 > t/1663-fault-hash-frozen-sort-over-an-element.pl
    python3 t/models/hash.py 1663 > t/1663-fault-hash-frozen-sort-over-an-element.expected
    python3 t/models/hash.py --program 1664 > t/1664-fault-hash-frozen-a-new-key.pl
    python3 t/models/hash.py 1664 > t/1664-fault-hash-frozen-a-new-key.expected
    python3 t/models/hash.py --program 1665 > t/1665-fault-hash-frozen-worked-on.pl
    python3 t/models/hash.py 1665 > t/1665-fault-hash-frozen-worked-on.expected
    python3 t/models/hash.py --program 1666 > t/1666-fault-hash-frozen-or-assigned.pl
    python3 t/models/hash.py 1666 > t/1666-fault-hash-frozen-or-assigned.expected
    python3 t/models/hash.py --program 1667 > t/1667-fault-hash-frozen-and-assigned-a-new-key.pl
    python3 t/models/hash.py 1667 > t/1667-fault-hash-frozen-and-assigned-a-new-key.expected
    python3 t/models/hash.py --program 1668 > t/1668-fault-hash-frozen-stepped.pl
    python3 t/models/hash.py 1668 > t/1668-fault-hash-frozen-stepped.expected
    python3 t/models/hash.py --program 1669 > t/1669-fault-hash-frozen-a-slice-stored.pl
    python3 t/models/hash.py 1669 > t/1669-fault-hash-frozen-a-slice-stored.expected
    python3 t/models/hash.py --program 1670 > t/1670-fault-hash-frozen-delete-under-an-element.pl
    python3 t/models/hash.py 1670 > t/1670-fault-hash-frozen-delete-under-an-element.expected
    python3 t/models/hash.py --program 1671 > t/1671-fault-hash-frozen-delete-of-a-slice-under-an-element.pl
    python3 t/models/hash.py 1671 > t/1671-fault-hash-frozen-delete-of-a-slice-under-an-element.expected
    python3 t/models/hash.py --program 1672 > t/1672-fault-hash-frozen-for-from-a-sub.pl
    python3 t/models/hash.py 1672 > t/1672-fault-hash-frozen-for-from-a-sub.expected
    python3 t/models/hash.py --program 1673 > t/1673-fault-hash-frozen-for-modifier-from-a-sub.pl
    python3 t/models/hash.py 1673 > t/1673-fault-hash-frozen-for-modifier-from-a-sub.expected
    python3 t/models/hash.py --program 1674 > t/1674-fault-hash-frozen-map-from-a-sub.pl
    python3 t/models/hash.py 1674 > t/1674-fault-hash-frozen-map-from-a-sub.expected
    python3 t/models/hash.py --program 1675 > t/1675-fault-hash-frozen-grep-from-a-sub.pl
    python3 t/models/hash.py 1675 > t/1675-fault-hash-frozen-grep-from-a-sub.expected
    python3 t/models/hash.py --program 1676 > t/1676-fault-hash-frozen-sort-from-a-sub.pl
    python3 t/models/hash.py 1676 > t/1676-fault-hash-frozen-sort-from-a-sub.expected
    python3 t/models/hash.py --program 1677 > t/1677-fault-hash-given-back-after-a-loop.pl
    python3 t/models/hash.py 1677 > t/1677-fault-hash-given-back-after-a-loop.expected
    python3 t/models/hash.py --program 1678 > t/1678-fault-hash-given-back-after-a-map.pl
    python3 t/models/hash.py 1678 > t/1678-fault-hash-given-back-after-a-map.expected
    python3 t/models/hash.py --program 1679 > t/1679-fault-hash-frozen-after-the-inner-loop.pl
    python3 t/models/hash.py 1679 > t/1679-fault-hash-frozen-after-the-inner-loop.expected
    python3 t/models/hash.py --program 1680 > t/1680-fault-hash-names-by-second-of-two.pl
    python3 t/models/hash.py 1680 > t/1680-fault-hash-names-by-second-of-two.expected
    python3 t/models/hash.py --program 1681 > t/1681-fault-hash-names-by-a-map-of-it.pl
    python3 t/models/hash.py 1681 > t/1681-fault-hash-names-by-a-map-of-it.expected
    python3 t/models/hash.py --program 1682 > t/1682-fault-hash-names-by-a-sort-of-it.pl
    python3 t/models/hash.py 1682 > t/1682-fault-hash-names-by-a-sort-of-it.expected
    python3 t/models/hash.py --program 1683 > t/1683-fault-hash-names-by-reverse.pl
    python3 t/models/hash.py 1683 > t/1683-fault-hash-names-by-reverse.expected
    python3 t/models/hash.py --program 1684 > t/1684-fault-hash-names-by-an-exists.pl
    python3 t/models/hash.py 1684 > t/1684-fault-hash-names-by-an-exists.expected
    python3 t/models/hash.py --program 1685 > t/1685-fault-hash-names-by-a-key-worked-out.pl
    python3 t/models/hash.py 1685 > t/1685-fault-hash-names-by-a-key-worked-out.expected
    python3 t/models/hash.py --program 1686 > t/1686-fault-hash-no-key-for.pl
    python3 t/models/hash.py 1686 > t/1686-fault-hash-no-key-for.expected
    python3 t/models/hash.py --program 1687 > t/1687-fault-hash-no-key-for-it.pl
    python3 t/models/hash.py 1687 > t/1687-fault-hash-no-key-for-it.expected
    python3 t/models/hash.py --program 1688 > t/1688-fault-hash-no-key-for-modifier.pl
    python3 t/models/hash.py 1688 > t/1688-fault-hash-no-key-for-modifier.expected
    python3 t/models/hash.py --program 1689 > t/1689-fault-hash-no-key-map.pl
    python3 t/models/hash.py 1689 > t/1689-fault-hash-no-key-map.expected
    python3 t/models/hash.py --program 1690 > t/1690-fault-hash-no-key-grep.pl
    python3 t/models/hash.py 1690 > t/1690-fault-hash-no-key-grep.expected
    python3 t/models/hash.py --program 1691 > t/1691-fault-hash-no-key-sort.pl
    python3 t/models/hash.py 1691 > t/1691-fault-hash-no-key-sort.expected
    python3 t/models/hash.py --program 1692 > t/1692-fault-hash-no-key-in-a-slice.pl
    python3 t/models/hash.py 1692 > t/1692-fault-hash-no-key-in-a-slice.expected
    python3 t/models/hash.py --program 1693 > t/1693-fault-hash-no-key-in-a-slice-in-a-map.pl
    python3 t/models/hash.py 1693 > t/1693-fault-hash-no-key-in-a-slice-in-a-map.expected
    python3 t/models/hash.py --program 1694 > t/1694-fault-hash-no-key-deleted-first.pl
    python3 t/models/hash.py 1694 > t/1694-fault-hash-no-key-deleted-first.expected
    python3 t/models/hash.py --program 1695 > t/1695-fault-hash-odd-arguments.pl
    python3 t/models/hash.py 1695 > t/1695-fault-hash-odd-arguments.expected
    python3 t/models/hash.py --program 1696 > t/1696-fault-hash-odd-arguments-from-a-list.pl
    python3 t/models/hash.py 1696 > t/1696-fault-hash-odd-arguments-from-a-list.expected
    python3 t/models/hash.py --program 1697 > t/1697-fault-hash-odd-arguments-no-name.pl
    python3 t/models/hash.py 1697 > t/1697-fault-hash-odd-arguments-no-name.expected
    python3 t/models/hash.py --program 1698 > t/1698-fault-hash-odd-arguments-before-a-default.pl
    python3 t/models/hash.py 1698 > t/1698-fault-hash-odd-arguments-before-a-default.expected
    python3 t/models/hash.py --program 1699 > t/1699-fault-hash-too-few-before-a-hash.pl
    python3 t/models/hash.py 1699 > t/1699-fault-hash-too-few-before-a-hash.expected
    python3 t/models/hash.py --program 1700 > t/1700-fault-hash-undef-in-a-string.pl
    python3 t/models/hash.py 1700 > t/1700-fault-hash-undef-in-a-string.expected
    python3 t/models/hash.py --program 1701 > t/1701-fault-hash-undef-key-in-a-string.pl
    python3 t/models/hash.py 1701 > t/1701-fault-hash-undef-key-in-a-string.expected
    python3 t/models/hash.py --program 1702 > t/1702-fault-hash-slice-stored-before-the-start.pl
    python3 t/models/hash.py 1702 > t/1702-fault-hash-slice-stored-before-the-start.expected
    python3 t/models/hash.py --program 1703 > t/1703-fault-hash-slice-stored-to-an-undef-key.pl
    python3 t/models/hash.py 1703 > t/1703-fault-hash-slice-stored-to-an-undef-key.expected
    python3 t/models/hash.py --program 1704 > t/1704-fault-hash-slice-read-with-an-undef-key.pl
    python3 t/models/hash.py 1704 > t/1704-fault-hash-slice-read-with-an-undef-key.expected
    python3 t/models/hash.py --program 1705 > t/1705-fault-hash-slice-stored-to-a-frozen-array.pl
    python3 t/models/hash.py 1705 > t/1705-fault-hash-slice-stored-to-a-frozen-array.expected
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import var
import sub as subs
from sub import arity as subs_arity
import list as lists
import each
import ret
import it
import sort
import interp
from var import Fault, UNDEF, TRUE, FALSE, get, logic, strings, text
from loop import block, do, step, set_, my, join
from sub import SCALAR, ucall, sub, req, say_, named
from sub import ret as returns
from list import A, el, mya, seta, sayl, setel, dump, Cases, items, element
from it import forit, formod
from ret import slurp
from ret import jn, rev
from it import IT, mp, gr
from sort import VA, VB, srt

ODD = 'an odd number of values for a hash'
NUM = ('<=>', VA, VB)

# The expressions: ('%', name), a hash; ('hel', name, key); ('sethel', op,
# name, key, e); ('stephel', op, before, name, key); ('exists', name, key);
# ('delete', name, key); ('keys', name); ('values', name); ('count', name),
# `scalar(keys(%name))`; and in a list,
# ('=>', word, e), a word and a value. A key is ('word', w), one word alone
# in the braces, or an expression. The statements: ('myh', name, items or
# None); ('seth', name, [items]).

def H(name):
    return ('%', name)

def W(word):
    return ('word', word)

def hel(name, key):
    return ('hel', name, W(key) if isinstance(key, str) and key.isidentifier() else key)

def sethel(name, key, e, op='='):
    return ('sethel', op, name, hel(name, key)[2], e)

def stephel(name, key, op='++', before=False):
    return ('stephel', op, before, name, hel(name, key)[2])

def myh(name, *es):
    return ('myh', name, list(es))

def seth(name, *es):
    return ('seth', name, list(es))

def pair(word, e):
    return ('=>', word, e)

class Hash:
    def __init__(self):
        self.items = {}
        self.frozen = 0

# ---- step 12b: ('hslice', name, [keys]), `@name{keys}`; ('hdelete', name,
# [keys]), `delete(@name{keys})`; the statements ('sethslice', name,
# [keys], [items]) and ('setslice', name, [indexes], [items]), a slice on
# the left of a list assignment; a last parameter (name, '%', None); and in
# a string a piece ('hel', name, key), its key a word or a scalar.
KEY_PAST = 'a key that is not there in a foreach, where perl would make it'
HSLICE_PAST = 'a slice with a key that is not there, where perl would make it'
SLURPYH = '%'

def odd_arguments(name):
    return f"an odd number of arguments for {name}'s hash"

def hslice(name, *keys):
    return ('hslice', name, list(keys))

def hdelete(name, *keys):
    return ('hdelete', name, list(keys))

def sethslice(name, keys, *items_):
    return ('sethslice', name, list(keys), list(items_))

def setslice(name, indexes, *items_):
    return ('setslice', name, list(indexes), list(items_))

def slurph(name=None):
    return (name, SLURPYH, None)

def hnames(e, into):
    """The hashes an expression names, anywhere in it: not by `keys`, whose
    list is copies (T217), and not in a string."""
    if not isinstance(e, tuple) or e[0] == 'qq':
        return into
    if e[0] in ('%', 'values', 'hel', 'hslice', 'exists', 'delete', 'hdelete'):
        into.append(e[1])
    elif e[0] == 'sethel':
        into.append(e[2])
    elif e[0] == 'stephel':
        into.append(e[3])
    for part in e[1:]:
        if isinstance(part, tuple):
            hnames(part, into)
        elif isinstance(part, list):
            for p in part:
                hnames(p, into)
    return into

lists.LISTY = lists.LISTY + ('%', 'keys', 'values', '=>', 'hslice', 'hdelete')
_shaped = ret.shaped
ret.shaped = lambda e: (isinstance(e, tuple) and e[0] in ('%', 'keys', 'values', 'hslice', 'hdelete')) or _shaped(e)

HFROZEN = 'a hash was changed while a foreach is over it'

def changing(h):
    if h.frozen:
        raise Fault(HFROZEN)
    return h

class Run(interp.Run):
    def __init__(self, statements):
        super().__init__(statements)
        # The file's hashes are there, empty, before anything runs.
        for s in statements:
            if s[0] == 'myh':
                self.scopes[0]['%' + s[1]] = Hash()

    def hash(self, name):
        for scope in reversed(self.scopes):
            if '%' + name in scope:
                return scope['%' + name]
        raise AssertionError(f'%{name} is not declared')

    def key(self, k):
        """A key, worked out: a string as `.` makes one."""
        if isinstance(k, tuple) and k[0] == 'word':
            return k[1]
        return logic.value(('.', get(self.ev(k)), ''))

    def fill(self, h, values):
        if len(values) % 2:
            raise Fault(ODD)
        new = {}
        for k, v in zip(values[::2], values[1::2]):
            new[logic.value(('.', k, ''))] = v
        changing(h).items = new

    def keys_of(self, es):
        return [logic.value(('.', v, '')) for item in es for v in self.evl(item)]

    def strict(self, e):
        """The fault for a key that is not there, in the list of a loop, a
        map, a grep or a sort (T216)."""
        kind = e[0] if isinstance(e, tuple) else None
        if kind == 'hel':
            if self.key(e[2]) not in self.hash(e[1]).items:
                raise Fault(KEY_PAST)
        elif kind == 'hslice':
            h = self.hash(e[1])
            if any(k not in h.items for k in self.keys_of(e[2])):
                raise Fault(HSLICE_PAST)
        else:
            super().strict(e)

    def frozen(self, its, run):
        """What `run` gives, with every hash the list names frozen while it
        runs (D17, T217). (No case has a list whose own working out changes
        a hash it names: D76 refuses those.)"""
        hashes = [self.hash(n) for n in dict.fromkeys(hnames(('list', its), []))]
        for h in hashes:
            h.frozen += 1
        try:
            return run()
        finally:
            for h in hashes:
                h.frozen -= 1

    def binder(self, e):
        return self.frozen(e[3], lambda: it.Run.binder(self, e))

    def sorter(self, e):
        return self.frozen(e[3], lambda: sort.Run.sorter(self, e))

    def called(self, name, args, want):
        _, _, params, body = sub_ = self.subs[name]
        if not params or params[-1][1] != SLURPYH:
            return super().called(name, args, want)
        # A last parameter that is a hash: an odd number of arguments left
        # for it is a fault as the sub is entered, before any default
        # (T226); then it is filled from them at its turn.
        fixed = len(params) - 1
        least = sum(1 for _, op, _ in params if op is None)
        fault = subs_arity(name, len(args), least, float('inf'))
        if fault:
            raise Fault(fault)
        if len(args) > fixed and (len(args) - fixed) % 2:
            raise Fault(odd_arguments(name))
        pname = params[-1][0]
        rest = ' rest of ' + name
        filled = [] if pname is None else [('myh', pname, [A(rest)])]
        self.subs[name] = (sub_[0], sub_[1], params[:-1] + [(rest, ret.SLURPY, None)], filled + list(body))
        try:
            return super().called(name, args, want)
        finally:
            self.subs[name] = sub_

    def evl(self, e):
        kind = e[0] if isinstance(e, tuple) else None
        if kind == 'hslice':
            keys = self.keys_of(e[2])
            h = self.hash(e[1])
            return [h.items.get(k, UNDEF) for k in keys]
        if kind == 'hdelete':
            keys = self.keys_of(e[2])
            h = self.hash(e[1])
            return [changing(h).items.pop(k) if k in h.items else UNDEF for k in keys]
        if kind == '%':
            return [x for pair_ in self.hash(e[1]).items.items() for x in pair_]
        if kind == 'keys':
            return list(self.hash(e[1]).items)
        if kind == 'values':
            return list(self.hash(e[1]).items.values())
        if kind == '=>':
            return [e[1]] + self.evl(e[2])
        return super().evl(e)

    def ev(self, e):
        kind = e[0] if isinstance(e, tuple) else None
        if kind not in ('%', 'keys', 'values', 'count', 'hel', 'sethel', 'stephel', 'exists', 'delete'):
            return super().ev(e)
        self.ctx = SCALAR
        h = self.hash(e[3] if kind == 'stephel' else e[2] if kind == 'sethel' else e[1])
        if kind in ('%', 'keys', 'values', 'count'):
            return len(h.items)
        if kind == 'hel':
            return h.items.get(self.key(e[2]), UNDEF)
        if kind == 'exists':
            return TRUE if self.key(e[2]) in h.items else FALSE
        if kind == 'delete':
            k = self.key(e[2])
            if k not in h.items:
                return UNDEF
            return changing(h).items.pop(k)
        if kind == 'stephel':
            _, op, before, _, key = e
            k = self.key(key)
            changing(h).items.setdefault(k, UNDEF)
            old = h.items[k]
            h.items[k] = var.step(op, old)
            return h.items[k] if before else 0 if old is UNDEF and op == '++' else old
        _, op, _, key, right = e
        if op == '=':
            r = self.ev(right)
            k = self.key(key)
            changing(h).items[k] = get(r)
            return h.items[k]
        k = self.key(key)
        changing(h).items.setdefault(k, UNDEF)
        if op in ('||=', '&&=', '//='):
            old = h.items[k]
            if old is UNDEF if op == '//=' else logic.truth(old) == (op == '&&='):
                h.items[k] = get(self.ev(right))
            return h.items[k]
        r = get(self.ev(right))
        left = h.items[k]
        if left is UNDEF and op in ('+=', '-=', '.='):
            left = '' if op == '.=' else 0
        h.items[k] = logic.value((op[:-1], left, r))
        return h.items[k]

    def run(self, s):
        if s[0] == 'myh':
            self.mark(s)
            values = None if s[2] is None else [v for item in s[2] for v in self.evl(item)]
            if self.top():
                h = self.scopes[0]['%' + s[1]]
            else:
                h = self.scopes[-1]['%' + s[1]] = Hash()
            if values is not None:
                self.fill(h, values)
        elif s[0] == 'seth':
            self.mark(s)
            self.fill(self.hash(s[1]), [v for item in s[2] for v in self.evl(item)])
        elif s[0] in ('sethslice', 'setslice'):
            # The right side, every key or index, then the stores: an undef
            # for each target the list does not reach (T228).
            self.mark(s)
            values = [v for item in s[3] for v in self.evl(item)]
            if s[0] == 'sethslice':
                keys = self.keys_of(s[2])
                h = self.hash(s[1])
                for n, k in enumerate(keys):
                    changing(h).items[k] = values[n] if n < len(values) else UNDEF
            else:
                indexes = [self.whole_of(v) for item in s[2] for v in self.evl(item)]
                a = self.arr(s[1])
                for n, i in enumerate(indexes):
                    a.items[self.target(a, i)] = values[n] if n < len(values) else UNDEF
        elif s[0] == 'foreach':
            self.frozen(s[3], lambda: super(Run, self).run(s))
        elif s[0] == 'formod':
            self.frozen(s[2], lambda: super(Run, self).run(s))
        else:
            super().run(s)

# ---- as source

def key_text(k):
    return k[1] if isinstance(k, tuple) and k[0] == 'word' else text(k)

def sort_text(e, top):
    if e[1] is None and isinstance(e[3][0], tuple) and e[3][0][0] in ('keys', 'values', '%'):
        return f'(sort {items(e[3])})'
    return _sort_text(e, top)

_sort_text = var.MORE['sort']
var.MORE.update({
    '%': lambda e, top: '%' + e[1],
    'keys': lambda e, top: f'keys(%{e[1]})',
    'count': lambda e, top: f'scalar(keys(%{e[1]}))',
    'values': lambda e, top: f'values(%{e[1]})',
    '=>': lambda e, top: f'{e[1]} => {text(e[2])}',
    'hel': lambda e, top: f'${e[1]}{{{key_text(e[2])}}}',
    'exists': lambda e, top: f'exists(${e[1]}{{{key_text(e[2])}}})',
    'delete': lambda e, top: f'delete(${e[1]}{{{key_text(e[2])}}})',
    'sethel': lambda e, top: (lambda s: s if top else f'({s})')(f'${e[2]}{{{key_text(e[3])}}} {e[1]} {text(e[4], False)}'),
    'stephel': lambda e, top: (lambda s: s if top else f'({s})')(f'{e[1]}${e[3]}{{{key_text(e[4])}}}' if e[2] else f'${e[3]}{{{key_text(e[4])}}}{e[1]}'),
    'sort': sort_text,
})

def piece_text(p):
    if p[0] == 'hel':
        key = p[2]
        assert isinstance(key, tuple) and key[0] in ('word', '$'), p
        return f'${p[1]}{{{key[1] if key[0] == "word" else "$" + key[1]}}}'
    return _piece_text(p)

_piece_text = interp.piece_text
interp.piece_text = piece_text

def parameter(p):
    name, op, default = p
    if op == SLURPYH:
        return '%' if name is None else '%' + name
    return _parameter(p)

_parameter = subs.parameter
subs.parameter = parameter
var.MORE.update({
    'hslice': lambda e, top: f'@{e[1]}{{{items(e[2])}}}',
    'hdelete': lambda e, top: f'delete(@{e[1]}{{{items(e[2])}}})',
})

_source = each.source

def source(s, depth=0):
    pad = '    ' * depth
    if s[0] == 'sethslice':
        return [f'{pad}@{s[1]}{{{items(s[2])}}} = ({items(s[3])});']
    if s[0] == 'setslice':
        return [f'{pad}@{s[1]}[{items(s[2])}] = ({items(s[3])});']
    if s[0] == 'myh':
        return [f'{pad}my %{s[1]};' if s[2] is None else f'{pad}my %{s[1]} = ({items(s[2])});']
    if s[0] == 'seth':
        return [f'{pad}%{s[1]} = ({items(s[2])});']
    return _source(s, depth)

each.source = source
it.source = source

def output(statements):
    r = Run(statements)
    try:
        for s in statements:
            r.run(s)
    except Fault as f:
        return r.out, str(f), r.alias.get(r.at, r.at)
    assert len(r.scopes) == 1 and r.frames == [] and r.wants == [], 'something was left open'
    return r.out, None, None

def quiet(setup, candidates):
    """The candidates that do not fault after the setup, in order."""
    return [c for c in candidates if output(setup + [c])[1] is None]

# ---- the cases

shown = var.shown

def gone(e):
    """What a delete gave, said once: it is not worked out twice."""
    return say_(('//', e, 'undef'))

def dumph(name):
    """A statement that prints a hash: its count, and each key and value,
    by key: the order a hash keeps is not perl's to agree with."""
    value = ('?:', ('call', 'defined', [('hel', name, IT)]), ('hel', name, IT), 'undef')
    return say_(join(('count', name), ':', jn(',', mp([srt([('keys', name)])], join('<', IT, '=', value, '>')))))

# Every word perl has a meaning of its own for, of a kind each.
WORDS = ['name', 'true', 'false', 'undef', 'if', 'my', 'sub', 'print', 'say', 'q', 'qq', 's', 'y', 'm', 'tr', 'x', 'and', 'or', 'not', 'lt', 'eq', 'cmp',
         'time', 'shift', 'keys', 'exists', 'delete', 'defined', 'length', 'sort', 'map', 'v65', '_x', 'a1', 'A', 'return', 'last', 'for']
# Every kind of value a key may be made from, with a string of its own.
KEYS = [0, 1, -7, 41, 2**53, 0.5, 3.0, -0.0, 1.5e300, 1e21, 0.1, 1 / 3, '', '0', 'ab', ' 3 ', '00', '3.0', '1e3', 'a b', "it's", '5', '-5', TRUE, FALSE]

def literal_cases():
    c = Cases(0)
    # A word before `=>`, and alone in braces, is its text.
    def words(f, g, G):
        h = g('h')
        s = [myh(h, *[pair(w, n) for n, w in enumerate(WORDS)]), dumph(h)]
        for w in WORDS:
            s += [say_(hel(h, w)), say_(('exists', h, W(w)))]
        s += [myh(g('e')), dumph(g('e')), ('myh', g('n'), None), dumph(g('n')),
              myh(g('one'), pair('only', 1)), dumph(g('one'))]
        return s
    c.case(words)
    # A key is a string, as `.` makes one: of every kind, as a literal's
    # item, held in a variable and worked out.
    def kinds(f, g, G):
        h, k = g('h'), g('k')
        s = [('myh', h, None), ('my', k, 0)]
        for n, v in enumerate(KEYS):
            s += [do(set_(k, v)), do(sethel(h, G('k'), n)), say_(('exists', h, ('.', G('k'), '')))]
        s += [dumph(h)]
        lit = [x for n, v in enumerate(KEYS) for x in (v, n)]
        s += [myh(g('l'), *lit), dumph(g('l')), say_(('==', ('keys', h), ('keys', g('l'))))]
        s += [myh(g('c'), ('+', 1, 1), 'two', ('.', 'a', 'b'), 'ab', ('*', 0.5, 4), 'again', ('call', 'length', ['abc']), 'three'), dumph(g('c'))]
        return s
    c.case(kinds)
    # A key given twice: the last value. A list of lists, an array, a hash.
    def lists_(f, g, G):
        h, a, o = g('h'), g('a'), g('o')
        return [myh(h, pair('a', 1), pair('b', 2), pair('a', 3), 'b', 4, pair('c', 5)), dumph(h),
                mya(a, 'p', 1, 'q', 2), myh(o, A(a)), dumph(o), seth(o, A(a), A(a)), dumph(o),
                seth(o, ('list', [pair('x', 1), ('list', [pair('y', 2)])]), pair('z', 3)), dumph(o),
                seth(o, H(h), pair('d', 6)), dumph(o), seth(o, H(o), pair('a', 9)), dumph(o), seth(o), dumph(o),
                seth(o, ('..', 1, 6)), dumph(o), seth(o, ('xl', [pair('r', 1)], 3)), dumph(o),
                seth(o, pair('u', UNDEF), pair('t', TRUE), pair('f', FALSE), pair('n', 1.5)), dumph(o)]
    c.case(lists_)
    return c.out

def element_cases():
    c = Cases(0)
    VALUES = [0, 1, -7, 0.5, 3.0, '', '0', 'ab', '00', ' 3 ', TRUE, FALSE, UNDEF]
    # Reading: what is there, what is not, and nothing is made.
    def reading(f, g, G):
        h, k = g('h'), g('k')
        s = [myh(h, *[x for n, v in enumerate(VALUES) for x in (f'k{n}', v)]), dumph(h)]
        for n in range(len(VALUES)):
            s += [shown(hel(h, f'k{n}')), shown(('hel', h, f'k{n}')), say_(('call', 'defined', [hel(h, f'k{n}')]))]
        s += [shown(hel(h, 'nope')), say_(('call', 'defined', [hel(h, 'nope')])), shown(('//', hel(h, 'nope'), 'dflt')),
              ('my', k, 'k1'), shown(hel(h, G('k'))), shown(hel(h, ('.', 'k', 2))), shown(hel(h, ('.', G('k'), 0))),
              ('my', g('v'), hel(h, 'zz')), sayl(hel(h, 'k1'), hel(h, 'k7'), hel(h, 'k1')), dumph(h)]
        return s
    c.case(reading)
    # Storing, and every operator that reads and stores, on what is there
    # and on what is not.
    def storing(f, g, G):
        h = g('h')
        s = [myh(h, pair('n', 5), pair('s', 'ab'), pair('u', UNDEF), pair('z', 0), pair('e', ''))]
        tries = []
        for key in ('n', 's', 'u', 'z', 'e', 'new'):
            for op, v in (('=', 7), ('+=', 2), ('-=', 2), ('*=', 3), ('.=', 'x'), ('x=', 2), ('//=', 9), ('||=', 8), ('&&=', 6), ('**=', 2), ('/=', 2), ('%=', 3)):
                tries.append(block(myh('t', H(h)), say_(sethel('t', key if key != 'new' else f'new{len(tries)}', v, op)), dumph('t')))
            for op in ('++', '--'):
                for before in (True, False):
                    tries.append(block(myh('t', H(h)), say_(stephel('t', key, op, before)), dumph('t')))
        return s + quiet(s, tries) + [dumph(h)]
    c.case(storing)
    # The orders (D80): the value, then the key, then the store; for an
    # operator that reads, the key first.
    def orders(f, g, G):
        h, i = g('h'), g('i')
        return [('myh', h, None), ('my', i, 'a'),
                do(sethel(h, G('i'), set_(i, 'b'))), dumph(h), say_(G('i')),
                seth(h), do(set_(i, 'a')), do(sethel(h, G('i'), set_(i, 'b'), '.=')), dumph(h),
                seth(h, pair('a', 1)), do(set_(i, 'a')), do(sethel(h, G('i'), set_(i, 5), '+=')), dumph(h),
                seth(h), do(sethel(h, 'p', sethel(h, 'q', 4))), dumph(h),
                seth(h, pair('n', 1)), do(sethel(h, 'm', ('+', hel(h, 'n'), 1))), do(sethel(h, 'n', ('+', hel(h, 'm'), hel(h, 'n')))), dumph(h)]
    c.case(orders)
    return c.out

def whole_cases():
    c = Cases(0)
    def exists_delete(f, g, G):
        h, k = g('h'), g('k')
        return [myh(h, pair('a', 1), pair('u', UNDEF), pair('z', 0), pair('e', ''), 1, 'one'), ('my', k, 'a'),
                say_(('exists', h, W('a'))), say_(('exists', h, W('u'))), say_(('exists', h, W('nope'))), say_(('exists', h, G('k'))),
                say_(('exists', h, 1)), say_(('exists', h, ('.', G('k'), 'x'))), say_(('!', ('exists', h, W('nope')))),
                say_(('?:', ('exists', h, W('z')), 'has z', 'no z')), say_(('&&', ('exists', h, W('a')), ('exists', h, W('e')))),
                ('if', [(('exists', h, W('nope')), [say_('wrong')]), (('exists', h, W('u')), [say_('u is there')])], None), dumph(h),
                gone(('delete', h, W('a'))), gone(('delete', h, W('a'))), gone(('delete', h, W('u'))), gone(('delete', h, W('nope'))),
                say_(('exists', h, W('a'))), dumph(h), ('my', g('d'), ('delete', h, 1)), say_(G('d')), do(('delete', h, W('z'))), dumph(h),
                do(sethel(h, 'a', 'back')), say_(('+', ('call', 'length', [('delete', h, W('a'))]), 1)), dumph(h),
                do(('delete', h, W('e'))), dumph(h), gone(('delete', h, W('e')))]
    c.case(exists_delete)
    def counts(f, g, G):
        h, e, n = g('h'), g('e'), g('n')
        return [myh(h, pair('a', 1), pair('b', 2), pair('c', 3), pair('d', 4)), ('myh', e, None),
                say_(('+', ('keys', h), 0)), ('my', n, H(h)), say_(G('n')), ('my', g('m'), ('keys', h)), say_(G('m')),
                ('my', g('z'), H(e)), say_(G('z')),
                ('if', [(H(h), [say_('some')])], [say_('none')]), ('if', [(H(e), [say_('some')])], [say_('none')]),
                ('if', [(('keys', e), [say_('keys')])], [say_('no keys')]), ('if', [(('values', h), [say_('values')])], None),
                say_(('+', ('keys', h), ('values', h))), say_(('==', ('keys', h), 4)), say_(('.', 'n', ('keys', h))),
                do(('delete', h, W('a'))), ('my', g('after'), H(h)), say_(G('after')),
                do(sethel(h, 'a', 9)), do(sethel(h, 'a', 10)), ('my', g('again'), H(h)), say_(G('again')),
                # (A hash in the list of a sort, other than by its keys, is
                # step 12b's, with the freeze: so through an array.)
                ('mya', g('vs'), [('values', h)]), ('mya', g('all'), [H(h)]),
                say_(jn(',', srt([('keys', h)]))), say_(jn(',', srt([A(g('vs'))], NUM))), say_(jn(',', srt([A(g('all'))]))),
                say_(jn(',', rev(srt([('keys', h)])))), say_(jn(',', mp([srt([('keys', h)])], ('x', IT, 2))))]
    c.case(counts)
    def copies(f, g, G):
        h, o, a = g('h'), g('o'), g('a')
        return [myh(h, pair('a', 1), pair('b', 2), pair('c', 3), pair('d', 4)), myh(o, H(h)), do(sethel(o, 'a', 9)), do(sethel(o, 'z', 0)),
                do(('delete', o, W('b'))), dumph(h), dumph(o), seth(o, H(h)), dumph(o), seth(h, H(h)), dumph(h),
                seth(h, H(h), pair('e', 5)), dumph(h), seth(h, pair('first', 0), H(h)), dumph(h),
                ('mya', g('flat'), [H(h)]), ('mya', a, [srt([A(g('flat'))])]), say_(('scalar', a)), ('mya', g('k'), [srt([('keys', h)])]), dump(g('k')),
                ('mya', g('vv'), [('values', h)]), ('mya', g('v'), [srt([A(g('vv'))], NUM)]), dump(g('v')),
                sub(f('size'), [req('n')], returns(('*', D('n'), 2))), say_(ucall(f('size'), ('+', ('keys', h), 0))), say_(ucall(f('size'), ('+', H(h), 0))),
                sub(f('made'), [], myh('t', pair('p', 1), pair('q', 2)), returns(H('t'))), myh(g('r'), ucall(f('made'))), dumph(g('r')),
                sub(f('twice'), [], myh('t', pair('p', 1)), do(sethel('t', 'q', 2)), returns(('keys', 't'))),
                ('mya', g('tw'), [ucall(f('twice'))]), say_(jn(',', srt([A(g('tw'))]))),
                block(myh('t', pair('in', 1)), dumph('t'), block(myh('t', pair('deeper', 2)), dumph('t')), dumph('t')),
                ('my', g('i'), 0), ('while', None, ('<', G('i'), 3), [myh('t', pair('k', G('i'))), do(sethel('t', ('.', 'x', G('i')), 1)), dumph('t'), do(step(g('i')))])]
    c.case(copies)
    return c.out

D = lambda n: ('$', n)

def rawh(name):
    """A statement that prints a hash as it stands: its keys, its values,
    and the hash in a list, each in the hash's own order (D27)."""
    return say_(join(jn(',', ('keys', name)), '|', jn(',', ('values', name)), '|', jn(',', H(name))))

def order_cases():
    """D27, where perl has no answer: the order is the order of first
    storing. A Python dict keeps that order, which is the model's whole
    claim to know it."""
    c = Cases(0)
    def stored(f, g, G):
        h, o, i = g('h'), g('o'), g('i')
        return [myh(h, pair('one', 1), pair('two', 2), pair('three', 3), pair('four', 4)), rawh(h),
                do(sethel(h, 'five', 5)), do(sethel(h, 'two', 22)), rawh(h),
                do(sethel(h, 'three', 1, '+=')), do(stephel(h, 'one')), do(sethel(h, 'six', 6, '//=')), do(sethel(h, 'four', 0, '&&=')), rawh(h),
                do(('delete', h, W('one'))), rawh(h), do(sethel(h, 'one', 11)), rawh(h),
                do(('delete', h, W('six'))), do(('delete', h, W('two'))), do(sethel(h, 'two', 2)), do(sethel(h, 'six', 6)), rawh(h),
                # A key given twice keeps its first place and its last value.
                myh(o, pair('a', 1), pair('b', 2), pair('a', 3), pair('c', 4), pair('b', 5), pair('d', 6)), rawh(o),
                seth(o, pair('z', 0), H(h), pair('last', 9), pair('two', 'again')), rawh(o),
                seth(o, H(o), pair('z', 1)), rawh(o), seth(h, H(h)), rawh(h), seth(h), rawh(h),
                # Numbers as keys are in the order stored, not their own.
                seth(h, 10, 'a', 9, 'b', 100, 'c', 1, 'd', 9.0, 'e'), rawh(h),
                # A key read, or asked after, is not made, and has no place.
                say_(('call', 'defined', [hel(h, 'nope')])), say_(('exists', h, W('none'))), do(sethel(h, 'nope', 1)), rawh(h)]
    c.case(stored)
    def grown(f, g, G):
        h, i, a = g('h'), g('i'), g('a')
        return [('myh', h, None), ('my', i, 0),
                ('while', None, ('<', G('i'), 40), [do(sethel(h, ('.', 'k', G('i')), G('i'))), do(step(i))]), rawh(h),
                # The holes a delete leaves are closed, and the order holds.
                do(set_(i, 0)), ('while', None, ('<', G('i'), 40), [('if', [(('&&', ('!=', G('i'), 3), ('&&', ('!=', G('i'), 17), ('!=', G('i'), 31))), [do(('delete', h, ('.', 'k', G('i'))))])], None), do(step(i))]), rawh(h),
                do(sethel(h, 'k5', 5)), do(sethel(h, 'k10', 'ten')), do(sethel(h, 'k4', 4)), rawh(h),
                do(set_(i, 0)), ('while', None, ('<', G('i'), 12), [do(sethel(h, ('.', 'n', G('i')), G('i'))), do(('delete', h, ('.', 'n', ('-', G('i'), 1)))), do(step(i))]), rawh(h),
                ('mya', a, [('keys', h)]), dump(a), ('mya', g('v'), [('values', h)]), dump(g('v')), ('mya', g('p'), [H(h)]), dump(g('p')),
                sub(f('made'), [], myh('t', pair('y', 1), pair('x', 2), pair('w', 3)), do(sethel('t', 'a', 0)), returns(H('t'))),
                myh(g('r'), ucall(f('made'))), rawh(g('r')), ('mya', g('l'), [ucall(f('made')), ('keys', g('r'))]), dump(g('l'))]
    c.case(grown)
    return c.out

SAME = {'1500': ('hash-literals-and-keys', literal_cases), '1501': ('hash-elements', element_cases), '1502': ('hash-exists-delete-counts', whole_cases)}
# What perl is not asked: the order (D27).
NEW = {'1503': ('hash-order-by-the-model', order_cases)}

def faults():
    out = {}
    n = [1510]
    def fault(name, near, far, subs_=()):
        out[str(n[0])] = ('fault-hash-' + name, list(subs_), near, far)
        n[0] += 1
    h4 = lambda: myh('h', pair('a', 1), pair('b', 2), pair('c', 3), pair('d', 4))
    # An odd list for a hash.
    fault('odd-list', block(myh('h', 1, 2), dumph('h')), block(myh('h', 1, 2, 3), dumph('h')))
    fault('odd-list-assigned', block(h4(), seth('h', pair('a', 1), pair('b', 2)), dumph('h')), block(h4(), seth('h', pair('a', 1), 'b'), dumph('h')))
    fault('odd-list-of-one', block(('myh', 'h', None), seth('h'), dumph('h')), block(('myh', 'h', None), seth('h', 'a'), dumph('h')))
    fault('odd-list-from-an-array', block(mya('a', 1, 2), myh('h', A('a')), dumph('h')), block(mya('a', 1, 2, 3), myh('h', A('a')), dumph('h')))
    fault('odd-list-from-a-hash-and-one', block(h4(), myh('g', H('h'), 'e', 5), dumph('g')), block(h4(), myh('g', H('h'), 'e'), dumph('g')))
    # An undef key.
    both = lambda make, good, bad: (block(h4(), *good, make()), block(h4(), *bad, make()))
    fault('undef-key-read', *both(lambda: shown(hel('h', D('k'))), [('my', 'k', '')], [('my', 'k', None)]))
    fault('undef-key-stored', *both(lambda: do(sethel('h', D('k'), 1)), [('my', 'k', 0)], [('my', 'k', None)]))
    fault('undef-key-worked-on', *both(lambda: do(sethel('h', D('k'), 1, '+=')), [('my', 'k', FALSE)], [('my', 'k', None)]))
    fault('undef-key-stepped', *both(lambda: do(stephel('h', D('k'))), [('my', 'k', 'a')], [('my', 'k', None)]))
    fault('undef-key-exists', *both(lambda: say_(('exists', 'h', D('k'))), [('my', 'k', 'a')], [('my', 'k', None)]))
    fault('undef-key-deleted', *both(lambda: do(('delete', 'h', D('k'))), [('my', 'k', 'a')], [('my', 'k', None)]))
    fault('undef-key-in-a-list', block(myh('g', '', 1), dumph('g')), block(myh('g', UNDEF, 1), dumph('g')))
    # D36: a whole Num from 10^15 is no string, so no key.
    fault('whole-num-key', *both(lambda: do(sethel('h', D('k'), 1)), [('my', 'k', 999999999999999.0)], [('my', 'k', 1e15)]))
    fault('whole-num-key-read', *both(lambda: shown(hel('h', D('k'))), [('my', 'k', 1e16)], [('my', 'k', 2.0**53 - 1)]))
    fault('whole-num-key-in-a-list', block(myh('g', 0.5, 1), dumph('g')), block(myh('g', 1e15, 1), dumph('g')))
    # What is not there is undef, and an undef is no number and no string.
    fault('missing-as-a-number', block(h4(), say_(('+', hel('h', 'a'), 1))), block(h4(), say_(('+', hel('h', 'nope'), 1))))
    fault('missing-as-a-string', block(h4(), say_(('.', hel('h', 'a'), '!'))), block(h4(), say_(('.', hel('h', 'nope'), '!'))))
    fault('deleted-as-a-string', block(h4(), say_(('.', ('delete', 'h', W('a')), '!'))), block(h4(), do(('delete', 'h', W('a'))), say_(('.', ('delete', 'h', W('a')), '!'))))
    # An operator that reads and stores makes the key, and then faults.
    fault('string-stepped', block(h4(), do(sethel('h', 'a', 2, '*=')), dumph('h')), block(h4(), do(sethel('h', 'a', 'x')), do(sethel('h', 'a', 2, '*=')), dumph('h')))
    # D18: a hash after return, reached for one value.
    fault('returned-for-one-value', block(('mya', 'r', [ucall('f')]), say_(('scalar', 'r'))), ('my', 'x', ucall('f')), [myh('g', pair('a', 1)), sub('f', [], returns(H('g')))])
    fault('keys-returned-for-one-value', block(('mya', 'r', [ucall('f')]), say_(('scalar', 'r'))), ('my', 'x', ucall('f')), [myh('g', pair('a', 1)), sub('f', [], returns(('keys', 'g')))])
    return out

FAULTS = faults()

# ---- step 12b

V, K = ('$', 'v'), ('$', 'k')
each_ = each.each
STOP = ('last', None)
qq = interp.qq
h4 = lambda h: myh(h, pair('a', 1), pair('b', 2), pair('c', 3), pair('d', 4))

def loop_cases():
    """A hash in the list of a loop, a map, a grep or a sort: read from the
    block while it is frozen, and given back on every way out."""
    c = Cases(0)
    def frozen_and_read(f, g, G):
        h, t = g('h'), g('t')
        read = [say_(hel(h, 'a')), say_(('exists', h, W('zz'))), say_(('count', h)), say_(jn(',', srt([('keys', h)])))]
        return [h4(h), ('my', t, 0),
                each_('v', [srt([('values', h)], NUM)], say_(V), *read),
                each_('v', [srt([H(h)])], do(set_(t, ('.', G('t'), V)))), say_(G('t')),
                each_('v', [hel(h, 'a'), hel(h, 'c')], say_(V), *read),
                each_('v', [hslice(h, 'd', 'a')], say_(V), *read),
                each_('v', [hslice(h, ('.', 'b', ''), 'b', ('.', 'c', ''))], say_(V)),
                forit([srt([('values', h)], NUM)], say_(('*', IT, hel(h, 'b')))),
                formod(say_(('+', IT, hel(h, 'd'))), srt([('values', h)], NUM)),
                say_(jn(',', mp([srt([('values', h)], NUM)], ('+', IT, hel(h, 'a'))))),
                say_(jn(',', gr([srt([H(h)])], ('exists', h, IT)))),
                say_(jn(',', srt([hslice(h, 'c', 'a', 'd')], ('<=>', VB, VA)))),
                say_(jn(',', mp([hel(h, 'a'), hslice(h, 'b', 'c')], ('.', IT, ('count', h))))),
                # Given back: a store after each.
                do(sethel(h, 'e', 5)), do(('delete', h, W('a'))), dumph(h)]
    c.case(frozen_and_read)
    def over_keys(f, g, G):
        h = g('h')
        return [h4(h),
                # keys are copies: the block may store, add and delete.
                each_('k', [srt([('keys', h)])], do(sethel(h, K, ('*', hel(h, K), 10))), do(sethel(h, ('.', K, 'x'), 1))), dumph(h),
                each_('k', [srt([('keys', h)])], ('if', [(('eq', K, 'b'), [do(('delete', h, K))])], None)), dumph(h),
                say_(jn(',', mp([srt([('keys', h)])], do(sethel(h, IT, 0)), IT))), dumph(h),
                say_(jn(',', gr([srt([('keys', h)])], ('delete', h, IT)))), dumph(h),
                # How many, in a loop's list, names nothing either.
                each_('i', [('..', 1, ('count', h))], do(sethel(h, ('.', 'n', ('$', 'i')), ('$', 'i')))), dumph(h)]
    c.case(over_keys)
    def given_back(f, g, G):
        h, o = g('h'), g('o')
        inner = each_('w', [srt([('values', h)], NUM)], say_(('.', V, ('$', 'w'))))
        return [h4(h), h4(o),
                # Left by last, by next, by a jump to a loop further out,
                # and by return; twice over one hash, and over two.
                each_('v', [srt([('values', h)], NUM)], STOP), do(sethel(h, 'a', 10)),
                each_('v', [srt([('values', h)], NUM)], ('next', None), say_('not reached')), do(sethel(h, 'b', 20)),
                ('foreach', 'OUT', 'v', [srt([('values', h)], NUM)], [each_('w', [srt([('values', o)], NUM)], ('last', 'OUT'))]), do(sethel(h, 'c', 30)), do(sethel(o, 'c', 30)),
                each_('v', [srt([hslice(h, 'a', 'b')], NUM)], inner), do(sethel(h, 'd', 40)),
                sub(f('first'), [], each_('v', [srt([('values', h)], NUM)], returns(V)), returns(0)), say_(ucall(f('first'))), do(sethel(h, 'e', 50)),
                sub(f('n'), [req('x')], returns(('+', D('x'), ('count', h)))),
                say_(jn(',', mp([srt([('values', o)], NUM)], ucall(f('n'), IT)))), do(sethel(o, 'e', 5)),
                dumph(h), dumph(o),
                # A hash of the sub's own, in a loop that the sub returns from.
                sub(f('own'), [], myh('t', pair('p', 1), pair('q', 2)), each_('v', [srt([('values', 't')], NUM)], ('if', [(('==', V, 2), [returns(('count', 't'))])], None)), returns(0)),
                say_(ucall(f('own'))), say_(ucall(f('own')))]
    c.case(given_back)
    return c.out

def unsorted_cases():
    """The same loops with no sort, where the order is D27's: perl is not
    asked."""
    c = Cases(0)
    def order(f, g, G):
        h, t = g('h'), g('t')
        return [myh(h, pair('one', 1), pair('two', 2), pair('three', 3), pair('four', 4)), do(('delete', h, W('two'))), do(sethel(h, 'two', 22)), ('my', t, ''),
                each_('v', [('values', h)], say_(V)), each_('v', [H(h)], do(set_(t, ('.', G('t'), V)))), say_(G('t')),
                each_('k', [('keys', h)], say_(('.', K, hel(h, K))), do(('delete', h, K)), do(sethel(h, ('.', K, K), 1))), rawh(h),
                forit([('values', h)], say_(IT)), formod(say_(IT), H(h)),
                say_(jn(',', mp([H(h)], ('.', IT, '!')))), say_(jn(',', mp([('values', h)], ('+', IT, 1)))), say_(jn(',', gr([('keys', h)], ('ne', IT, 'oneone')))),
                say_(jn(',', srt([('values', h)], 0))), say_(jn(',', rev(('keys', h)))),
                say_(jn(',', srt([('keys', h)], do(sethel(h, 'seen', 1)), ('cmp', VA, VB)))), rawh(h),
                ('mya', g('sl'), [hslice(h, 'twotwo', 'oneone', 'nope')]), dump(g('sl')), say_(jn(',', mp([hslice(h, 'fourfour', 'threethree')], IT))),
                ('mya', g('d'), [hdelete(h, 'threethree', 'nope', 'oneone')]), say_(('scalar', g('d'))), rawh(h),
                sethslice(h, ['z', 'y', 'twotwo', 'x'], 26, 25, 2, 24), rawh(h)]
    c.case(order)
    return c.out

def slice_cases():
    c = Cases(0)
    def read(f, g, G):
        h, a, k, l = g('h'), g('a'), g('k'), g('l')
        # (Through an array: a slice with a key that is not there, in a
        # map's own list, is the fault.)
        def dumpl(*es):
            return [st for e in es for st in (seta(l, e), dump(l))]
        return [h4(h), ('my', k, 'b'), mya(a, 'c', 'a'), ('mya', l, None),
                *dumpl(hslice(h, 'a', 'b'), hslice(h, 'd', 'nope', 'a'), hslice(h, G('k'), ('.', G('k'), 'x'), ('.', 'c', '')),
                       hslice(h, A(a)), hslice(h, A(a), 'd'), hslice(h, srt([('keys', h)])), hslice(h, 'a', 'a'), hslice(h, 1, 2)), dumph(h),
                ('mya', g('v'), [hslice(h, 'b', 'c')]), dump(g('v')), ('mya', g('w'), [hslice(h, 'a', 'b'), 9, hslice(h, 'c', 'd')]), dump(g('w')),
                ('lassign', True, [('$', g('p')), ('$', g('q'))], [hslice(h, 'c', 'd')]), say_(('+', G('p'), G('q'))),
                say_(('scalar', g('v'))), say_(jn('-', rev(hslice(h, 'a', 'b', 'c')))),
                sub(f('cnt'), [slurp('r')], returns(('scalar', 'r'))), say_(ucall(f('cnt'), hslice(h, 'a', 'b', 'c'))), say_(ucall(f('cnt'), 0, hslice(h, 'd', 'a'))),
                myh(g('o'), pair('x', 0), hslice(h, 'a', 'b')), dumph(g('o')),
                # A slice of a list of the hash's own keys and values.
                say_(('scalar', g('w')))]
    c.case(read)
    def stored(f, g, G):
        h, a, i = g('h'), g('a'), g('i')
        return [h4(h), mya(a, 1, 2, 3), ('my', i, 0),
                sethslice(h, ['a', 'b'], 10, 20), dumph(h), sethslice(h, ['x', 'y'], 1, 2), dumph(h),
                # An undef for each target the list does not reach (T228).
                sethslice(h, ['c', 'new', 'more'], 30), dumph(h), sethslice(h, ['p', 'q']), dumph(h),
                sethslice(h, ['a', 'b'], 1, 2, 3, 4), dumph(h), sethslice(h, ['a', 'b'], hslice(h, 'b', 'a')), dumph(h),
                sethslice(h, ['k', 'k'], 1, 2), dumph(h), sethslice(h, [A(a), 'z'], A(a), 26), dumph(h),
                # The right side, then every key, then the stores.
                ('my', g('n'), 'one'), sethslice(h, [G('n'), ('.', G('n'), '!')], set_(g('n'), 'two'), 2), dumph(h),
                setslice(a, [0, 1], 'x', 'y'), dump(a), setslice(a, [2, 4], 'z'), dump(a), setslice(a, [-1, 0], 9, 8), dump(a),
                setslice(a, [('..', 1, 3)], 1, 2, 3), dump(a), setslice(a, [1, 1], 5, 6), dump(a), setslice(a, [0, 1], ('slice', a, [1, 0])), dump(a),
                setslice(a, [6, 5]), dump(a), setslice(a, [G('i'), ('+', G('i'), 1)], set_(i, 3), 7), dump(a)]
    c.case(stored)
    def deleted(f, g, G):
        h, l = g('h'), g('l')
        return [h4(h), ('mya', l, None), seta(l, hdelete(h, 'a', 'c')), dump(l), dumph(h), seta(l, hdelete(h, 'a', 'b', 'nope')), dump(l), dumph(h),
                seta(l, hdelete(h, 'd', 'd')), dump(l), dumph(h), h4(g('o')), ('mya', g('got'), [hdelete(g('o'), srt([('keys', g('o'))]))]), dump(g('got')), dumph(g('o'))]
    c.case(deleted)
    return c.out

def opts_cases():
    c = Cases(0)
    def opts(f, g, G):
        h = g('h')
        show = lambda name: say_(join(('count', name), ':', jn(',', mp([srt([('keys', name)])], join(IT, '=', hel(name, IT))))))
        return [h4(h),
                sub(f('all'), [slurph('o')], show('o'), returns(('count', 'o'))),
                sub(f('one'), [req('x'), slurph('o')], say_(D('x')), show('o'), returns(hel('o', 'k'))),
                sub(f('dflt'), [req('x'), ('y', '=', 7), slurph('o')], say_(join(D('x'), D('y'))), show('o'), returns(1)),
                sub(f('none'), [req('x'), slurph()], returns(D('x'))),
                sub(f('keep'), [slurph('o')], do(sethel('o', 'added', 1)), do(('delete', 'o', W('a'))), returns(jn(',', srt([('keys', 'o')])))),
                say_(ucall(f('all'))), say_(ucall(f('all'), pair('a', 1))), say_(ucall(f('all'), pair('a', 1), pair('b', 2), pair('a', 3))), say_(ucall(f('all'), H(h))),
                say_(ucall(f('all'), H(h), pair('e', 5))), say_(ucall(f('all'), 'k', '')),
                say_(ucall(f('one'), 1, pair('k', 'v'))), say_(('//', ucall(f('one'), 2), 'none')), say_(ucall(f('one'), 3, H(h), pair('k', 9))),
                say_(ucall(f('dflt'), 1)), say_(ucall(f('dflt'), 1, 2)), say_(ucall(f('dflt'), 1, 2, pair('a', 1))), say_(ucall(f('dflt'), 1, 2, H(h))),
                say_(ucall(f('none'), 1)), say_(ucall(f('none'), 1, pair('a', 1))), say_(ucall(f('none'), 2, H(h))),
                # A copy: the caller's hash is as it was.
                say_(ucall(f('keep'), H(h))), dumph(h),
                # A hash of the sub's own name beside the file's.
                sub(f('same'), [slurph(h)], do(sethel(h, 'in', 1)), returns(('count', h))), say_(ucall(f('same'), pair('p', 1))), dumph(h)]
    c.case(opts)
    return c.out

def string_cases():
    c = Cases(0)
    def strings_(f, g, G):
        h, k = g('h'), g('k')
        return [myh(h, pair('a', 1), pair('b', 'two'), pair('c', 0.5), pair('d', TRUE), pair('e', ''), pair('if', 'word'), pair('k1', 'n')), ('my', k, 'b'),
                say_(qq(hel(h, 'a'))), say_(qq('a=', hel(h, 'a'), ', b=', hel(h, G('k')), '.')), say_(qq(hel(h, 'a'), hel(h, 'b'), hel(h, 'c'), hel(h, 'd'), hel(h, 'e'), hel(h, 'if'))),
                say_(qq('[', hel(h, 'e'), ']')), say_(qq(hel(h, 'a'), ' [0]')), say_(qq(hel(h, 'a'), '->x')), say_(qq(hel(h, 'a'), '(1)')),
                say_(qq(hel(h, 'a'), '-', hel(h, 'a'))), say_(qq(hel(h, 'k1'), hel(h, G('k')))), say_(qq('%', h, ' ', hel(h, 'a'), ' %')),
                do(set_(k, 'c')), say_(qq(hel(h, G('k')), ' ', ('$', k), ' ', hel(h, 'b'))),
                ('my', g('s'), qq(hel(h, 'a'), '+', hel(h, 'a'))), say_(G('s')), say_(('.', qq(hel(h, 'a')), qq(hel(h, 'b')))), say_(('call', 'length', [qq(hel(h, 'b'), hel(h, 'b'))])),
                do(sethel(h, 'a', qq(hel(h, 'a'), hel(h, 'a')))), say_(hel(h, 'a')), do(sethel(h, qq(hel(h, 'b'), '!'), 1)), dumph(h),
                each_('x', [srt([('keys', h)])], say_(qq(('$', 'x'), '=', hel(h, ('$', 'x'))))),
                say_(jn(',', mp([srt([('keys', h)])], qq('<', hel(h, IT), '>'))))]
    c.case(strings_)
    return c.out

SAME.update({'1620': ('hash-in-loops', loop_cases), '1622': ('hash-slices', slice_cases), '1623': ('hash-parameter', opts_cases), '1624': ('hash-in-strings', string_cases)})
NEW.update({'1621': ('hash-loops-order-by-the-model', unsorted_cases)})

def faults_12b():
    out = {}
    n = [1640]
    def fault(name, near, far, subs_=()):
        out[str(n[0])] = ('fault-hash-' + name, list(subs_), near, far)
        n[0] += 1
    hh = lambda: h4('h')
    # (No block here reads the value it is handed, and a grep or a sort,
    # which hand their list on, is over a sorted one: perl's order of a
    # hash is its own, and a test compared with perl can't show it.)
    quiet = hel('h', 'a')
    said = say_(hel('h', 'a'))
    store = do(sethel('h', 'a', 9))
    add = do(sethel('h', 'new', 9))
    values, sorted_values = [('values', 'h')], [srt([('values', 'h')], NUM)]
    # Each binder over each way of naming the hash, and a store to a key
    # that is there: in a run that only reads, and then one that stores.
    named_ = [('values', values, sorted_values), ('the-hash', [H('h')], [srt([H('h')])]),
              ('a-slice', [hslice('h', 'a', 'b')], None), ('an-element', [hel('h', 'a')], None)]
    binders = [
        ('for', False, lambda its, *b: each_('v', its, *(b or [said]), STOP)),
        ('for-it', False, lambda its, *b: forit(its, *(b or [said]), STOP)),
        ('for-modifier', False, lambda its, *b: formod(b[0] if b else said, *its)),
        ('map', False, lambda its, *b: ('mya', 'r', [mp(its, *b, quiet)])),
        ('grep', True, lambda its, *b: ('mya', 'r', [gr(its, *b, quiet)])),
        ('sort', True, lambda its, *b: ('mya', 'r', [srt(its, *b, ('cmp', VA, VB))])),
    ]
    for bname, hands_on, make in binders:
        for nname, its, in_order in named_:
            if hands_on and in_order is not None:
                its = in_order
            if bname == 'sort' and nname == 'an-element':
                its = [hel('h', 'a'), hel('h', 'b')]        # one value is never compared
            fault(f'frozen-{bname}-over-{nname}', block(hh(), make(its)), block(hh(), make(its, store)))
    # Every way of changing it that perl survives (T131, T194: a delete or
    # an assignment under a loop over the hash's own values reads freed
    # memory in perl, and those are the runtime's own tests, in C).
    over = lambda *b: each_('v', values, *b, STOP)
    ways = [('a-new-key', add), ('worked-on', do(sethel('h', 'a', 1, '+='))), ('or-assigned', do(sethel('h', 'a', 1, '||='))), ('and-assigned-a-new-key', do(sethel('h', 'nope', 1, '&&='))),
            ('stepped', do(stephel('h', 'a'))), ('a-slice-stored', sethslice('h', ['a', 'b'], 1, 2))]
    for wname, change in ways:
        fault('frozen-' + wname, block(hh(), over(said)), block(hh(), over(change)))
    # Over an element, a delete of another key is safe to ask perl about:
    # the loop's own value is not the one that goes.
    one = lambda *b: each_('v', [hel('h', 'a')], *b, STOP)
    fault('frozen-delete-under-an-element', block(hh(), one(say_(V))), block(hh(), one(do(('delete', 'h', W('b'))))))
    fault('frozen-delete-of-a-slice-under-an-element', block(hh(), mya('r'), one(say_(V))), block(hh(), mya('r'), one(seta('r', hdelete('h', 'b', 'c')))))
    poke = sub('poke', [], do(sethel('h', 'a', 30)), returns(0))
    for bname, hands_on, make in binders:
        if bname != 'for-it':
            its = sorted_values if hands_on else values
            fault(f'frozen-{bname}-from-a-sub', block(make(its)), block(make(its, do(ucall('poke')))), [hh(), poke])
    # Given back when the binder ends, and not when an inner one does.
    fault('given-back-after-a-loop', block(hh(), over(said), store, dumph('h')), block(hh(), over(store)))
    fault('given-back-after-a-map', block(hh(), ('mya', 'r', [mp(values, quiet)]), store, dumph('h')), block(hh(), ('mya', 'r', [mp(values, store, quiet)])))
    inner = each_('w', values, said, STOP)
    fault('frozen-after-the-inner-loop', block(hh(), each_('v', values, inner, STOP)), block(hh(), each_('v', values, inner, store, STOP)))
    # Named by what is in the list, anywhere in it.
    for name, its in (('second-of-two', [A('b'), hslice('h', 'c', 'd')]), ('a-map-of-it', [mp(values, 1)]), ('a-sort-of-it', sorted_values),
                      ('reverse', [rev(srt([H('h')]))]), ('an-exists', [('exists', 'h', W('a'))]), ('a-key-worked-out', [hel('h', ('.', 'a', ''))])):
        fault('names-by-' + name, block(hh(), mya('b', 7), ('mya', 'r', [mp(its, quiet)])), block(hh(), mya('b', 7), ('mya', 'r', [mp(its, store, quiet)])))
    # A key that is not there, in each list (T216).
    for bname, hands_on, make in binders:
        fault(f'no-key-{bname}', block(hh(), make([hel('h', 'a'), hel('h', 'b')])), block(hh(), make([hel('h', 'a'), hel('h', 'nope')])))
    fault('no-key-in-a-slice', block(hh(), each_('v', [hslice('h', 'a', 'b')], say_(V))), block(hh(), each_('v', [hslice('h', 'a', 'nope')], say_(V))))
    fault('no-key-in-a-slice-in-a-map', block(hh(), ('mya', 'r', [mp([hslice('h', 'a', 'b')], quiet)])), block(hh(), ('mya', 'r', [mp([hslice('h', 'nope', 'b')], quiet)])))
    fault('no-key-deleted-first', block(hh(), each_('v', [hel('h', 'a')], say_(V))), block(hh(), do(('delete', 'h', W('a'))), each_('v', [hel('h', 'a')], say_(V))))
    # An odd number of arguments for a hash parameter, as the sub is
    # entered: before any default, and whether it has a name (T226).
    count = sub('count', [req('x'), slurph('o')], returns(('count', 'o')))
    fault('odd-arguments', say_(ucall('count', 1, pair('a', 1))), say_(ucall('count', 1, 'a')), [count])
    fault('odd-arguments-from-a-list', block(mya('l', 'a', 1), say_(ucall('count', 1, A('l')))), block(mya('l', 'a', 1, 'b'), say_(ucall('count', 1, A('l')))), [count])
    fault('odd-arguments-no-name', say_(ucall('take', 1, 2, 3)), say_(ucall('take', 1, 2)), [sub('take', [req('x'), slurph()], returns(D('x')))])
    fault('odd-arguments-before-a-default', say_(ucall('dflt', 1, 2, 3)), say_(ucall('dflt', UNDEF, 'k')),
          [sub('told', [], say_('the default ran'), returns(5)), sub('dflt', [('x', '//=', ucall('told')), slurph('o')], returns(('+', D('x'), ('count', 'o'))))])
    fault('too-few-before-a-hash', say_(ucall('count', 1)), say_(ucall('count')), [count])
    # In a string an element is made a string: an undef there is a fault.
    fault('undef-in-a-string', block(hh(), say_(qq('<', hel('h', 'a'), '>'))), block(hh(), say_(qq('<', hel('h', 'nope'), '>'))))
    fault('undef-key-in-a-string', block(hh(), ('my', 'k', 'a'), say_(qq(hel('h', ('$', 'k'))))), block(hh(), ('my', 'k', None), say_(qq(hel('h', ('$', 'k'))))))
    # A slice stored to: an array's before its start, and an undef key.
    fault('slice-stored-before-the-start', block(mya('a', 1, 2), setslice('a', [-2, 0], 5, 6), dump('a')), block(mya('a', 1, 2), setslice('a', [0, -3], 5, 6), dump('a')))
    fault('slice-stored-to-an-undef-key', block(hh(), sethslice('h', ['a', ''], 1, 2), dumph('h')), block(hh(), sethslice('h', ['a', UNDEF], 1, 2), dumph('h')))
    fault('slice-read-with-an-undef-key', block(hh(), ('mya', 'r', [hslice('h', 'a', '')]), say_(('scalar', 'r'))), block(hh(), ('mya', 'r', [hslice('h', 'a', UNDEF)])))
    fault('slice-stored-to-a-frozen-array', block(mya('a', 1, 2), each_('v', [A('a')], say_(V), STOP)), block(mya('a', 1, 2), each_('v', [A('a')], setslice('a', [0, 1], 5, 6), STOP)))
    return out

FAULTS.update(faults_12b())

def commands():
    return ''.join(f'    python3 t/models/hash.py --program {n} > t/{n}-{name}.pl\n'
                   f'    python3 t/models/hash.py {n} > t/{n}-{name}.expected\n'
                   for n, name in sorted([(n, SAME[n][0]) for n in SAME] + [(n, NEW[n][0]) for n in NEW] + [(n, FAULTS[n][0]) for n in FAULTS]))

def program(statements, header):
    text_lines = [line for s in statements for line in source(s)]
    return ''.join(f'# {h}\n' for h in header) + 'use v5.42;\n' + strings.OPEN + ''.join(line + '\n' for line in text_lines)

def main(argv):
    sys.setrecursionlimit(20000)
    if argv == ['--commands']:
        sys.stdout.write(commands())
        return
    want_program = argv[0] == '--program'
    number = argv[-1]
    out = sys.stdout.buffer
    model = ['model: t/models/hash.py']
    if number in NEW:
        model = ['kind: new', "D27: a hash keeps its keys in the order they were first stored. perl's order is its own, so perl is not asked."] + model
    if number in SAME or number in NEW:
        cases = (SAME.get(number) or NEW[number])[1]()
        for c in cases:
            assert output(c)[1] is None, (number, output(c)[1], output(c)[0][-200:])
        statements = [s for c in cases for s in c]
        out.write((program(statements, model) if want_program else output(statements)[0]).encode())
        return
    name, the_subs, near, far = FAULTS[number]
    path = f't/{number}-{name}.pl'
    header = ['kind: fault'] + model
    statements = the_subs + [('say', 1), near, far, ('say', 2)]
    if want_program:
        out.write(program(statements, header).encode())
        return
    printed, fault, at = output(statements)
    assert fault is not None and output(the_subs + [('say', 1), near])[1] is None, (number, printed, fault)
    found = {}
    it.lines_(statements, len(header) + 3, found)
    out.write(f'{printed}fault: {fault} at {path} line {found[at]}.\nexit: 1\n'.encode())

if __name__ == '__main__':
    main(sys.argv[1:])
