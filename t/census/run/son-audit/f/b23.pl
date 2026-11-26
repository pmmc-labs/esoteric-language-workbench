use v5.42;
my %h; $h{a}{b}{c}=1; print join(",",keys %{$h{a}}),"\n";
