# kind: fault
# perl gives a small e with an acute, then a.
use v5.42;
use utf8;
use open ":std", ":encoding(UTF-8)";
say lcfirst("Éa");
