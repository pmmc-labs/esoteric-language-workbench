use v5.42;
my $p = 1 + time() * 0;
my $q = 2 + time() * 0;
my $o = "";
for my $v ($p, $q) { $o .= "[$v]" }
print join(",", map { "[$_]" } $p, $q), " ", join(",", grep { $_ > 1 } $p, $q), " $o\n";
