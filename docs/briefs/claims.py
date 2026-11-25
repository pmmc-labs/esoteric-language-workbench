#!/usr/bin/env python3
"""Every statement these documents make about what perl does, as a program
and what the document says of it, run under a perl and compared.

Step 0 wrote it to rerun under perl 5.42 what had been run under 5.38.2
(`docs/PLAN.md`, step 0). It is a record and a tool, not a test: nothing in
`make test` runs it. A document that gains a "perl prints" gains a row
here, and a new perl is met by running this first:

    python3 docs/briefs/claims.py                      # $CURLY_PERL, `use v5.42;`
    python3 docs/briefs/claims.py --perl perl --old    # the machine's 5.38.2

Each row is (id, where it is said, the program, what is said). What is
said is some of:

    out      perl's stdout, exactly
    outre    a pattern perl's whole stdout matches
    err      'none' (the default): nothing on stderr. 'some': something.
             Or a pattern found in it.
    exit     0 (the default), or the status, or 'nonzero'
    compiles False: `perl -c` fails, and err is searched in what it says
    raw      True: the program is the whole file, its first line included
    csda     True: perl is run with -CSDA, its streams UTF-8, as the oracle
             ran it before D39. What is said is then said of that.
    outbytes perl's stdout, exactly, as bytes: for a claim about encoding

The program is given `use v5.42;` (with --old, `use v5.38;` and the
experimental features 5.42 has since made stable), and perl is run as the
oracle runs it: plain, one hash seed, empty stdin.
"""

import os
import re
import subprocess
import sys
import tempfile

NEW = 'use v5.42;\n'
OLD = "use v5.38; use experimental qw(try builtin for_list);\n"

def c(id, where, code, **said):
    return (id, where, code, said)

CLASS = "use experimental 'class';\n"

CLAIMS = [
    # ---- TRAPS.md: reading and evaluating
    c('T1', 'TRAPS', 'my $total = 5; sub step() { $total += 100; return 1 } say $total + step();', out='106\n'),
    c('T2', 'TRAPS', 'my %c = (n => 0); sub inc() { $c{n}++; return $c{n} } say join ",", $c{n}, inc(), $c{n};', out='1,1,1\n'),
    c('T3', 'TRAPS', 'my $n = 0; my @s = sort { $n++; $a <=> $b } (5,3,8,1,9,2,7); say $n;', out='14\n'),
    c('T4', 'TRAPS', 'say join ",", sort { length($a) <=> length($b) } qw(bb a ccc dd e fff);', out='a,e,bb,dd,ccc,fff\n'),
    # ---- aliases
    c('T5', 'TRAPS', 'my @a=(1,2,3); for my $x (@a) { $a[0] = 9; say $x }', out='9\n2\n3\n'),
    c('T6', 'TRAPS', 'my @a=(3,1,2); for my $x (sort { $a <=> $b } @a) { $a[0]=7; $a[1]=7; $a[2]=7; say $x }', out='7\n7\n7\n'),
    c('T6-grep', 'TRAPS', 'my @a=(3,1,2); for my $x (grep { 1 } @a) { $a[0]=7; $a[1]=7; $a[2]=7; say $x }', out='7\n7\n7\n'),
    c('T6-reverse', 'TRAPS', 'my @a=(3,1,2); for my $x (reverse @a) { $a[0]=7; $a[1]=7; $a[2]=7; say $x }', out='7\n7\n7\n'),
    c('T6-slice', 'TRAPS', 'my @a=(3,1,2); for my $x (@a[0,1,2]) { $a[0]=7; $a[1]=7; $a[2]=7; say $x }', out='7\n7\n7\n'),
    c('T6-ternary', 'TRAPS', 'my @a=(3,1,2); my $c = 1; for my $x ($c ? @a : ()) { $a[0]=7; $a[1]=7; $a[2]=7; say $x }', out='7\n7\n7\n'),
    c('T6-two', 'TRAPS', 'my @a=(3,1); my @b=(2); for my $x (@a, @b) { $a[0]=7; $a[1]=7; $b[0]=7; say $x }', out='7\n7\n7\n'),
    c('T6-elements', 'TRAPS', 'my @a=(3,1); for my $x ($a[0], $a[1]) { $a[0]=7; $a[1]=7; say $x }', out='7\n7\n'),
    c('T7', 'TRAPS', 'my %h=(a=>1); for my $v (values %h) { $h{a} = 9; say $v }', out='9\n'),
    c('T7-hash', 'TRAPS', 'my %h=(a=>1); for my $v (%h) { $h{a} = 9; say $v }', out='a\n9\n'),
    c('T7-slice', 'TRAPS', 'my %h=(a=>1,b=>2); for my $v (@h{"a","b"}) { $h{a} = 9; $h{b} = 9; say $v }', out='9\n9\n'),
    c('T7-keys', 'TRAPS; D17', 'my %h=(a=>1); for my $k (keys %h) { $h{$k}++ } say $h{a};', out='2\n'),
    c('T8', 'TRAPS', 'my @a=(1,2,3); say join ",", map { $a[2] = 8; $_ } grep { 1 } @a;', out='1,2,8\n'),
    c('T9', 'TRAPS', 'my @a=("ab","cd"); for my $x (@a) { chop $x } say "@a";', out='a c\n'),
    c('T9-substr', 'TRAPS', 'my @a=("ab","cd"); for my $x (@a) { substr($x, 0, 1, "Z") } say "@a";', out='Zb Zd\n'),
    c('T9-undef', 'TRAPS', 'my @a=("ab","cd"); for my $x (@a) { undef $x } say defined $a[0] ? "kept" : "gone";', out='gone\n'),
    c('T9-list', 'TRAPS', 'my @a=("ab","cd"); for my $x (@a) { ($x) = ("q") } say "@a";', out='q q\n'),
    c('T10', 'TRAPS', 'my @a=(1,2); my @b = sort { $a = 5; 0 } @a; say "@a";', out='5 2\n'),
    c('T11', 'TRAPS; D17', 'my @a=(1,2); my @s; for my $x (@a) { push @s, sub { $x } } $a[0]=9; say $s[0]->();', out='9\n'),
    c('T12', 'TRAPS; D17', 'my @a=(1,2); my @r; for my $x (@a) { push @r, \\$x } ${$r[0]} = 7; say "@a";', out='7 2\n'),
    c('T13', 'TRAPS', 'my ($p,$q)=(1,2); for my $x ($p,$q) { $p = 7; say $x }', out='7\n2\n'),
    c('T14', 'TRAPS', 'my $x = 10; my $f = sub { $x }; for $x (1,2) { say $f->() }', out='10\n10\n'),
    c('T15', 'TRAPS', 'sub show() { say $_ } for (1..2) { show() }', out='1\n2\n'),
    # ---- context
    c('T16', 'TRAPS; D18', 'sub a() { my @a = (42); return @a } my $x = a(); say $x;', out='1\n'),
    c('T17', 'TRAPS; D18', 'my @a=(7,8,9); sub f($c) { return $c ? @a : 0 } my $v = f(1); say $v;', out='3\n'),
    c('T18', 'TRAPS', 'sub f() { my @r = (5,6,7); } my $v = f(); say $v;', out='3\n'),
    c('T19', 'TRAPS; D18', 'sub f($x) { if ($x) { "yes" } } say "[", f(0), "]";', out='[0]\n'),
    c('T20', 'TRAPS', 'sub f() { return (1,2,3) } f(); say "ok";', out='ok\n'),
    c('T21', 'TRAPS', 'my @a=(1,2,3); say "x" . @a; say -@a; say uc(@a);', out='x3\n-3\n3\n'),
    c('T22', 'TRAPS', 'my @a=("%s-%s",2,3); say sprintf(@a);', out='3\n'),
    c('T23', 'TRAPS', 'say reverse("abc"); say scalar reverse("abc");', out='abc\ncba\n'),
    # ---- parsing
    c('T24', 'TRAPS; PLAN 0', 'say 010;', out='8\n'),
    c('T24-08', 'TRAPS; PLAN 0', 'say 08;', compiles=False, err='Illegal octal digit'),
    c('T25', 'TRAPS; D15; D21; PLAN 1', 'say (1+2)*3;', out='3\n', err='some'),
    c('T26', 'TRAPS', 'my $x = 5; say $x -1;', out='', err='some', exit='nonzero'),
    c('T27', 'TRAPS; PLAN 1', 'say - -5;', out='5\n'),
    c('T27-dec', 'TRAPS; PLAN 1', 'say --5;', compiles=False, err="Can't modify constant item"),
    c('T28', 'TRAPS; D21', 'sub q($x) { return $x * 2 } say q(5);', out='5\n'),
    c('T29', 'TRAPS; D21', 'sub dbl(@x) { return map { $_ * 2 } @x } my @s = sort dbl(3,1,2); say "@s";', out='3 1 2\n'),
    c('T30', 'TRAPS; D21', 'sub f($c) { my $x = 10 if $c; $x++; return $x } say f(1); say f(0); say f(0);', out='11\n1\n2\n'),
    c('T31', 'TRAPS; D21', 'for my $i (1..3) { my $n = $i * 10; sub get() { return $n } say get(); }', out='10\n10\n10\n'),
    c('T32', 'TRAPS', 'for my $i (1..3) { { last; } say $i }', out='1\n2\n3\n'),
    c('T33', 'TRAPS', 'say 2 == 2 == 2 ? "y" : "n"; say 1 < 5 < 3 ? "y" : "n";', out='y\nn\n'),
    c('T34', 'TRAPS', 'say "cost: $$";', outre=r'cost: \d+\n'),
    c('T34-at', 'TRAPS', 'say "user@example.com";', compiles=False, err='Possible unintended interpolation'),
    # ---- numbers
    c('T35', 'TRAPS; D23; PLAN 2', 'my $x = 1e15; say $x; my $y = $x + 1; say $x;', out='1e+15\n1000000000000000\n'),
    c('T36', 'TRAPS; D23', 'say 4000000000000000/2; say 18014398509481984/2;', out='2e+15\n9007199254740992\n'),
    c('T37', 'TRAPS; D23', 'say 10**15; say 7**20; say 2**50;', out='1000000000000000\n79792266297612001\n1.12589990684262e+15\n'),
    c('T38', 'TRAPS; D23', 'say "1e16" + 1; say 1e16 + 1;', out='10000000000000001\n1e+16\n'),
    c('T39', 'TRAPS; D23', 'say 9007199254740993 == 2**53 ? "eq" : "ne";', out='eq\n'),
    c('T40', 'TRAPS', 'say -10 % 3e19;', out='3e+19\n'),
    c('T40-half', 'TRAPS', 'say 7 % 0.5;', out='', err='Illegal modulus zero', exit='nonzero'),
    c('T41', 'TRAPS', 'say join ",", "08".."11"; say join ",", "a".."e";', out='08,09,10,11\na,b,c,d,e\n'),
    c('T42', 'TRAPS', 'my ($p, $q) = ([], []); say $p <=> $q;', outre=r'-?1\n'),
    c('T43', 'TRAPS', 'my $x; my $y = $x--; say defined $y ? "[$y]" : "undef";', out='undef\n'),
    c('T43-inc', 'TRAPS', 'my $x; my $y = $x++; say defined $y ? "[$y]" : "undef";', out='[0]\n'),
    c('T43-mul', 'TRAPS; SURFACE', 'my $x; $x *= 2; say $x;', out='0\n', err='uninitialized'),
    c('T43-add', 'TRAPS; SURFACE', 'my $x; $x += 2; say $x;', out='2\n'),
    c('T44', 'TRAPS; SURFACE', 'my $s = "ab"; $s--; say $s;', out='-1\n'),
    # ---- strings
    c('T45', 'TRAPS', 'use utf8;\nsay uc("straße"); say length(uc("straße"));', out='STRASSE\n7\n'),
    c('T73', 'TRAPS', 'use utf8; say uc("straße");', compiles=False, err='Use of non-ASCII character 0xC3 illegal'),
    c('T73-comment', 'TRAPS', '# café\nsay 1;', compiles=False, err='Use of non-ASCII character 0xC3 illegal'),
    c('T46', 'TRAPS', 'say "12" & "10"; say "12" &. "10";', out='8\n10\n'),
    c('T47', 'TRAPS', 'say -"foo"; say -"-foo";', out='-foo\n+foo\n'),
    # ---- reading that writes
    c('T48', 'TRAPS', 'my $h = {}; my $x = $h->{a}{b}; say exists $h->{a} ? "made" : "no";', out='made\n'),
    c('T49', 'TRAPS', 'my %h; for my $x ($h{l}->@*) { } say exists $h{l} ? "made" : "no";', out='made\n'),
    c('T49-map', 'TRAPS', 'my %h; my @m = map { $_ } $h{l}->@*; say exists $h{l} ? "made" : "no";', out='made\n'),
    c('T49-keys', 'TRAPS', 'my %h; my @k = keys $h{l}->%*; say exists $h{l} ? "made" : "no";', out='made\n'),
    c('T50', 'TRAPS', 'my @a; my $t = $a[3][0]; say scalar(@a);', out='4\n'),
    # ---- accepted by the obvious parser, refused by perl
    c('T51', 'TRAPS', 'say 1 <=> 2 == -1;', compiles=False, err='syntax error'),
    c('T51-range', 'TRAPS', 'my @r = (1 .. 2 .. 3);', compiles=False, err='syntax error'),
    c('T52', 'TRAPS', CLASS + 'class P { } my $o = P->new; say 0 < $o isa P;', compiles=False, err='syntax error'),
    c('T52-eq', 'TRAPS', CLASS + 'class P { } my $o = P->new; say $o isa P == 1 ? "y" : "n";', out='y\n'),
    c('T53', 'TRAPS', 'try { say 1 } catch { say 2 }', compiles=False, err=r'catch block requires a \(VAR\)'),
    c('T54', 'TRAPS', 'my @a = (1,2); my %h = map { "$_" => 1 } @a; say join ",", sort keys %h;', compiles=False, err='syntax error'),
    c('T54-semi', 'TRAPS', 'my @a = (1,2); my %h = map {; "$_" => 1 } @a; say join ",", sort keys %h;', out='1,2\n'),
    c('T54-plus', 'TRAPS', 'my @a = (1,2); my %h = map +( "$_" => 1 ), @a; say join ",", sort keys %h;', out='1,2\n'),
    c('T55', 'TRAPS', 'sub n(:$x) { }', compiles=False, err=r"A signature parameter must start with '\$', '@' or '%'"),
    c('T56', 'TRAPS; PLAN 17', CLASS + 'class A { field $x = 1; } class B :isa(A) { method m() { return $x } }', compiles=False, err=r'Global symbol "\$x" requires explicit package name'),
    c('T57', 'TRAPS', 'my $s = "ab"; say($s x3);', compiles=False, err='Bareword "x3" not allowed'),
    # ---- found by reading Crayon
    c('T58', 'TRAPS', 'my $x = 5; { my $x = $x // 9; say $x }', out='5\n'),
    c('T59', 'TRAPS', 'for my $i (1..3) { my @r = map { last if $_ == 2; $_ } (1,2,3); say $i } say "done";', out='done\n'),
    c('T60', 'TRAPS', 'sub f() { next } for my $i (1..3) { f() if $i == 2; say $i }', out='1\n3\n', err='Exiting subroutine via next'),
    c('T61', 'TRAPS', 'my $a = 5; my @s = sort { $a <=> $b } (3,1,2); say "@s";', out='2 1 3\n', err='some'),
    c('T62', 'TRAPS; SURFACE', 'say 65.66.67;', out='ABC\n'),
    c('T63', 'TRAPS; SURFACE', 'my %h = (010 => "a", 0x10 => "c"); say join ",", sort keys %h;', out='16,8\n'),
    c('T64', 'TRAPS', 'my $i = 5; do { say $i; $i++ } while ($i < 3);', out='5\n'),
    c('T65', 'TRAPS', 'sub f() { try { 42 } catch ($e) { 0 } } say "[", f(), "]";', out='[42]\n'),
    c('T66', 'TRAPS', '"abc" =~ /b/; say "xbx" =~ // ? "y" : "n";', out='y\n'),
    c('T67', 'TRAPS', 'use utf8;\nsay "٣" =~ /^\\d$/ ? "digit" : "no"; say "a\\n" =~ /a$/ ? "match" : "no";', out='digit\nmatch\n'),
    c('T68', 'TRAPS; SURFACE', 'my $x = (4,5,6); say $x;', out='6\n', err='Useless use of a constant'),
    c('T69', 'TRAPS; SURFACE', 'say -foo;', out='-foo\n'),
    c('T70', 'TRAPS', 'sub f() { ... } f();', out='', err=r'Unimplemented at \S+ line 2\.', exit=255),
    c('T71', 'TRAPS', 'my $name = "x"; say "$name\'s";', out="x's\n"),
    # ---- found at step 0
    c('T72', 'TRAPS; D33', '#!/usr/bin/perl -n\nuse v5.42;\nsay 42;', raw=True, out=''),
    c('T72-blanks', 'TRAPS; D33', ' \t#!/usr/bin/perl -n\nuse v5.42;\nsay 42;', raw=True, out=''),
    c('T72-other', 'TRAPS; D33', '#!/bin/echo hello\nuse v5.42;\nsay 42;', raw=True, out='hello claim.pl\n'),
    c('T72-plain', 'TRAPS; D33', '#!/usr/bin/perl\nuse v5.42;\nsay 42;', raw=True, out='42\n'),
    c('T72-line-2', 'TRAPS; D33', '\n#!/usr/bin/perl -n\nuse v5.42;\nsay 42;', raw=True, out='42\n'),
    c('T72-renumbered', 'TRAPS; D33', 'use v5.42;\nsay 1;\n# line 1\n#!perl -n\nsay 2;', raw=True, out='1\n'),
    c('T72-renumbered-other', 'TRAPS; D33', 'use v5.42;\nsay 1;\n# line 1\n#!/bin/echo hello\nsay 2;', raw=True, out='hello claim.pl\n'),
    c('T72-after-code', 'TRAPS; D33', 'use v5.42;\nsay 1;\n# line 1\nsay 2; #!perl -n\nsay 3;', raw=True, out='1\n2\n3\n'),
    c('T75', 'TRAPS', 'use v5.42#c\n;\nsay 42;', raw=True, compiles=False, err=r"Can't locate v5\.pm"),
    c('T75-space', 'TRAPS', 'use v5.42 #c\n;\nsay 42;', raw=True, out='42\n'),
    c('T74', 'TRAPS', '# line 100 "other.pl"\nsay 42;\ndie "x";', out='42\n', err=r'x at other\.pl line 101\.', exit=255),
    c('T74-tight', 'TRAPS', '#line 100\ndie "x";', out='', err=r'x at claim\.pl line 100\.', exit=255),
    c('T74-indented', 'TRAPS', '  # line 100\ndie "x";', out='', err=r'x at claim\.pl line 3\.', exit=255),
    c('T74-words', 'TRAPS', '# line 100 and more words\ndie "x";', out='', err=r'x at claim\.pl line 3\.', exit=255),
    c('S-ctrl-d', 'LANGUAGE; lexer.ts', 'say 1;\n\x04say 2;', out='1\n'),
    c('S-ctrl-z', 'LANGUAGE; lexer.ts', 'say 1;\n\x1asay 2;', out='1\n'),
    c('S-cr', 'LANGUAGE; lexer.ts', 'say 1;\rdie "x";', out='1\n', err=r'x at claim\.pl line 2\.', exit=255),
    c('S-42x3', 'lexer.ts', 'say 42x3; say 1_000; say 0x10; say 1e3;', out='424242\n1000\n16\n1000\n'),
    # ---- TRAPS.md: the checks themselves
    c('checks-100-deep', 'TRAPS; PLAN 8', 'sub d($n) { return $n == 0 ? 0 : 1 + d($n - 1) } say d(101);', out='101\n', err='Deep recursion'),
    c('checks-99-deep', 'TRAPS; PLAN 8', 'sub d($n) { return $n == 0 ? 0 : 1 + d($n - 1) } say d(98);', out='98\n'),
    c('checks-trim', 'TRAPS; PLAN 0', 'sub trim($s) { return "mine" } say trim("  x  ");', out='mine\n', err='Subroutine trim redefined'),
    c('checks-ceil', 'TRAPS; PLAN 0', 'sub ceil($n) { return "mine" } say ceil(1.5);', out='mine\n', err='Subroutine ceil redefined'),
    c('checks-for-list', 'TRAPS', 'my %h = (a => 1); for my ($k, $v) (%h) { say "$k=$v" }', out='a=1\n'),
    c('checks-try', 'TRAPS', 'try { die "x\\n" } catch ($e) { print "caught $e" }', out='caught x\n'),
    c('checks-xor', 'TRAPS; SURFACE', 'say((1 ^^ 0) ? "t" : "f"); my $t = 1; $t ^^= 1; say $t ? "t" : "f";', out='t\nf\n'),
    c('checks-any', 'TRAPS; SURFACE', 'say((any { $_ > 1 } 1, 2) ? "y" : "n");', compiles=False, err='syntax error'),
    c('checks-any-on', 'TRAPS; SURFACE', 'use feature "keyword_any"; no warnings "experimental::keyword_any"; say((any { $_ > 1 } 1, 2) ? "y" : "n");', out='y\n'),
    c('checks-source-encoding', 'TRAPS', 'say "é";', compiles=False, err='Use of non-ASCII character 0xC3 illegal when \'use source::encoding "ascii"\' is in effect'),
    c('checks-reader', 'TRAPS; PLAN 17', CLASS + 'class P { field $x :param :reader; field @l :reader = (1,2,3); method c() { return __CLASS__ } } my $p = P->new(x => 4); say $p->x; say scalar(my @got = $p->l); say $p->c;', out='4\n3\nP\n'),
    c('checks-writer', 'TRAPS; PLAN 17', CLASS + 'class P { field $x :param :writer :reader; } my $p = P->new(x => 4); $p->set_x(5); say $p->x;', out='5\n'),
    c('checks-my-method', 'TRAPS; PLAN 17', CLASS + 'class P { my method secret() { return 7 } method pub() { return $self->&secret() } } say P->new->pub;', out='7\n'),
    # ---- step 1
    c('T76', 'TRAPS', 'say (1 +\n2);', out='3\n', err=r'say \(\.\.\.\) interpreted as function'),
    c('T76-semicolon', 'TRAPS', 'say (1 + 2)\n;', out='3\n', err=r'say \(\.\.\.\) interpreted as function'),
    c('T76-comment', 'TRAPS', 'say (1 + 2) # c\n;', out='3\n', err=r'say \(\.\.\.\) interpreted as function'),
    c('T76-one-line', 'TRAPS', 'say (1 + 2) ; say ((1 + 2) * 3); # c', out='3\n9\n'),
    c('T76-two-blanks', 'TRAPS', 'say  (1 +\n2)\n;', out='3\n'),
    c('T76-tab', 'TRAPS', 'say\t(1 +\n2)\n;', out='3\n'),
    c('T76-newline', 'TRAPS', 'say\n(1 +\n2)\n;', out='3\n'),
    c('T76-none', 'TRAPS', 'say(1 +\n2\n)\n;', out='3\n'),
    c('T25-no-blank', 'TRAPS; LANGUAGE', 'say(1 + 2) * 3;', out='3\n', err='Useless use of multiplication'),
    c('T25-plus', 'LANGUAGE', 'say +(1 + 2) * 3; say -(1 + 2) * 3; say((1 + 2) * 3); say 3 * (1 + 2);', out='9\n-9\n9\n9\n'),
    c('S1-glob', 't/038', 'say 2 * *3;', out='0\n', err="isn't numeric in multiplication"),
    c('S1-glob-first', 'parser.test', 'say * 2;', out='*main::2\n'),
    c('S1-hash-first', 'parser.test', 'say % 2;', out='\n'),
    c('S1-empty', 'parser.test', 'say(());', out='\n'),
    c('S1-repeat', 'parser.test', 'say 4 x 2;', out='44\n'),
    c('S1-hard-against', 't/031', 'say 7 %+3; say 7 %-3; say 2 *-3; say 1 -(2);', out='1\n-2\n-6\n-1\n'),
    c('S1-mod', 'LANGUAGE; D23', 'say 7 % 3; say -7 % 3; say 7 % -3; say -7 % -3;', out='1\n2\n-2\n-1\n'),
    c('S1-mod-min', 'rt.c', 'say((-9223372036854775807 - 1) % -1); say -0;', out='0\n0\n'),
    c('S1-mod-zero', 'PLAN 1', 'say 1;\nsay 5 % 0;', out='1\n', err=r'Illegal modulus zero at claim\.pl line 3\.', exit=255),
    c('D34-line', 'D34', 'say 1;\nsay 2\n+ 5 % 0\n+ 3;', out='1\n', err=r'Illegal modulus zero at claim\.pl line 3\.', exit=255),
    c('S1-overflow', 'LANGUAGE', 'say 9223372036854775806 + 1; say 9223372036854775807 + 1; say -(-9223372036854775807 - 1);', out='9223372036854775807\n9223372036854775808\n9223372036854775808\n'),
    c('S1-back-in-range', 'TRAPS', 'say - - (-9223372036854775807 - 1); say 0 * (9223372036854775807 + 1);', out='-9223372036854775808\n0\n'),
    # ---- step 2's proposal (PLAN.md) and T77 to T82
    c('P2-table-1', 'PLAN 2', 'say 7 / 2; say 6 / 2; say 0.1 + 0.2; say 1 / 3; say 1e3 + 1; say 1e15 + 1; say 1e16 + 1;', out='3.5\n3\n0.3\n0.333333333333333\n1001\n1000000000000001\n1e+16\n'),
    c('P2-table-2', 'PLAN 2', 'say 10 ** 15; say 2 ** 10; say 2 ** 0.5; say 3 ** 40; say 18014398509481984 / 2; say 9223372036854775807 / 2;', out='1000000000000000\n1024\n1.4142135623731\n1.21576654590569e+19\n9007199254740992\n4.61168601842739e+18\n'),
    c('P2-table-3', 'PLAN 2', 'say 1e10 * 1e10; say 5e9 * 5e9; say 1.5e10 * 1e10; say 1e10 * 1e9; say 9223372036854775807 + 1.0;', out='1e+20\n2.5e+19\n1.5e+20\n10000000000000000000\n9223372036854775808\n'),
    c('P2-table-4', 'PLAN 2', 'say 1e15; say 2 ** 50; say 4000000000000000 / 2; say 1e15 + 0; say 1e16; say 2 ** 62;', out='1e+15\n1.12589990684262e+15\n2e+15\n1000000000000000\n1e+16\n4.61168601842739e+18\n'),
    c('P2-table-5', 'PLAN 2', 'say 1e308 * 10; say((-8) ** 0.5); say(0 ** -1); say 1e400;', out='Inf\nNaN\nInf\nInf\n'),
    c('P2-div-zero', 'PLAN 2', 'say 1;\nsay 1.5 / 0.0;', out='1\n', err='Illegal division by zero', exit=255),
    c('P2-zero-zero', 'PLAN 2', 'say 0 / 0;', out='', err='Illegal division by zero', exit=255),
    c('P2-precedence', 'PLAN 2', 'say -2 ** 2; say 2 ** 3 ** 2; say 2 ** -1; say 2 ** -2 ** 2; say 4 / 2 * 3; say 7 / 2 % 2;', out='-4\n512\n0.5\n0.0625\n6\n1\n'),
    c('P2-mod-num', 'PLAN 2', 'say 10 % 3.7; say -10 % 3.7; say 10.9 % 3; say 10 % -3.7; say 7.5 % 2.5; say 1e20 % 7;', out='1\n2\n1\n-2\n1\n2\n'),
    c('P2-mod-half', 'PLAN 2', 'say 7 % 0.5;', out='', err='Illegal modulus zero', exit=255),
    c('P2-print', 'PLAN 2', 'say 1e21; say 3.0; say 1.50; say 1e-5; say 0.0001; say 1234567890123456.7; say -0.0; say 0 * -1.5;', out='1e+21\n3\n1.5\n1e-05\n0.0001\n1.23456789012346e+15\n0\n0\n'),
    c('P2-nan-order', 'PLAN 2', 'my $n = 9**9**9 - 9**9**9; say defined($n <=> 1) ? "def" : "undef"; say -7 % 9**9**9; say "inf" + 0; say "nan" + 0; say "Infinity" + 0;', out='undef\nInf\nInf\nNaN\nInf\n'),
    c('P2-builtin-inf', 'PLAN 2', 'say builtin::inf();', out='Inf\n', err="Built-in function 'builtin::inf' is experimental"),
    c('P2-literals', 'PLAN 2', 'say 1.5; say .5; say 1e3; say 1.5e-3; say 1E3; say 0x1F; say 0X1f; say 0b101; say 0B101; say 0o17; say 0O17; say 1_000; say 0xff_ff; say 1.5_0; say 1e1_0;', out='1.5\n0.5\n1000\n0.0015\n1000\n31\n31\n5\n5\n15\n15\n1000\n65535\n1.5\n10000000000\n'),
    c('P2-32-bits', 'PLAN 2', 'say 0xFFFFFFFF; say 0b11111111111111111111111111111111; say 0o37777777777;', out='4294967295\n4294967295\n4294967295\n'),
    c('P2-33-bits-hex', 'PLAN 2', 'say 0x100000000;', out='4294967296\n', err='Hexadecimal number > 0xffffffff non-portable'),
    c('P2-33-bits-bin', 'PLAN 2', 'say 0b100000000000000000000000000000000;', out='4294967296\n', err='Binary number > 0b11111111111111111111111111111111 non-portable'),
    c('P2-33-bits-oct', 'PLAN 2', 'say 0o40000000000;', out='4294967296\n', err='Octal number > 0o37777777777 non-portable'),
    c('P2-octal', 'PLAN 2; T24', 'say 017; say 001; say 00;', out='15\n1\n0\n'),
    c('P2-point', 'PLAN 2', 'say 1.; say 1.e3;', out='1\n1000\n'),
    c('P2-hex-float', 'PLAN 2', 'say 0x1p3; say 0x1.8p3;', out='8\n12\n'),
    c('T77', 'TRAPS', 'say 10 ** 4611686018427387904; say 9 ** 4611686018427387904; say 7 ** 6148914691236517206; say 3 ** 9223372036854775807;', out='0\n1\n4660168006209859345\nInf\n'),
    c('T78', 'TRAPS', 'say 00.5; say 0x1.8; say 1.5 .5; say 1 .5; say 1.5e3.2;', out='05\n18\n1.55\n15\n15002\n'),
    c('T79-print', 'TRAPS', 'say -0.0; say 0 / -5; say sprintf("%g", -0.0); say sprintf("%.1f", 0 * -1.5); say atan2(0, -0.0);', out='0\n0\n-0\n-0.0\n3.14159265358979\n'),
    c('T79-fresh', 'TRAPS', 'my $x = 0.0; say atan2(0, -$x); say sprintf("%g", -$x); say((-$x) ** -1);', out='3.14159265358979\n-0\n-Inf\n'),
    c('T79-used', 'TRAPS', 'my $x = 0.0; my $t = $x + 1; say atan2(0, -$x); say sprintf("%g", -$x); say((-$x) ** -1);', out='0\n0\nInf\n'),
    c('T80', 'TRAPS', 'say 1e10 * 1e9; say 1e10 * 1e10; say 9223372036854775807 * 2.0; say 9223372036854775807 * 3.0; say -1e10 * 1e9; say -9223372036854775807 - 2.0;', out='10000000000000000000\n1e+20\n18446744073709551614\n2.76701161105643e+19\n-1e+19\n-9.22337203685478e+18\n'),
    c('T81', 'TRAPS', 'say 9223372036854775808; say 18446744073709551616; say 99999999999999999999; say 1e400; say 1e-400;', out='9223372036854775808\n1.84467440737096e+19\n1e+20\nInf\n0\n'),
    c('T82-1', 'TRAPS', 'say 1__0;', out='10\n', err='Misplaced _ in number'),
    c('T82-2', 'TRAPS', 'say 1_e3;', out='1000\n', err='Misplaced _ in number'),
    c('T82-3', 'TRAPS', 'say 1e_3;', out='1000\n', err='Misplaced _ in number'),
    c('T82-4', 'TRAPS', 'say 0x_ff;', out='255\n', err='Misplaced _ in number'),
    c('T82-5', 'TRAPS', 'say 0_17;', out='15\n', err='Misplaced _ in number'),
    c('T82-6', 'TRAPS', 'say 1_.5;', out='1.5\n', err='Misplaced _ in number'),
    c('T82-7', 'TRAPS', 'say 1.5_;', out='1.5\n', err='Misplaced _ in number'),
    c('T35-window', 'TRAPS', 'my $x = 9007199254740991.0; say $x; my $t = $x + 1; say $x; my $y = 9007199254740992.0; say $y; $t = $y + 1; say $y; my $z = 1e16; $t = $z + 1; say $z;', out='9.00719925474099e+15\n9007199254740991\n9.00719925474099e+15\n9.00719925474099e+15\n1e+16\n'),
    c('T35-below', 'TRAPS', 'my $x = 999999999999999.0; say $x; my $t = $x + 1; say $x; say -$x;', out='999999999999999\n999999999999999\n-999999999999999\n'),
    c('T35-negate', 'TRAPS', 'my $x = 2e15; say -$x; my $t = $x + 1; say -$x; my $y = 2e15; --$y; say $y; my $z = 2e15; $t = $z + 1; --$z; say $z;', out='-2e+15\n-2000000000000000\n2e+15\n1999999999999999\n'),
    c('L2-examples', 'LANGUAGE', 'say 1_000_000; say 0xff_ff; say 1.000_1; say 7 ** 20; say 4 / 2 * 3; say 2 - 3 - 4; say 7 % 3; say 7 % -3; say 1e19;', out='1000000\n65535\n1.0001\n79792266297612001\n6\n-5\n1\n-2\n1e+19\n'),
    c('T79-signs', 'TRAPS; runtime/tests/zero.c', 'say sprintf("%g %g %g %g %g %g %g", -(0.0), -(-(0.0)), 0 * -1.5, 0.0 * -1, 0 / -5, -(0.0) + 0, -(0));', out='-0 0 -0 0 -0 0 0\n'),
    # ---- step 3's proposal (PLAN.md) and T83 to T90
    c('T83-fresh', 'TRAPS; PLAN 3', 'my $s = "3.0";\nsay $s + 9007199254740990; say "3.0" + 1; say "10.00" * 3;', out='9.00719925474099e+15\n4\n30\n'),
    c('T83-used', 'TRAPS; PLAN 3', 'my $s = "3.0"; my $t = $s > 0.5;\nsay $s + 9007199254740990;', out='9007199254740993\n'),
    c('T83-exponent', 'TRAPS; PLAN 3; D23', 'my $s = "1e16"; say $s + 1; my $u = "1e16"; my $t = $u > 0.5; say $u + 1;', out='10000000000000001\n1e+16\n'),
    c('P3-silent', 'PLAN 3', 'say "12" + 1; say " -12 " + 1; say "012" + 1; say "12\\n" + 1; say "1e3" + 1; say "1.5e1" + 1; say ".5" + 1; say "+3" + 1; say "5." + 1;', out='13\n-11\n13\n13\n1001\n16\n1.5\n4\n6\n'),
    c('P3-silent-odd', 'PLAN 3', 'say "Inf" + 0; say "NaN" + 0; say "0 but true" + 5;', out='Inf\nNaN\n5\n'),
    c('P3-warns-1', 'PLAN 3', 'say "" + 1;', out='1\n', err="isn't numeric"),
    c('P3-warns-2', 'PLAN 3', 'say "1_000" + 1;', out='2\n', err="isn't numeric"),
    c('P3-warns-3', 'PLAN 3', 'say "0x10" + 1;', out='1\n', err="isn't numeric"),
    c('T84', 'TRAPS', 'my $s = "12abc"; my $t = $s + 0; say "between"; say $s + 1;', out='between\n13\n', err=r"\AArgument \"12abc\" isn't numeric in addition \(\+\) at claim\.pl line 2\.\n\Z"),
    c('T85', 'TRAPS; PLAN 3', 'say -"+0"; say -"+12"; say -"-foo"; say -"foo"; say -"12"; say -"0";', out='-0\n-12\n+foo\n-foo\n-12\n0\n'),
    c('T86', 'TRAPS; PLAN 3', 'say length "\\x"; say length "\\x{}"; say ord "\\x"; say "\\-\\%\\ |";', out='1\n1\n0\n-% |\n'),
    c('T86-warns', 'TRAPS; PLAN 3', 'say "\\q";', out='q\n', err=r'Unrecognized escape \\q passed through'),
    c('T86-digit', 'TRAPS; PLAN 3', 'say "\\8";', out='8\n', err=r'Unrecognized escape \\8 passed through'),
    c('P3-escapes', 'PLAN 3', 'say "\\x41\\x{263A}\\101\\o{101}\\N{U+263A}\\e[0m\\0|\\$x \\@y \\" \\\\";', out='A\u263aAA\u263a\x1b[0m\x00|$x @y " \\\n', csda=True),
    c('P3-single', 'PLAN 3', "say 'a\\tb \\\\ \\' $x @y';", out="a\\tb \\ ' $x @y\n"),
    c('T87', 'TRAPS; PLAN 3', 'say length "abc" . "de"; say length("abc") . "de"; say length ("abc") . "de"; say length "abc" == 3; say uc "abc" . "def";', out='5\n3de\n3de\n1\nABCDEF\n'),
    c('T87-warns', 'TRAPS; PLAN 3', 'say length "abc" + 1;', out='1\n', err="isn't numeric in addition"),
    c('T88', 'TRAPS; PLAN 3', 'say length(chr(55296)); say length(chr(1114112)); say chr(65534);', out='1\n1\n\ufffe\n', err='Unicode non-character U\\+FFFE is not recommended for open interchange', csda=True),
    c('T88-open', 'TRAPS; PLAN 3', 'use open ":std", ":encoding(UTF-8)";\nsay chr(233); say chr(65534);', out='\xe9\n\\x{FFFE}\n', err='Unicode non-character'),
    c('T89', 'TRAPS; PLAN 3', 'say "ab" x 3; say "ab"x3; say "ab" x3; say "a" x 2.7; say "a" x "2"; say 2 x 3;', out='ababab\nababab\nababab\naa\naa\n222\n'),
    c('T89-negative', 'TRAPS; PLAN 3', 'say "a" x -1;', out='\n', err='Negative repeat count does nothing'),
    c('T89-huge', 'TRAPS; PLAN 3', 'say "a" x 1e30;', out='\n', err='Negative repeat count does nothing'),
    c('T90', 'TRAPS; PLAN 3', 'say "a".5; say 1 . .5; say "a" . 1 + 2 . "b";', out='a5\n10.5\n2b\n', err="isn't numeric"),
    c('P3-substr', 'PLAN 3', 'say "[", substr("abcdef", -9, 3), "]"; say substr("abcdef", 2, 3); say substr("abcdef", -2); say substr("abcdef", 6), "|";', out='[]\ncde\nef\n|\n'),
    c('P3-substr-outside', 'PLAN 3', 'say "before"; say substr("abcdef", 7);', out='before\n\n', err='substr outside of string'),
    c('P3-concat', 'PLAN 3', 'say 1 . 2 + 3; say "x" . 2 * 3; say "a" x 2 . "b"; say 1e16 . ""; say 0.1 + 0.2 . "";', out='15\nx6\naab\n1e+16\n0.3\n'),
    # ---- step 3 as built: D39 to D45, LANGUAGE.md, and what the build found (T94 to T99)
    c('D39-latin1', 'D39; LANGUAGE', 'say "\\x{e9}";', outbytes=b'\xe9\n'),
    c('D39-wide', 'D39; LANGUAGE', 'say "\\x{263A}";', outbytes=b'\xe2\x98\xba\n', err='Wide character in say'),
    c('D39-open', 'D39', 'use open ":std", ":encoding(UTF-8)";\nsay "\\x{e9}\\x{263A}";', outbytes=b'\xc3\xa9\xe2\x98\xba\n'),
    c('D39-qw', 'D39', 'use open qw(:std :encoding(UTF-8));\nuse open ":std", ":utf8";\nsay "\\x{e9}";', outbytes=b'\xc3\xa9\n'),
    c('D40-min', 'D40', 'say "-9223372036854775808" + 0; say "-9223372036854775808" + 1; say "9223372036854775808" + 0;', out='-9223372036854775808\n-9223372036854775807\n9223372036854775808\n'),
    c('D40-blanks', 'D40; LANGUAGE', 'say "3\\x0b" + 1; say "\\f3\\r" + 1; say " 12\\n" + 1; say "1.5" * 2;', out='4\n4\n13\n3\n'),
    c('D40-nul', 'D40', 'say "3\\0" + 1;', out='4\n', err="isn't numeric"),
    c('D40-plus', 'D40; LANGUAGE', 'say +"abc"; say -"12"; say -"7.5";', out='abc\n-12\n-7.5\n'),
    c('L3-concat', 'LANGUAGE', 'say "ab" . "cd"; say "ab" x 3; say "-" x 10 . ">"; say "a" . "b" x 2; say 1 + 2 . 3; say "n = " . (0.1 + 0.2); say length 1000;', out='abcd\nababab\n---------->\nabb\n33\nn = 0.3\n4\n'),
    c('L3-concat-fault', 'LANGUAGE', 'say "n = " . 0.1 + 0.2;', out='0.2\n', err="isn't numeric"),
    c('L3-builtins', 'LANGUAGE', 'say uc "abc"; say ord "A"; say chr 65; say chr 65.9; say length "ab" . "c"; say length("ab") . "c";', out='ABC\n65\nA\nA\n3\n2c\n'),
    c('L3-substr', 'LANGUAGE', 'say substr("abcdef", 2); say substr("abcdef", 2, 3); say substr("abcdef", -2); say substr("abcdef", 1, -1); say index("abcabc", "c"); say index("abcabc", "c", 3); say index("abcabc", "x");', out='cdef\ncde\nef\nbcde\n2\n5\n-1\n'),
    c('L3-utf8', 'LANGUAGE; D24', 'use utf8;\nuse open ":std", ":encoding(UTF-8)";\nsay length "café"; say "café";', outbytes=b'4\ncaf\xc3\xa9\n'),
    c('T94', 'TRAPS; D41', 'say length - 5;', out='2\n', err='Use of "length" without parentheses is ambiguous'),
    c('T94-hard', 'TRAPS; D41', 'say length-5;', out='2\n', err='Use of "length-5" without parentheses is ambiguous'),
    c('T94-fine', 'TRAPS; D41', 'say length -5; say length +"ab"; say - length "ab"; say -length "ab";', out='2\n2\n-2\n-2\n'),
    c('T95', 'TRAPS; D43', 'say "\\x4 ";', out='\x04 \n', err='Non-hex character .* terminates \\\\x early'),
    c('T95-end', 'TRAPS; D43', 'say "\\x4"; say "\\x41g";', out='\x04\nAg\n'),
    c('T95-octal', 'TRAPS; D43', 'say "\\18";', out='\x018\n', err="Non-octal character '8' terminates"),
    c('T95-octal-fine', 'TRAPS; D43', 'say "\\0008|\\1a|\\x048";', out='\x008|\x01a|\x048\n'),
    c('T95-quiet', 'TRAPS; D43', 'say "a\\\nb\\\t|\\_"; say "\\x{ 41 }\\x{4_1}";', out='a\nb\t|_\nAA\n'),
    c('T96', 'TRAPS; D41', 'say "[", substr("abcde", -8, 2), "]";', out='[]\n', err='substr outside of string'),
    c('T96-edge', 'TRAPS; D41', 'say "[", substr("abcde", -8, 3), "]"; say "[", substr("abc", 1, -5), "]"; say "[", substr("abc", -4), "]";', out='[]\n[]\n[abc]\n'),
    c('T97', 'TRAPS; D41', 'say substr("abc", 0, 1e30); say substr("abc", 1e30); say index("abc", "c", 1e30);', out='ab\nc\n2\n'),
    c('T98', 'TRAPS; D44', 'say "[", "a" x -0.5, "]";', out='[]\n', err='Negative repeat count does nothing'),
    c('T98-string', 'TRAPS; D44', 'say "[", "a" x "-0.5", "]"; say "[", "a" x -0.0, "]"; say "[", "" x 4611686018427387904, "]";', out='[]\n[]\n[]\n'),
    c('T98-chr', 'TRAPS; D42', 'say ord chr(-0.5);', out='65533\n', err='Invalid negative number \\(-0.5\\) in chr'),
    c('T99', 'TRAPS; D44', 'say "a"x 3; say "c" x.5, "|"; say "d" x"2"; say "b" x(2);', out='aaa\n|\ndd\nbb\n'),
    c('T99-assign', 'TRAPS; D44', 'say "a" x= 3;', compiles=False, err="Can't modify constant item in repeat"),
    c('D44-print', 'D44', 'print "a"; print "b\\n"; print -1; print "\\n"; say -"1"; say\'a\';', out='ab\n-1\n-1\na\n'),
    c('D42-noncharacter-source', 'D42', 'use utf8;\nsay length "￾";', out='1\n'),
    # ---- found by the review of step 3's definition (T100 to T103)
    c('T94-below', 'TRAPS; D41', 'say length\n-5;', out='2\n', err='without parentheses is ambiguous'),
    c('T94-below-fine', 'TRAPS; D41', 'say length\n    -5;', out='2\n'),
    c('T100', 'TRAPS', 'say ("(");', out='(\n', err=r'say \(\.\.\.\) interpreted as function'),
    c('T100-closes-early', 'TRAPS', 'say (")" . "a");', out=')a\n', err=r'say \(\.\.\.\) interpreted as function'),
    c('T100-fine', 'TRAPS', 'say (1); # and (\nsay\t("(");\nsay  ("(");\nsay("(");', out='1\n(\n(\n(\n'),
    c('T101', 'TRAPS; D44', 'say(("a") x 3); say +("a") x 3; say length(("a") x 3);', out='aaa\naaa\n3\n'),
    c('T101-memory', 'TRAPS; D44', 'say "before"; say(("") x 9223372036854775807);', out='before\n', err='Out of memory', exit=255),
    c('T102', 'TRAPS', 'say "before";\nsay length("b" x 999999999999999);', out='', err='fold_constants', exit='nonzero'),
    c('T102-wrap', 'TRAPS; t/models/str.py 148', 'say "before";\nsay length("ab" x 9223372036854775807);', out='before\n', err='panic: memory wrap', exit='nonzero'),
    c('T103-fresh', 'TRAPS; D40', 'my $x = "1.99999999999999999"; say substr("abcdefgh", $x); my $y = "0.99999999999999995"; say "<" . "ab" x $y . ">"; my $z = "0.99999999999999995"; say ord(chr($z));', out='bcdefgh\n<>\n1\n'),
    c('T103-used', 'TRAPS; D40', 'my $x = "1.99999999999999999"; my $t = $x + 0.5; say substr("abcdefgh", $x); my $y = "0.99999999999999995"; $t = $y * 1.5; say "<" . "ab" x $y . ">"; my $z = "0.99999999999999995"; $t = $z + 0; say ord(chr($z));', out='cdefgh\n<ab>\n0\n'),
    # ---- step 4's proposal (PLAN.md) and T104 to T108
    c('P4-bool', 'PLAN 4', 'say true; say "[", false, "]"; say true + 1; say false + 1; say true . "x"; say false . "x"; say length false; say -true; say -false; say true x 3;', out='1\n[]\n2\n1\n1x\nx\n0\n-1\n0\n111\n'),
    c('P4-bool-results', 'PLAN 4', 'say 1 == 1; say "[", 1 == 2, "]"; say "[", !1, "]"; say !0; say !!"a"; say true == 1; say "[", false eq "", "]"; say "[", false eq "0", "]"; say false == 0;', out='1\n[]\n[]\n1\n1\n1\n[1]\n[]\n1\n'),
    c('P4-empty-is-not-false', 'PLAN 4', 'say "" == 0;', out='1\n', err="isn't numeric"),
    c('P4-undef-warns', 'PLAN 4', 'say "a" . undef; say 1 + undef; say undef == 1; say undef eq ""; say undef;', out='a\n1\n\n1\n\n', err='uninitialized'),
    c('P4-undef-quiet', 'PLAN 4', 'say undef // 1; say undef || 2; say undef ? 3 : 4; say !undef; say "[", defined undef, "]"; say defined 1; say "[", defined length undef, "]"; say defined false;', out='1\n2\n4\n1\n[]\n1\n[]\n1\n'),
    c('T105', 'TRAPS; PLAN 4', 'say "before"; say undef * 2; say undef % 2;', out='before\n\n\n', err='uninitialized value in say'),
    c('T105-plus', 'TRAPS; PLAN 4', 'say undef + 1;', compiles=False, err="Can't modify constant item in undef operator"),
    c('T105-less', 'TRAPS; PLAN 4', 'say undef < 1;', compiles=False, err='Unterminated <> operator'),
    c('T105-fine', 'TRAPS; PLAN 4', 'say(undef or 1); say(undef xor 1); say defined(1 ? undef : 2) ? "d" : "u";', out='1\n1\nu\n'),
    c('P4-compare', 'PLAN 4; T39', 'say 9007199254740993 == 2**53; say "[", 9007199254740993 == 9007199254740992, "]"; say 9007199254740993 == 9007199254740992.0; say 9007199254740993 <=> 9007199254740992.0; say 1 <=> 2; say 2 <=> 1; say 3 <=> 3.0; say "1.0" == 1; say 9223372036854775807 == 9223372036854775808.0;', out='1\n[]\n1\n0\n-1\n1\n0\n1\n1\n'),
    c('P4-strings', 'PLAN 4', 'say 10 lt 9; say "[", 10 < 9, "]"; say "[", "1.0" eq 1, "]"; say 1.0 eq 1; say "[", 0.1 + 0.2 == 0.3, "]"; say 0.1 + 0.2 eq 0.3; say "a" cmp "b"; say "2" cmp "10"; say "\\x{e9}" lt "\\x{100}"; say "\\x{10000}" gt "\\x{ffff}"; say "a\\0" gt "a";', out='1\n[]\n[]\n1\n[]\n1\n-1\n1\n1\n1\n1\n'),
    c('T33-chains', 'TRAPS; PLAN 4', 'say 1 < 5 < 3 ? "y" : "n"; say "[", 1 != 1 == 0, "]"; say 1 < 2 == 1; say 1 == 2 < 3; say 1 < 2 lt 3;', out='n\n[]\n1\n1\n1\n'),
    c('T51-more', 'TRAPS; PLAN 4', 'say 1 == 2 <=> 3;', compiles=False, err='syntax error'),
    c('P4-truth', 'PLAN 4', 'say "0.0" || "f"; say "00" || "f"; say " " || "f"; say 0.0 || "f"; say -0.0 || "f"; say "0" || "f"; say "" || "f"; say 5e-324 || "f"; say "[", 0 && 1, "]"; say 2 || 3; say 1 && "y"; say 0 // 5; say "[", "" // 5, "]";', out='0.0\n00\n \nf\nf\nf\nf\n4.94065645841247e-324\n[0]\n2\ny\n0\n[]\n'),
    c('P4-short', 'PLAN 4', 'say 1 || 1/0; say 0 && 1/0; say 1 // 1/0; say 1 ? 2 : 1/0;', out='1\n0\n1\n2\n'),
    c('P4-ternary', 'PLAN 4', 'say 0 ? 2 : 3 ? 4 : 5; say 1 ? 0 ? "a" : "b" : "c"; say 0 ? 2 : 3 + 1; say 1 || 2 ? 3 : 4; say 0 ? 1 : 2 || 3;', out='4\nb\n4\n3\n2\n'),
    c('P4-precedence', 'PLAN 4', 'say "[", !2 ** 2, "]"; say !1 + 1; say !1 . "a"; say 1 && 0 || 2; say 1 || 0 && 2; say 0 || 0 // 5; say length "ab" == 2; say defined 1 == 1; say 1 + 2 == 3; say "a" . "b" eq "ab"; say 2 x 3 == 222;', out='[]\n1\na\n2\n1\n0\n1\n1\n1\n1\n1\n'),
    c('T106', 'TRAPS; PLAN 4', 'say 0 or 2;', out='0\n', err='Useless use of a constant'),
    c('T106-and', 'TRAPS; PLAN 4', 'say true and false;', out='1\n'),
    c('T106-brackets', 'TRAPS; PLAN 4', 'say(0 or 2); say(1 and 2); say "[", (1 xor 1), "]"; say(0 xor 5); say(1 or 0 and 0); say "[", (0 or 1 xor 1), "]";', out='2\n2\n[]\n1\n1\n[]\n'),
    c('T107', 'TRAPS; PLAN 4', 'say "[", (not 0 || 1), "]"; say(not(0) || 1); say(not (0) + 1); say((not 1) . "a"); say(1 + not 0); say(1 && not 0);', out='[]\n1\n2\na\n2\n1\n'),
    c('T104', 'TRAPS; PLAN 4', 'say scalar(() = (0 || ("a") x 3)); say scalar(() = (1 && ("a") x 3)); say scalar(() = (undef // ("a") x 3)); say scalar(() = (1 ? ("a") x 3 : "b")); say scalar(() = (("a") x 3 || 0)); say scalar(() = (1 xor ("a") x 3));', out='3\n3\n3\n3\n1\n1\n'),
    c('P4-spelling', 'PLAN 4', 'say 1<2; say 1 <=>2; say "a"lt"b"; say 1?2:3; say true .5; say true -1; say true x3;', out='1\n-1\n1\n2\n15\n0\n111\n'),
    c('P4-spelling-refused', 'PLAN 4', 'say 1 lt2;', compiles=False, err='syntax error'),
    c('P4-defined-ambiguous', 'PLAN 4; T94', 'say defined - 1;', out='1\n', err='Use of "defined" without parentheses is ambiguous'),
    c('P4-newer', 'PLAN 4; SURFACE', 'say 1 ^^ 0; say true(); say "[", (defined), "]";', out='1\n1\n[]\n'),
    # ---- found by the review of step 2
    c('T91', 'TRAPS', 'say 1;\nsay 1.' + '0' * 249 + ';', compiles=False, err='Number too long'),
    c('T91-250', 'TRAPS', 'say 1.' + '0' * 248 + '; say 0x' + '0' * 300 + '1F;', out='1\n31\n'),
    c('T92-fresh', 'TRAPS; PLAN 3', 'my $x = 10000000000000000; say $x + 1.0; say $x * 3.0; say 10000000000000000 + 1.0;', out='10000000000000001\n30000000000000000\n10000000000000001\n'),
    c('T92-used', 'TRAPS; PLAN 3', 'my $x = 10000000000000000; my $t = $x / 3; say $x + 1.0; say $x * 3.0; say $x + 1;', out='1e+16\n3e+16\n10000000000000001\n'),
    c('T92-odd', 'TRAPS', 'my $x = 9007199254740993; my $t = $x / 3; say $x + 1.0; my $y = 9223372036854775807; $t = $y / 3; say $y - 1.0;', out='9007199254740994\n9223372036854775806\n'),
    c('T92-other', 'TRAPS', 'my $i = 10000000000000000; my $u = $i / 3; my $one = 1.0; my $v = $one % 7; say $i + $one;', out='10000000000000001\n'),
    c('T93-fresh', 'TRAPS', 'my $x = -9007199254740991.0; $x--; say $x - 1;', out='-9.00719925474099e+15\n'),
    c('T93-used', 'TRAPS', 'my $x = -9007199254740991.0; my $t = $x % 7; $x--; say $x - 1;', out='-9007199254740993\n'),
    c('T79-more', 'TRAPS', 'my $x = 0.0; say unpack("H*", pack("d", -$x)); say sprintf("%a", -$x); my $y = 0.0; my $t = $y % 7; say unpack("H*", pack("d", -$y)); say sprintf("%a", -$y);', out='0000000000000080\n-0x0p+0\n0000000000000000\n0x0p+0\n'),
    # ---- DECISIONS.md
    c('D13-catch', 'D13', 'my $z = 0; try { say 1 / $z } catch ($e) { say "caught" }', out='caught\n'),
    c('D14-late', 'D14; BACKGROUND', 'my $r = [0]; sub f($v) { $r->[0] = $v; return $v } say f(1), $r->[0], f(0), $r->[0];', out='1000\n'),
    c('D14-element', 'D14', 'my @a = (1); say $a[0] + ($a[0] = 10) + $a[0];', out='30\n'),
    c('D15-abc', 'D15', 'say "abc" + 1;', out='1\n', err="isn't numeric"),
    c('D15-undef', 'D15', 'my $u; say $u + 1;', out='1\n', err='uninitialized'),
    c('D15-interp', 'D15', 'my $u; say "x: $u";', out='x: \n', err='uninitialized'),
    c('D15-substr', 'D15', 'my $s = "abc"; my $t = substr($s, 5); say defined $t ? "def" : "undef";', out='undef\n', err='substr outside of string'),
    c('D15-my-twice', 'D15; PLAN 5', 'my $x; my $x; say "ran";', out='ran\n', err='masks earlier declaration'),
    c('D15-12', 'D15', 'say "12" + 1; say "3 " + 1;', out='13\n4\n'),
    c('D15-count', 'D15', 'my %count; my $word = "w"; $count{$word}++; say $count{$word};', out='1\n'),
    c('D15-plus-eq', 'D15', 'my %total; my $k = "k"; $total{$k} += 5; my $s; $s .= "x"; say $total{$k}, $s;', out='5x\n'),
    c('D17-rewrite', 'D17; BACKGROUND', 'my @a = (1,2,3); for my $x (@a) { $x *= 2 } say "@a";', out='2 4 6\n'),
    c('D18-list', 'D18', 'sub a() { return (4, 5, 6) } my $x = a(); say $x;', out='6\n'),
    c('D21-say', 'D21', 'sub say($x) { print "mine\\n" } sub defined($x) { return "mine" } say(defined(1));', out='1\n'),
    c('D21-print', 'D21', 'sub print($x) { say "mine" } print("x\\n");', out='x\n'),
    c('D23-unsigned', 'D23; PLAN 0', 'say 9223372036854775807 + 1; say 9223372036854775808;', out='9223372036854775808\n9223372036854775808\n'),
    c('D23-float', 'D23', 'say 5_000_000_000 * 5_000_000_000;', out='2.5e+19\n'),
    c('D23-mod', 'D23; PLAN 1', 'say -7 % 3; say 7 % -3;', out='2\n-2\n'),
    c('D23-values', 'D23', 'say 1e15 + 1; say 1e15 * 10; say 1e16 + 1;', out='1000000000000001\n10000000000000000\n1e+16\n'),
    c('D23-div', 'D23', 'say 7 / 2;', out='3.5\n'),
    c('D23-history-compare', 'D23', 'my $x = 1e15; my $c = $x > 1; say $x;', out='1000000000000000\n'),
    c('D23-history-mod', 'D23', 'my $x = 1e15; my $c = $x % 7; say $x;', out='1000000000000000\n'),
    c('D23-history-int', 'D23', 'my $x = 1e15; my $c = int($x); say $x;', out='1000000000000000\n'),
    c('D23-history-index', 'D23', 'my @a = (1); my $x = 1e15; my $c = $a[$x]; say $x;', out='1000000000000000\n'),
    c('D23-history-sort', 'D23', 'my $x = 1e15; my @s = sort { $a <=> $b } ($x, 2); say $x;', out='1000000000000000\n'),
    c('D23-string-history', 'D23', 'my $h = "1e16"; my $c = $h > 0.5; say $h + 1;', out='1e+16\n'),
    c('D12-die', 'D12', 'say "before"; die "stopped\\n";', out='before\n', err='stopped', exit=255),
    # ---- PLAN.md
    c('P1-plus', 'PLAN 1; SURFACE', 'say +(1 + 2) * 3;', out='9\n'),
    c('P1-min', 'PLAN 1', 'say -9223372036854775807 - 1;', out='-9223372036854775808\n'),
    c('P2-sum', 'PLAN 2', 'say 0.1 + 0.2; say 1e16;', out='0.3\n1e+16\n'),
    c('P2-inf', 'PLAN 2', 'say 9**9**9; say -9**9**9; say 9**9**9 - 9**9**9;', out='Inf\n-Inf\nNaN\n'),
    c('P2-mod', 'PLAN 2', 'say 10 % 3.7;', out='1\n'),
    c('P2-underscores', 'PLAN 2', 'say 1__0;', out='10\n', err='Misplaced _ in number'),
    c('P2-hex', 'PLAN 2', 'say 0x1_0000_0000;', out='4294967296\n', err='some'),
    c('P2-literals', 'PLAN 2', 'say 0o17; say .5; say 1.; say 1e3;', out='15\n0.5\n1\n1000\n'),
    c('P3-quiet', 'PLAN 3', 'say "3 " + 0; say " 3" + 0; say "1e3" + 0; say ".5" + 0; say "+3" + 0; say "Inf" + 0; say "0 but true" + 5;', out='3\n3\n1000\n0.5\n3\nInf\n5\n'),
    c('P3-empty', 'PLAN 3', 'say "" + 0;', out='0\n', err="isn't numeric"),
    c('P3-12abc', 'PLAN 3', 'say "12abc" + 0;', out='12\n', err="isn't numeric"),
    c('P3-0x10', 'PLAN 3', 'say "0x10" + 0;', out='0\n', err="isn't numeric"),
    c('P4-bool', 'PLAN 4', 'say true; say "[" . false . "]"; say false + 0;', out='1\n[]\n0\n'),
    c('P8-args', 'PLAN 8', 'sub f($x) { return $x } say "before"; f(1, 2);', out='before\n', err='Too many arguments for subroutine', exit=255),
    c('P9-past', 'PLAN 9', 'my @a = (1); say defined $a[5] ? "def" : "undef"; say scalar(@a); $a[3] = 1; say scalar(@a);', out='undef\n1\n4\n'),
    c('P13-write', 'PLAN 13; SURFACE', 'my %h; $h{a}{b} = 1; push $h{k}->@*, 1; say join ",", sort keys %h;', out='a,k\n'),
    # ---- SURFACE.md
    c('S-undef-quiet', 'SURFACE', 'my ($p, $q, $r, $s, $t, $u); $p += 1; $q -= 1; $r .= "x"; $s ||= 2; $t //= 3; $u++; say "$p $q $r $s $t $u";', out='1 -1 x 2 3 1\n'),
    c('S-undef-div', 'SURFACE', 'my $x; $x /= 2; say $x;', out='0\n', err='uninitialized'),
    c('S-undef-pow', 'SURFACE', 'my $x; $x **= 2; say $x;', out='0\n', err='uninitialized'),
    c('S-undef-mod', 'SURFACE', 'my $x; $x %= 2; say $x;', out='0\n', err='uninitialized'),
    c('S-undef-x', 'SURFACE', 'my $x; $x x= 2; say "[$x]";', out='[]\n', err='uninitialized'),
    c('S-chain', 'SURFACE', 'my $x = 5; say 1 < $x < 10 ? "y" : "n"; say "a" lt "b" lt "c" ? "y" : "n";', out='y\ny\n'),
    c('S-given', 'SURFACE', 'my $x = 1; given ($x) { when (1) { say "one" } }', compiles=False, err='syntax error'),
    c('S-refmy', 'SURFACE', 'my $y = 1; \\my $x = \\$y; say $x;', compiles=False, err='some'),
    c('S-builtins', 'SURFACE', 'say ceil(1.2), floor(1.8), "[", trim("  a "), "]"; for my ($i, $v) (indexed "p", "q") { say "$i=$v" } my $keep = []; my $r = $keep; say reftype($r), defined blessed($r) ? 1 : 0, refaddr($r) > 0 ? 1 : 0; weaken($r); say is_weak($r) ? 1 : 0; unweaken($r); say is_tainted($r) ? 1 : 0;', out='21[a]\n0=p\n1=q\nARRAY01\n1\n0\n'),
    c('S-qw-comma', 'SURFACE', 'my @w = qw(a, b); say scalar(@w);', out='2\n', err='Possible attempt to separate words with commas'),
    c('S-symref', 'SURFACE', 'my $n = "x"; say "before"; say $$n;', out='before\n', err='as a SCALAR ref while "strict refs"', exit=255),
    c('S-defer', 'SURFACE', 'use feature "defer"; { defer { say "later" } say "now" }', out='now\nlater\n', err='defer is experimental'),
    c('S-finally', 'SURFACE', 'try { say "t" } catch ($e) { } finally { say "f" }', out='t\nf\n', err='try/catch/finally is experimental'),
    c('S-module-true', 'SURFACE', 'BEGIN { open my $f, ">", "M.pm" or die; print $f "package M; use v5.42; sub f() { return 7 } 0;\\n"; close $f } use lib "."; use M; say M::f();', out='7\n'),
    # ---- BACKGROUND.md, CLAUDE.md
    c('B-lvalue', 'BACKGROUND', 'my $x; ($x = 5) += 2; say $x;', out='7\n'),
    c('B-incr', 'BACKGROUND', 'my $s = "Zz9"; $s++; say $s;', out='AAa0\n'),
    c('B-pow', 'BACKGROUND; CLAUDE', 'say 2 ** 62;', out='4.61168601842739e+18\n'),
]

def run(perl, prelude, code, flags):
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, 'claim.pl')
        open(path, 'w', encoding='utf-8', newline='').write(prelude + code + '\n')
        env = {'PATH': os.environ.get('PATH', ''), 'PERL_HASH_SEED': '1'}
        try:
            r = subprocess.run([perl, *flags, 'claim.pl'], cwd=d, env=env, stdin=subprocess.DEVNULL,
                               capture_output=True, timeout=10)
        except subprocess.TimeoutExpired:
            return None, b'', b'(no end in 10 seconds)'
        return r.returncode, r.stdout, r.stderr

def judge(said, status, out, err):
    """What differs from what the document says; nothing if nothing does."""
    wrong = []
    if 'outbytes' in said and out != said['outbytes']:
        wrong.append(f'stdout is not the bytes {said["outbytes"]!r}')
    out, err = out.decode('utf-8', 'replace'), err.decode('utf-8', 'replace')
    if said.get('compiles', True) is False:
        if status == 0:
            wrong.append('it compiles')
        elif said.get('err', 'some') != 'some' and not re.search(said['err'], err):
            wrong.append(f'perl -c does not say /{said["err"]}/')
        return wrong, out, err
    if 'out' in said and out != said['out']:
        wrong.append(f'stdout is {out!r}, not {said["out"]!r}')
    if 'outre' in said and not re.fullmatch(said['outre'], out):
        wrong.append(f'stdout {out!r} is not /{said["outre"]}/')
    want = said.get('err', 'none')
    if want == 'none' and err:
        wrong.append('stderr is not empty')
    elif want == 'some' and not err:
        wrong.append('stderr is empty')
    elif want not in ('none', 'some') and not re.search(want, err):
        wrong.append(f'stderr does not have /{want}/')
    want = said.get('exit', 0)
    if want == 'nonzero' and status == 0 or want != 'nonzero' and status != want:
        wrong.append(f'exit status is {status}, not {want}')
    return wrong, out, err

def main(argv):
    perl = os.environ.get('CURLY_PERL', 'perl')
    prelude = NEW
    only = []
    i = 0
    while i < len(argv):
        if argv[i] == '--perl':
            perl = argv[i + 1]; i += 2
        elif argv[i] == '--old':
            prelude = OLD; i += 1
        else:
            only.append(argv[i]); i += 1
    version = subprocess.run([perl, '-e', 'print $^V'], capture_output=True, text=True).stdout
    print(f'perl {version} ({perl}), each program after: {prelude.strip()}')
    differ = 0
    for id, where, code, said in CLAIMS:
        if only and id not in only:
            continue
        compiles = said.get('compiles', True)
        flags = ['-c'] if not compiles else ['-CSDA'] if said.get('csda') else []
        status, out, err = run(perl, '' if said.get('raw') else prelude, code, flags)
        wrong, out, err = judge(said, status, out, err)
        if wrong or only:
            differ += bool(wrong)
            print(f'{"DIFFERS" if wrong else "as said"} {id} ({where})\n    {code}')
            for w in wrong:
                print(f'    {w}')
            print(f'    exit {status}; stdout {out!r}; stderr {err!r}')
    n = len(only) or len(CLAIMS)
    print(f'{n} claims, {differ} differ from what the documents say')
    return 1 if differ else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
