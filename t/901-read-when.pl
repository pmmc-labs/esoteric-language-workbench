# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my $x101 = 1;
sub set101() {
    $x101 = 9;
    return 0;
}
sub show101($p, $q) {
    return ($p . ',') . $q;
}
$x101 = 1;
say(show101($x101, set101()));
say($x101);
$x101 = 1;
say(show101($x101 + 0, set101()));
say($x101);
$x101 = 1;
say(show101(+$x101, set101()));
say($x101);
$x101 = 1;
say(show101($x101 = 4, set101()));
say($x101);
$x101 = 1;
say(show101($x101 += 4, set101()));
say($x101);
$x101 = 1;
say(show101(++$x101, set101()));
say($x101);
$x101 = 1;
say(show101($x101++, set101()));
say($x101);
$x101 = 1;
say(show101(-$x101, set101()));
say($x101);
$x101 = 1;
say(show101(1 ? $x101 : 0, set101()));
say($x101);
$x101 = 1;
say(show101($x101 || 0, set101()));
say($x101);
$x101 = 1;
say(show101($x101 && $x101, set101()));
say($x101);
$x101 = 1;
say(show101($x101 // 0, set101()));
say($x101);
$x101 = 1;
say(show101($x101 x 2, set101()));
say($x101);
$x101 = 1;
say(show101(length($x101), set101()));
say($x101);
$x101 = 1;
say(show101($x101, $x101++));
$x101 = 1;
say(show101($x101, $x101 = 5));
$x101 = 1;
say(show101($x101++, $x101));
$x101 = 1;
say(show101(set101(), $x101));
my $t102 = 5;
sub step102() {
    $t102 += 100;
    return 1;
}
sub get102() {
    return $t102;
}
sub last102() {
    $t102;
}
sub tern102() {
    return 1 ? $t102 : 0;
}
sub or102() {
    return $t102 || 0;
}
sub show102($p, $q) {
    return $p;
}
say($t102 + step102());
$t102 = 5;
say(get102() + step102());
$t102 = 5;
say(last102() + step102());
$t102 = 5;
say(tern102() + step102());
$t102 = 5;
say(or102() + step102());
$t102 = 5;
say(show102(get102(), step102()));
$t102 = 5;
say(show102($t102, step102()));
my $v103 = 1;
sub bump103() {
    $v103 = 9;
    return 5;
}
sub dd103($p //= bump103(), $q = 0) {
    return ($p . ',') . $q;
}
sub oo103($p ||= bump103(), $q = 0) {
    return ($p . ',') . $q;
}
sub three103($p, $q //= bump103(), $r = 0) {
    return ((($p . ',') . $q) . ',') . $r;
}
say(dd103((undef), $v103));
$v103 = 1;
say(dd103(3, $v103));
$v103 = 1;
say(oo103(0, $v103));
$v103 = 1;
say(dd103((undef), $v103 + 0));
$v103 = 1;
say(three103($v103, (undef), $v103));
$v103 = 1;
say(three103($v103, 2, $v103));
my $n104 = 0;
my $log104 = "";
sub a104($p) {
    $n104 += $p;
    return b104($p + 1);
}
sub b104($p) {
    $n104 += $p;
    $log104 .= 'b';
    return c104($p + 1);
}
sub c104($p) {
    $n104 += $p;
    $log104 .= 'c';
    return $n104;
}
say(a104(1));
say($n104);
say(a104(10));
say($log104);
bump105();
my $x105;
say(defined($x105) ? (('[' . $x105) . ']') : 'undef');
bump105();
bump105();
my $y105 += 10;
say(defined($y105) ? (('[' . $y105) . ']') : 'undef');
tag105();
my $s105 .= 'a';
say(defined($s105) ? (('[' . $s105) . ']') : 'undef');
one105();
my $d105 //= 10;
say(defined($d105) ? (('[' . $d105) . ']') : 'undef');
my $e105 //= 10;
say(defined($e105) ? (('[' . $e105) . ']') : 'undef');
my $z105 = setz105();
say(defined($z105) ? (('[' . $z105) . ']') : 'undef');
sub bump105() {
    $x105++;
    $y105++;
}
sub tag105() {
    $s105 = 'q';
}
sub one105() {
    $d105 = 1;
}
sub setz105() {
    $z105 = 7;
    return 8;
}
my $x106 = 1;
sub set106($p) {
    $x106 = $p;
    return 3;
}
$x106 = set106(50);
say($x106);
$x106 += set106(50);
say($x106);
$x106 ||= set106(0);
say($x106);
$x106 = 2;
say($x106 * set106(10));
$x106 = 2;
say(set106(10) * $x106);
$x106 = 2;
say($x106 < set106(10));
