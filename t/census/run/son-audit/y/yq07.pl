use v5.42;
print $^O eq "linux" ? "linux" : "other", $] >= 5.042 ? "new" : "old", "\n";
