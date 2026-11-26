# Hashes, by hand, with perl's answers: what the model of step 12a does not
# reach. Words of perl's own as keys, in braces and before `=>` (T214, T215);
# what a key is when it is a number, a boolean or worked out; small
# programs. Everything that shows an order sorts.
use v5.42;

# Any word alone in the braces, and any word before =>, is that string.
my %words = (if => 1, q => 2, print => 3, true => 4, x => 5, y => 6, s => 7, m => 8, tr => 9, undef => 10, not => 11, and => 12, v66 => 13, keys => 14, sub => 15, my => 16, __PACKAGE__ => 17);
say join(",", sort keys %words);
say $words{if}, $words{q}, $words{print}, $words{true}, $words{x}, $words{y}, $words{s}, $words{m}, $words{tr};
say $words{undef}, $words{not}, $words{and}, $words{v66}, $words{keys}, $words{sub}, $words{my}, $words{__PACKAGE__};
say $words{ if }, $words{	x	}, exists $words{say} ? "say" : "no say";

# A sub's name before => and in braces is not a call.
sub name() { return "called" }
my %subs = (name => 1, other => 2, third => 3, fourth => 4);
say join(",", sort keys %subs), $subs{name}, $subs{name()} // "undef";

# A key is a string: numbers by how they print, booleans as 1 and "".
my %n = (1 => "one", 1.0 => "float", "1" => "str", 2 => "two", 0x10 => "hex", 1e3 => "exp", 1.5 => "half", -1 => "minus", 3 => "three");
say join(",", map { $_ . "=" . $n{$_} } sort keys %n);
say $n{1}, $n{1.0}, $n{"1"}, $n{16}, $n{1000}, $n{1.50}, $n{-1}, $n{0 - 1}, $n{2 + 1};
my %b = ((true) => "t", (false) => "f", (1 == 1) => "eq", "a b" => "blank", "" . 5 => "five");
say scalar(%b), "|", join(",", map { "[" . $_ . "]=" . $b{$_} } sort keys %b);
say $b{(true)}, $b{!1}, $b{""}, $b{"a" . " " . "b"}, $b{5}, $b{"5"}, $b{2 + 3};

# A key worked out: one expression, made a string as . makes one.
my $i = 1;
my %made;
$made{$i} = "a";
$made{$i + 1} = "b";
$made{"k" . $i} = "c";
$made{$i * 1.5} = "d";
$made{$i == 1 ? "yes" : "no"} = "e";
$made{length("four")} = "f";
say join(",", map { $_ . "=" . $made{$_} } sort keys %made);

# Hard against operators: a brace after an element ends a value.
my %o = (a => 7, b => 3, c => 2, d => 1);
say $o{a} % $o{b}, $o{a} %3, $o{a} x 2, $o{a} . $o{b}, $o{a}++ % 2, $o{a}-- * 2, -$o{a}, $o{a} ** $o{c};
say $o{a} <=> $o{b}, $o{a} == 7 ? "seven" : "not", !$o{d}, !!$o{d};
say scalar(%o) % 3, %o ? "some" : "none", !%o ? "none" : "some", %o + 0, %o == 4 ? "four" : "not", "n" . %o;

# The count where one value is wanted, each way to ask.
my $count = %o;
my $keys = keys %o;
my $values = values(%o);
say $count, $keys, $values, scalar(%o), scalar(keys %o), scalar(values(%o)), keys(%o) + values(%o);
my @two = (scalar(%o), keys(%o) + 0);
say "@two";

# exists and delete, with brackets and without, where each may stand.
say exists $o{a} ? "a" : "no a", exists($o{z}) ? "z" : "no z", exists $o{a} && exists $o{b} ? "both" : "not both";
say exists $o{a} == 1 ? "true" : "false", (exists $o{zz}) ? 1 : 0, !exists $o{zz} ? 1 : 0;
if (exists $o{a} and not exists $o{z}) { say "a and no z" }
my $gone = delete $o{a};
my $none = delete($o{a});
say $gone, defined($none) ? "defined" : "undef", scalar(%o), exists $o{a} ? "still" : "gone";
delete $o{b};
delete($o{nope});
say join(",", sort keys %o);

# Counting words.
my @text = ("the", "cat", "and", "the", "dog", "and", "the", "bird");
my %seen;
for my $w (@text) { $seen{$w}++; }
say join(" ", map { $_ . ":" . $seen{$_} } sort keys %seen);
my @once = grep { $seen{$_} == 1 } sort keys %seen;
say "@once";
my @by_count = sort { $seen{$b} <=> $seen{$a} or $a cmp $b } keys %seen;
say "@by_count";

# Turned round, through a list in brackets (D102).
my %color = (apple => "red", grass => "green", sky => "blue", sun => "yellow");
my %thing = map { ($color{$_} => $_) } sort keys %color;
say join(",", map { $_ . "=" . $thing{$_} } sort keys %thing);
my %set = map { ($_ => 1) } @text;
say join(",", sort keys %set), "|", scalar(%set);

# A hash handed to a sub, and one given back.
sub total(@pairs) {
    my %h = @pairs;
    my $sum = 0;
    for my $k (sort keys %h) { $sum += $h{$k}; }
    return $sum;
}
sub defaults() { return (width => 80, height => 24, depth => 1, title => "none") }
my %config = (defaults(), height => 50, extra => 0);
say total(width => 1, height => 2, depth => 3, more => 4), "|", join(",", map { $_ . "=" . $config{$_} } sort keys %config);

# A hash, an array and a scalar of one name are three variables.
my %same = (a => 1, b => 2, c => 3, d => 4);
my @same = (10, 20);
my $same = "scalar";
say $same, $same[1], $same{b}, scalar(@same), scalar(%same);

# Emptied, and filled again.
%same = ();
say scalar(%same), %same ? "some" : "none";
%same = (x => 1, y => 2, x => 3, z => 4, w => 5);
say join(",", map { $_ . "=" . $same{$_} } sort keys %same);
my ($first, %rest) = ("head", p => 1, q => 2, r => 3, s => 4);
say $first, join(",", map { $_ . "=" . $rest{$_} } sort keys %rest);

# What follows exists, keys and values without brackets: a comparison may.
my %cmp = (a => 1, b => 2, c => 3, d => 4);
say exists $cmp{c} < 2 ? "lt" : "ge", (keys %cmp > 1) ? "many" : "few", (values %cmp != 0) ? "some" : "none", (keys %cmp <= 9) ? "le" : "gt";

# The value, then the key, then the store; and an operator makes the key
# first, &&= too, which then stores nothing.
my $ki = "a";
$cmp{$ki = "k"} = $ki x 1;
$cmp{$ki = "m"} = uc($ki . "v");
$cmp{nope} &&= 5;
my $anded = ($cmp{also} &&= 5);
say $ki, defined($anded) ? "defined" : "undef", "|", join(",", map { $_ . "=" . ($cmp{$_} // "undef") } sort keys %cmp);

# Elements as the targets of a list assignment: a swap, and keys made.
my %sw = (l => "left", r => "right", m => "mid", x => "other");
($sw{l}, $sw{r}) = ($sw{r}, $sw{l});
($sw{new1}, $sw{new2}, $sw{new3}) = (1, 2);
say join(",", map { $_ . "=" . ($sw{$_} // "undef") } sort keys %sw);

# A my in a loop is a new hash each time round.
for my $i (1 .. 3) {
    my %fresh;
    $fresh{$i} = $i;
    $fresh{"also"} = 1 if $i == 2;
    say scalar(%fresh), join(",", sort keys %fresh);
}

# keys are copies, so a delete after them in a list is no change to them.
my %kd = (a => 1, b => 2, c => 3, d => 4);
# (1542 has it without the sort, where the order is the language's own.)
my @kd = ((sort keys(%kd)), delete($kd{a}));
say "@kd|", scalar(%kd);
