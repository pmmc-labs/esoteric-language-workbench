use v5.42;
eval { die }; print $@ =~ /^Died/ ? "d" : "n", "\n";
