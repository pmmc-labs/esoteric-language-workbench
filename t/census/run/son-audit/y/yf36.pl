use v5.42;
my %h; $h{a}{b}{c}++; $h{a}{b}{c}++; print join(",", keys %{$h{a}}), $h{a}{b}{c}, "\n";
