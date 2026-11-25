# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
{
    my $v = (undef);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = true;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = true;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = false;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = false;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = false;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = false;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1);
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1);
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9223372036854775806;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9223372036854775806;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807 - 1);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807 - 1);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740991;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740991;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740991;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740991;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740992);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740992);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740992);
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740992);
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.0;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.0;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.0;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.0;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.5);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.5);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.5);
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.5);
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1.0);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1.0);
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1.0);
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1.0);
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740990.0;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740991.0;
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740991.0);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740990.0);
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-12';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-12';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-12';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-12';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = ' 12 ';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = ' 12 ';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = ' 12 ';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = ' 12 ';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '09';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '09';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '009';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '009';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '00';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '00';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0.0';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0.0';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0.0';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0.0';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-0.5';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-0.5';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-0.5';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-0.5';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '.5';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '.5';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '.5';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '.5';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e-3';
    my $r = ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    ++$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e-3';
    my $r = $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e-3';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e-3';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '999999999999999';
    my $r = --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '999999999999999';
    my $r = $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
