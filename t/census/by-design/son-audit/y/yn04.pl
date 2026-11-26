use v5.42;
eval { eval { die "in\n" }; die "re:$@" if $@; }; print $@;
