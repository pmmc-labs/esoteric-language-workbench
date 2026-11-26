use v5.42;
use feature "state";
state $n = 1;
{
  state $n = 2;
  print "$n\n";
}
print "$n\n";
