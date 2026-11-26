use v5.42;
my $x = 1;
{
  my $x = 2;
  print "in $x\n";
}
print "out $x\n";
{
  print "again\n";
}
