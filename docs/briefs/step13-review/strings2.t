### braces-name-then-bracket
my $x = "s"; my @x = (7); say "<${x}[0]>";
### braces-name-then-arrow
my $x = [5]; say "<${x}->[0]>";
### braces-name-then-brace
my $x = "s"; my %x = (a => 7); say "<${x}{a}>";
### elem-then-arrow-at
my @a = ([1, 2]); say "<$a[0]->@*>";
### helem-chain-arrow-dollar
my %h = (a => \5); say "<$h{a}->$*>";
### chain-then-at-star-after-two
my $r = [[[1, 2]]]; say "<$r->[0][0]->@*>";
### lastidx-braces-chain-sub
my $r = [[1, 2]]; say "<$#{ $r->[0] }>";
### dollar-braces-chain-then-bracket
my $x = [9]; my $r = [\$x]; say "<${ $r->[0] }[0]>";
### dollar-braces-chain-then-arrow
my $x = [9]; my $r = [\$x]; say "<${ $r->[0] }->[0]>";
### at-braces-chain-then-bracket
my $r = [[5, 6]]; say "<@{ $r->[0] }[1]>";
### at-braces-then-brace
my $r = {a => 5}; say "<@{ $r }{a}>";
### at-braces-chain-hash
my $r = [{a => 5}]; say "<@{ $r->[0] }{a}>";
### postfix-slice-then-bracket
my $r = [5, 6]; say "<$r->@[0][1]>";
### lastidx-postfix-then-arrow
my $r = [5, 6]; say "<$r->$#*->[0]>";
### at-star-then-arrow-word
my $r = [5, 6]; say "<$r->@*->x>";
