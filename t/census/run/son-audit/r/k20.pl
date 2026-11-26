use v5.42;
sub f { my %o=(v=>1); my %c=%o; $c{v}=2; return $o{v} } print f(),"\n";
