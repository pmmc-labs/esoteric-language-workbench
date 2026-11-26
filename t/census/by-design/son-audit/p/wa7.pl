use v5.42;
my @a = (1,2); sub cnt { scalar @a } @a = (1,2,3); print cnt(), "\n";
