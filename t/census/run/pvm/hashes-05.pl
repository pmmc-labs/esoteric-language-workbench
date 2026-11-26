use v5.42;
my %h = (a => 1, b => 2, c => 3);
delete @h{"a", "b"};
print scalar(keys %h), "\n";
print( (@h{"c"}), "\n");
