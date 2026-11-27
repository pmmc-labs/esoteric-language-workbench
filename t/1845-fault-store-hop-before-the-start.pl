# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $r = [1];
$r->[-3]{a} = 1;
say(2);
