# kind: fault
# model: t/models/it.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    my @r = ((map { my $t = 6 / $_; $t } (@a)));
}
{
    my @a = (1, 2, 3);
    my @r = ((map { my $t = 6 / ($_ - 2); $t } (@a)));
}
say(2);
