use v5.42;
my $s = "ab12"; $s =~ s/(\d)/<$1>/; print "$s\n";
