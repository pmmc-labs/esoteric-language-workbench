use v5.42;
my $o=bless {}, 'A'; my $r=ref $o; bless $o, 'B'; print $r, ref $o, "\n";
