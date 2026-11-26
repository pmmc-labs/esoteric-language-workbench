use v5.42;
use feature "state";
our $g = 1;
my $x = 2;
state $s = 3;
{
  local $g = $g + 10;
  my $x = $x * 2;
  state $s = $s + 100;
  print "$g $x $s\n";
}
print "$g $x $s\n";
