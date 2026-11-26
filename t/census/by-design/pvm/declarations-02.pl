use v5.42;
our $x = 1;
{
  my $x = 2;
  print "$x $main::x\n";
}
print "$x\n";
