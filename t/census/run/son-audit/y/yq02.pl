use v5.42;
print scalar(keys %ENV) > 0 ? "env" : "empty", "\n";
