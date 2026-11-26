use v5.42;
my @a=("a"); for ($a[0] .= "b") { $_ .= "!" } print "@a\n";
