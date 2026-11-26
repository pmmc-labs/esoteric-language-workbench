use v5.42;
my @a=(1,2); sub j { local $"=$_[0]; "@a" } print j("+"), "@a\n";
