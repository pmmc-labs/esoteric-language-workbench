# kind: fault
# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @u = (3, (undef), 1);
    my @r = ((sort { ($a // 0) <=> ($b // 0) } (@u)));
    @u = (reverse((sort { ($a // 0) <=> ($b // 0) } (@u))));
    {
        my $dump_i = 0;
        my $dump_s = "";
        while ($dump_i < @u) {
            $dump_s .= (defined($u[$dump_i]) ? (('<' . $u[$dump_i]) . '>') : '<undef>');
            $dump_i++;
        }
        say((scalar(@u) . ':') . $dump_s);
    }
}
{
    my @u = (3, (undef), 1);
    @u = ((sort { ($a // 0) <=> ($b // 0) } (@u)));
}
say(2);
