# kind: refused
# perl warns `Non-octal character '8' terminates \0 early`.
use v5.42;
say "\18";
