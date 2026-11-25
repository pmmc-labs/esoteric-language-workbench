# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a201 = (1, 2);
my @b201 = ('x');
my @e201;
my @c201 = (0, (1, (2, 3)), @a201, @e201, @b201, (), 9);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @c201) {
        $dump_s .= (defined($c201[$dump_i]) ? (('<' . $c201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@c201) . ':') . $dump_s);
}
my @d201 = ((((7))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @d201) {
        $dump_s .= (defined($d201[$dump_i]) ? (('<' . $d201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@d201) . ':') . $dump_s);
}
my @h201 = (@e201, @e201);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @h201) {
        $dump_s .= (defined($h201[$dump_i]) ? (('<' . $h201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@h201) . ':') . $dump_s);
}
say(1, 2, 3);
say(@a201);
say('x', @a201, 'y');
say(@e201);
say(@a201, @a201);
say((@a201, 5), ':', scalar(@a201));
say($a201[0], '-', $a201[1]);
my @r202;
my $n202 = 3;
@r202 = ((1 .. 5));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((3 .. 1));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((0 .. 0));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = (((-2) .. 2));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((1.9 .. 4.1));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = (((-1.9) .. 1.9));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((false .. true));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((1 .. $n202));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((($n202 - 1) .. ($n202 * 2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((9223372036854775806 .. 9223372036854775807));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = (((-9223372036854775807 - 1) .. (-9223372036854775807)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((5 .. 4));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((2.0 .. 4.0));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = (((-0.0) .. 1));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = (0, (2 .. 3), (7 .. 8));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
say((1 .. 9));
@r202 = ((1 .. @r202));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((0 .. $#r202));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
my @a203 = (10, 20, 30, 40);
my @s203;
my @i203 = (0, 2);
my @e203;
@s203 = (@a203[1, 2]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = (@a203[(1 .. 3)]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = (@a203[(-1), 0]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = (@a203[5, 1]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = (@a203[@i203]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = (@a203[0, 0, 0]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = (@a203[(-5), (-4)]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = (@a203[3, 2, 1, 0]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = (@a203[@e203]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = (@a203[1.9, '2']);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = (@a203[@i203, (0 .. 1)]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = (@a203[(0)]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = (@a203[0, (1, 2)]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = ((10, 20, 30)[1]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = ((10, 20, 30)[0, 2]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = ((@a203, 9)[4]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = (((1 .. 5))[(-1)]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = ((@a203)[9, 10]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = ((@a203)[1, 9]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = ((@e203)[0, 1]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = ((@e203)[0]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = (()[0, 1]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = ((1, 2, 3)[5, 6]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = ((1, 2, 3)[5]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
@s203 = ((@a203)[@i203]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @s203) {
        $dump_s .= (defined($s203[$dump_i]) ? (('<' . $s203[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@s203) . ':') . $dump_s);
}
say((10, 20, 30)[1]);
say((@a203)[(-1)] + 1);
say(defined((@e203)[0]) ? (('[' . (@e203)[0]) . ']') : 'undef');
say(defined((@a203)[9]) ? (('[' . (@a203)[9]) . ']') : 'undef');
my @r204;
my @a204 = (1, 2);
@r204 = (((0) x 3));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r204) {
        $dump_s .= (defined($r204[$dump_i]) ? (('<' . $r204[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r204) . ':') . $dump_s);
}
@r204 = (((1, 2) x 2));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r204) {
        $dump_s .= (defined($r204[$dump_i]) ? (('<' . $r204[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r204) . ':') . $dump_s);
}
@r204 = (((@a204) x 2));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r204) {
        $dump_s .= (defined($r204[$dump_i]) ? (('<' . $r204[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r204) . ':') . $dump_s);
}
@r204 = ((('a') x 0));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r204) {
        $dump_s .= (defined($r204[$dump_i]) ? (('<' . $r204[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r204) . ':') . $dump_s);
}
@r204 = (((@a204, 'x') x 1));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r204) {
        $dump_s .= (defined($r204[$dump_i]) ? (('<' . $r204[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r204) . ':') . $dump_s);
}
@r204 = ((() x 3));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r204) {
        $dump_s .= (defined($r204[$dump_i]) ? (('<' . $r204[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r204) . ':') . $dump_s);
}
@r204 = (((5) x 2.9));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r204) {
        $dump_s .= (defined($r204[$dump_i]) ? (('<' . $r204[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r204) . ':') . $dump_s);
}
@r204 = (((5) x '2'));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r204) {
        $dump_s .= (defined($r204[$dump_i]) ? (('<' . $r204[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r204) . ':') . $dump_s);
}
@r204 = (((5) x true));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r204) {
        $dump_s .= (defined($r204[$dump_i]) ? (('<' . $r204[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r204) . ':') . $dump_s);
}
@r204 = (((5) x false));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r204) {
        $dump_s .= (defined($r204[$dump_i]) ? (('<' . $r204[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r204) . ':') . $dump_s);
}
@r204 = ((((1 .. 3)) x 2));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r204) {
        $dump_s .= (defined($r204[$dump_i]) ? (('<' . $r204[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r204) . ':') . $dump_s);
}
@r204 = (('ab' x 2));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r204) {
        $dump_s .= (defined($r204[$dump_i]) ? (('<' . $r204[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r204) . ':') . $dump_s);
}
say((('-') x 5));
@r204 = (((0) x @a204));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r204) {
        $dump_s .= (defined($r204[$dump_i]) ? (('<' . $r204[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r204) . ':') . $dump_s);
}
