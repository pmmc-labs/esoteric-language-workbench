use v5.42;
$x = 1;
{
  local $x = 2;
  print "$x\n";
}
print "$x\n";
