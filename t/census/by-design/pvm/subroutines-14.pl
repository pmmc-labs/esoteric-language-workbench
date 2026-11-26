use v5.42;
our $v = "outer";
sub show  { print "$v\n" }
sub relay { show() }
sub inner { local $v = "inner"; show(); relay() }
inner();
show();
