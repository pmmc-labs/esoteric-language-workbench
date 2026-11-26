use v5.42;
sub h { f() } *f = sub { 7 }; print h(), "\n";
