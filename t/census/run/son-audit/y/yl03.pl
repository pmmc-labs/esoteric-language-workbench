use v5.42;
if ("ab" =~ /(a)/) { } print defined $1 ? $1 : "u", "\n";
