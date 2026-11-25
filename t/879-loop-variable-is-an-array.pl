# kind: refused
# perl: Missing $ on loop variable.
use v5.42;
my @a = (1, 2);
for my @x (@a) {
    say 1;
}
