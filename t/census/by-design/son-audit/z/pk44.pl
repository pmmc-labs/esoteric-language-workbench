use v5.42;
$_="x"; sub show { $_ } print show(), (map { show() } 1,2), show(), "\n";
