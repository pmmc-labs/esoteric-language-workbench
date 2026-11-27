# kind: fault
# perl dies: Integer overflow in format string for sprintf (T283); from 2^31 it makes a string that long.
use v5.42;
say sprintf("%.*f", 2, 1.5);
say length sprintf("%*d", 4611686018427387904, 1);
