use v5.42;
# each row: label, code string evaluated on a fresh @a = (1..5)
my @rows = (
 'splice(@a)', 'splice(@a, 1)', 'splice(@a, -2)', 'splice(@a, 5)', 'splice(@a, 6)', 'splice(@a, -5)', 'splice(@a, -6)',
 'splice(@a, 1, 2)', 'splice(@a, 1, 0)', 'splice(@a, 1, 99)', 'splice(@a, 1, -1)', 'splice(@a, 1, -4)', 'splice(@a, 1, -5)', 'splice(@a, 1, -99)',
 'splice(@a, -2, 1)', 'splice(@a, -2, -1)', 'splice(@a, -2, -3)', 'splice(@a, 5, 1)', 'splice(@a, 5, -1)', 'splice(@a, 6, 0)', 'splice(@a, 0, 0)',
 'splice(@a, 1.7, 1.7)', 'splice(@a, -1.7, 1)', 'splice(@a, "1", "2")', 'splice(@a, true, true)', 'splice(@a, false)', 'splice(@a, undef)', 'splice(@a, 1, undef)', 'splice(@a, 0, 1, undef)',
 'splice(@a, 1, 1, 7, 8)', 'splice(@a, 1, 0, 7, 8)', 'splice(@a, 5, 0, 7)', 'splice(@a, 6, 0, 7)', 'splice(@a, -1, 0, 7)', 'splice(@a, 0, 1, @a)', 'splice(@a, 1, 1, $a[0])', 'splice(@a, $#a, 1, shift(@a))',
 'splice(@a, 1, 2, ())', 'splice(@a, 1e30)', 'splice(@a, 0, 1e30)', 'splice(@a, -1e30)', 'splice(@a, 0, -1e30)', 'splice(@a, "abc")', 'splice(@a, 1, "")', 'splice(@a, 2**31)', 'splice(@a, 0, 9223372036854775807)', 'splice(@a, 1, -9223372036854775807 - 1)','splice(@a, -9223372036854775807 - 1)', 'splice(@a, 2, 0.9)', 'splice(@a, 4.99)', 'splice(@a, 5.5)', 'splice(@a, -0.5)', 'splice(@a, -5.5)',
);
for my $r (@rows) {
  my @a = (1..5); my @w;
  local $SIG{__WARN__} = sub { push @w, $_[0] =~ s/ at .*//sr };
  my @got = eval $r; my $err = $@ =~ s/ at .*//sr;
  say sprintf("%-42s got (%s) left (%s)%s%s", $r, join(",", map { $_ // "u" } @got), join(",", map { $_ // "u" } @a), @w ? " WARN: @w" : "", $err ? " DIES: $err" : "");
}
