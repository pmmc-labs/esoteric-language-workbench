# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a700;
{
    @a700 = (0, 1);
    my $v = $a700[0];
    my $w = $a700[1];
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    push(@a700, 0, 1);
    $w = pop(@a700);
    $v = pop(@a700);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    ($v, $w) = (@a700[0, 1]);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
}
{
    @a700 = (0.5, 9007199254740992);
    my $v = $a700[0];
    my $w = $a700[1];
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    push(@a700, 0.5, 9007199254740992);
    $w = pop(@a700);
    $v = pop(@a700);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    ($v, $w) = (@a700[0, 1]);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
}
{
    @a700 = ('12', ' 3 ');
    my $v = $a700[0];
    my $w = $a700[1];
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    push(@a700, '12', ' 3 ');
    $w = pop(@a700);
    $v = pop(@a700);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    ($v, $w) = (@a700[0, 1]);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
}
{
    @a700 = (true, 0);
    my $v = $a700[0];
    my $w = $a700[1];
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    push(@a700, true, 0);
    $w = pop(@a700);
    $v = pop(@a700);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    ($v, $w) = (@a700[0, 1]);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
}
{
    @a700 = ((-7), false);
    my $v = $a700[0];
    my $w = $a700[1];
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    push(@a700, (-7), false);
    $w = pop(@a700);
    $v = pop(@a700);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    ($v, $w) = (@a700[0, 1]);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
}
{
    @a700 = (3.0, 0);
    my $v = $a700[0];
    my $w = $a700[1];
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    push(@a700, 3.0, 0);
    $w = pop(@a700);
    $v = pop(@a700);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    ($v, $w) = (@a700[0, 1]);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
}
{
    @a700 = (true, 9007199254740992);
    my $v = $a700[0];
    my $w = $a700[1];
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    push(@a700, true, 9007199254740992);
    $w = pop(@a700);
    $v = pop(@a700);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    ($v, $w) = (@a700[0, 1]);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
}
{
    @a700 = ((-7), 9007199254740992);
    my $v = $a700[0];
    my $w = $a700[1];
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    push(@a700, (-7), 9007199254740992);
    $w = pop(@a700);
    $v = pop(@a700);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
    ($v, $w) = (@a700[0, 1]);
    say(defined($v + $w) ? (('[' . ($v + $w)) . ']') : 'undef');
}
my @a701;
{
    @a701 = (0, 1);
    my $v = $a701[0];
    my $w = $a701[1];
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    push(@a701, 0, 1);
    $w = pop(@a701);
    $v = pop(@a701);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    ($v, $w) = (@a701[0, 1]);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
}
{
    @a701 = (0.5, 9007199254740992);
    my $v = $a701[0];
    my $w = $a701[1];
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    push(@a701, 0.5, 9007199254740992);
    $w = pop(@a701);
    $v = pop(@a701);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    ($v, $w) = (@a701[0, 1]);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
}
{
    @a701 = ('12', ' 3 ');
    my $v = $a701[0];
    my $w = $a701[1];
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    push(@a701, '12', ' 3 ');
    $w = pop(@a701);
    $v = pop(@a701);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    ($v, $w) = (@a701[0, 1]);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
}
{
    @a701 = (true, 0);
    my $v = $a701[0];
    my $w = $a701[1];
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    push(@a701, true, 0);
    $w = pop(@a701);
    $v = pop(@a701);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    ($v, $w) = (@a701[0, 1]);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
}
{
    @a701 = ((-7), false);
    my $v = $a701[0];
    my $w = $a701[1];
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    push(@a701, (-7), false);
    $w = pop(@a701);
    $v = pop(@a701);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    ($v, $w) = (@a701[0, 1]);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
}
{
    @a701 = (9007199254740992.0, (-2.5));
    my $v = $a701[0];
    my $w = $a701[1];
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    push(@a701, 9007199254740992.0, (-2.5));
    $w = pop(@a701);
    $v = pop(@a701);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    ($v, $w) = (@a701[0, 1]);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
}
{
    @a701 = (true, 9007199254740992);
    my $v = $a701[0];
    my $w = $a701[1];
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    push(@a701, true, 9007199254740992);
    $w = pop(@a701);
    $v = pop(@a701);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    ($v, $w) = (@a701[0, 1]);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
}
{
    @a701 = ((-7), 9007199254740992);
    my $v = $a701[0];
    my $w = $a701[1];
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    push(@a701, (-7), 9007199254740992);
    $w = pop(@a701);
    $v = pop(@a701);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
    ($v, $w) = (@a701[0, 1]);
    say(defined($v - $w) ? (('[' . ($v - $w)) . ']') : 'undef');
}
my @a702;
{
    @a702 = (0, 1);
    my $v = $a702[0];
    my $w = $a702[1];
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    push(@a702, 0, 1);
    $w = pop(@a702);
    $v = pop(@a702);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    ($v, $w) = (@a702[0, 1]);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
}
{
    @a702 = ((-2.5), '12');
    my $v = $a702[0];
    my $w = $a702[1];
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    push(@a702, (-2.5), '12');
    $w = pop(@a702);
    $v = pop(@a702);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    ($v, $w) = (@a702[0, 1]);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
}
{
    @a702 = (' 3 ', false);
    my $v = $a702[0];
    my $w = $a702[1];
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    push(@a702, ' 3 ', false);
    $w = pop(@a702);
    $v = pop(@a702);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    ($v, $w) = (@a702[0, 1]);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
}
{
    @a702 = (false, (-2.5));
    my $v = $a702[0];
    my $w = $a702[1];
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    push(@a702, false, (-2.5));
    $w = pop(@a702);
    $v = pop(@a702);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    ($v, $w) = (@a702[0, 1]);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
}
{
    @a702 = (0.5, 0.5);
    my $v = $a702[0];
    my $w = $a702[1];
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    push(@a702, 0.5, 0.5);
    $w = pop(@a702);
    $v = pop(@a702);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    ($v, $w) = (@a702[0, 1]);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
}
{
    @a702 = (' 3 ', 1);
    my $v = $a702[0];
    my $w = $a702[1];
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    push(@a702, ' 3 ', 1);
    $w = pop(@a702);
    $v = pop(@a702);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    ($v, $w) = (@a702[0, 1]);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
}
{
    @a702 = (false, '12');
    my $v = $a702[0];
    my $w = $a702[1];
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    push(@a702, false, '12');
    $w = pop(@a702);
    $v = pop(@a702);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    ($v, $w) = (@a702[0, 1]);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
}
{
    @a702 = (9223372036854775807, true);
    my $v = $a702[0];
    my $w = $a702[1];
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    push(@a702, 9223372036854775807, true);
    $w = pop(@a702);
    $v = pop(@a702);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
    ($v, $w) = (@a702[0, 1]);
    say(defined($v * $w) ? (('[' . ($v * $w)) . ']') : 'undef');
}
my @a703;
{
    @a703 = (0, 1);
    my $v = $a703[0];
    my $w = $a703[1];
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    push(@a703, 0, 1);
    $w = pop(@a703);
    $v = pop(@a703);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    ($v, $w) = (@a703[0, 1]);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
}
{
    @a703 = (0.5, 9007199254740992);
    my $v = $a703[0];
    my $w = $a703[1];
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    push(@a703, 0.5, 9007199254740992);
    $w = pop(@a703);
    $v = pop(@a703);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    ($v, $w) = (@a703[0, 1]);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
}
{
    @a703 = ('12', ' 3 ');
    my $v = $a703[0];
    my $w = $a703[1];
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    push(@a703, '12', ' 3 ');
    $w = pop(@a703);
    $v = pop(@a703);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    ($v, $w) = (@a703[0, 1]);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
}
{
    @a703 = (0, 9223372036854775807);
    my $v = $a703[0];
    my $w = $a703[1];
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    push(@a703, 0, 9223372036854775807);
    $w = pop(@a703);
    $v = pop(@a703);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    ($v, $w) = (@a703[0, 1]);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
}
{
    @a703 = ((-2.5), '1e3');
    my $v = $a703[0];
    my $w = $a703[1];
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    push(@a703, (-2.5), '1e3');
    $w = pop(@a703);
    $v = pop(@a703);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    ($v, $w) = (@a703[0, 1]);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
}
{
    @a703 = (false, '12');
    my $v = $a703[0];
    my $w = $a703[1];
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    push(@a703, false, '12');
    $w = pop(@a703);
    $v = pop(@a703);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    ($v, $w) = (@a703[0, 1]);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
}
{
    @a703 = (9223372036854775807, true);
    my $v = $a703[0];
    my $w = $a703[1];
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    push(@a703, 9223372036854775807, true);
    $w = pop(@a703);
    $v = pop(@a703);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    ($v, $w) = (@a703[0, 1]);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
}
{
    @a703 = (9007199254740992.0, '3.0');
    my $v = $a703[0];
    my $w = $a703[1];
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    push(@a703, 9007199254740992.0, '3.0');
    $w = pop(@a703);
    $v = pop(@a703);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
    ($v, $w) = (@a703[0, 1]);
    say(defined($v / $w) ? (('[' . ($v / $w)) . ']') : 'undef');
}
my @a704;
{
    @a704 = (0, 1);
    my $v = $a704[0];
    my $w = $a704[1];
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    push(@a704, 0, 1);
    $w = pop(@a704);
    $v = pop(@a704);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    ($v, $w) = (@a704[0, 1]);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
}
{
    @a704 = (0.5, 9007199254740992);
    my $v = $a704[0];
    my $w = $a704[1];
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    push(@a704, 0.5, 9007199254740992);
    $w = pop(@a704);
    $v = pop(@a704);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    ($v, $w) = (@a704[0, 1]);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
}
{
    @a704 = ('12', ' 3 ');
    my $v = $a704[0];
    my $w = $a704[1];
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    push(@a704, '12', ' 3 ');
    $w = pop(@a704);
    $v = pop(@a704);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    ($v, $w) = (@a704[0, 1]);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
}
{
    @a704 = (false, (-2.5));
    my $v = $a704[0];
    my $w = $a704[1];
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    push(@a704, false, (-2.5));
    $w = pop(@a704);
    $v = pop(@a704);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    ($v, $w) = (@a704[0, 1]);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
}
{
    @a704 = (9223372036854775807, '3.0');
    my $v = $a704[0];
    my $w = $a704[1];
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    push(@a704, 9223372036854775807, '3.0');
    $w = pop(@a704);
    $v = pop(@a704);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    ($v, $w) = (@a704[0, 1]);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
}
{
    @a704 = ('3.0', 3.0);
    my $v = $a704[0];
    my $w = $a704[1];
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    push(@a704, '3.0', 3.0);
    $w = pop(@a704);
    $v = pop(@a704);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    ($v, $w) = (@a704[0, 1]);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
}
{
    @a704 = ((-7), 9007199254740992);
    my $v = $a704[0];
    my $w = $a704[1];
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    push(@a704, (-7), 9007199254740992);
    $w = pop(@a704);
    $v = pop(@a704);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    ($v, $w) = (@a704[0, 1]);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
}
{
    @a704 = (0.5, ' 3 ');
    my $v = $a704[0];
    my $w = $a704[1];
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    push(@a704, 0.5, ' 3 ');
    $w = pop(@a704);
    $v = pop(@a704);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
    ($v, $w) = (@a704[0, 1]);
    say(defined($v % $w) ? (('[' . ($v % $w)) . ']') : 'undef');
}
my @a705;
{
    @a705 = (0, 1);
    my $v = $a705[0];
    my $w = $a705[1];
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    push(@a705, 0, 1);
    $w = pop(@a705);
    $v = pop(@a705);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    ($v, $w) = (@a705[0, 1]);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
}
{
    @a705 = (0.5, 9007199254740992);
    my $v = $a705[0];
    my $w = $a705[1];
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    push(@a705, 0.5, 9007199254740992);
    $w = pop(@a705);
    $v = pop(@a705);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    ($v, $w) = (@a705[0, 1]);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
}
{
    @a705 = (' 3 ', false);
    my $v = $a705[0];
    my $w = $a705[1];
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    push(@a705, ' 3 ', false);
    $w = pop(@a705);
    $v = pop(@a705);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    ($v, $w) = (@a705[0, 1]);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
}
{
    @a705 = (0, 9223372036854775807);
    my $v = $a705[0];
    my $w = $a705[1];
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    push(@a705, 0, 9223372036854775807);
    $w = pop(@a705);
    $v = pop(@a705);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    ($v, $w) = (@a705[0, 1]);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
}
{
    @a705 = (0.5, 0.5);
    my $v = $a705[0];
    my $w = $a705[1];
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    push(@a705, 0.5, 0.5);
    $w = pop(@a705);
    $v = pop(@a705);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    ($v, $w) = (@a705[0, 1]);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
}
{
    @a705 = ('3.0', 3.0);
    my $v = $a705[0];
    my $w = $a705[1];
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    push(@a705, '3.0', 3.0);
    $w = pop(@a705);
    $v = pop(@a705);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    ($v, $w) = (@a705[0, 1]);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
}
{
    @a705 = (0, 9007199254740992.0);
    my $v = $a705[0];
    my $w = $a705[1];
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    push(@a705, 0, 9007199254740992.0);
    $w = pop(@a705);
    $v = pop(@a705);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    ($v, $w) = (@a705[0, 1]);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
}
{
    @a705 = (0.5, ' 3 ');
    my $v = $a705[0];
    my $w = $a705[1];
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    push(@a705, 0.5, ' 3 ');
    $w = pop(@a705);
    $v = pop(@a705);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
    ($v, $w) = (@a705[0, 1]);
    say(defined($v ** $w) ? (('[' . ($v ** $w)) . ']') : 'undef');
}
my @a706;
{
    @a706 = (0, 1);
    my $v = $a706[0];
    my $w = $a706[1];
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    push(@a706, 0, 1);
    $w = pop(@a706);
    $v = pop(@a706);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    ($v, $w) = (@a706[0, 1]);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
}
{
    @a706 = (0.5, 9007199254740992);
    my $v = $a706[0];
    my $w = $a706[1];
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    push(@a706, 0.5, 9007199254740992);
    $w = pop(@a706);
    $v = pop(@a706);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    ($v, $w) = (@a706[0, 1]);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
}
{
    @a706 = ('3.0', (-9223372036854775807 - 1));
    my $v = $a706[0];
    my $w = $a706[1];
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    push(@a706, '3.0', (-9223372036854775807 - 1));
    $w = pop(@a706);
    $v = pop(@a706);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    ($v, $w) = (@a706[0, 1]);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
}
{
    @a706 = (0, 9223372036854775807);
    my $v = $a706[0];
    my $w = $a706[1];
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    push(@a706, 0, 9223372036854775807);
    $w = pop(@a706);
    $v = pop(@a706);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    ($v, $w) = (@a706[0, 1]);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
}
{
    @a706 = ((-2.5), '1e3');
    my $v = $a706[0];
    my $w = $a706[1];
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    push(@a706, (-2.5), '1e3');
    $w = pop(@a706);
    $v = pop(@a706);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    ($v, $w) = (@a706[0, 1]);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
}
{
    @a706 = ('1e3', "");
    my $v = $a706[0];
    my $w = $a706[1];
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    push(@a706, '1e3', "");
    $w = pop(@a706);
    $v = pop(@a706);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    ($v, $w) = (@a706[0, 1]);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
}
{
    @a706 = (0, 9007199254740992.0);
    my $v = $a706[0];
    my $w = $a706[1];
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    push(@a706, 0, 9007199254740992.0);
    $w = pop(@a706);
    $v = pop(@a706);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    ($v, $w) = (@a706[0, 1]);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
}
{
    @a706 = (0.5, ' 3 ');
    my $v = $a706[0];
    my $w = $a706[1];
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    push(@a706, 0.5, ' 3 ');
    $w = pop(@a706);
    $v = pop(@a706);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
    ($v, $w) = (@a706[0, 1]);
    say(defined($v . $w) ? (('[' . ($v . $w)) . ']') : 'undef');
}
my @a707;
{
    @a707 = (0, 1);
    my $v = $a707[0];
    my $w = $a707[1];
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    push(@a707, 0, 1);
    $w = pop(@a707);
    $v = pop(@a707);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    ($v, $w) = (@a707[0, 1]);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
}
{
    @a707 = (3.0, true);
    my $v = $a707[0];
    my $w = $a707[1];
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    push(@a707, 3.0, true);
    $w = pop(@a707);
    $v = pop(@a707);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    ($v, $w) = (@a707[0, 1]);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
}
{
    @a707 = ("", 0.5);
    my $v = $a707[0];
    my $w = $a707[1];
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    push(@a707, "", 0.5);
    $w = pop(@a707);
    $v = pop(@a707);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    ($v, $w) = (@a707[0, 1]);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
}
{
    @a707 = ((-7), false);
    my $v = $a707[0];
    my $w = $a707[1];
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    push(@a707, (-7), false);
    $w = pop(@a707);
    $v = pop(@a707);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    ($v, $w) = (@a707[0, 1]);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
}
{
    @a707 = (3.0, 0);
    my $v = $a707[0];
    my $w = $a707[1];
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    push(@a707, 3.0, 0);
    $w = pop(@a707);
    $v = pop(@a707);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    ($v, $w) = (@a707[0, 1]);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
}
{
    @a707 = ('0', '0');
    my $v = $a707[0];
    my $w = $a707[1];
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    push(@a707, '0', '0');
    $w = pop(@a707);
    $v = pop(@a707);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    ($v, $w) = (@a707[0, 1]);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
}
{
    @a707 = (9223372036854775807, true);
    my $v = $a707[0];
    my $w = $a707[1];
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    push(@a707, 9223372036854775807, true);
    $w = pop(@a707);
    $v = pop(@a707);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    ($v, $w) = (@a707[0, 1]);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
}
{
    @a707 = (' 3 ', 0.5);
    my $v = $a707[0];
    my $w = $a707[1];
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    push(@a707, ' 3 ', 0.5);
    $w = pop(@a707);
    $v = pop(@a707);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
    ($v, $w) = (@a707[0, 1]);
    say(defined($v x $w) ? (('[' . ($v x $w)) . ']') : 'undef');
}
my @a708;
{
    @a708 = (0, 1);
    my $v = $a708[0];
    my $w = $a708[1];
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    push(@a708, 0, 1);
    $w = pop(@a708);
    $v = pop(@a708);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    ($v, $w) = (@a708[0, 1]);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
}
{
    @a708 = (0.5, 9007199254740992);
    my $v = $a708[0];
    my $w = $a708[1];
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    push(@a708, 0.5, 9007199254740992);
    $w = pop(@a708);
    $v = pop(@a708);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    ($v, $w) = (@a708[0, 1]);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
}
{
    @a708 = (' 3 ', false);
    my $v = $a708[0];
    my $w = $a708[1];
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    push(@a708, ' 3 ', false);
    $w = pop(@a708);
    $v = pop(@a708);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    ($v, $w) = (@a708[0, 1]);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
}
{
    @a708 = (false, (-2.5));
    my $v = $a708[0];
    my $w = $a708[1];
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    push(@a708, false, (-2.5));
    $w = pop(@a708);
    $v = pop(@a708);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    ($v, $w) = (@a708[0, 1]);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
}
{
    @a708 = (9223372036854775807, '3.0');
    my $v = $a708[0];
    my $w = $a708[1];
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    push(@a708, 9223372036854775807, '3.0');
    $w = pop(@a708);
    $v = pop(@a708);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    ($v, $w) = (@a708[0, 1]);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
}
{
    @a708 = (' 3 ', 1);
    my $v = $a708[0];
    my $w = $a708[1];
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    push(@a708, ' 3 ', 1);
    $w = pop(@a708);
    $v = pop(@a708);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    ($v, $w) = (@a708[0, 1]);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
}
{
    @a708 = (0, 9007199254740992.0);
    my $v = $a708[0];
    my $w = $a708[1];
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    push(@a708, 0, 9007199254740992.0);
    $w = pop(@a708);
    $v = pop(@a708);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    ($v, $w) = (@a708[0, 1]);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
}
{
    @a708 = ((-9223372036854775807 - 1), 9223372036854775807);
    my $v = $a708[0];
    my $w = $a708[1];
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    push(@a708, (-9223372036854775807 - 1), 9223372036854775807);
    $w = pop(@a708);
    $v = pop(@a708);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
    ($v, $w) = (@a708[0, 1]);
    say(defined($v == $w) ? (('[' . ($v == $w)) . ']') : 'undef');
}
my @a709;
{
    @a709 = (0, 1);
    my $v = $a709[0];
    my $w = $a709[1];
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    push(@a709, 0, 1);
    $w = pop(@a709);
    $v = pop(@a709);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    ($v, $w) = (@a709[0, 1]);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
}
{
    @a709 = (0.5, 9007199254740992);
    my $v = $a709[0];
    my $w = $a709[1];
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    push(@a709, 0.5, 9007199254740992);
    $w = pop(@a709);
    $v = pop(@a709);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    ($v, $w) = (@a709[0, 1]);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
}
{
    @a709 = (' 3 ', false);
    my $v = $a709[0];
    my $w = $a709[1];
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    push(@a709, ' 3 ', false);
    $w = pop(@a709);
    $v = pop(@a709);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    ($v, $w) = (@a709[0, 1]);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
}
{
    @a709 = (false, (-2.5));
    my $v = $a709[0];
    my $w = $a709[1];
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    push(@a709, false, (-2.5));
    $w = pop(@a709);
    $v = pop(@a709);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    ($v, $w) = (@a709[0, 1]);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
}
{
    @a709 = (9223372036854775807, '3.0');
    my $v = $a709[0];
    my $w = $a709[1];
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    push(@a709, 9223372036854775807, '3.0');
    $w = pop(@a709);
    $v = pop(@a709);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    ($v, $w) = (@a709[0, 1]);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
}
{
    @a709 = (' 3 ', 1);
    my $v = $a709[0];
    my $w = $a709[1];
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    push(@a709, ' 3 ', 1);
    $w = pop(@a709);
    $v = pop(@a709);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    ($v, $w) = (@a709[0, 1]);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
}
{
    @a709 = (0, 9007199254740992.0);
    my $v = $a709[0];
    my $w = $a709[1];
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    push(@a709, 0, 9007199254740992.0);
    $w = pop(@a709);
    $v = pop(@a709);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    ($v, $w) = (@a709[0, 1]);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
}
{
    @a709 = ((-9223372036854775807 - 1), 9223372036854775807);
    my $v = $a709[0];
    my $w = $a709[1];
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    push(@a709, (-9223372036854775807 - 1), 9223372036854775807);
    $w = pop(@a709);
    $v = pop(@a709);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
    ($v, $w) = (@a709[0, 1]);
    say(defined($v < $w) ? (('[' . ($v < $w)) . ']') : 'undef');
}
my @a710;
{
    @a710 = (0, 1);
    my $v = $a710[0];
    my $w = $a710[1];
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    push(@a710, 0, 1);
    $w = pop(@a710);
    $v = pop(@a710);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    ($v, $w) = (@a710[0, 1]);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
}
{
    @a710 = (0.5, 9007199254740992);
    my $v = $a710[0];
    my $w = $a710[1];
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    push(@a710, 0.5, 9007199254740992);
    $w = pop(@a710);
    $v = pop(@a710);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    ($v, $w) = (@a710[0, 1]);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
}
{
    @a710 = (' 3 ', false);
    my $v = $a710[0];
    my $w = $a710[1];
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    push(@a710, ' 3 ', false);
    $w = pop(@a710);
    $v = pop(@a710);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    ($v, $w) = (@a710[0, 1]);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
}
{
    @a710 = (false, (-2.5));
    my $v = $a710[0];
    my $w = $a710[1];
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    push(@a710, false, (-2.5));
    $w = pop(@a710);
    $v = pop(@a710);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    ($v, $w) = (@a710[0, 1]);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
}
{
    @a710 = (9223372036854775807, '3.0');
    my $v = $a710[0];
    my $w = $a710[1];
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    push(@a710, 9223372036854775807, '3.0');
    $w = pop(@a710);
    $v = pop(@a710);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    ($v, $w) = (@a710[0, 1]);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
}
{
    @a710 = (' 3 ', 1);
    my $v = $a710[0];
    my $w = $a710[1];
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    push(@a710, ' 3 ', 1);
    $w = pop(@a710);
    $v = pop(@a710);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    ($v, $w) = (@a710[0, 1]);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
}
{
    @a710 = (0, 9007199254740992.0);
    my $v = $a710[0];
    my $w = $a710[1];
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    push(@a710, 0, 9007199254740992.0);
    $w = pop(@a710);
    $v = pop(@a710);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    ($v, $w) = (@a710[0, 1]);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
}
{
    @a710 = ((-9223372036854775807 - 1), 9223372036854775807);
    my $v = $a710[0];
    my $w = $a710[1];
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    push(@a710, (-9223372036854775807 - 1), 9223372036854775807);
    $w = pop(@a710);
    $v = pop(@a710);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
    ($v, $w) = (@a710[0, 1]);
    say(defined($v <=> $w) ? (('[' . ($v <=> $w)) . ']') : 'undef');
}
my @a711;
{
    @a711 = (0, 1);
    my $v = $a711[0];
    my $w = $a711[1];
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    push(@a711, 0, 1);
    $w = pop(@a711);
    $v = pop(@a711);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    ($v, $w) = (@a711[0, 1]);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
}
{
    @a711 = (0.5, 9007199254740992);
    my $v = $a711[0];
    my $w = $a711[1];
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    push(@a711, 0.5, 9007199254740992);
    $w = pop(@a711);
    $v = pop(@a711);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    ($v, $w) = (@a711[0, 1]);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
}
{
    @a711 = ('3.0', (-9223372036854775807 - 1));
    my $v = $a711[0];
    my $w = $a711[1];
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    push(@a711, '3.0', (-9223372036854775807 - 1));
    $w = pop(@a711);
    $v = pop(@a711);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    ($v, $w) = (@a711[0, 1]);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
}
{
    @a711 = (0, 9223372036854775807);
    my $v = $a711[0];
    my $w = $a711[1];
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    push(@a711, 0, 9223372036854775807);
    $w = pop(@a711);
    $v = pop(@a711);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    ($v, $w) = (@a711[0, 1]);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
}
{
    @a711 = ((-2.5), '1e3');
    my $v = $a711[0];
    my $w = $a711[1];
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    push(@a711, (-2.5), '1e3');
    $w = pop(@a711);
    $v = pop(@a711);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    ($v, $w) = (@a711[0, 1]);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
}
{
    @a711 = ('1e3', "");
    my $v = $a711[0];
    my $w = $a711[1];
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    push(@a711, '1e3', "");
    $w = pop(@a711);
    $v = pop(@a711);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    ($v, $w) = (@a711[0, 1]);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
}
{
    @a711 = (0, 9007199254740992.0);
    my $v = $a711[0];
    my $w = $a711[1];
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    push(@a711, 0, 9007199254740992.0);
    $w = pop(@a711);
    $v = pop(@a711);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    ($v, $w) = (@a711[0, 1]);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
}
{
    @a711 = (0.5, ' 3 ');
    my $v = $a711[0];
    my $w = $a711[1];
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    push(@a711, 0.5, ' 3 ');
    $w = pop(@a711);
    $v = pop(@a711);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
    ($v, $w) = (@a711[0, 1]);
    say(defined($v eq $w) ? (('[' . ($v eq $w)) . ']') : 'undef');
}
my @a712;
{
    @a712 = (0, 1);
    my $v = $a712[0];
    my $w = $a712[1];
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    push(@a712, 0, 1);
    $w = pop(@a712);
    $v = pop(@a712);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    ($v, $w) = (@a712[0, 1]);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
}
{
    @a712 = (0.5, 9007199254740992);
    my $v = $a712[0];
    my $w = $a712[1];
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    push(@a712, 0.5, 9007199254740992);
    $w = pop(@a712);
    $v = pop(@a712);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    ($v, $w) = (@a712[0, 1]);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
}
{
    @a712 = ('3.0', (-9223372036854775807 - 1));
    my $v = $a712[0];
    my $w = $a712[1];
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    push(@a712, '3.0', (-9223372036854775807 - 1));
    $w = pop(@a712);
    $v = pop(@a712);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    ($v, $w) = (@a712[0, 1]);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
}
{
    @a712 = (0, 9223372036854775807);
    my $v = $a712[0];
    my $w = $a712[1];
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    push(@a712, 0, 9223372036854775807);
    $w = pop(@a712);
    $v = pop(@a712);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    ($v, $w) = (@a712[0, 1]);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
}
{
    @a712 = ((-2.5), '1e3');
    my $v = $a712[0];
    my $w = $a712[1];
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    push(@a712, (-2.5), '1e3');
    $w = pop(@a712);
    $v = pop(@a712);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    ($v, $w) = (@a712[0, 1]);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
}
{
    @a712 = ('1e3', "");
    my $v = $a712[0];
    my $w = $a712[1];
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    push(@a712, '1e3', "");
    $w = pop(@a712);
    $v = pop(@a712);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    ($v, $w) = (@a712[0, 1]);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
}
{
    @a712 = (0, 9007199254740992.0);
    my $v = $a712[0];
    my $w = $a712[1];
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    push(@a712, 0, 9007199254740992.0);
    $w = pop(@a712);
    $v = pop(@a712);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    ($v, $w) = (@a712[0, 1]);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
}
{
    @a712 = (0.5, ' 3 ');
    my $v = $a712[0];
    my $w = $a712[1];
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    push(@a712, 0.5, ' 3 ');
    $w = pop(@a712);
    $v = pop(@a712);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
    ($v, $w) = (@a712[0, 1]);
    say(defined($v lt $w) ? (('[' . ($v lt $w)) . ']') : 'undef');
}
my @a713;
{
    @a713 = (0, 1);
    my $v = $a713[0];
    my $w = $a713[1];
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    push(@a713, 0, 1);
    $w = pop(@a713);
    $v = pop(@a713);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    ($v, $w) = (@a713[0, 1]);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
}
{
    @a713 = (0.5, 9007199254740992);
    my $v = $a713[0];
    my $w = $a713[1];
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    push(@a713, 0.5, 9007199254740992);
    $w = pop(@a713);
    $v = pop(@a713);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    ($v, $w) = (@a713[0, 1]);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
}
{
    @a713 = ('3.0', (-9223372036854775807 - 1));
    my $v = $a713[0];
    my $w = $a713[1];
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    push(@a713, '3.0', (-9223372036854775807 - 1));
    $w = pop(@a713);
    $v = pop(@a713);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    ($v, $w) = (@a713[0, 1]);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
}
{
    @a713 = (0, 9223372036854775807);
    my $v = $a713[0];
    my $w = $a713[1];
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    push(@a713, 0, 9223372036854775807);
    $w = pop(@a713);
    $v = pop(@a713);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    ($v, $w) = (@a713[0, 1]);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
}
{
    @a713 = ((-2.5), '1e3');
    my $v = $a713[0];
    my $w = $a713[1];
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    push(@a713, (-2.5), '1e3');
    $w = pop(@a713);
    $v = pop(@a713);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    ($v, $w) = (@a713[0, 1]);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
}
{
    @a713 = ('1e3', "");
    my $v = $a713[0];
    my $w = $a713[1];
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    push(@a713, '1e3', "");
    $w = pop(@a713);
    $v = pop(@a713);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    ($v, $w) = (@a713[0, 1]);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
}
{
    @a713 = (0, 9007199254740992.0);
    my $v = $a713[0];
    my $w = $a713[1];
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    push(@a713, 0, 9007199254740992.0);
    $w = pop(@a713);
    $v = pop(@a713);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    ($v, $w) = (@a713[0, 1]);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
}
{
    @a713 = (0.5, ' 3 ');
    my $v = $a713[0];
    my $w = $a713[1];
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    push(@a713, 0.5, ' 3 ');
    $w = pop(@a713);
    $v = pop(@a713);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
    ($v, $w) = (@a713[0, 1]);
    say(defined($v cmp $w) ? (('[' . ($v cmp $w)) . ']') : 'undef');
}
my @a714;
{
    @a714 = (0, 1);
    my $v = $a714[0];
    my $w = $a714[1];
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    push(@a714, 0, 1);
    $w = pop(@a714);
    $v = pop(@a714);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    ($v, $w) = (@a714[0, 1]);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
}
{
    @a714 = ((-2.5), '12');
    my $v = $a714[0];
    my $w = $a714[1];
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    push(@a714, (-2.5), '12');
    $w = pop(@a714);
    $v = pop(@a714);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    ($v, $w) = (@a714[0, 1]);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
}
{
    @a714 = ('ab', (undef));
    my $v = $a714[0];
    my $w = $a714[1];
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    push(@a714, 'ab', (undef));
    $w = pop(@a714);
    $v = pop(@a714);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    ($v, $w) = (@a714[0, 1]);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
}
{
    @a714 = (1, ' 3 ');
    my $v = $a714[0];
    my $w = $a714[1];
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    push(@a714, 1, ' 3 ');
    $w = pop(@a714);
    $v = pop(@a714);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    ($v, $w) = (@a714[0, 1]);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
}
{
    @a714 = (3.0, 0);
    my $v = $a714[0];
    my $w = $a714[1];
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    push(@a714, 3.0, 0);
    $w = pop(@a714);
    $v = pop(@a714);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    ($v, $w) = (@a714[0, 1]);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
}
{
    @a714 = ("", 9007199254740992.0);
    my $v = $a714[0];
    my $w = $a714[1];
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    push(@a714, "", 9007199254740992.0);
    $w = pop(@a714);
    $v = pop(@a714);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    ($v, $w) = (@a714[0, 1]);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
}
{
    @a714 = ((-7), 9007199254740992);
    my $v = $a714[0];
    my $w = $a714[1];
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    push(@a714, (-7), 9007199254740992);
    $w = pop(@a714);
    $v = pop(@a714);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    ($v, $w) = (@a714[0, 1]);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
}
{
    @a714 = (9007199254740992.0, '3.0');
    my $v = $a714[0];
    my $w = $a714[1];
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    push(@a714, 9007199254740992.0, '3.0');
    $w = pop(@a714);
    $v = pop(@a714);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
    ($v, $w) = (@a714[0, 1]);
    say(defined($v && $w) ? (('[' . ($v && $w)) . ']') : 'undef');
}
my @a715;
{
    @a715 = (0, 1);
    my $v = $a715[0];
    my $w = $a715[1];
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    push(@a715, 0, 1);
    $w = pop(@a715);
    $v = pop(@a715);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    ($v, $w) = (@a715[0, 1]);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
}
{
    @a715 = ((-2.5), '12');
    my $v = $a715[0];
    my $w = $a715[1];
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    push(@a715, (-2.5), '12');
    $w = pop(@a715);
    $v = pop(@a715);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    ($v, $w) = (@a715[0, 1]);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
}
{
    @a715 = ('ab', (undef));
    my $v = $a715[0];
    my $w = $a715[1];
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    push(@a715, 'ab', (undef));
    $w = pop(@a715);
    $v = pop(@a715);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    ($v, $w) = (@a715[0, 1]);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
}
{
    @a715 = (1, ' 3 ');
    my $v = $a715[0];
    my $w = $a715[1];
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    push(@a715, 1, ' 3 ');
    $w = pop(@a715);
    $v = pop(@a715);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    ($v, $w) = (@a715[0, 1]);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
}
{
    @a715 = (3.0, 0);
    my $v = $a715[0];
    my $w = $a715[1];
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    push(@a715, 3.0, 0);
    $w = pop(@a715);
    $v = pop(@a715);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    ($v, $w) = (@a715[0, 1]);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
}
{
    @a715 = ("", 9007199254740992.0);
    my $v = $a715[0];
    my $w = $a715[1];
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    push(@a715, "", 9007199254740992.0);
    $w = pop(@a715);
    $v = pop(@a715);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    ($v, $w) = (@a715[0, 1]);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
}
{
    @a715 = ((-7), 9007199254740992);
    my $v = $a715[0];
    my $w = $a715[1];
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    push(@a715, (-7), 9007199254740992);
    $w = pop(@a715);
    $v = pop(@a715);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    ($v, $w) = (@a715[0, 1]);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
}
{
    @a715 = (9007199254740992.0, '3.0');
    my $v = $a715[0];
    my $w = $a715[1];
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    push(@a715, 9007199254740992.0, '3.0');
    $w = pop(@a715);
    $v = pop(@a715);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
    ($v, $w) = (@a715[0, 1]);
    say(defined($v || $w) ? (('[' . ($v || $w)) . ']') : 'undef');
}
my @a716;
{
    @a716 = (0, 1);
    my $v = $a716[0];
    my $w = $a716[1];
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    push(@a716, 0, 1);
    $w = pop(@a716);
    $v = pop(@a716);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    ($v, $w) = (@a716[0, 1]);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
}
{
    @a716 = ((-2.5), '12');
    my $v = $a716[0];
    my $w = $a716[1];
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    push(@a716, (-2.5), '12');
    $w = pop(@a716);
    $v = pop(@a716);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    ($v, $w) = (@a716[0, 1]);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
}
{
    @a716 = ('ab', (undef));
    my $v = $a716[0];
    my $w = $a716[1];
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    push(@a716, 'ab', (undef));
    $w = pop(@a716);
    $v = pop(@a716);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    ($v, $w) = (@a716[0, 1]);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
}
{
    @a716 = (1, ' 3 ');
    my $v = $a716[0];
    my $w = $a716[1];
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    push(@a716, 1, ' 3 ');
    $w = pop(@a716);
    $v = pop(@a716);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    ($v, $w) = (@a716[0, 1]);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
}
{
    @a716 = (3.0, 0);
    my $v = $a716[0];
    my $w = $a716[1];
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    push(@a716, 3.0, 0);
    $w = pop(@a716);
    $v = pop(@a716);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    ($v, $w) = (@a716[0, 1]);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
}
{
    @a716 = ("", 9007199254740992.0);
    my $v = $a716[0];
    my $w = $a716[1];
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    push(@a716, "", 9007199254740992.0);
    $w = pop(@a716);
    $v = pop(@a716);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    ($v, $w) = (@a716[0, 1]);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
}
{
    @a716 = ((-7), 9007199254740992);
    my $v = $a716[0];
    my $w = $a716[1];
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    push(@a716, (-7), 9007199254740992);
    $w = pop(@a716);
    $v = pop(@a716);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    ($v, $w) = (@a716[0, 1]);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
}
{
    @a716 = (9007199254740992.0, '3.0');
    my $v = $a716[0];
    my $w = $a716[1];
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    push(@a716, 9007199254740992.0, '3.0');
    $w = pop(@a716);
    $v = pop(@a716);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
    ($v, $w) = (@a716[0, 1]);
    say(defined($v // $w) ? (('[' . ($v // $w)) . ']') : 'undef');
}
my @a717;
{
    @a717 = (0, 1);
    my $v = $a717[0];
    my $w = $a717[1];
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    push(@a717, 0, 1);
    $w = pop(@a717);
    $v = pop(@a717);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    ($v, $w) = (@a717[0, 1]);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
}
{
    @a717 = ((-2.5), '12');
    my $v = $a717[0];
    my $w = $a717[1];
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    push(@a717, (-2.5), '12');
    $w = pop(@a717);
    $v = pop(@a717);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    ($v, $w) = (@a717[0, 1]);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
}
{
    @a717 = ('1e3', '3.0');
    my $v = $a717[0];
    my $w = $a717[1];
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    push(@a717, '1e3', '3.0');
    $w = pop(@a717);
    $v = pop(@a717);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    ($v, $w) = (@a717[0, 1]);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
}
{
    @a717 = ((-7), false);
    my $v = $a717[0];
    my $w = $a717[1];
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    push(@a717, (-7), false);
    $w = pop(@a717);
    $v = pop(@a717);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    ($v, $w) = (@a717[0, 1]);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
}
{
    @a717 = (9007199254740992.0, (-2.5));
    my $v = $a717[0];
    my $w = $a717[1];
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    push(@a717, 9007199254740992.0, (-2.5));
    $w = pop(@a717);
    $v = pop(@a717);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    ($v, $w) = (@a717[0, 1]);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
}
{
    @a717 = (true, 9007199254740992);
    my $v = $a717[0];
    my $w = $a717[1];
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    push(@a717, true, 9007199254740992);
    $w = pop(@a717);
    $v = pop(@a717);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    ($v, $w) = (@a717[0, 1]);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
}
{
    @a717 = (9223372036854775807, true);
    my $v = $a717[0];
    my $w = $a717[1];
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    push(@a717, 9223372036854775807, true);
    $w = pop(@a717);
    $v = pop(@a717);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    ($v, $w) = (@a717[0, 1]);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
}
{
    @a717 = (' 3 ', 0.5);
    my $v = $a717[0];
    my $w = $a717[1];
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    push(@a717, ' 3 ', 0.5);
    $w = pop(@a717);
    $v = pop(@a717);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
    ($v, $w) = (@a717[0, 1]);
    say(defined(-$v) ? (('[' . (-$v)) . ']') : 'undef');
}
my @a718;
{
    @a718 = (0, 1);
    my $v = $a718[0];
    my $w = $a718[1];
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    push(@a718, 0, 1);
    $w = pop(@a718);
    $v = pop(@a718);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    ($v, $w) = (@a718[0, 1]);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
}
{
    @a718 = ((-2.5), '12');
    my $v = $a718[0];
    my $w = $a718[1];
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    push(@a718, (-2.5), '12');
    $w = pop(@a718);
    $v = pop(@a718);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    ($v, $w) = (@a718[0, 1]);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
}
{
    @a718 = ('ab', (undef));
    my $v = $a718[0];
    my $w = $a718[1];
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    push(@a718, 'ab', (undef));
    $w = pop(@a718);
    $v = pop(@a718);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    ($v, $w) = (@a718[0, 1]);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
}
{
    @a718 = (1, ' 3 ');
    my $v = $a718[0];
    my $w = $a718[1];
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    push(@a718, 1, ' 3 ');
    $w = pop(@a718);
    $v = pop(@a718);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    ($v, $w) = (@a718[0, 1]);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
}
{
    @a718 = (3.0, 0);
    my $v = $a718[0];
    my $w = $a718[1];
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    push(@a718, 3.0, 0);
    $w = pop(@a718);
    $v = pop(@a718);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    ($v, $w) = (@a718[0, 1]);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
}
{
    @a718 = ("", 9007199254740992.0);
    my $v = $a718[0];
    my $w = $a718[1];
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    push(@a718, "", 9007199254740992.0);
    $w = pop(@a718);
    $v = pop(@a718);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    ($v, $w) = (@a718[0, 1]);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
}
{
    @a718 = ((-7), 9007199254740992);
    my $v = $a718[0];
    my $w = $a718[1];
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    push(@a718, (-7), 9007199254740992);
    $w = pop(@a718);
    $v = pop(@a718);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    ($v, $w) = (@a718[0, 1]);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
}
{
    @a718 = (9007199254740992.0, '3.0');
    my $v = $a718[0];
    my $w = $a718[1];
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    push(@a718, 9007199254740992.0, '3.0');
    $w = pop(@a718);
    $v = pop(@a718);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
    ($v, $w) = (@a718[0, 1]);
    say(defined(!$v) ? (('[' . (!$v)) . ']') : 'undef');
}
my @a719;
{
    @a719 = (0, 1);
    my $v = $a719[0];
    my $w = $a719[1];
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    push(@a719, 0, 1);
    $w = pop(@a719);
    $v = pop(@a719);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    ($v, $w) = (@a719[0, 1]);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
}
{
    @a719 = ((-2.5), '12');
    my $v = $a719[0];
    my $w = $a719[1];
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    push(@a719, (-2.5), '12');
    $w = pop(@a719);
    $v = pop(@a719);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    ($v, $w) = (@a719[0, 1]);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
}
{
    @a719 = ('ab', (undef));
    my $v = $a719[0];
    my $w = $a719[1];
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    push(@a719, 'ab', (undef));
    $w = pop(@a719);
    $v = pop(@a719);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    ($v, $w) = (@a719[0, 1]);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
}
{
    @a719 = (1, ' 3 ');
    my $v = $a719[0];
    my $w = $a719[1];
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    push(@a719, 1, ' 3 ');
    $w = pop(@a719);
    $v = pop(@a719);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    ($v, $w) = (@a719[0, 1]);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
}
{
    @a719 = (3.0, 0);
    my $v = $a719[0];
    my $w = $a719[1];
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    push(@a719, 3.0, 0);
    $w = pop(@a719);
    $v = pop(@a719);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    ($v, $w) = (@a719[0, 1]);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
}
{
    @a719 = ("", 9007199254740992.0);
    my $v = $a719[0];
    my $w = $a719[1];
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    push(@a719, "", 9007199254740992.0);
    $w = pop(@a719);
    $v = pop(@a719);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    ($v, $w) = (@a719[0, 1]);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
}
{
    @a719 = ((-7), 9007199254740992);
    my $v = $a719[0];
    my $w = $a719[1];
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    push(@a719, (-7), 9007199254740992);
    $w = pop(@a719);
    $v = pop(@a719);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    ($v, $w) = (@a719[0, 1]);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
}
{
    @a719 = (9007199254740992.0, '3.0');
    my $v = $a719[0];
    my $w = $a719[1];
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    push(@a719, 9007199254740992.0, '3.0');
    $w = pop(@a719);
    $v = pop(@a719);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
    ($v, $w) = (@a719[0, 1]);
    say(defined(length($v)) ? (('[' . length($v)) . ']') : 'undef');
}
my @a720;
{
    @a720 = (0, 1);
    my $v = $a720[0];
    my $w = $a720[1];
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    push(@a720, 0, 1);
    $w = pop(@a720);
    $v = pop(@a720);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    ($v, $w) = (@a720[0, 1]);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
}
{
    @a720 = ((-2.5), '12');
    my $v = $a720[0];
    my $w = $a720[1];
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    push(@a720, (-2.5), '12');
    $w = pop(@a720);
    $v = pop(@a720);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    ($v, $w) = (@a720[0, 1]);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
}
{
    @a720 = ('ab', (undef));
    my $v = $a720[0];
    my $w = $a720[1];
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    push(@a720, 'ab', (undef));
    $w = pop(@a720);
    $v = pop(@a720);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    ($v, $w) = (@a720[0, 1]);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
}
{
    @a720 = ((-7), false);
    my $v = $a720[0];
    my $w = $a720[1];
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    push(@a720, (-7), false);
    $w = pop(@a720);
    $v = pop(@a720);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    ($v, $w) = (@a720[0, 1]);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
}
{
    @a720 = (9007199254740992.0, (-2.5));
    my $v = $a720[0];
    my $w = $a720[1];
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    push(@a720, 9007199254740992.0, (-2.5));
    $w = pop(@a720);
    $v = pop(@a720);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    ($v, $w) = (@a720[0, 1]);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
}
{
    @a720 = ('0', '0');
    my $v = $a720[0];
    my $w = $a720[1];
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    push(@a720, '0', '0');
    $w = pop(@a720);
    $v = pop(@a720);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    ($v, $w) = (@a720[0, 1]);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
}
{
    @a720 = (9223372036854775807, true);
    my $v = $a720[0];
    my $w = $a720[1];
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    push(@a720, 9223372036854775807, true);
    $w = pop(@a720);
    $v = pop(@a720);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    ($v, $w) = (@a720[0, 1]);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
}
{
    @a720 = (' 3 ', 0.5);
    my $v = $a720[0];
    my $w = $a720[1];
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    push(@a720, ' 3 ', 0.5);
    $w = pop(@a720);
    $v = pop(@a720);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
    ($v, $w) = (@a720[0, 1]);
    say(defined(uc($v)) ? (('[' . uc($v)) . ']') : 'undef');
}
my @a721;
{
    @a721 = (0, 1);
    my $v = $a721[0];
    my $w = $a721[1];
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    push(@a721, 0, 1);
    $w = pop(@a721);
    $v = pop(@a721);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    ($v, $w) = (@a721[0, 1]);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
}
{
    @a721 = ((-2.5), '12');
    my $v = $a721[0];
    my $w = $a721[1];
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    push(@a721, (-2.5), '12');
    $w = pop(@a721);
    $v = pop(@a721);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    ($v, $w) = (@a721[0, 1]);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
}
{
    @a721 = ('ab', (undef));
    my $v = $a721[0];
    my $w = $a721[1];
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    push(@a721, 'ab', (undef));
    $w = pop(@a721);
    $v = pop(@a721);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    ($v, $w) = (@a721[0, 1]);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
}
{
    @a721 = (1, ' 3 ');
    my $v = $a721[0];
    my $w = $a721[1];
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    push(@a721, 1, ' 3 ');
    $w = pop(@a721);
    $v = pop(@a721);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    ($v, $w) = (@a721[0, 1]);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
}
{
    @a721 = (3.0, 0);
    my $v = $a721[0];
    my $w = $a721[1];
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    push(@a721, 3.0, 0);
    $w = pop(@a721);
    $v = pop(@a721);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    ($v, $w) = (@a721[0, 1]);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
}
{
    @a721 = ("", 9007199254740992.0);
    my $v = $a721[0];
    my $w = $a721[1];
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    push(@a721, "", 9007199254740992.0);
    $w = pop(@a721);
    $v = pop(@a721);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    ($v, $w) = (@a721[0, 1]);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
}
{
    @a721 = ((-7), 9007199254740992);
    my $v = $a721[0];
    my $w = $a721[1];
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    push(@a721, (-7), 9007199254740992);
    $w = pop(@a721);
    $v = pop(@a721);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    ($v, $w) = (@a721[0, 1]);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
}
{
    @a721 = (9007199254740992.0, '3.0');
    my $v = $a721[0];
    my $w = $a721[1];
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    push(@a721, 9007199254740992.0, '3.0');
    $w = pop(@a721);
    $v = pop(@a721);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
    ($v, $w) = (@a721[0, 1]);
    say(defined($v ? $w : $v) ? (('[' . ($v ? $w : $v)) . ']') : 'undef');
}
my @a722;
{
    @a722 = (0, 1);
    my $v = $a722[0];
    my $w = $a722[1];
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    push(@a722, 0, 1);
    $w = pop(@a722);
    $v = pop(@a722);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    ($v, $w) = (@a722[0, 1]);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
}
{
    @a722 = (0.5, 9007199254740992);
    my $v = $a722[0];
    my $w = $a722[1];
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    push(@a722, 0.5, 9007199254740992);
    $w = pop(@a722);
    $v = pop(@a722);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    ($v, $w) = (@a722[0, 1]);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
}
{
    @a722 = ('3.0', (-9223372036854775807 - 1));
    my $v = $a722[0];
    my $w = $a722[1];
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    push(@a722, '3.0', (-9223372036854775807 - 1));
    $w = pop(@a722);
    $v = pop(@a722);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    ($v, $w) = (@a722[0, 1]);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
}
{
    @a722 = (0, 9223372036854775807);
    my $v = $a722[0];
    my $w = $a722[1];
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    push(@a722, 0, 9223372036854775807);
    $w = pop(@a722);
    $v = pop(@a722);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    ($v, $w) = (@a722[0, 1]);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
}
{
    @a722 = ((-2.5), '1e3');
    my $v = $a722[0];
    my $w = $a722[1];
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    push(@a722, (-2.5), '1e3');
    $w = pop(@a722);
    $v = pop(@a722);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    ($v, $w) = (@a722[0, 1]);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
}
{
    @a722 = ('1e3', "");
    my $v = $a722[0];
    my $w = $a722[1];
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    push(@a722, '1e3', "");
    $w = pop(@a722);
    $v = pop(@a722);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    ($v, $w) = (@a722[0, 1]);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
}
{
    @a722 = (0, 9007199254740992.0);
    my $v = $a722[0];
    my $w = $a722[1];
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    push(@a722, 0, 9007199254740992.0);
    $w = pop(@a722);
    $v = pop(@a722);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    ($v, $w) = (@a722[0, 1]);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
}
{
    @a722 = (0.5, ' 3 ');
    my $v = $a722[0];
    my $w = $a722[1];
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    push(@a722, 0.5, ' 3 ');
    $w = pop(@a722);
    $v = pop(@a722);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
    ($v, $w) = (@a722[0, 1]);
    say(defined(index($v, $w)) ? (('[' . index($v, $w)) . ']') : 'undef');
}
