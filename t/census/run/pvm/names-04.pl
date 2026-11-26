use v5.42;
%::h = (a => 1, b => 2);
print scalar(keys %::h), "\n";
print $::h{a}, "\n";
