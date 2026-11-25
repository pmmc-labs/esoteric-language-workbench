use v5.42;
# What the program can reach at the end is $n, an Int. What the frame
# still holds: $big's slot, which no later block declares a variable in,
# and t2 of line 10, which no later statement has as many
# temporaries as to overwrite.
my $n = 0;
my $i = 0;
{
    my $big = "x" x 300000;
    $n = length(("y" x 300000) . $big) + 0;
}
while ($i < 3) { $i++; }
say $n;
