use v5.42;
my %h = (a => 1, b => 2);
my $r = \%h;
my %copy = %{$r};
print scalar(keys %copy), " ", ${$r}{a}, "\n";
