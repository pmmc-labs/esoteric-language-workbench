use v5.42;
my $a = $ENV{X} // 12;
print ~$a & 255, "\n";
