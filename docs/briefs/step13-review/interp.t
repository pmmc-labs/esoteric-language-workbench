### dot-eq-interp
my $x = 3; my $t = "t"; $t .= "$x-" . ($x = 5); say $t;
### dot-eq-interp-alone
my $x = 3; my $t = "t"; $t .= "$x" . ($x = 5); say $t;
### dot-eq-interp-chain
my $r = [3]; my $t = "t"; $t .= "$r->[0]-" . ($r->[0] = 5); say $t;
### assign-interp
my $x = 3; my $t = "$x-" . ($x = 5); say $t;
### interp-alone-then
my $x = 3; say "$x" . ($x = 5);
### interp-chain-alone-then
my $r = [3]; say "$r->[0]" . ($r->[0] = 5);
### interp-deref-alone-then
my $x = 3; my $r = \$x; say "${ $r }" . ($x = 5);
### interp-postfix-alone-then
my $x = 3; my $r = \$x; say "$r->$*" . ($x = 5);
### interp-elem-alone-then
my @a = (3); say "$a[0]" . ($a[0] = 5);
