# Interpolation, by hand, with perl's answers: what the model of step 11a
# does not write. A string is a value made where it stands (T196, T209),
# what follows a name and is text (T199, T201, T203), and the assignments
# perl keeps (T198).
use v5.42;
use utf8;
use open ':std', ':encoding(UTF-8)';

# A string is made where it stands: no later piece of the row shows in it.
my $x = 3;
say "$x-" . ($x = 5);
$x = 3;
say "$x" . "a" . ($x = 5);
$x = 3;
say "a$x" . ($x = 5);
$x = 3;
say "$x" + ($x = 5);
$x = 3;
say "$x" x 2 . ($x = 5);
$x = 3;
say "$x", ($x = 5);
$x = 3;
say "$x-", ($x = 5);
$x = 3;
say(("$x" || 0) + ($x = 5));
sub ch() { $x = 5; return "c"; }
$x = 3;
say "$x-" . ch();
$x = 3;
say "$x" . ch();
$x = 3;
my @l = ("$x", ch());
say @l;
$x = 3;
@l = ("$x-", ch());
say @l;
sub two($p, $q) { return "$p$q"; }
$x = 3;
say two("$x", $x = 5);
$x = 3;
say two("$x-", $x = 5);

# And an array's values are read there too.
my @a = (1, 2);
sub store() { $a[0] = 9; return "c"; }
say "@a" . store();
@a = (1, 2);
say "@a-" . store();
@a = (1, 2);
say "-@a-" . store() . "@a";
@a = (1, 2);
say "$a[0]" . store();
@a = (1, 2);
say "$a[0]-", store();
@a = (1, 2);
say "@a[0, 1]-" . store();
@a = (1, 2);
say "$#a-" . push(@a, 3);
@a = (1, 2);
say "@a" . shift(@a);
@a = (1, 2);
say "$a[0]$a[1]" . shift(@a);
@a = (1, 2);
my $i = 0;
say "$a[$i]-" . ($i = 1);
$i = 0;
say "$a[$i]" . ($i = 1);

# A string as what is assigned, to a variable it reads.
my $s = "a";
$s = "$s$s";
say $s;
$s .= "$s-$s";
say $s;
$s = "b$s";
say $s;
my $t = "t";
$t = "$s$t" . $t;
say $t;
@a = (1, 2);
$a[0] = "@a";
say "@a";
$a[0] .= "@a";
say "@a";
push @a, "@a";
say "@a";
@a = ("@a", "@a");
say scalar(@a);

# The assignments perl keeps (T198): a string that is one thing alone,
# more after the bracket, and any operator but `.=`.
my $u = "u";
my $z = "z";
$x = "a";
@a = (1, 2);
$t = "t";
$t .= ($u = "$x");
say "$t $u";
$t = "t";
$t .= ($u = "@a");
say "$t $u";
$t = "t";
$t .= ($u = "$a[0]");
say "$t $u";
$t = "t";
$t .= ($u = "@a[0, 1]");
say "$t $u";
$t = "t";
$t .= ($u = "$#a");
say "$t $u";
$t = "t";
$t .= ($u = "${x}");
say "$t $u";
$t = "t";
$t .= ($u = "$x$z") . "b";
say "$t $u";
$t = ($u = "$x$z");
say "$t $u";
$t = "t";
$t = $t . ($u = "$x$z");
say "$t $u";
$t = "t";
$t .= "$x$z" . ($u = "q");
say "$t $u";
$t = "t";
$t .= ($u .= "$x$z");
say "$t $u";

# What follows a name, and is text.
$x = 3;
my @b = (7, 8, 9);
say "$x's";
say "$x:";
say "$x: $x";
say "$x:y";
say "$x\::y";
say "${x}::y";
say "$x:\:";
say "@b's";
say "@b:";
say "@{b}::";
say "$#{b}::";
say "$x->";
say "$x->y";
say "$x->(1)";
say "$x->%*";
say "$x-\>[0]";
say "$x\->[0]";
say "$x->\[0]";
say "$b[0]->";
say "@b[0, 1]->";
say "$#b->";
say "${x}->[0]";
say "@{b}->[0]";
say "${x}{a}";
say "${x}[1]";
say "$x\[1]";
say "$x [1]";
say "$x\{a}";
say "$x {a}";
say "@{b}[0, 1]";
say "@b [0]";
say "@b\[0]";
say "$#{b}[0]";
say "$b[1]]";
say "$b[1]s";
say "$b[ 1 ]";
say "@b[ 0 , 1 ]";
say "@b[0,1]";
say "@b[0..1]";
say "@b[0, 1,]";
say "$b[-0]";
say "\$x \@b \\$x \\\$x";
say "$x\n$x\t$x\x41$x\101$x\$";
say "100% of $x, %h and &f() and me\@example.com";
say "a string
over two lines, with $x and @b
in it";

# A name perl has a meaning for is only a name.
my $q = 2;
my $y = 3;
my $m = 4;
my $tr = 5;
my $print = 6;
my @sort = (7, 8);
my $x1 = 9;
say "$q$y$m$tr$print@sort$x1";
say "${q}${y}${m}${tr}${print}@{sort}${x1}";

# Past ASCII: before a variable, and after braces, an element and a slice.
my $e = "e";
say "é$e";
say "${e}é";
say "→$e → $e";
say "$b[0]é";
say "@b[0, 1]é";
say "@{b}é";
say "$#{b}é";

# After a string an operator comes next; and a string is one value.
say "$x" -1;
say "$x" . 1 + 1;
sub whole() { return "@b"; }
my $v = whole();
say $v;
say length("@b");
my @one = ("@b");
say scalar(@one);
if ("$x" eq "3") { say "yes"; }
say "v$x" lt "v10" ? "lt" : "ge";

# A string in a loop's list is a copy (T209).
$x = 3;
for my $c ("$x", "$x-") { $x = 5; say $c; }
@a = (1, 2);
for my $c ("@a") { push @a, 3; say $c; }
for my $c ("$a[0]") { $a[0] = 9; say $c; }
say "@a";

# In a sort's block `$a[0]` is the array's element (T210).
@a = (3, 1, 2);
my @r = sort { say "$a[0]$b"; $a <=> $b } @a;
say "@r";
