# kind: fault
# model: t/models/it.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a = (1, 2, 3);
sub f() {
    return (map { $_ } (@a));
}
say(1);
say(f());
my $x = f();
say(2);
