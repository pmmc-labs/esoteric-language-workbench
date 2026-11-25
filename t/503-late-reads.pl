# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
{
    my $v = 3;
    say($v + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ($v x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ($v x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ($v x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ($v x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ($v x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say($v <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ($v x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((+$v) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((+$v) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((+$v) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((+$v) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((+$v) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((+$v) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((+$v) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v || 0) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v || 0) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v || 0) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v || 0) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v || 0) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v || 0) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v || 0) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 && $v) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 && $v) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 && $v) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 && $v) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 && $v) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 && $v) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 && $v) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v // 0) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v // 0) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v // 0) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v // 0) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v // 0) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v // 0) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v // 0) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 ? $v : 0) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 ? $v : 0) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 ? $v : 0) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 ? $v : 0) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 ? $v : 0) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? $v : 0) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 ? $v : 0) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 ? 0 : $v) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 ? 0 : $v) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 ? 0 : $v) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 ? 0 : $v) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 ? 0 : $v) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 ? 0 : $v) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 ? 0 : $v) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v = 4) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v = 4) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v = 4) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v = 4) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v = 4) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v = 4) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v = 4) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v += 1) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v += 1) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v += 1) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v += 1) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v += 1) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v += 1) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v += 1) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v .= '1') x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v .= '1') x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v .= '1') x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v .= '1') x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v .= '1') x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v .= '1') <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v .= '1') x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((++$v) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((++$v) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((++$v) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((++$v) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((++$v) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((++$v) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((++$v) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((--$v) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((--$v) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((--$v) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((--$v) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((--$v) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((--$v) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((--$v) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v or 0) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v or 0) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v or 0) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v or 0) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v or 0) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v or 0) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v or 0) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 and $v) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 and $v) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 and $v) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 and $v) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 and $v) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 and $v) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 and $v) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 || ($v || 1)) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 || ($v || 1)) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 || ($v || 1)) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 || ($v || 1)) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 || ($v || 1)) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v || 1)) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 || ($v || 1)) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v ? (2 && $v) : 0) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v ? (2 && $v) : 0) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v ? (2 && $v) : 0) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v ? (2 && $v) : 0) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v ? (2 && $v) : 0) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v ? (2 && $v) : 0) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v ? (2 && $v) : 0) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v++) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v++) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v++) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v++) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v++) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v++) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v++) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v--) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v--) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v--) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v--) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v--) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v--) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v--) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((-$v) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((-$v) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((-$v) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((-$v) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((-$v) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((-$v) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((-$v) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((!$v) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((!$v) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((!$v) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((!$v) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((!$v) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((!$v) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((!$v) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v . "") x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v . "") x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v . "") x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v . "") x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v . "") x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v . "") <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v . "") x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v + 0) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v + 0) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v + 0) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v + 0) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v + 0) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v + 0) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v + 0) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v * 1) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v * 1) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v * 1) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v * 1) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v * 1) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v * 1) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v * 1) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (length($v) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (length($v) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (length($v) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (length($v) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (length($v) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(length($v) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (length($v) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v == 3) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v == 3) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v == 3) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v == 3) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v == 3) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v == 3) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v == 3) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v x 1) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v x 1) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v x 1) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v x 1) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v x 1) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(($v x 1) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . (($v x 1) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 || ($v + 0)) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 || ($v + 0)) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 || ($v + 0)) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 || ($v + 0)) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 || ($v + 0)) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((0 || ($v + 0)) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((0 || ($v + 0)) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) + ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) - ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) == ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) <=> ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 ? (-$v) : 0) x ($v = 5)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) + ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) - ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) == ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) <=> ($v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 ? (-$v) : 0) x ($v += 10)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) + (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) - (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) == (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) <=> (++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 ? (-$v) : 0) x (++$v)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) + ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) - ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) == ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) <=> ($v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 ? (-$v) : 0) x ($v--)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) + ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) - ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) == ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) <=> ($v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 ? (-$v) : 0) x ($v .= '0')));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) + ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) - ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) == ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((1 ? (-$v) : 0) <=> ($v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say("" . ((1 ? (-$v) : 0) x ($v ||= 9)));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(substr('abcdefghijklmnop', $v, $v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(index('abc3abc5abc13', $v, $v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    my $w = ($v + ($v = 5)) + $v;
    say(defined($w) ? (('[' . $w) . ']') : 'undef');
}
{
    my $v = 3;
    $v += ($v = 5);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    $v = (($v++) + ($v++));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((($v = 1) + ($v = 2)) + $v);
}
{
    my $v = 3;
    my $w = 4;
    say(((($v = 5) + 0) ? $v : $w) + ($w = 100));
}
{
    my $v = 3;
    say(substr('abcdefghijklmnop', $v, $v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(index('abc3abc5abc13', $v, $v += 10));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    my $w = ($v + ($v += 10)) + $v;
    say(defined($w) ? (('[' . $w) . ']') : 'undef');
}
{
    my $v = 3;
    $v += ($v += 10);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    $v = (($v++) + ($v++));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((($v = 1) + ($v = 2)) + $v);
}
{
    my $v = 3;
    my $w = 4;
    say(((($v += 10) + 0) ? $v : $w) + ($w = 100));
}
{
    my $v = 3;
    say(substr('abcdefghijklmnop', $v, ++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(index('abc3abc5abc13', $v, ++$v));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    my $w = ($v + (++$v)) + $v;
    say(defined($w) ? (('[' . $w) . ']') : 'undef');
}
{
    my $v = 3;
    $v += (++$v);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    $v = (($v++) + ($v++));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((($v = 1) + ($v = 2)) + $v);
}
{
    my $v = 3;
    my $w = 4;
    say((((++$v) + 0) ? $v : $w) + ($w = 100));
}
{
    my $v = 3;
    say(substr('abcdefghijklmnop', $v, $v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(index('abc3abc5abc13', $v, $v--));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    my $w = ($v + ($v--)) + $v;
    say(defined($w) ? (('[' . $w) . ']') : 'undef');
}
{
    my $v = 3;
    $v += ($v--);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    $v = (($v++) + ($v++));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((($v = 1) + ($v = 2)) + $v);
}
{
    my $v = 3;
    my $w = 4;
    say(((($v--) + 0) ? $v : $w) + ($w = 100));
}
{
    my $v = 3;
    say(index('abc3abc5abc13', $v, $v .= '0'));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    my $w = ($v + ($v .= '0')) + $v;
    say(defined($w) ? (('[' . $w) . ']') : 'undef');
}
{
    my $v = 3;
    $v += ($v .= '0');
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    $v = (($v++) + ($v++));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((($v = 1) + ($v = 2)) + $v);
}
{
    my $v = 3;
    my $w = 4;
    say(((($v .= '0') + 0) ? $v : $w) + ($w = 100));
}
{
    my $v = 3;
    say(substr('abcdefghijklmnop', $v, $v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say(index('abc3abc5abc13', $v, $v ||= 9));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    my $w = ($v + ($v ||= 9)) + $v;
    say(defined($w) ? (('[' . $w) . ']') : 'undef');
}
{
    my $v = 3;
    $v += ($v ||= 9);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    $v = (($v++) + ($v++));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 3;
    say((($v = 1) + ($v = 2)) + $v);
}
{
    my $v = 3;
    my $w = 4;
    say(((($v ||= 9) + 0) ? $v : $w) + ($w = 100));
}
