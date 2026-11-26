use v5.42;
use utf8;
use open ":std", ":encoding(UTF-8)";
my $x = "e"; my @a = (1, 2); my $w = "☺"; my @u = ("é", "ü");
say "${x}é|@{a}é|$#{a}é|é$x é|é@a é|é$a[0] ×|${x}́|@{a}٣|${x}→|$x é$x|é$#a é";
say "$w$x|$x$w|@u|$u[0]$x|\x{e9}$w|\xe9$x|$x\xe9|é$w";
say length("$w$x"), length("@u"), length("\xe9$w"), length("$x\xe9");
say "$x\x{263A}$x" eq $x . "\x{263A}" . $x ? "same" : "differ";
