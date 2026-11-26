use v5.42;
use feature 'class';
no warnings 'experimental::class';
class Log {
    field $log = "";
    ADJUST { $log .= "start" }
    method add ($x) { $log .= "<$x>"; return $self }
    method close { $log = "[$log]"; return $log }
}
print Log->new->add("a")->add("b")->close, "\n";
