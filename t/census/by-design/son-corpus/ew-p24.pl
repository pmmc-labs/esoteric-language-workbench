use v5.42;
our $s = "a"; sub app { $s = $s . "b" } app(); app(); print "$s\n";
