use v5.42;
our $g=1; sub r { return ($g, $g++) } print r(), "\n";
