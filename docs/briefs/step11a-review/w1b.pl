use v5.42;
# W1, the other half: perl does not compile an 8 or a 9 after a leading zero.
my @a = (0 .. 20);
say "$a[08]";
