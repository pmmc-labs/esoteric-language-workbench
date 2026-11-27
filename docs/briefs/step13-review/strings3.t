### dbraces-arrow-onstring
my $x = "abc"; my $r = \$x; say "<${ $r }->[0]>";
### dbraces-arrow-onstring-nospace
my $x = "abc"; my $r = \$x; say "<${$r}->[0]>";
### dbraces-arrow-brace-onstring
my $x = "abc"; my $r = \$x; say "<${ $r }->{k}>";
### dbraces-bracket-onstring
my $x = "abc"; my $r = \$x; say "<${ $r }[0]>";
### dbraces-brace-onstring
my $x = "abc"; my $r = \$x; say "<${ $r }{k}>";
### lastidx-braces-then-bracket-text
my $r = [1, 2, 3]; say "<$#{ $r }[x]>";
### lastidx-braces-then-brace
my $r = [1, 2, 3]; say "<$#{ $r }{x}>";
### lastidx-braces-then-arrow
my $r = [1, 2, 3]; say "<$#{ $r }->[0]>";
### at-braces-then-arrow
my $r = [1, 2, 3]; say "<@{ $r }->[0]>";
### dollar-postfix-then-bracket-string
my $x = "abc"; my $r = \$x; say "<$r->$*[0]>";
### dollar-postfix-then-arrow-string
my $x = "abc"; my $r = \$x; say "<$r->$*->[0]>";
### dbraces-colon
my $x = "abc"; my $r = \$x; say "<${ $r }::y>";
### dbraces-chain-then-bracket-num
my $x = 7; my $r = [\$x]; say "<${ $r->[0] }[0]>";
