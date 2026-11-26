use v5.42;
my $x = 1;
{
  my $x = 2;
  print "$x\n";
}
print "$x\n";
