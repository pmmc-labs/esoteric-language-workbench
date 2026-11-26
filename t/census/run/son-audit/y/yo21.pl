use v5.42;
use Term::ANSIColor; print length(color("red")), length(colored("x", "bold")), color("reset") eq "\e[0m" ? "reset" : "other", "\n";
