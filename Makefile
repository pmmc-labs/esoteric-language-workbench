# make test     the unit tests, the golden tests (t/run.sh), and the
#               mechanical checks (t/checks.py: perl 5.42 gives every
#               test's expected output that perl can give; every model's
#               files are what it writes now; every test has its .expected)
# make unit     the unit tests alone (node:test): the compiler's passes,
#               and the runtime's, which are C programs
# make golden   the golden tests alone; JOBS=n runs n at once
# make checks   the mechanical checks alone
# make oracle   write every same and dies test's .expected from perl
#               (never by hand, and never from the compiler)
# make models   rerun every model and write its files (never patch them)
# make doctor   each tool's version; fails on a perl that isn't 5.42 with
#               64-bit integers and doubles
# make commits  every commit since origin/main that touches the
#               implementation names a decision or a plan step
# make hooks    install the commit-msg hook that checks that as you commit
# make sanitize the golden tests built with clang's UBSan and ASan, every
#               finding fatal; not part of make test, since it needs
#               clang's sanitizer runtime (Xcode has it; on Ubuntu,
#               apt-get install libclang-rt-18-dev). Run it after any
#               change to the runtime. It runs them twice: with the
#               collector's poison knob on, and off
# make check    type-check the compiler (needs `npm install` first)
# make decisions  the decision-log browser (tools/decisions/) for this
#               log and a64-slight's (A64=path, ../a64-slight by default),
#               as build/decisions-*.html
# make clean    remove build/
#
# The compiler emits C and the driver links it with cc (D3), so a binary
# runs on the machine that built it and nothing is cross-compiled.
# CURLY_PERL is the perl the checks ask (default: perl); CURLY_CC is the C
# compiler the driver and the runtime's tests call (default: cc).

test: unit golden checks

# The golden tests under another C compiler, since the cloud machine's cc
# is gcc and a Mac's is clang: CURLY_CC=clang make golden, or this.
golden-clang:
	@CURLY_CC=clang ./t/run.sh

# Twice: as the tests are always run, with a collected string's memory
# kept and marked dead, which the runtime itself checks; and with the
# poison knob off, so that the memory is really freed and it is the
# sanitizer that sees a use of it (step 7).
sanitize:
	@CURLY_CC="clang -fsanitize=undefined,address -fno-sanitize-recover=all" ./t/run.sh
	@CURLY_GC_POISON=0 CURLY_CC="clang -fsanitize=undefined,address -fno-sanitize-recover=all" ./t/run.sh

unit:
	node --test "compiler/tests/**/*.test.ts" "runtime/tests/**/*.test.ts" "t/harness/*.test.ts"

golden:
	@./t/run.sh

checks:
	@python3 t/checks.py

oracle:
	@python3 t/checks.py oracle --write

models:
	@python3 t/checks.py models --write

doctor:
	@python3 t/checks.py doctor

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
	@python3 $(DEC)/extract.py docs/DECISIONS.md -o build/decisions-curly.json $(call DOCS,docs)
	@python3 $(DEC)/page.py build/decisions-curly.json -o build/decisions-curly.html --name curly \
		--base https://github.com/pmmc-labs/esoteric-language-workbench/blob/main/docs/
	@if [ -f $(A64)/docs/DECISIONS.md ]; then \
		python3 $(DEC)/extract.py $(A64)/docs/DECISIONS.md -o build/decisions-a64-slight.json $(call DOCS,$(A64)/docs) && \
		python3 $(DEC)/page.py build/decisions-a64-slight.json -o build/decisions-a64-slight.html --name a64-slight \
			--base https://github.com/pmmc-labs/a64-slight/blob/main/docs/ \
			$(if $(wildcard $(A64)/editors/sublime/Slight/Slight.sublime-syntax),--syntax $(A64)/editors/sublime/Slight/Slight.sublime-syntax); \
	else echo "no $(A64)/docs/DECISIONS.md: set A64 to a64-slight's checkout"; fi

clean:
	rm -rf build

.PHONY: test unit golden golden-clang sanitize checks oracle models doctor commits hooks check decisions clean
