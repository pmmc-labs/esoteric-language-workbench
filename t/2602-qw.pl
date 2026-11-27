# t/models/quote.py 2602
use v5.42;
use utf8;
use open ':std', ':encoding(UTF-8)';
my $x = "X"; my $n = 42; my @a = (1, 2); my @e = (); my %h = (k => "v");
{ my @w = qw(); say scalar(@w), ":", join("|", @w); }
{ my @w = qw(  =c$$  9/c
  ); say scalar(@w), ":", join("|", @w); }
{ my @w = qw(-1 
/0 
= 
c_1;  ); say scalar(@w), ":", join("|", @w); }
{ my @w = qw(?~c "  !*b	b*	/b); say scalar(@w), ":", join("|", @w); }
{ my @w = qw(	); say scalar(@w), ":", join("|", @w); }
{ my @w = qw(  Z:	|%./	! ); say scalar(@w), ":", join("|", @w); }
{ my @w = qw(=.Y 
X	); say scalar(@w), ":", join("|", @w); }
{ my @w = qw(;c@c
  9 
$_;0	. 
.9$); say scalar(@w), ":", join("|", @w); }
{ my @w = qw(a	Y"	?_"	Y;:;); say scalar(@w), ":", join("|", @w); }
{ my @w = qw(;b* 1 |'Y=  ~^); say scalar(@w), ":", join("|", @w); }
{ my @w = qw[	.b0']; say scalar(@w), ":", join("|", @w); }
{ my @w = qw[  '	*b&% |X
  ^X  ::']; say scalar(@w), ":", join("|", @w); }
{ my @w = qw[	~!?Y
  *]; say scalar(@w), ":", join("|", @w); }
{ my @w = qw[	&/0b 
*  +b0	;& 
]; say scalar(@w), ":", join("|", @w); }
{ my @w = qw[  .Z?@	" _]; say scalar(@w), ":", join("|", @w); }
{ my @w = qw[ 
Y*.
  ;?
  ]; say scalar(@w), ":", join("|", @w); }
{ my @w = qw[b@
  |  1;	]; say scalar(@w), ":", join("|", @w); }
{ my @w = qw[]; say scalar(@w), ":", join("|", @w); }
{ my @w = qw[9 ]; say scalar(@w), ":", join("|", @w); }
{ my @w = qw[]; say scalar(@w), ":", join("|", @w); }
{ my @w = qw{=+ 
c@}; say scalar(@w), ":", join("|", @w); }
{ my @w = qw{ X.$ @^+  0?Y	X%}; say scalar(@w), ":", join("|", @w); }
{ my @w = qw{|& 
:Y~ ?|  a  :^:a	}; say scalar(@w), ":", join("|", @w); }
{ my @w = qw{}; say scalar(@w), ":", join("|", @w); }
{ my @w = qw{  _ acc%
  ^  }; say scalar(@w), ":", join("|", @w); }
{ my @w = qw{ 
09  ~c
  }; say scalar(@w), ":", join("|", @w); }
{ my @w = qw{.!b}; say scalar(@w), ":", join("|", @w); }
{ my @w = qw{	_
  ZbcX _c
  "c*0 }; say scalar(@w), ":", join("|", @w); }
{ my @w = qw{- 
$9$ _-"  ?9  _^!|}; say scalar(@w), ":", join("|", @w); }
{ my @w = qw{}; say scalar(@w), ":", join("|", @w); }
{ my @w = qw<?-1>; say scalar(@w), ":", join("|", @w); }
{ my @w = qw<	>; say scalar(@w), ":", join("|", @w); }
{ my @w = qw<
  >; say scalar(@w), ":", join("|", @w); }
{ my @w = qw<$$	+";*  . .-^b a'>; say scalar(@w), ":", join("|", @w); }
{ my @w = qw<0- 
|Y	>; say scalar(@w), ":", join("|", @w); }
{ my @w = qw<  >; say scalar(@w), ":", join("|", @w); }
{ my @w = qw<^?  &;&!  +
  "  -XZ>; say scalar(@w), ":", join("|", @w); }
{ my @w = qw<+ c 
;>; say scalar(@w), ":", join("|", @w); }
{ my @w = qw<~  1a ~:b 
ab$:>; say scalar(@w), ":", join("|", @w); }
{ my @w = qw<"
  $>; say scalar(@w), ":", join("|", @w); }
say qw(a b c)[1], qw<a b c>[-1], join("", (qw(a b c))[0, 2]);
{ my @l = qw(a b) x 2; say "@l"; }
{ my ($p, $q, @r) = qw(p q r s); say $p, $q, "@r"; }
{ my $one = qw(only); say $one; }
say join(",", map { uc($_) } qw(x y)), " ", join(",", sort { $b cmp $a } qw(m z a));
for my $w (qw(i j)) { say $w }
say "a" . qw(b) . "c";
