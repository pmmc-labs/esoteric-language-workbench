use v5.42;
"ab"=~/(a)(b)/; "c"=~/(c)/; print defined $2 ? 1 : 0, "\n";
