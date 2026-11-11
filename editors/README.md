# Editor support

## Sublime Text

`sublime/SMOL.sublime-syntax` highlights `.smol` files: comments, strings,
integers, keywords, names with their sigils, method calls, the built-in
functions, and the bootstrap's classes. `sublime/Comments.tmPreferences` makes
Cmd+/ (Ctrl+/) comment with `//`.

To install on macOS, copy both files into Sublime's User packages folder. In
Sublime, choose Preferences > Browse Packages, which opens that folder, and
copy the two files into `User`. Or link them, so that they follow the repository:

    cd editors/sublime
    ln -s "$PWD/SMOL.sublime-syntax" "$PWD/Comments.tmPreferences" \
        "$HOME/Library/Application Support/Sublime Text/Packages/User/"

Open a `.smol` file. SMOL should appear in the status bar's syntax menu, and
the file should be highlighted. If it isn't, choose SMOL there.

The highlighting is lexical: it follows the tokens of the lexer, so it cannot
tell a built-in from a name the program has bound with the same name. The list
of built-in functions and classes in `SMOL.sublime-syntax` must be kept in step
with docs/LANGUAGE.md.
