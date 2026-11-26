use v5.42;
sub f { return reverse "abc" } sub g { scalar reverse "abc" } print f(), g(), scalar(f()), "\n";
