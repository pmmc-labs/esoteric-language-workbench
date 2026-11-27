# kind: same
# sprintf, printf, chomp, ucfirst, lcfirst, rindex, qw and a heredoc beside elements through references (steps 13a and 16).
use v5.42;
my $r = { name => "ann", n => 3 }; my @l = ([1, 2], [3, 4]);
printf("%s has %d, %s\n", $r->{name}, $r->{n}, sprintf("%03d", $l[1][0]));
my $s = $r->{name}; chomp($s); say ucfirst($s), lcfirst("ABC"), rindex($r->{name}, "n");
for my $w (qw(a b)) { $r->{$w} = uc $w; }
say join(",", map { $r->{$_} } qw(a b));
my $h = { qw(x 1 y 2) };
say $h->{y}, [qw(p q r)]->[2], ref([qw(a)]);
say <<"END";
name: $s
END
say qq{n=$s}, q(->[0]);
