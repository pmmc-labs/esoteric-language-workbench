**D31. Functions: a program is any number of definitions, `(def (name
param ...) body)`, and then one expression; a call is `(name arg
...)`.** *(Default, Claude's, written for the interpreter experiments
the person asked for, to check what is particular to an interpreter;
fair to revisit.)* A definition names a function, its parameters (none
or more, each a name: a symbol, never an integer or a boolean) and its
body, one expression. The definitions
come first and the expression last, and every definition sees every
other whatever their order, so functions may call themselves and each
other. A parameter is visible in its own function's body and nowhere
else, and evaluates to the value the call gave it. A call applies a
defined function to as many arguments as it has parameters. Functions
are not values: a function's name is only ever a call's head, and a
parameter only ever a value, so the language stays first order. Each of
these is an error before running (D28): a definition after the
expression, or anywhere but the top; a program of definitions with no
expression; two definitions of one name; a definition whose name is an
operator, `if`, `within` or `def`; a `def` of other than two parts, or
whose first part isn't a list of names; two parameters with one name,
or a parameter with the name of a function, an operator, `if`, `within`
or `def`; a call with the wrong number of arguments (`f takes 2
arguments, not 3`, as an operator's); a name that is neither a
parameter in scope nor a call's head; a function's name used as a
value; a parameter used as a call's head. Rejected: functions as values,
and `lambda` (closures are a step of their own, and not what this one
is for); definitions of values; definitions inside a body.

**D32. A call evaluates its arguments left to right, then is charged
as one operation, then is checked for depth (D34), then evaluates the
body with the parameters bound to the arguments.** *(Default, Claude's,
as D31.)* D21 said a call would need to be an operation when calls
came, or a recursive program would run outside every budget: so `(within
1 (f (+ 1 2)))` faults `budget spent` whatever `f`'s body is, the `+`
and the call being two. Charged after the arguments and before the
body, as D22 charges an operator after its operands and before its own
checks. The arguments' order is D25's: the first fault in it is the
one reported. A function's body runs under every budget in force where
it's called (D23), whichever function's `within` set it. Rejected: calls free (D21's reason); charging when the
call's form is entered, before the arguments (D22's reason); charging
when the body returns (a call that never returns would never be
charged).

**D33. A call in tail position replaces its caller, so any number of
tail calls run in constant space.** *(Default, Claude's, as D31.)* A
function's body is in tail position, and so are both branches of an
`if` in tail position; nothing else is: not an operator's operand, an
`if`'s test, a call's argument, a `within`'s budget or body (when the
body ends the outer budget is put back, so the `within` is still in
progress), nor the program's own expression (a call from it makes
depth 1, D34). The language has no loop but a function that calls itself,
so this is what makes a loop: `(def (count n acc) (if (== n 0) acc
(count (- n 1) (+ acc 1))))` and `(count 1000000 0)` is `1000000`. A
tail call is still charged (D32), and adds nothing to the depth, so it
never faults `stack`. Rejected: no tail calls (every loop would be
bounded by D34's depth); a `within`'s body in tail position (the budget
is put back after it, which is work the caller still has to do).

**D34. Calls not in tail position may nest 10,000 deep; the call that
would make it 10,001 faults `stack`.** *(Default, Claude's, as D31.)*
The depth is the number of calls in progress, a tail call replacing its
caller rather than adding to it (D33); the program's expression is at
depth 0, and a call from it makes depth 1. So `(def (sum n) (if (== n
0) 0 (+ n (sum (- n 1)))))` gives `(sum 9999)` as `49995000`, ten
thousand calls from `(sum 9999)` down to `(sum 0)`, and `(sum 10000)`
faults `stack`: `fault: stack` on stderr, exit 1, as
every fault (D6). The check comes after the call's charge (D32) and
before its body, so a call refused for depth has been charged, and one
refused by its budget never reaches the check. A fixed number, so a
program behaves the same under every Node and on every machine, which
the host's own stack doesn't (`make golden-node`), and one past what a
tree-walker reaches if it recurses on the host's stack for every call,
so the interpreter decides its depth and the host doesn't. That
overtakes D30's reason for keeping the evaluator on the host's stack
(no program was deep enough to need a stack of its own): one now is.
D30's limit on nesting in the source is another thing and stays. Rejected: no limit
(the failure would come when memory ran out, in the host's words); the
host's stack as the limit (it differs between Node versions and
machines, and a golden test at the edge would pass on one and fail on
another); a limit as low as a naive tree-walker reaches (the language's
depth would be the host's accident).

