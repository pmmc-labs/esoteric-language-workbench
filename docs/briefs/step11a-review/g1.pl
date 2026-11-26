use v5.42;
# G1: how large may the number be?  perl takes any digits, in silence, and
# from 2^63 on they are not the element they say.
my @a = (10 .. 14);
say "$a[18446744073709551615]";     # 2^64 - 1: perl prints 14, the last element
say "$a[18446744073709551614]";     # 13
say "$a[18446744073709551616]";     # 2^64: 14 again
say "$a[99999999999999999999]";     # T202's: 14
say "@a[0, 18446744073709551615]";  # 10 14
