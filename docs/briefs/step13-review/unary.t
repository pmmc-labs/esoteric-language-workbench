### defined-postfix-array
my $r = [1]; say defined $r->@* ? "y" : "n";
### defined-braces-array
my $r = [1]; say defined(@{ $r }) ? "y" : "n";
### defined-postfix-hash
my $r = {a => 1}; say defined $r->%* ? "y" : "n";
### length-postfix-array
my $r = [1, 2, 3]; say length($r->@*);
### length-braces-hash
my $r = {a => 1}; say length(%{ $r });
### ref-postfix-array
my $r = [[1]]; say ref($r->@*);
### ref-postfix-array-two
my $r = [[1], 5]; say ref($r->@*);
### uc-postfix-array
my $r = ["a", "b"]; say uc($r->@*);
### chr-postfix-array
my $r = [65, 66]; say chr($r->@*);
### ord-lastidx
my $r = [65, 66]; say ord($r->$#*);
### ref-slice
my $r = [[1], 5]; say ref($r->@[0, 1]) || "empty";
### scalar-slice-postfix
my $r = [7, 8]; my $x = $r->@[0, 1]; say $x;
### keys-elem-hash
my $r = {a => {b => 1}}; say scalar(keys $r->{a}->%*);
### ref-keys
my $r = {a => 1}; say ref(keys $r->%*) || "empty";
