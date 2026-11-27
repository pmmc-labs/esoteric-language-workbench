# t/models/quote.py 2603
use v5.42;
use utf8;
use open ':std', ':encoding(UTF-8)';
my $x = "X"; my $n = 42; my @a = (1, 2); my @e = (); my %h = (k => "v");
print "[", <<"TEXT", "]\n";
 / } $a[-2] 
@a[0, 1] \n
TEXT
print "[", <<"END", "]\n";
 \"

 bc$#a @e 
END
print "[", <<"EOT", "]\n";

EOT
print "[", <<"EOT", "]\n";

 $a[-2] $#a \x419

   
EOT
print "[", <<"TEXT", "]\n";
 \x41$h{k} '@e $a[-2] @e 
 !\0\${$h{k} 
.@{a} \x41
 
TEXT
print "[", <<~"END", "]\n";
	  $n \e@{a}  
	  @a $x @{a} @e @e 
	+$x @a \n$#a @e 
	$n > |
	END
print "[", <<~"TEXT", "]\n";
	  \e[\t 
	 $a[-2] 
	  [$n 
	TEXT
print "[", <<~"EOT", "]\n";
    \t[~
  !@a[0, 1] "

    
  EOT
print "[", <<~"END", "]\n";
    @a \101"
  \n$#a 9$a[-2]  
   

  END
print "[", <<~"EOT", "]\n";
  
  EOT
print "[", <<'EOT', "]\n";
aq(
a\#q(
EOT
print "[", <<'EOT', "]\n";

"a'\ \n

 q(@a}
EOT
print "[", <<'EOT', "]\n";

\n
EOT
print "[", <<'E_2', "]\n";
$x
 #'aq(q(
 
'
E_2
print "[", <<'E_2', "]\n";

q(a@a
E_2
print "[", <<~'EOT', "]\n";
	
	 
	EOT
print "[", <<~'EOT', "]\n";
    }q(q(a$x@a
     aq("q(
       
    EOT
print "[", <<~'EOT', "]\n";

      }}
        @a\
    EOT
print "[", <<~'EOT', "]\n";
  EOT
print "[", <<~'E_2', "]\n";
     ''\n
    E_2
print "[", <<TEXT, "]\n";
 =a
  ".
TEXT
print "[", <<END, "]\n";
END
print "[", <<EOT, "]\n";
 @{a} \x{263A}$a[1] ,?\\
$#a {,
EOT
print "[", <<EOT, "]\n";
 \t$h{k} =\$\$
@{a} '\n[\N{U+42}@e 
 
$n a@e a"\\
EOT
print "[", <<E_2, "]\n";
.\101

E_2
print "[", <<~TEXT, "]\n";
    TEXT
print "[", <<~END, "]\n";
     *?;a\101

    END
print "[", <<~E_2, "]\n";
     ,@{a} ^
      @e $h{k} $n 
    E_2
print "[", <<~EOT, "]\n";

      @a )
    EOT
print "[", <<~TEXT, "]\n";
	TEXT
my $s = lc <<END . "tail\n";
ABC
END
print $s;
print(<<END);
in brackets
END
say length <<'END'; # a comment after it
12345
END
say "a
b" . <<END;
c
END
