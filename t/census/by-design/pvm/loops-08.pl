use v5.42;
my $n = $ENV{N} // 5;
my $i = 0;
my @s;
while ($i < $n) {
    $i = $i + 1;
    next if $i == 2;
    last if $i == 4;
    push @s, "b$i";
} continue {
    push @s, "c$i";
}
print "@s\n";
