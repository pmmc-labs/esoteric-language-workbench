# kind: refused
# perl takes the first word for the format: a-b.
use v5.42;
say sprintf(qw(%s-%s a b));
