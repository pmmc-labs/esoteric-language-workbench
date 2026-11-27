### s-postfix-after-elem
my $r = [[1, 2]];
say "<$r->[0]->@*>";
### s-postfix-after-elem-noarrow
my $r = [[1, 2]];
my @a = ([3, 4]);
say "<$a[0]->@*>";
### s-lastidx-after-elem
my $r = [[1, 2]];
say "<$r->[0]->$#*>";
### s-scalar-deref
my $x = 5; my $r = \$x;
say "<$r->$*>";
### s-hash-deref
my $r = {a => 1};
say "<$r->%*>";
### s-at-star-then-bracket
my $r = [1, 2];
say "<$r->@*[0]>";
### s-lastidx-then-bracket
my $r = [1, 2];
say "<$r->$#*[0]>";
### s-scalar-deref-then-bracket
my $x = [5]; my $r = \$x;
say "<$r->$*[0]>";
### s-scalar-deref-then-arrow
my $x = [5]; my $r = \$x;
say "<$r->$*->[0]>";
### s-braces-scalar-then-arrow
my $x = [5]; my $r = \$x;
say "<${ $r }->[0]>";
### s-braces-scalar-then-bracket
my $x = [5]; my @y = (6); my $r = \$x;
say "<${ $r }[0]>";
### s-braces-at-then-bracket
my $r = [5, 6];
say "<@{ $r }[1]>";
### s-braces-lastidx-then-bracket
my $r = [[5, 6, 7]];
say "<$#{ $r }[0]>";
### s-braces-lastidx-then-bracket2
my $r = [[5, 6, 7], 1];
say "<$#{$r}[0]>";
### s-arrow-space-bracket
my $r = [5];
say "<$r-> [0]>";
### s-at-slice-postfix
my $r = [5, 6, 7];
say "<$r->@[0, 1]>";
### s-at-slice-postfix-after-elem
my $r = [[5, 6, 7]];
say "<$r->[0]->@[0, 1]>";
### s-at-no-star
my $r = [5];
say "<$r->@>";
### s-at-hash-slice
my $r = {a => 1, b => 2};
say "<$r->@{a}>";
### s-hash-then-postfix
my %h = (a => [1, 2]);
say "<$h{a}->@*>";
### s-at-braces-word
our @true = (1);
say "<@{true}>";
### s-at-braces-space-word
my @x = (1, 2);
say "<@{ x }>";
### s-at-braces-chain
my $r = [[1, 2]];
say "<@{ $r->[0] }>";
### s-dollar-braces-chain
my $x = 5; my $r = [\$x];
say "<${ $r->[0] }>";
### s-elem-then-colon
my $r = [5];
say "<$r->[0]::x>";
### s-elem-then-arrow-word
my $r = [5];
say "<$r->[0]->x>";
### s-elem-then-arrow-amp
my $r = [5];
say "<$r->[0]->&*>";
### s-arrow-arrow
my $r = [[5, 6]];
say "<$r->[0]->[1]>";
### s-elem-brace-elem
my $r = [{k => 7}];
say "<$r->[0]{k}>";
### s-named-elem-brace
my @a = ({k => 7});
say "<$a[0]{k}>";
### s-neg-index
my $r = [5, 6];
say "<$r->[-1]>";
### s-at-star-then-arrow
my $r = [[5]];
say "<$r->@*->[0]>";
### s-chain-hyphen-gt
my $r = {a => 5};
say "<$r->{a}->>";
### s-chain-then-at
my $r = [5]; my @x = (1);
say "<$r->[0]@x>";
### s-lastidx-postfix-then-star
my $r = [5, 6];
say "<$r->$#**>";
### s-at-star-star
my $r = [5, 6];
say "<$r->@**>";
### s-dollar-star-then-star
my $x = 5; my $r = \$x;
say "<$r->$**>";
### s-dollar-hash-brace
my $x = {a => 1}; my $r = \$x;
say "<$r->$*{a}>";
