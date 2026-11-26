use v5.42;
"ab"=~/(?<n>a)/; my $v=$+{n}; "b"=~/(?<n>b)/; print "$v$+{n}\n";
