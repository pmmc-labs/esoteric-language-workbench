use v5.42;
# W2: join's separator is a container too, read when join runs, after its list has been worked out.
my $sep = "-";
sub chs() { $sep = "+"; return 1 }
say join($sep, chs(), 2, 3);
my @a = (",");
sub chg() { $a[0] = ";"; return 1 }
say join($a[0], chg(), 2, 3);
