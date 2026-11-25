# kind: fault
# model: t/models/it.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    say($_) for (@a);
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
    my @a = (1, 2, 3);
    $a[0] = 9 for (@a);
}
say(2);
