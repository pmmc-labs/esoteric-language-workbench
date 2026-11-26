use v5.42;
my $a = "abc" =~ m#abc#;
my $s = "abc";
$s =~ s#a#z#;
print "$a$s\n";
