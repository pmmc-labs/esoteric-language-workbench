# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2);
    @a[(-2), 0] = (5, 6);
    {
        my $dump_i = 0;
        my $dump_s = "";
        while ($dump_i < @a) {
            $dump_s .= (defined($a[$dump_i]) ? (('<' . $a[$dump_i]) . '>') : '<undef>');
            $dump_i++;
        }
        say((scalar(@a) . ':') . $dump_s);
    }
}
{
    my @a = (1, 2);
    @a[0, (-3)] = (5, 6);
    {
        my $dump_i = 0;
        my $dump_s = "";
        while ($dump_i < @a) {
            $dump_s .= (defined($a[$dump_i]) ? (('<' . $a[$dump_i]) . '>') : '<undef>');
            $dump_i++;
        }
        say((scalar(@a) . ':') . $dump_s);
    }
}
say(2);
