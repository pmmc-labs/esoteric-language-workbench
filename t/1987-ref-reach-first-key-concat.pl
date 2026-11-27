# kind: refused
# perl runs it: 'b!\n'.
use v5.42;
my %h;
my $k = "a";
$h{$k = "b"}{x} = $k . "!";
say $h{b}{x};
