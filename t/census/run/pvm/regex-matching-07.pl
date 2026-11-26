use v5.42;
my $s = "key=value";
$s =~ /(\w+)=(\w+)/;
print "$2 $1\n";
