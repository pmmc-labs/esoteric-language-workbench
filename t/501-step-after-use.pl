# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
{
    my $v = (undef);
    my $t = length($v);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (undef);
    my $t = !$v;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (undef);
    my $t = length($v);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (undef);
    my $t = !$v;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (undef);
    my $t = length($v);
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (undef);
    my $t = !$v;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (undef);
    my $t = length($v);
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (undef);
    my $t = !$v;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v . "";
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v * 1.5;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v == 1;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v x 1;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v . "";
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v * 1.5;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v == 1;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v x 1;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v . "";
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v * 1.5;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v == 1;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v x 1;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v . "";
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v * 1.5;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v == 1;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $t = $v x 1;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = $v > 0.5;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = $v % 7;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = $v eq 'a';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = defined($v);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = $v > 0.5;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = $v % 7;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = $v eq 'a';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = defined($v);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = $v > 0.5;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = $v % 7;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = $v eq 'a';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = defined($v);
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = $v > 0.5;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = $v % 7;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = $v eq 'a';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $t = defined($v);
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807);
    my $t = $v + 0;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807);
    my $t = -$v;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807);
    my $t = length($v);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807);
    my $t = !$v;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807);
    my $t = $v + 0;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807);
    my $t = -$v;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807);
    my $t = length($v);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807);
    my $t = !$v;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v . "";
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v * 1.5;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v == 1;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v x 1;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v . "";
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v * 1.5;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v == 1;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v x 1;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v . "";
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v * 1.5;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v == 1;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v x 1;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v . "";
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v * 1.5;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v == 1;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $t = $v x 1;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = $v > 0.5;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = $v % 7;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = $v eq 'a';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = defined($v);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = $v > 0.5;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = $v % 7;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = $v eq 'a';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = defined($v);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = $v > 0.5;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = $v % 7;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = $v eq 'a';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = defined($v);
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = $v > 0.5;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = $v % 7;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = $v eq 'a';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $t = defined($v);
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = $v + 0;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = -$v;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = length($v);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = !$v;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = $v + 0;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = -$v;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = length($v);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = !$v;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = $v + 0;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = -$v;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = length($v);
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = !$v;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = $v + 0;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = -$v;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = length($v);
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $t = !$v;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v . "";
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v * 1.5;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v == 1;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v x 1;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v . "";
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v * 1.5;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v == 1;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v x 1;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v . "";
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v * 1.5;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v == 1;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v x 1;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v . "";
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v * 1.5;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v == 1;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $t = $v x 1;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740990.0);
    my $t = $v + 0;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740990.0);
    my $t = -$v;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740990.0);
    my $t = !$v;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = $v > 0.5;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = $v % 7;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = $v eq 'a';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = defined($v);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = $v > 0.5;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = $v % 7;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = $v eq 'a';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = defined($v);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = $v > 0.5;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = $v % 7;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = $v eq 'a';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = defined($v);
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = $v > 0.5;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = $v % 7;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = $v eq 'a';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $t = defined($v);
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $t = $v + 0;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $t = length($v);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $t = !$v;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $t = $v + 0;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $t = length($v);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $t = !$v;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $t = $v + 0;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $t = length($v);
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $t = !$v;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $t = $v + 0;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $t = length($v);
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $t = !$v;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '00';
    my $t = $v . "";
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '00';
    my $t = $v * 1.5;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '00';
    my $t = $v == 1;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '00';
    my $t = $v x 1;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '00';
    my $t = $v . "";
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '00';
    my $t = $v * 1.5;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '00';
    my $t = $v == 1;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '00';
    my $t = $v x 1;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = $v > 0.5;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = $v % 7;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = $v eq 'a';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = defined($v);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = $v > 0.5;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = $v % 7;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = $v eq 'a';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = defined($v);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = $v > 0.5;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = $v % 7;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = $v eq 'a';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = defined($v);
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = $v > 0.5;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = $v % 7;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = $v eq 'a';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $t = defined($v);
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = $v + 0;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = -$v;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = length($v);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = !$v;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = $v + 0;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = -$v;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = length($v);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = !$v;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = $v + 0;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = -$v;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = length($v);
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = !$v;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = $v + 0;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = -$v;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = length($v);
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $t = !$v;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
