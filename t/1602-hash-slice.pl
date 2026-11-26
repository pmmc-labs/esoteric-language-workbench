# kind: refused
# perl: 1 2. Step 12b (D100).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my @v = @h{"a", "b"};
say "@v";
