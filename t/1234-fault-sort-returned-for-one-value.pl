# kind: fault
# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a = (3, 1, 2);
sub f() {
    return (sort { $a <=> $b } (@a));
}
say(1);
say(f());
my $x = f();
say(2);
