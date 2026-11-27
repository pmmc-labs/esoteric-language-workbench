# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my %h = (a => 1);
my $r = \%h;
for my $v (values(%h)) {
    $r->{b} = 5;
    last;
}
say(2);
