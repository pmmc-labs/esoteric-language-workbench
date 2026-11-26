use v5.42;
use v5.36; sub w ($cb) { $cb->(5) } print w(sub { $_[0] + 1 }), "\n";
