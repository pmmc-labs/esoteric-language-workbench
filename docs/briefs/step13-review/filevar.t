### filevar-ref-before-my
my $r = g();
my $x = 5;
say $r->$*;
sub g() { return \$x; }
### filevar-ref-before-my-noinit
my $r = g();
$r->$* = 7;
my $x;
say defined $x ? $x : "undef";
sub g() { return \$x; }
### filevar-array-ref-before-my
my $r = g();
push $r->@*, 1;
my @a = (9);
say scalar($r->@*), " ", $r == \@a ? "same" : "diff";
sub g() { return \@a; }
### filevar-array-ref-before-my-nostore
my $r = g();
push $r->@*, 1;
my @a;
say scalar($r->@*), " ", $r == \@a ? "same" : "diff", " ", scalar(@a);
sub g() { return \@a; }
### filevar-hash-ref-before-my
my $r = g();
$r->{k} = 1;
my %h;
say scalar(keys %h), " ", $r == \%h ? "same" : "diff";
sub g() { return \%h; }
