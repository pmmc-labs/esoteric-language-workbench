# A backslash before a punctuation mark or a space is that mark (D43).
use v5.42;
say "\ \!\#\%\&\'\(\)\*\+\,\-\.\/";
say "\:\;\<\=\>\?";
say "\[\]\^\_\`";
say "\{\|\}\~";
say length "\ \!\#\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\[\]\^\_\`\{\|\}\~";
