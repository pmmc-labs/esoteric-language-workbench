# kind: fault
# model: t/models/ret.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a = (4, 5, 6);
sub f() {
    return 1 ? @a : 0;
}
say(1);
say(f());
my $x = f();
say(2);
