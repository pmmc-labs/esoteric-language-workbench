# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub none301() {
    return;
}
sub empty301() {
}
my $none301301 = none301();
say(defined($none301301) ? (('[' . $none301301) . ']') : 'undef');
$none301301 = none301();
say(defined($none301301) ? (('[' . $none301301) . ']') : 'undef');
say(defined(none301()) ? 'defined' : 'undef');
say(none301() ? 'true' : 'false');
say(none301() // 'left is scalar');
say(none301() || 'left is scalar');
if (none301()) {
    say('yes');
} else {
    say('no');
}
say('unless') unless none301();
say(!none301());
none301();
none301() if 1;
for ($none301301 = none301(); !defined($none301301); $none301301 = 1) {
    say('for');
}
my $empty301301 = empty301();
say(defined($empty301301) ? (('[' . $empty301301) . ']') : 'undef');
$empty301301 = empty301();
say(defined($empty301301) ? (('[' . $empty301301) . ']') : 'undef');
say(defined(empty301()) ? 'defined' : 'undef');
say(empty301() ? 'true' : 'false');
say(empty301() // 'left is scalar');
say(empty301() || 'left is scalar');
if (empty301()) {
    say('yes');
} else {
    say('no');
}
say('unless') unless empty301();
say(!empty301());
empty301();
empty301() if 1;
for ($empty301301 = empty301(); !defined($empty301301); $empty301301 = 1) {
    say('for');
}
sub none302() {
    return;
}
sub ret302() {
    return none302();
}
sub last302() {
    none302();
}
sub tern302($p) {
    return $p ? none302() : 5;
}
sub or302() {
    return 0 || none302();
}
sub and302() {
    return 1 && none302();
}
sub dor302() {
    return (undef) // none302();
}
sub plus302() {
    return +none302();
}
sub two302() {
    return ret302();
}
my $v302;
$v302 = ret302();
say(defined($v302) ? (('[' . $v302) . ']') : 'undef');
ret302();
$v302 = last302();
say(defined($v302) ? (('[' . $v302) . ']') : 'undef');
last302();
$v302 = tern302(1);
say(defined($v302) ? (('[' . $v302) . ']') : 'undef');
tern302(1);
$v302 = tern302(0);
say(defined($v302) ? (('[' . $v302) . ']') : 'undef');
tern302(0);
$v302 = or302();
say(defined($v302) ? (('[' . $v302) . ']') : 'undef');
or302();
$v302 = and302();
say(defined($v302) ? (('[' . $v302) . ']') : 'undef');
and302();
$v302 = dor302();
say(defined($v302) ? (('[' . $v302) . ']') : 'undef');
dor302();
$v302 = plus302();
say(defined($v302) ? (('[' . $v302) . ']') : 'undef');
plus302();
$v302 = two302();
say(defined($v302) ? (('[' . $v302) . ']') : 'undef');
two302();
sub if303($p) {
    if ($p) {
        say('if');
    }
}
sub else303($p) {
    if ($p) {
        say('if');
    } else {
        say('else');
    }
}
sub unless303($p) {
    unless ($p) {
        say('unless');
    }
}
sub while303($p) {
    my $i = 0;
    while ($i < $p) {
        $i++;
    }
}
sub for303($p) {
    for (my $i = 0; $i < $p; $i++) {
        say($i);
    }
}
sub block303($p) {
    {
        say('block');
    }
}
sub mod303($p) {
    say('mod') if $p;
}
sub retif303($p) {
    return 1 if $p;
}
sub setif303($p) {
    my $x = 0;
    $x = 7 unless $p;
}
sub tail303($p) {
    if303($p);
}
if303(1);
if303(0);
if303(2) if 1;
else303(1);
else303(0);
else303(2) if 1;
unless303(1);
unless303(0);
unless303(2) if 1;
while303(1);
while303(0);
while303(2) if 1;
for303(1);
for303(0);
for303(2) if 1;
block303(1);
block303(0);
block303(2) if 1;
mod303(1);
mod303(0);
mod303(2) if 1;
retif303(1);
retif303(0);
retif303(2) if 1;
setif303(1);
setif303(0);
setif303(2) if 1;
tail303(1);
tail303(0);
tail303(2) if 1;
my $k303 = 0;
for ($k303 = 0; $k303 < 2; $k303++) {
    if303($k303);
}
for (if303(1), $k303 = 0; $k303 < 2; mod303($k303), $k303++) {
    say($k303);
}
mod303(1) while ($k303++) < 4;
say(retif303(1));
sub none304() {
    return;
}
sub empty304() {
}
sub show304($p = 'default', $q = 'second') {
    return ((defined($p) ? (('[' . $p) . ']') : 'undef') . ' ') . (defined($q) ? (('[' . $q) . ']') : 'undef');
}
sub tail304($p) {
    return $p || (+none304());
}
say(none304());
say(empty304());
say(show304(none304()));
say(show304(empty304()));
say(show304(none304(), 1));
say(show304(1, none304()));
say(show304(1 ? empty304() : 0));
say(show304(0 ? empty304() : 0));
say(show304(tail304(0)));
say(show304(tail304(4)));
say(show304(!none304()));
say(show304(none304() // 'scalar'));
say(tail304(0));
sub decl305() {
    my $x;
}
sub undef305() {
    return (undef);
}
sub show305($p = 'default') {
    return defined($p) ? (('[' . $p) . ']') : 'undef';
}
say(show305(decl305()));
say(show305(undef305()));
say(show305());
