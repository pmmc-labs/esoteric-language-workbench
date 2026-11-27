# kind: refused
# perl chomps the element.
use v5.42;
my %h = (k => "v\n");
chomp $h{k};
