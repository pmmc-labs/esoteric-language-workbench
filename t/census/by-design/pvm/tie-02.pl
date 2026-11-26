use v5.42;
package Counter;
sub TIESCALAR { return bless {}, "Counter" }
sub FETCH { return 42 }
package main;
tie my $x, $ENV{X} // "Counter";
my $plain = 1;
print tied($x) ? "t" : "u", tied($plain) ? "t" : "u", "\n";
