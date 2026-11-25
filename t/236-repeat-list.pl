# In say's list, brackets round the left of x make it a list, repeated
# (T101): three values, which print as one string would. A list from step
# 9 (D80); until then this test was of its refusal.
use v5.42;
say(("a") x 3);
say(("a", "b") x 2);
