# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a101 = (1, 2, 3);
$a101[0] = 'z';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
$a101[2] = 'l';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
$a101[3] = 'n';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
$a101[6] = 'far';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
$a101[(-1)] = 'm1';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
$a101[(-7)] = 'first';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
$a101[1.9] = 'frac';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
$a101['2'] = 'str';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
my @e101;
$e101[2] = 1;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @e101) {
        $dump_s .= (defined($e101[$dump_i]) ? (('<' . $e101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@e101) . ':') . $dump_s);
}
my @z101;
$z101[0] = (undef);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @z101) {
        $dump_s .= (defined($z101[$dump_i]) ? (('<' . $z101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@z101) . ':') . $dump_s);
}
my @a102 = (5, 'ab', 0, (undef));
$a102[0] += 2;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[0] -= 1;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[0] *= 3;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[0] /= 2;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[0] %= 5;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[0] **= 2;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[1] .= 'c';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[1] x= 2;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[2] ||= 'was false';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[2] ||= 'not now';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[2] &&= 'was true';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[3] //= 'was undef';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[3] //= 'not now';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[5] += 1;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[6] .= 's';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[7] -= 1;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[9] //= 'made';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[11] &&= 'not stored';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
$a102[12] ||= 'stored';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
say(++$a102[0]);
++$a102[14];
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
say($a102[0]++);
$a102[14]++;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
say(--$a102[0]);
--$a102[14];
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
say($a102[0]--);
$a102[14]--;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
my @a103 = (1, 2, 3);
my $i103 = 0;
$a103[$i103] = ($i103 = 2);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a103) {
        $dump_s .= (defined($a103[$dump_i]) ? (('<' . $a103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a103) . ':') . $dump_s);
}
say($i103);
@a103 = (1, 2, 3);
$i103 = 0;
$a103[$i103] += ($i103 = 2);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a103) {
        $dump_s .= (defined($a103[$dump_i]) ? (('<' . $a103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a103) . ':') . $dump_s);
}
@a103 = (1, 2, 3);
$i103 = 0;
$a103[$i103] .= ($i103 = 2);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a103) {
        $dump_s .= (defined($a103[$dump_i]) ? (('<' . $a103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a103) . ':') . $dump_s);
}
@a103 = (0, 2, 3);
$i103 = 0;
$a103[$i103] ||= ($i103 = 2);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a103) {
        $dump_s .= (defined($a103[$dump_i]) ? (('<' . $a103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a103) . ':') . $dump_s);
}
@a103 = (7, 7, 7);
$i103 = 0;
$a103[$i103++] = $i103;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a103) {
        $dump_s .= (defined($a103[$dump_i]) ? (('<' . $a103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a103) . ':') . $dump_s);
}
@a103 = (10, 20, 30);
$i103 = 0;
say($a103[$i103++] + $a103[$i103++]);
say($i103);
$i103 = 0;
$a103[$i103] = $a103[++$i103];
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a103) {
        $dump_s .= (defined($a103[$dump_i]) ? (('<' . $a103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a103) . ':') . $dump_s);
}
$i103 = 1;
$a103[$i103] = ($a103[$i103 - 1] + $a103[$i103]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a103) {
        $dump_s .= (defined($a103[$dump_i]) ? (('<' . $a103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a103) . ':') . $dump_s);
}
$a103[0] = $a103[2];
$a103[@a103] = 'at the count';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a103) {
        $dump_s .= (defined($a103[$dump_i]) ? (('<' . $a103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a103) . ':') . $dump_s);
}
my $v103 = $a103[1] = 'value of a store';
say($v103);
my $w103 = $a103[0] += 5;
say($w103);
