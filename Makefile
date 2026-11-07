# make test     the compiler's unit tests, the golden tests (t/run.sh), and
#               the mechanical checks (t/checks.py: every model's files are
#               what it writes now; every test has its .expected; every
#               referee in t/referee/ agrees with every test it covers)
# make unit     the unit tests alone (node:test)
# make golden   the golden tests alone; JOBS=n runs n at once
# make checks   the mechanical checks alone
# make models   rerun every model and write its files (never patch them)
# make commits  every commit since origin/main that touches the
#               implementation names a decision or a plan step
# make hooks    install the commit-msg hook that checks that as you commit
# make golden-node  the golden tests under a second Node, the
#               interpreter's second oracle: LANG_NODE_OTHER, or
#               /opt/node24/bin/node, the cloud machine's (the person's
#               machine runs its own Node with `make golden`)
# make check    type-check the compiler (needs `npm install` first)
# make decisions  the decision-log browser (tools/decisions/) for this
#               log and a64-slight's (A64=path, ../a64-slight by default),
#               as build/decisions-*.html
# make clean    remove build/
#
# This branch builds an interpreter (D28, D29): `node bin/lang.ts FILE`
# runs a program, and there's nothing to compile or link. main's Makefile
# has the compiler's targets, golden-clang and sanitize.

test: unit golden checks

# The golden tests under another Node: a host's behaviour can move
# between its versions, and the language mustn't move with it.
golden-node:
	@LANG_NODE=$${LANG_NODE_OTHER:-/opt/node24/bin/node} ./t/run.sh

unit:
	@if ls interp/tests/*.test.ts >/dev/null 2>&1; then node --test "interp/tests/**/*.test.ts"; else echo "unit: no tests yet"; fi

golden:
	@./t/run.sh

checks:
	@python3 t/checks.py

models:
	@python3 t/checks.py models --write

commits:
	@python3 t/checks.py commits

# The hooks directory asked of git, since in a worktree .git is a file
# and the hooks are the main checkout's.
hooks:
	@dir=$$(git rev-parse --git-path hooks) && mkdir -p "$$dir" && \
	printf '#!/bin/sh\nexec python3 t/checks.py commit-msg "$$1" --staged\n' > "$$dir/commit-msg" && \
	chmod +x "$$dir/commit-msg" && echo "installed $$dir/commit-msg"

check:
	npx tsc --noEmit

A64 ?= ../a64-slight
DEC = tools/decisions
# The project's other documents, those of them that exist.
DOCS = $(foreach f,PLAN DESIGN LANGUAGE BACKGROUND,$(if $(wildcard $(1)/$(f).md),--doc $(1)/$(f).md))

decisions:
	@mkdir -p build
	@python3 $(DEC)/extract.py docs/DECISIONS.md -o build/decisions-workbench.json $(call DOCS,docs)
	@python3 $(DEC)/page.py build/decisions-workbench.json -o build/decisions-workbench.html --name workbench \
		--base https://github.com/pmmc-labs/esoteric-language-workbench/blob/main/docs/
	@if [ -f $(A64)/docs/DECISIONS.md ]; then \
		python3 $(DEC)/extract.py $(A64)/docs/DECISIONS.md -o build/decisions-a64-slight.json $(call DOCS,$(A64)/docs) && \
		python3 $(DEC)/page.py build/decisions-a64-slight.json -o build/decisions-a64-slight.html --name a64-slight \
			--base https://github.com/pmmc-labs/a64-slight/blob/main/docs/ \
			$(if $(wildcard $(A64)/editors/sublime/Slight/Slight.sublime-syntax),--syntax $(A64)/editors/sublime/Slight/Slight.sublime-syntax); \
	else echo "no $(A64)/docs/DECISIONS.md: set A64 to a64-slight's checkout"; fi

clean:
	rm -rf build

.PHONY: test unit golden golden-node checks models commits hooks check decisions clean
