// A format of `sprintf` or `printf` (step 16b; D124 to D127, D131): a
// string literal with no variable in it, read here as the program
// compiles, so that every conversion is one the language has and the
// runtime, which reads it again, finds nothing it doesn't expect.
import { refuse } from './errors.ts';
import type { Expr, Pos } from './ast.ts';

// The conversions (D125), and the flags each may take; `%%` takes none.
const CONVERSIONS = 'scduoxXbBeEfgG';
const NUMERIC_FLAGS = '-+ 0#';
const FLAGS: Readonly<Record<string, string>> = { s: '-0', c: '' };
// perl's other spellings, and what the language writes for each.
const OTHER: Readonly<Record<string, string>> = { i: '%d', D: '%ld, which is %d', U: '%lu, which is %u', O: '%lo, which is %o', F: '%f' };
// What perl ignores between the flags and the conversion (T270's kin).
const SIZES = 'hlqLVztj';
const LIMIT = 2147483647;

// The format's value is checked, after its escapes: `"\x25d"` is `%d`
// (D131). How many values it takes is the runtime's to count.
export const checkFormat = (args: readonly Expr[], name: string, pos: Pos): void => {
    const f = args[0];
    if (f === undefined) return refuse(`${name} needs a format: ${name}("...", ...)`, pos);
    if (f.kind !== 'str') {
        return refuse(`${name}'s format is a string literal with no variable in it (D124): perl takes the first value of an array, or a string made as the program runs, for one (T274)`, f.pos);
    }
    const text = f.value;
    const at = f.pos;
    const bad = (what: string): never => refuse(`${what} in ${name}'s format`, at);
    for (let k = 0; k < text.length; k++) {
        if (text[k] !== '%') continue;
        const from = k;
        k += 1;
        if (k >= text.length) bad("a '%' at the end, which perl warns of (T270): write %% for the character");
        if (text[k] === '%') continue;
        let flags = '';
        while (k < text.length && NUMERIC_FLAGS.includes(text[k]!)) flags += text[k++];
        const number = (): void => {
            if (text[k] === '*') {
                k += 1;
                return;
            }
            let digits = '';
            while (k < text.length && text[k]! >= '0' && text[k]! <= '9') digits += text[k++];
            if (digits !== '' && Number(digits) > LIMIT) bad(`a width or precision of 2^31 or more, ${digits}, which perl does not survive (T271),`);
        };
        if (text[k] === '$' || /^[0-9]+\$/.test(text.slice(k))) bad(`an argument by its number, ${text.slice(from, k + 3)}..., which is not in the language (T276),`);
        const widthAt = k;
        number();
        const width = k > widthAt;
        if (text[k] === '$') bad('an argument by its number, which is not in the language (T276),');
        let precision = false;
        if (text[k] === '.') {
            k += 1;
            precision = true;
            number();
        }
        const conv = text[k] ?? '';
        const shown = text.slice(from, k + 1);
        if (conv === '') bad(`an unfinished conversion, ${shown}, which perl prints as it is and warns of (T270),`);
        if (conv === '%') bad(`a flag, width or precision on %%, ${shown}, which perl pads: write the padding,`);
        if (SIZES.includes(conv)) bad(`a size letter, ${shown}..., which perl ignores: leave it out,`);
        if (OTHER[conv] !== undefined) bad(`${shown}, perl's other spelling of ${OTHER[conv]}: write that,`);
        if (conv === 'v' || conv === 'n' || conv === 'p' || conv === 'a' || conv === 'A') {
            bad(`${shown}, which is not in the language (${conv === 'v' ? 'a version string\'s format' : conv === 'n' ? 'a write to its argument' : conv === 'p' ? 'an address' : 'a hex float'}; T276),`);
        }
        if (!CONVERSIONS.includes(conv)) bad(`${shown}, which is no conversion: perl prints it as it is and warns (T270),`);
        const allowed = FLAGS[conv] ?? NUMERIC_FLAGS;
        for (const flag of flags) {
            if (!allowed.includes(flag)) bad(`the flag '${flag}' on %${conv}, which perl ignores${conv === 'c' ? '' : ' there'},`);
        }
        if (conv === 'c' && (width || precision)) bad("a width or a precision on %c: perl pads a character past U+00FF by its bytes (T277), and %.0c is nothing,");
    }
};
