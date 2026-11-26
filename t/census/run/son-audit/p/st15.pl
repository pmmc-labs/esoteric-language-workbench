use v5.42;
my $o = {}; if (@ARGV) { bless $o, "K" } my $a = ref($o); bless $o, "J"; print "$a ", ref($o), "\n";
