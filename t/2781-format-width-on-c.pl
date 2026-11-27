# kind: refused
# perl pads a wide character by its bytes: no blank before it (T277).
use v5.42;
say sprintf("%3c", 0x263A);
