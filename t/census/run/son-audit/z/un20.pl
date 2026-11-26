use v5.42;
eval { die { code=>5 } }; print $@->{code}, "\n";
