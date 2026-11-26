use v5.42;
sub twice { return $_[0] * 2 }
sub one ($) { return $_[0] }
my @a = (10, 20);
my %h = (k => 1);
my $s = \@a;
my $hr = \%h;
my @r = \(@a);
my $l = [30, 40];
my $c = \&twice;
my $proto = prototype \&one;
my @at = @{$s};
my @sig = @$s;
my @post = $s->@*;
my %copy = %{$hr};
print ref($s), " ", $$s[0], " ", ${$r[1]}, " ", $l->[0], " ", ${$l}[1], " ", $c->(21), "\n";
print $at[0], " ", $sig[1], " ", $post[0], " ", $copy{k}, " ", $proto, "\n";
