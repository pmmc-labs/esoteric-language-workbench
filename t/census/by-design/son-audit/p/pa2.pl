use v5.42;
our @g = (1); print @g ? "t" : "f"; shift @g; print @g ? "t" : "f", "\n";
