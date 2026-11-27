### p-ref-brace
my $t = ref {a => 1}; say $t;
### p-ref-brace-var
my $x = "k"; my $t = ref { $x => 1 }; say $t;
### p-defined-brace
say defined {a => 1} ? "y" : "n";
### p-scalar-brace
my $n = scalar({a => 1}); say ref $n;
### p-not-brace
say !{a => 1} ? "y" : "n";
### p-reverse-brace
my @l = reverse { a => 1 }; say scalar(@l), " ", ref $l[0];
### p-reverse-brace-var
my $x = "a"; my @l = reverse { $x => 1 }; say scalar(@l), " ", ref $l[0];
### p-join-brace
my $x = "a"; my $s = join "-", { $x => 1 }; say $s =~ /HASH/ ? "hash" : $s;
### p-push-brace-var
my @a; my $x = "a"; push @a, { $x => 1 }; say ref $a[0];
### p-unshift-brace-var
my @a; my $x = "a"; unshift @a, { $x, 1 }; say ref $a[0];
### p-return-brace-var
sub f($x) { return { $x => 1 }; } say ref f("a");
### p-return-brace-lc
sub f($x) { return { lc($x) => 1 }; } say ref f("a");
### p-return-brace-empty
sub f() { return {}; } say ref f();
### p-keys-brace
my $x = "a"; my @k = keys { $x => 1 }->%*; say "@k";
### p-arrow-space
my $r = [5]; say $r -> [0];
### p-arrow-newline
my $r = [5]; say $r
  ->[0];
### p-arrow-at-space
my $r = [5, 6]; my @x = $r-> @*; say "@x";
### p-arrow-at-space-star
my $r = [5, 6]; my @x = $r->@ *; say "@x";
### p-elem-space-elem
my @a = ([1, 2]); say $a[0] [1];
### p-helem-space-helem
my %h = (a => {b => 3}); say $h{a} {b};
### p-at-star-bracket
my $r = [5, 6]; say $r->@*[0];
### p-at-star-arrow
my $r = [[5, 6]]; say $r->@*->[0];
### p-postfix-chain
my $r = [[5, [7, 8]]]; say $r->[0]->[1]->@*;
### p-call-bracket
sub f() { return [5, 6]; } say f()[1];
### p-listslice-chain
my @l = ([1, 2]); say +(@l)[0][1];
### p-anon-bracket
say [5, 6][1];
### p-anon-arrow
say [5, 6]->[1];
### p-say-anon
say [5, 6]->@*;
### p-incr-chain
my $r = [5]; ++$r->[0]; say $r->[0];
### p-backslash-eq
my @a; my $r = \@a; say \@a == $r ? "same" : "diff";
### p-backslash-space
my @a = (1); my $r = \ @a; say $r->[0];
### p-not-backslash
my @a; say !\@a ? "f" : "t";
### p-dollar-braces-word
our $true = 7; say ${true};
### p-at-braces-word-strict
my @x = @{true}; say scalar(@x);
### p-at-braces-undef-word
my @x = @{ undef }; say scalar(@x);
### p-at-braces-plus-word
my @x = @{ +true }; say scalar(@x);
### p-lastidx-braces
my $r = [1, 2, 3]; say $#{$r}, $#{ $r }, $r->$#* + 1;
### p-lastidx-braces-word
my @x = (1, 2); say $#{x};
### p-lastidx-braces-space-word
my @x = (1, 2); say $#{ x };
### p-hash-braces-word
my %x = (a => 1); my @k = keys %{x}; say "@k";
### p-ternary-brace
my $c = 1; my $x = "a"; my $h = $c ? { $x => 1 } : [1]; say ref $h;
### p-stmt-brace-var-fatcomma
my $x = "a";
{ $x => 1 };
say "ran";
### p-map-plus-brace
my @l = map { +{ n => $_ } } 1, 2; say ref $l[0];
### p-map-bracket-first
my @l = map { [$_] } 1, 2; say ref $l[0], scalar(@l);
### p-map-paren-brace
my @l = map { ({ n => $_ }) } 1, 2; say ref $l[0], scalar(@l);
### p-map-brace-semicolon
my @l = map {; "$_" => 1 } 1, 2; say scalar(@l);
### p-sort-brace-anon
my @l = sort { $a->{n} <=> $b->{n} } ({n => 2}, {n => 1}); say $l[0]{n};
### p-grep-brace-arrow
my @l = grep { $_->[0] } ([0], [1]); say scalar(@l);
