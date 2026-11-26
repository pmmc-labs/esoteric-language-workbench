use v5.42;
$_=1; sub f { local $_=5; $_[0] } print f($_), "\n";
