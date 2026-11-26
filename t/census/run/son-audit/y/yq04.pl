use v5.42;
print scalar(@ARGV), defined $ARGV[0] ? "d" : "u", "\n";
