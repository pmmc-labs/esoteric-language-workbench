use v5.42;
my $a = "abc" =~ m{abc};
my $b = "abc" =~ m!abc!;
my $s = "abc";
$s =~ s{a}{z};
print "$a$b$s\n";
