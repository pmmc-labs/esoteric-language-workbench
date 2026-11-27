### deref-brace-hash-var
my $k = "a"; my @k = keys %{ { $k => 1 } }; say "@k";
### deref-brace-hash-word
my @k = keys %{ { a => 1 } }; say "@k";
### deref-brace-hash-lc
my $k = "A"; my @k = keys %{ { lc($k) => 1 } }; say "@k";
### deref-brace-hash-empty
my $n = keys %{ {} }; say $n;
### deref-at-brace-hash-var
my $k = "a"; my @l = @{ { $k => 1 } }{a}; say "@l";
### deref-dollar-brace-var
my $k = "a"; my $x = ${ { $k => \5 } }{a}; say $x;
### deref-at-bracket
my @l = @{ [1, 2] }; say "@l";
### deref-lastidx-bracket
say $#{ [1, 2, 3] };
### deref-at-plus-brace-var
my $k = "a"; my @k = keys %{ +{ $k => 1 } }; say "@k";
### say-paren-brace-var-alone
my $k = "a"; say({ $k => 1 });
### say-paren-brace-var-comma
my $k = "a"; say({ $k, 1 });
### print-paren-brace-var
my $k = "a"; print({ $k => 1 }, "\n");
### say-paren-brace-lc
my $k = "a"; say({ lc($k) => 1 }->{a});
### say-paren-spaced-brace
my $k = "a"; say( { $k => 1 }->{a} );
### ref-paren-brace-var
my $k = "a"; say ref({ $k => 1 });
