# kind: refused
# perl takes the last statement of the file without its semicolon too; here only a block's may go without (D75).
use v5.42;
say 1;
say 2
