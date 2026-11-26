use v5.42;
# G1: at and below 2^63 - 1 perl reads past the end, and warns: a fault here.
my @a = (10 .. 14);
say "$a[9223372036854775807]|";
say "$a[9223372036854775808]|";
say "$a[-9223372036854775808]|";
say "$a[-99999999999999999999]|";
