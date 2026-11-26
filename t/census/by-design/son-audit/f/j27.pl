use v5.42;
my @a; sub noop {} noop($a[3]); noop(@a[0,1]); print scalar(@a),"\n";
