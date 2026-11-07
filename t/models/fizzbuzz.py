#!/usr/bin/env python3
"""Model for examples/fizzbuzz.strata: FizzBuzz, 1 to 100.

Computed from the rule directly: multiples of 3 say Fizz, of 5 say Buzz,
of both the two words joined, anything else the number.

    python3 t/models/fizzbuzz.py > examples/fizzbuzz.expected
"""
for i in range(1, 101):
    print(("Fizz" if i % 3 == 0 else "") + ("Buzz" if i % 5 == 0 else "") or i)
