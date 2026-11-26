use v5.42;
# W1: "The number is decimal digits with a minus or without" (Q1a).
# To perl an index in a string is code, and a number with a leading zero is octal.
my @a = (0 .. 20);
say "$a[010]";              # perl: 8.   decimal digits: 10
say "$a[-010]";             # perl: 13.  decimal digits: 11
say "$a[017] $a[0010]";     # perl: 15 8
say "@a[010, 011]";         # perl: 8 9
say "@a[07 .. 010]";        # perl: 7 8. decimal digits: 7 8 9 10
say "$a[00] $a[01] $a[07]"; # the same either way: 0 1 7
