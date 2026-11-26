use v5.42;
my $c = "Foo"; my $o = bless {}, $c; print ref $o, "\n";
