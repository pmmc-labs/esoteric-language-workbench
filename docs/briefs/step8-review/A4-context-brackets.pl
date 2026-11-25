use v5.42;
sub none() { return; }
sub show($p) { return defined($p) ? "[" . $p . "]" : "U" }
sub cnt($p = "-", $q = "-") { return show($p) . show($q) }
say cnt(none());
say cnt((none()));
say cnt(+none());
say cnt((1 and none()));
say cnt((0 or none()));
say cnt(1 && none());
say cnt(none() || none());
say cnt(1 ? none() : 0);
say cnt((none()), "z");
my $v = (none());
say show($v);
