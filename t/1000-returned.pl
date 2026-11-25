# model: t/models/ret.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a1 = (4, 5, 6);
my @e1;
my @r1;
sub one1() {
    return 7;
}
sub none1() {
    return;
}
sub r0_1() {
    return @a1;
}
sub l0_1() {
    @a1;
}
@a1 = (4, 5, 6);
@r1 = (r0_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l0_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r1_1() {
    return (1, 2, 3);
}
sub l1_1() {
    (1, 2, 3);
}
@a1 = (4, 5, 6);
@r1 = (r1_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l1_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r2_1() {
    return ();
}
sub l2_1() {
    ();
}
@a1 = (4, 5, 6);
@r1 = (r2_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l2_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r3_1() {
    return (@a1, 9);
}
sub l3_1() {
    (@a1, 9);
}
@a1 = (4, 5, 6);
@r1 = (r3_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l3_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r4_1() {
    return 2 .. 5;
}
sub l4_1() {
    2 .. 5;
}
@a1 = (4, 5, 6);
@r1 = (r4_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l4_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r5_1() {
    return @a1[2, 0];
}
sub l5_1() {
    @a1[2, 0];
}
@a1 = (4, 5, 6);
@r1 = (r5_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l5_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r6_1() {
    return (@a1, 8)[3, 0];
}
sub l6_1() {
    (@a1, 8)[3, 0];
}
@a1 = (4, 5, 6);
@r1 = (r6_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l6_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r7_1() {
    return ('x', 'y') x 2;
}
sub l7_1() {
    ('x', 'y') x 2;
}
@a1 = (4, 5, 6);
@r1 = (r7_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l7_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r8_1() {
    return reverse(@a1);
}
sub l8_1() {
    reverse(@a1);
}
@a1 = (4, 5, 6);
@r1 = (r8_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l8_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r9_1() {
    return reverse(1, @a1, 2);
}
sub l9_1() {
    reverse(1, @a1, 2);
}
@a1 = (4, 5, 6);
@r1 = (r9_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l9_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r10_1() {
    return (@e1, @e1);
}
sub l10_1() {
    (@e1, @e1);
}
@a1 = (4, 5, 6);
@r1 = (r10_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l10_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r11_1() {
    return 1 ? @a1 : 0;
}
sub l11_1() {
    1 ? @a1 : 0;
}
@a1 = (4, 5, 6);
@r1 = (r11_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l11_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r12_1() {
    return 0 ? @a1 : 0;
}
sub l12_1() {
    0 ? @a1 : 0;
}
@a1 = (4, 5, 6);
@r1 = (r12_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l12_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r13_1() {
    return 0 || @a1;
}
sub l13_1() {
    0 || @a1;
}
@a1 = (4, 5, 6);
@r1 = (r13_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l13_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r14_1() {
    return 3 || @a1;
}
sub l14_1() {
    3 || @a1;
}
@a1 = (4, 5, 6);
@r1 = (r14_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l14_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r15_1() {
    return (undef) // (1, 2);
}
sub l15_1() {
    (undef) // (1, 2);
}
@a1 = (4, 5, 6);
@r1 = (r15_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l15_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r16_1() {
    return 1 && (8, 9);
}
sub l16_1() {
    1 && (8, 9);
}
@a1 = (4, 5, 6);
@r1 = (r16_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l16_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r17_1() {
    return +@a1;
}
sub l17_1() {
    +@a1;
}
@a1 = (4, 5, 6);
@r1 = (r17_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l17_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r18_1() {
    return $a1[1];
}
sub l18_1() {
    $a1[1];
}
@a1 = (4, 5, 6);
@r1 = (r18_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l18_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r19_1() {
    return (undef);
}
sub l19_1() {
    (undef);
}
@a1 = (4, 5, 6);
@r1 = (r19_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l19_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r20_1() {
    return ((undef), (undef));
}
sub l20_1() {
    ((undef), (undef));
}
@a1 = (4, 5, 6);
@r1 = (r20_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l20_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r21_1() {
    return one1();
}
sub l21_1() {
    one1();
}
@a1 = (4, 5, 6);
@r1 = (r21_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l21_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r22_1() {
    return none1();
}
sub l22_1() {
    none1();
}
@a1 = (4, 5, 6);
@r1 = (r22_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l22_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r23_1() {
    return (none1(), one1(), none1());
}
sub l23_1() {
    (none1(), one1(), none1());
}
@a1 = (4, 5, 6);
@r1 = (r23_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l23_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r24_1() {
    return $a1[0] + 1;
}
sub l24_1() {
    $a1[0] + 1;
}
@a1 = (4, 5, 6);
@r1 = (r24_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l24_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r25_1() {
    return ((1, (2)), 3);
}
sub l25_1() {
    ((1, (2)), 3);
}
@a1 = (4, 5, 6);
@r1 = (r25_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l25_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r26_1() {
    return @e1;
}
sub l26_1() {
    @e1;
}
@a1 = (4, 5, 6);
@r1 = (r26_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l26_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r27_1() {
    return splice(@a1, 1, 1);
}
sub l27_1() {
    splice(@a1, 1, 1);
}
@a1 = (4, 5, 6);
@r1 = (r27_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l27_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub r28_1() {
    return join('-', @a1);
}
sub l28_1() {
    join('-', @a1);
}
@a1 = (4, 5, 6);
@r1 = (r28_1());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@a1 = (4, 5, 6);
@r1 = (0, l28_1(), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
sub three2() {
    return (1, 2, 3);
}
sub pair2($p) {
    return ($p, ($p * 2));
}
sub none2() {
    return ();
}
sub count2($p = '-', $q = '-', $r = '-', $s = '-') {
    return (((defined($p) ? (('[' . $p) . ']') : 'undef') . (defined($q) ? (('[' . $q) . ']') : 'undef')) . (defined($r) ? (('[' . $r) . ']') : 'undef')) . (defined($s) ? (('[' . $s) . ']') : 'undef');
}
my @a2 = (0);
my @r2;
say(three2());
say('[', three2(), '|', pair2(5), '|', none2(), ']');
say(three2());
say(none2());
my ($x2, $y2) = (three2());
say($x2 . $y2);
($y2, undef, $x2, @r2) = (pair2(5), three2(), none2(), pair2(5));
say($x2 . $y2);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
($x2, $y2) = (none2());
say(defined($x2) ? (('[' . $x2) . ']') : 'undef');
say(defined($y2) ? (('[' . $y2) . ']') : 'undef');
push(@a2, three2(), pair2(5));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
unshift(@a2, none2());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
splice(@a2, 1, 2, pair2(5));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
for my $v (three2(), none2(), pair2(5)) {
    say('v', $v);
}
for my $v (none2()) {
    say('never');
}
say(count2(three2()));
say(count2(pair2(5), pair2(5)));
say(count2(none2()));
say(count2(0, none2(), three2()));
say((three2())[1]);
say((three2(), pair2(5))[4, 0]);
say(((pair2(5)) x 2));
say(reverse(three2(), pair2(5)));
@r2 = (@a2[pair2(5)]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((1 .. (pair2(5))[0]));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((1 ? three2() : pair2(5)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((0 || pair2(5)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
three2();
none2();
pair2(5);
my @r3;
sub two3() {
    return ('a', 'b');
}
sub pass3() {
    return two3();
}
sub last3() {
    two3();
}
sub both3() {
    return (pass3(), last3());
}
sub pick3($p) {
    return $p ? two3() : 'z';
}
sub upto3($p) {
    return () if $p == 0;
    return (upto3(($p - 1)), $p);
}
sub walk3($p) {
    my @mine = (upto3($p));
    push(@mine, 0);
    return @mine;
}
sub early3($p) {
    for my $v (upto3(5)) {
        return ($v, $v) if $v == $p;
    }
    return ();
}
@r3 = (pass3());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
@r3 = (last3());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
@r3 = (both3());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
@r3 = (pick3(1));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
@r3 = (pick3(0));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
say(('<' . pick3(0)) . '>');
@r3 = (upto3(6));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
@r3 = (upto3(0));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
@r3 = (walk3(3), walk3(1));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
@r3 = (early3(3));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
@r3 = (early3(9));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
@r3 = (reverse(upto3(4)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
my @a4 = (1, 2, 3);
my @r4;
sub all4() {
    return @a4;
}
sub grown4() {
    push(@a4, 9);
    return @a4;
}
@r4 = (all4());
$r4[0] = 'r';
$a4[1] = 'a';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r4) {
        $dump_s .= (defined($r4[$dump_i]) ? (('<' . $r4[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r4) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a4) {
        $dump_s .= (defined($a4[$dump_i]) ? (('<' . $a4[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a4) . ':') . $dump_s);
}
@a4 = (grown4(), grown4());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a4) {
        $dump_s .= (defined($a4[$dump_i]) ? (('<' . $a4[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a4) . ':') . $dump_s);
}
@a4 = (reverse(all4()));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a4) {
        $dump_s .= (defined($a4[$dump_i]) ? (('<' . $a4[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a4) . ':') . $dump_s);
}
for my $v (all4()) {
    push(@a4, $v);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a4) {
        $dump_s .= (defined($a4[$dump_i]) ? (('<' . $a4[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a4) . ':') . $dump_s);
}
my @a5 = (4, 5, 6);
sub seven5() {
    return (7);
}
sub empty5() {
    return ();
}
sub elem5() {
    return $a5[1];
}
sub of5() {
    return (@a5)[2];
}
sub count5() {
    return scalar(@a5);
}
sub or5($p) {
    return @a5 || $p;
}
sub joined5() {
    return join(',', @a5);
}
sub pushed5() {
    push(@a5, 1);
}
my $x5 = seven5();
say($x5);
say(defined(empty5()) ? (('[' . empty5()) . ']') : 'undef');
say(elem5() + of5());
say((count5() . or5(0)) . joined5());
if (empty5()) {
    say('never');
} elsif (seven5()) {
    say('seven');
}
say($a5[count5() - 1]);
say(pushed5());
