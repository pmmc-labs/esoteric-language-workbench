# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
{
    my $v = (undef);
    my $r = $v += 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v += 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v += (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v += 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v += 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v += '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v += 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v += 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v += (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v += 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v += '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v += 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v += 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v += (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v += 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v += 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v += '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v += 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v += 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v += (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v += 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v += '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v += 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v += (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v += 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v += 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v += 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v += (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v += 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v += 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v += '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v += 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v += 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v += (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v += 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v += '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v += 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v += 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v += 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v += 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v += '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v += 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v += 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v += (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v += 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v += '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v += 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v += 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v += (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v += 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v += '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v -= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v -= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v -= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v -= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v -= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v -= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v -= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v -= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v -= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v -= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v -= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v -= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v -= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v -= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v -= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v -= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v -= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v -= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v -= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v -= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v -= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v -= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v -= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v -= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v -= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v -= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v -= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v -= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v -= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v -= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v -= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v -= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v -= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v -= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v -= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v -= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v -= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v -= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v -= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v -= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v -= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v -= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v -= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v -= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v -= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v -= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v -= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v -= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v -= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v -= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v -= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v -= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v -= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v -= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v -= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v *= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v *= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v *= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v *= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v *= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v *= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v *= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v *= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v *= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v *= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v *= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v *= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v *= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v *= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v *= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v *= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v *= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v *= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v *= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v *= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v *= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v *= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v *= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v *= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v *= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v *= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v *= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v *= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v *= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v *= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v *= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v *= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v *= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v *= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v *= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v *= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v *= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v *= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v *= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v *= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v *= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v *= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v *= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v *= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v *= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v *= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v *= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v /= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v /= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v /= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v /= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v /= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v /= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v /= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v /= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v /= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v /= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v /= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v /= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v /= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v /= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v /= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v /= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v /= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v /= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v /= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v /= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v /= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v /= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v /= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v /= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v /= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v /= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v /= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v /= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v /= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v /= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v /= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v /= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v /= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v /= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v /= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v /= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v /= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v /= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v /= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v /= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v /= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v /= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v %= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v %= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v %= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v %= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v %= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v %= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v %= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v %= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v %= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v %= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v %= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v %= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v %= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v %= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v %= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v %= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v %= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v %= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v %= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v %= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v %= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v %= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v %= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v %= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v %= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v %= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v %= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v %= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v %= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v %= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v %= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v %= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v %= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v %= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v %= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v %= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v **= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v **= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v **= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v **= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v **= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v **= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v **= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v **= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v **= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v **= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v **= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v **= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v **= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v **= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v **= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v **= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v **= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v **= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v **= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v **= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v **= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v **= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v **= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v **= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v **= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v **= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v **= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v **= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v **= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v **= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v **= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v **= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v **= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v **= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v **= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v **= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v **= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v **= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v **= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v **= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v **= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v **= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v **= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v **= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v **= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v **= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v .= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v .= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v .= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v .= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v .= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v .= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v .= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v .= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v .= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v .= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v .= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v .= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v .= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v .= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v .= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v .= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v .= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v .= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v .= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v .= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v .= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v .= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v .= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v .= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v .= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v .= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v .= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v .= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v .= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v .= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v .= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v .= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v .= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v .= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v .= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v .= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v .= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v .= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v .= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v .= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v .= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v .= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v .= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v .= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v .= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v .= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v .= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v .= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v .= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v .= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v .= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v .= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v .= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v .= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v .= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v .= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v .= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v .= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v .= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v .= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v .= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v .= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v .= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v .= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v .= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v .= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v .= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v .= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v .= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v .= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v .= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v .= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v .= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v .= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v .= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v .= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v .= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v .= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v .= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v .= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v .= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v .= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v .= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v .= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v x= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v x= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v x= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v x= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v x= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v x= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v x= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v x= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v x= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v x= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v x= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v x= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v x= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v x= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v x= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v x= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v x= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v x= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v x= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v x= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v x= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v x= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v x= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v x= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v x= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v x= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v x= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v x= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v x= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v x= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v x= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v x= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v x= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v x= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v x= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v x= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v x= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v x= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v x= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v x= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v x= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v x= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v x= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v x= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v x= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v ||= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v ||= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v ||= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v ||= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v ||= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v ||= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v ||= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v ||= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v ||= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v ||= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v ||= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v ||= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v ||= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v ||= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v ||= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v ||= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v ||= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v ||= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v ||= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v ||= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v ||= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v ||= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v ||= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v ||= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v ||= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v ||= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v ||= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v ||= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v ||= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v ||= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v ||= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v ||= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v ||= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v ||= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v ||= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v ||= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v ||= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v ||= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v ||= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v ||= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v ||= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v ||= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v ||= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v ||= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v ||= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v ||= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v ||= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v ||= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v ||= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v ||= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v ||= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v ||= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v ||= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v ||= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v ||= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v ||= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v ||= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v ||= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v ||= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v ||= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v ||= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v ||= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v ||= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v ||= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v ||= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v ||= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v ||= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v ||= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v ||= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v ||= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v ||= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v ||= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v ||= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v ||= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v ||= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v ||= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v ||= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v ||= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v ||= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v ||= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v ||= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v ||= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v ||= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v ||= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v ||= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v ||= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v ||= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v ||= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v ||= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v ||= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v ||= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v ||= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v ||= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v ||= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v ||= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v ||= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v &&= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v &&= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v &&= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v &&= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v &&= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v &&= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v &&= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v &&= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v &&= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v &&= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v &&= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v &&= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v &&= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v &&= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v &&= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v &&= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v &&= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v &&= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v &&= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v &&= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v &&= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v &&= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v &&= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v &&= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v &&= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v &&= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v &&= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v &&= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v &&= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v &&= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v &&= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v &&= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v &&= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v &&= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v &&= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v &&= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v &&= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v &&= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v &&= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v &&= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v &&= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v &&= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v &&= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v &&= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v &&= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v &&= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v &&= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v &&= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v &&= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v &&= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v &&= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v &&= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v &&= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v &&= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v &&= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v &&= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v &&= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v &&= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v &&= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v &&= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v &&= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v &&= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v &&= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v &&= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v &&= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v &&= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v &&= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v &&= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v &&= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v &&= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v &&= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v &&= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v &&= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v &&= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v &&= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v &&= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v &&= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v &&= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v &&= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v &&= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v &&= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v &&= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v &&= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v &&= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v &&= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v &&= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v &&= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v &&= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v &&= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v &&= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v &&= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v &&= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v &&= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v &&= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v &&= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v &&= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v //= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v //= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v //= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v //= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v //= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v //= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v //= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    my $r = $v //= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v //= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v //= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v //= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v //= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v //= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v //= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v //= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = true;
    my $r = $v //= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v //= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v //= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v //= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v //= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v //= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v //= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v //= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0;
    my $r = $v //= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v //= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v //= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v //= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v //= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v //= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v //= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v //= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 5;
    my $r = $v //= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v //= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v //= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v //= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v //= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v //= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v //= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v //= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    my $r = $v //= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v //= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v //= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v //= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v //= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v //= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v //= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v //= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 0.5;
    my $r = $v //= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v //= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v //= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v //= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v //= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v //= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v //= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v //= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 3.0;
    my $r = $v //= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v //= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v //= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v //= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v //= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v //= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v //= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v //= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    my $r = $v //= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v //= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v //= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v //= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v //= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v //= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v //= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v //= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = "";
    my $r = $v //= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v //= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v //= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v //= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v //= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v //= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v //= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v //= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '12';
    my $r = $v //= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v //= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v //= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v //= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v //= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v //= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v //= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v //= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = '3.0';
    my $r = $v //= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v //= 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v //= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v //= (-1);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v //= 0.5;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v //= 9223372036854775807;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v //= '3.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v //= 'x';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = 'ab';
    my $r = $v //= (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($r) ? (('[' . $r) . ']') : 'undef');
}
{
    my $v = (undef);
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = true;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = false;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1);
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9223372036854775806;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807);
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807 - 1);
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740991;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740992);
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.0;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.5;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.5);
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3.0;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1.0);
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740990.0;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740991.0;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740991.0);
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740990.0);
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1e+16;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1e+16);
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1e+300;
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-12';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = ' 12 ';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '09';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '009';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '00';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0.0';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '3.0';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-0.5';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '.5';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e-3';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '9007199254740990';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '9007199254740991';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '9007199254740992';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-9007199254740992';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '999999999999999';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (undef);
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = true;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = false;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1);
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9223372036854775806;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807);
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740991;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740992);
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.0;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.5;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.5);
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3.0;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1.0);
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740990.0;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740991.0;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740991.0);
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740992.0);
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740990.0);
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1e+16;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1e+16);
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1e+300;
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-12';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = ' 12 ';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '09';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '009';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '00';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0.0';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '3.0';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-0.5';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '.5';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e-3';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '9007199254740990';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '9007199254740991';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '9007199254740992';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-9007199254740992';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '9223372036854775807';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '999999999999999';
    $v -= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (undef);
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = true;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = false;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1);
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9223372036854775806;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807);
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807 - 1);
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740991;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740992);
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.0;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.5;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.5);
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3.0;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1.0);
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740992.0);
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1e+16;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1e+16);
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1e+300;
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-12';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = ' 12 ';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '09';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '009';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '00';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0.0';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '3.0';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-0.5';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '.5';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e-3';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '9007199254740990';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '9007199254740991';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '9007199254740992';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-9007199254740992';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '9223372036854775807';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '999999999999999';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = "";
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 'ab';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 'a9';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 'zz';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12abc';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0x10';
    $v .= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (undef);
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = true;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = false;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1);
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 41;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9223372036854775806;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9223372036854775807;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807);
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807 - 1);
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740991;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740992);
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.0;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.0);
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0.5;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-0.5);
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1.5;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3.0;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1.0);
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 999999999999998.0;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 9007199254740992.0;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9007199254740992.0);
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1e+16;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-1e+16);
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1e+300;
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-12';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = ' 12 ';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '+12';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '09';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '009';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '00';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0.0';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '3.0';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1.5';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-0.5';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '.5';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e3';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '1e-3';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '9007199254740990';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '9007199254740991';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '9007199254740992';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '-9007199254740992';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '9223372036854775807';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '999999999999999';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = "";
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 'ab';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 'a9';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 'zz';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '12abc';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '0x10';
    $v //= 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
