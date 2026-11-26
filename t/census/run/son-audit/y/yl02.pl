use v5.42;
"q" =~ /(q)/; { "x" =~ /(x)/; print $1 } print $1, "\n";
