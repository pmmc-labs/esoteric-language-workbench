use v5.42;
my $s = $ENV{X} // "hello world";
my $first = index($s, "o");
my $next = index($s, "o", $first + 1);
my $none = index($s, "z");
print "[$first][$next][$none]\n";
