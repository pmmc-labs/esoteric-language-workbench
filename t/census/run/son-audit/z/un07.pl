use v5.42;
our %h=(k=>1); eval { local $h{n}=2; die "x\n" }; print join(",", sort keys %h), "\n";
