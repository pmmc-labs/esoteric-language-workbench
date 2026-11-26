use v5.42;
use Unicode::Normalize; use utf8; print length(NFD("\x{e9}")), "\n";
