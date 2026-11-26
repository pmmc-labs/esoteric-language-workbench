use v5.42;
sub f { my %h=@_; my %c=%h; $c{a}=2; $h{a} } print f(a=>1),"\n";
