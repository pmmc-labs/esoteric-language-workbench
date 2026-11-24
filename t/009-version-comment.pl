# kind: refused
# perl takes `v5.42` for a version only before a blank or a semicolon. With
# a comment hard against it perl looks for a module called v5, and doesn't
# compile the file (T75).
use v5.42# the version
;
say 42;
