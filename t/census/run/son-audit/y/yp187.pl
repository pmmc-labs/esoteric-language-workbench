use v5.42;
our $g="ab"; sub t { $g =~ tr/a/z/ } print $g . t() . $g, "\n";
