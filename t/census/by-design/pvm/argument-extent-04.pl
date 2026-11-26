use v5.42;
local $SIG{__WARN__} = sub { };
my @greedy = (warn "a", "b");
my @cut = (warn("a"), "b");
print scalar @greedy, scalar @cut, "\n";
