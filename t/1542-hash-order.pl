# kind: new
# D27: a hash keeps its keys in the order they were first stored. perl's
# order is another every run, so perl is not asked, and the answers are by
# hand: keys, values and the hash in a list go in that order; a key stored
# again keeps its place; a key deleted and stored again is last.
use v5.42;
my %h = (one => 1, two => 2, three => 3, four => 4);
say join(",", keys %h);
say join(",", values %h);
say join(",", %h);
say %h;
$h{five} = 5;
$h{two} = 22;
say join(",", keys %h), "|", join(",", values %h);
delete $h{one};
say join(",", keys %h);
$h{one} = 11;
say join(",", keys %h), "|", join(",", values %h);
# A key given twice keeps its first place and its last value.
my %twice = (a => 1, b => 2, a => 3, c => 4, b => 5);
say join(",", %twice);
# A copy has the order of what it was copied from, and its own after.
my %copy = %h;
$copy{six} = 6;
delete $copy{three};
say join(",", keys %copy), "|", join(",", keys %h);
my %more = (zero => 0, %h, last => 9, two => 2);
say join(",", keys %more);
# Numbers as keys are in the order stored, not their own.
my %n = (10 => "a", 9 => "b", 100 => "c", 1 => "d");
say join(",", keys %n);
my @k = keys %n;
my @v = values %n;
my @first = (keys %n)[0, 1];
say "@k|@v|@first";
# Every key deleted, and stored again in another order.
for my $k (sort keys %n) { delete $n{$k}; }
say scalar(%n), "[", join(",", keys %n), "]";
$n{z} = 1;
$n{y} = 2;
$n{x} = 3;
$n{w} = 4;
say join(",", keys %n);
# keys are copies, so a delete after them in a list is no change to them;
# and keys or values in one arm of a ? : are a list where a list is wanted.
my %kd = (a => 1, b => 2, c => 3, d => 4);
my @kd = (keys(%kd), delete($kd{a}));
my @either = (1 ? keys %kd : (0));
my @other = (0 ? (0) : values(%kd), 9);
say "@kd|@either|@other";
# Many keys: the order holds as the table grows, and after holes are closed.
my %big;
for my $i (1 .. 1000) { $big{"k" . $i} = $i; }
for my $i (1 .. 990) { delete $big{"k" . $i}; }
$big{k5} = 5;
say join(",", keys %big), "|", scalar(%big);
my $sum = 0;
@v = values %big;
for my $v (@v) { $sum += $v; }
say $sum;
