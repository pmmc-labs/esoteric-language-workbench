use v5.42;
my $s = $ENV{X} // "  a b ";
my @pat = split / /, $s;
my @str = split " ", $s;
print scalar(@pat), " [@pat] ", scalar(@str), " [@str]\n";
