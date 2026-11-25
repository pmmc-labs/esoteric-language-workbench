# model: t/models/ret.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a101 = (5, 6);
my @e101;
sub all101(@rest) {
    return join('|', scalar(@rest), join(',', @rest));
}
sub one101($p, @rest) {
    return join('|', $p, scalar(@rest), join(',', @rest));
}
sub def101($p, $q = 'dq', @rest) {
    return join('|', $p, $q, scalar(@rest), join(',', @rest));
}
sub dor101($p //= 'dp', @rest) {
    return join('|', $p, scalar(@rest), join(',', @rest));
}
sub bare101($p, @) {
    return $p;
}
sub skip101($, @rest) {
    return join('|', scalar(@rest), join(',', @rest));
}
sub only101(@) {
    return 'only';
}
say(all101());
say(all101(1));
say(all101(1, 2, 3));
say(all101(@a101, @a101));
say(all101(@e101));
say(all101((), 0, false, ""));
say(all101((1 .. 5)));
say(all101(reverse(@a101)));
say(one101(1));
say(one101(1, 2));
say(one101(@a101));
say(one101(@a101, @a101));
say(def101(1));
say(def101(1, 2));
say(def101(1, 2, 3, 4));
say(def101(@a101, @a101));
say(dor101());
say(dor101((undef), 8, 9));
say(dor101(0, 8));
say(bare101(1));
say(bare101(1, 2, 3));
say(skip101(1));
say(skip101(1, 2));
say(only101());
say(only101(@a101, 1));
my @a102 = (1, 2, 3);
my @r102;
sub change102(@v) {
    $v[0] = 'changed';
    push(@v, 'more');
    return @v;
}
sub same102(@v) {
    return @v;
}
sub on102($p, @v) {
    return same102(@v, $p);
}
sub twice102(@v) {
    return (@v, @v);
}
sub sum102(@v) {
    my $t = 0;
    for my $n (@v) {
        $t += $n;
    }
    return $t;
}
sub deep102($p, @v) {
    return @v if $p == 0;
    return deep102(($p - 1), @v, $p);
}
@r102 = (change102(@a102));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r102) {
        $dump_s .= (defined($r102[$dump_i]) ? (('<' . $r102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r102) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
@r102 = (on102(@a102));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r102) {
        $dump_s .= (defined($r102[$dump_i]) ? (('<' . $r102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r102) . ':') . $dump_s);
}
@r102 = (twice102(twice102(7)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r102) {
        $dump_s .= (defined($r102[$dump_i]) ? (('<' . $r102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r102) . ':') . $dump_s);
}
say(sum102(@a102, 10, twice102(100)));
say(sum102());
@r102 = (deep102(4, 'x'));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r102) {
        $dump_s .= (defined($r102[$dump_i]) ? (('<' . $r102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r102) . ':') . $dump_s);
}
my $v103 = 5;
sub bump103() {
    $v103 = 9;
    return 5;
}
sub rest103($p, @rest) {
    return join('|', $p, @rest);
}
sub dflt103($p, $q //= bump103(), @rest) {
    return join('|', $p, $q, @rest);
}
say(rest103(1, $v103, bump103()));
$v103 = 5;
say(dflt103(1, (undef), $v103));
$v103 = 5;
say(dflt103(1, 2, $v103));
