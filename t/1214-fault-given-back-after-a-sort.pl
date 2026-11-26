# kind: fault
# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (3, 1, 2);
    my @r = ((sort { $a <=> $b } (@a)));
    $a[0] = 9;
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
    my @a = (3, 1, 2);
    my @r = ((sort { $a[0] = 9; $a <=> $b } (@a)));
}
say(2);
