use v5.42;
eval { $@ = "preset\n"; die }; print $@ =~ /^preset\n\t\.\.\.propagated/ ? "prop" : "other", "\n";
