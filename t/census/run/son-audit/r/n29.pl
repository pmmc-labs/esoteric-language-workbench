use v5.42;
my %o=(k=>"v"); my %copy=%o; $copy{k}=uc $copy{k}; print "$o{k} $copy{k}\n";
