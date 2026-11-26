use v5.42;
# N2: what in today's compiler stands on a string being a plain token
# (lexer.ts afterValue, parser.ts T175 and `undef`), with an interpolated one.
my $x = 5; my @a = (1, 2);
say "$x" -1;                 # 4: an operator after the string, not the number -1
say "$x" .5;                 # 55
say "$x" x 3;                # 555
say "$x"x 3;                 # 555
say "@a" . "!" x 2;          # 1 2!!
sub f() { return "@a" }      # one value, not a list (shapes.ts)
sub g() { "@a[0, 1]" }
my $s = f(); my $t = g(); say "$s|$t";
say scalar("@a"), "|", "@a" . @a, "|", length "@a";   # 1 2|1 22|3
my @r = map { "$_"; } @a;   say "@r";
@r = map { ("$_", 1) } @a;  say "@r";
