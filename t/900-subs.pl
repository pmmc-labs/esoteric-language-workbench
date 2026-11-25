# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub id1($p) {
    return $p;
}
sub last1($p) {
    $p;
}
say(defined(id1(0)) ? (('[' . id1(0)) . ']') : 'undef');
say(defined(id1(1)) ? (('[' . id1(1)) . ']') : 'undef');
say(defined(id1((-7))) ? (('[' . id1((-7))) . ']') : 'undef');
say(defined(id1(41)) ? (('[' . id1(41)) . ']') : 'undef');
say(defined(id1(0.5)) ? (('[' . id1(0.5)) . ']') : 'undef');
say(defined(id1(3.0)) ? (('[' . id1(3.0)) . ']') : 'undef');
say(defined(id1("")) ? (('[' . id1("")) . ']') : 'undef');
say(defined(id1('0')) ? (('[' . id1('0')) . ']') : 'undef');
say(defined(id1('ab')) ? (('[' . id1('ab')) . ']') : 'undef');
say(defined(id1(' 3 ')) ? (('[' . id1(' 3 ')) . ']') : 'undef');
say(defined(id1('00')) ? (('[' . id1('00')) . ']') : 'undef');
say(defined(id1(true)) ? (('[' . id1(true)) . ']') : 'undef');
say(defined(id1(false)) ? (('[' . id1(false)) . ']') : 'undef');
say(defined(id1((undef))) ? (('[' . id1((undef))) . ']') : 'undef');
say(defined(last1(0)) ? (('[' . last1(0)) . ']') : 'undef');
say(defined(last1(1)) ? (('[' . last1(1)) . ']') : 'undef');
say(defined(last1((-7))) ? (('[' . last1((-7))) . ']') : 'undef');
say(defined(last1(41)) ? (('[' . last1(41)) . ']') : 'undef');
say(defined(last1(0.5)) ? (('[' . last1(0.5)) . ']') : 'undef');
say(defined(last1(3.0)) ? (('[' . last1(3.0)) . ']') : 'undef');
say(defined(last1("")) ? (('[' . last1("")) . ']') : 'undef');
say(defined(last1('0')) ? (('[' . last1('0')) . ']') : 'undef');
say(defined(last1('ab')) ? (('[' . last1('ab')) . ']') : 'undef');
say(defined(last1(' 3 ')) ? (('[' . last1(' 3 ')) . ']') : 'undef');
say(defined(last1('00')) ? (('[' . last1('00')) . ']') : 'undef');
say(defined(last1(true)) ? (('[' . last1(true)) . ']') : 'undef');
say(defined(last1(false)) ? (('[' . last1(false)) . ']') : 'undef');
say(defined(last1((undef))) ? (('[' . last1((undef))) . ']') : 'undef');
sub d2($p = 'dflt') {
    return $p;
}
say(defined(d2()) ? (('[' . d2()) . ']') : 'undef');
say(defined(d2(0)) ? (('[' . d2(0)) . ']') : 'undef');
say(defined(d2(1)) ? (('[' . d2(1)) . ']') : 'undef');
say(defined(d2((-7))) ? (('[' . d2((-7))) . ']') : 'undef');
say(defined(d2(41)) ? (('[' . d2(41)) . ']') : 'undef');
say(defined(d2(0.5)) ? (('[' . d2(0.5)) . ']') : 'undef');
say(defined(d2(3.0)) ? (('[' . d2(3.0)) . ']') : 'undef');
say(defined(d2("")) ? (('[' . d2("")) . ']') : 'undef');
say(defined(d2('0')) ? (('[' . d2('0')) . ']') : 'undef');
say(defined(d2('ab')) ? (('[' . d2('ab')) . ']') : 'undef');
say(defined(d2(' 3 ')) ? (('[' . d2(' 3 ')) . ']') : 'undef');
say(defined(d2('00')) ? (('[' . d2('00')) . ']') : 'undef');
say(defined(d2(true)) ? (('[' . d2(true)) . ']') : 'undef');
say(defined(d2(false)) ? (('[' . d2(false)) . ']') : 'undef');
say(defined(d2((undef))) ? (('[' . d2((undef))) . ']') : 'undef');
sub d3($p //= 'dflt') {
    return $p;
}
say(defined(d3()) ? (('[' . d3()) . ']') : 'undef');
say(defined(d3(0)) ? (('[' . d3(0)) . ']') : 'undef');
say(defined(d3(1)) ? (('[' . d3(1)) . ']') : 'undef');
say(defined(d3((-7))) ? (('[' . d3((-7))) . ']') : 'undef');
say(defined(d3(41)) ? (('[' . d3(41)) . ']') : 'undef');
say(defined(d3(0.5)) ? (('[' . d3(0.5)) . ']') : 'undef');
say(defined(d3(3.0)) ? (('[' . d3(3.0)) . ']') : 'undef');
say(defined(d3("")) ? (('[' . d3("")) . ']') : 'undef');
say(defined(d3('0')) ? (('[' . d3('0')) . ']') : 'undef');
say(defined(d3('ab')) ? (('[' . d3('ab')) . ']') : 'undef');
say(defined(d3(' 3 ')) ? (('[' . d3(' 3 ')) . ']') : 'undef');
say(defined(d3('00')) ? (('[' . d3('00')) . ']') : 'undef');
say(defined(d3(true)) ? (('[' . d3(true)) . ']') : 'undef');
say(defined(d3(false)) ? (('[' . d3(false)) . ']') : 'undef');
say(defined(d3((undef))) ? (('[' . d3((undef))) . ']') : 'undef');
sub d4($p ||= 'dflt') {
    return $p;
}
say(defined(d4()) ? (('[' . d4()) . ']') : 'undef');
say(defined(d4(0)) ? (('[' . d4(0)) . ']') : 'undef');
say(defined(d4(1)) ? (('[' . d4(1)) . ']') : 'undef');
say(defined(d4((-7))) ? (('[' . d4((-7))) . ']') : 'undef');
say(defined(d4(41)) ? (('[' . d4(41)) . ']') : 'undef');
say(defined(d4(0.5)) ? (('[' . d4(0.5)) . ']') : 'undef');
say(defined(d4(3.0)) ? (('[' . d4(3.0)) . ']') : 'undef');
say(defined(d4("")) ? (('[' . d4("")) . ']') : 'undef');
say(defined(d4('0')) ? (('[' . d4('0')) . ']') : 'undef');
say(defined(d4('ab')) ? (('[' . d4('ab')) . ']') : 'undef');
say(defined(d4(' 3 ')) ? (('[' . d4(' 3 ')) . ']') : 'undef');
say(defined(d4('00')) ? (('[' . d4('00')) . ']') : 'undef');
say(defined(d4(true)) ? (('[' . d4(true)) . ']') : 'undef');
say(defined(d4(false)) ? (('[' . d4(false)) . ']') : 'undef');
say(defined(d4((undef))) ? (('[' . d4((undef))) . ']') : 'undef');
my $n5 = 10;
sub two5($p, $q = 2) {
    return ($p . ',') . $q;
}
sub twice5($p, $q = $p * 2) {
    return ($p . ',') . $q;
}
sub file5($p = $n5) {
    return $p;
}
sub one5() {
    return 1;
}
sub viasub5($p = one5() + 1) {
    return $p;
}
say(two5(1));
say(two5(1, 5));
say(twice5(4));
say(twice5(4, 1));
say(file5());
$n5 = 11;
say(file5());
say(file5(3));
say(viasub5());
say(viasub5(9));
my $n6 = 0;
sub count6($p = $n6++) {
    return $p;
}
say(count6());
say(count6(9));
say(count6());
say($n6);
my $n7 = 0;
sub skip7($, $q) {
    return $q;
}
sub maybe7($ = $n7++, $q = 6) {
    return $q;
}
say(skip7(1, 2));
say(maybe7());
say(maybe7(1));
say(maybe7(1, 2));
say($n7);
my $p = 3;
my $q = 10;
sub own8($p = $p) {
    $p += 1;
    return $p;
}
sub later8($r = $q, $q = 2) {
    return ($r . ' ') . $q;
}
say(own8());
say(own8(7));
say($p);
say(later8());
say(later8(1, 5));
my $v9 = 4;
sub work9($p) {
    $p = ($p * 2);
    $p++;
    $p .= '!';
    return $p;
}
say(work9($v9));
say($v9);
my $n10 = 3;
sub assign10($p) {
    $p += 5;
}
sub after10() {
    $n10++;
}
sub before10() {
    ++$n10;
}
sub down10() {
    $n10--;
}
sub decl10() {
    my $x = 5;
}
sub alone10($p) {
    $p * 2;
}
sub const10() {
    42;
}
sub str10() {
    's';
}
sub tern10($p) {
    $p ? 'yes' : 'no';
}
sub call10($p) {
    alone10($p);
}
sub says10() {
    say('said');
}
say(assign10(1));
say(after10());
say(before10());
say(down10());
say($n10);
say(decl10());
say(alone10(4));
say(const10());
say(str10());
say(tern10(1));
say(tern10(0));
say(call10(5));
my $r10 = says10();
say($r10);
say(says10() + 1);
sub sign11($p) {
    return 'neg' if $p < 0;
    return 'zero' unless $p;
    return 'pos';
    say('never');
}
sub early11($p) {
    if ($p) {
        say('in');
        return 'a';
    } else {
        return 'b';
    }
    say('never');
}
say(sign11((-3)));
say(sign11(0));
say(sign11(8));
say(early11(1));
say(early11(0));
sub fresh12($p) {
    my $x;
    say(defined($x) ? 'kept' : 'new');
    $x = $p;
    return $x;
}
say(fresh12(1));
say(fresh12(2));
sub inc13($p) {
    return $p + 1;
}
sub dbl13($p) {
    return $p * 2;
}
say(inc13(1) + dbl13(2));
say(inc13(dbl13(inc13(1))));
say(-inc13(5));
say(!inc13((-1)));
say('ab' x inc13(1));
say(length(dbl13(50)));
say(substr('abcdef', inc13(0), dbl13(1)));
if (inc13(1) > 1) {
    say('more');
} else {
    say('less');
}
say('mod') if inc13(0);
my $i13 = 0;
while (inc13($i13) < 4) {
    say($i13);
    $i13 = inc13($i13);
}
for (my $j = inc13(0); $j < dbl13(2); $j = inc13($j)) {
    say($j);
}
say(inc13((-1)) ? dbl13(1) : dbl13(2));
say(inc13((-1)) || dbl13(4));
say(inc13(1) && dbl13(4));
say(inc13(1) // dbl13(4));
