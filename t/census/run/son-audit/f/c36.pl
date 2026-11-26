use v5.42;
my %h=(a=>1); my $f=sub { my %c=%h; $c{a}++; $c{a} }; $f->(); print $f->(), $h{a}, "\n";
