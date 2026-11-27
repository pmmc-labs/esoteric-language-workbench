### say-paren-brace
say({a => 1}->{a});
### say-paren-brace-var
my $k = "a"; say({ $k => 1 }->{a});
### say-paren-brace-plus
say(+{a => 1}->{a});
### print-paren-brace
print({a => 5}->{a}, "\n");
### say-paren-bracket
say([7]->[0]);
### say-bracket
say [7]->[0];
### say-paren-paren-brace
say(({a => 1})->{a});
### say-brace-str-comma
say {"a", 1}->{a};
### say-paren-brace-empty
say(scalar(%{{}}));
### say-list-second-brace
say 1, {a => 2}->{a};
### say-paren-brace-word-noarrow
my $h = {a => 1}; say({ a => 1 } == $h ? "same" : "diff");
