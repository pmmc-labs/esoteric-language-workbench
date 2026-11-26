use v5.42;
open(my $out, ">", \my $buf);
print $out "captured\n";
close($out);
print $buf;
