# kind: fault
# perl gives the capital E with an acute, by its tables (titlecase).
use v5.42;
use utf8;
use open ":std", ":encoding(UTF-8)";
say ucfirst("aé");
say ucfirst("éa");
