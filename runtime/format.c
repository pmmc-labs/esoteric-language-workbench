// `sprintf` and `printf` (step 16b; D124 to D127, D131), which rt.c
// includes. The format is the list's first value, a literal the compiler
// has read already (compiler/src/format.ts), so a conversion the language
// doesn't have is the runtime's internal error here, not a fault.
//
// perl formats strings and whole numbers itself, in sv_vcatpvfn, and so
// does this: C's `%b` is glibc's alone, and C leaves `#` on `%d` and `+`
// on `%x` undefined. Floats go to C's snprintf, as perl's do, but for a
// bare `%.0f`, which perl rounds itself (T280).
//
// The format is worked through twice, as `join` works through its list:
// once to count, where every fault is met, and once, after the one
// allocation, to write. Nothing is held on the C heap, so a fault leaves
// nothing behind.

typedef struct {
    char *out;          // NULL while counting
    uint64_t len;
    uint64_t chars;
} buffer;

static void put(rt_ctx *cx, buffer *b, const char *bytes, uint64_t len, uint64_t chars) {
    if (b->chars + chars > (uint64_t)INT32_MAX) rt_fault(cx, "formatted string too long");
    if (b->out != NULL) memcpy(b->out + b->len, bytes, len);
    b->len += len;
    b->chars += chars;
}

static void put_fill(rt_ctx *cx, buffer *b, char c, int64_t n) {
    if (n <= 0) return;
    if (b->chars + (uint64_t)n > (uint64_t)INT32_MAX) rt_fault(cx, "formatted string too long");
    if (b->out != NULL) memset(b->out + b->len, c, (size_t)n);
    b->len += (uint64_t)n;
    b->chars += (uint64_t)n;
}

// One conversion, as the format says it: `%-08.3x` is left, zero, width
// 8, precision 3, `x`. A width or a precision that is a star has been
// taken from the list by now.
typedef struct {
    int left, plus, space, zero, alt;
    int64_t width;          // 0 for none
    int64_t precision;      // -1 for none
    char conv;
} spec;

// A width or a precision from the list (D131): a whole number as `%d`
// takes one; past 2^31 - 1 either way, perl prints gigabytes or stops.
static int64_t star(rt_ctx *cx, rt_value v) {
    int64_t n = whole_number(cx, numeric(cx, v));
    if (n > INT32_MAX || n < -INT32_MAX) rt_fault(cx, "a format's width or precision of 2^31 or more");
    return n;
}

// The digits, a sign or a prefix, and the padding, for every conversion
// that isn't a float: C's rules, which are perl's.
static void put_number(rt_ctx *cx, buffer *b, const spec *s, const char *sign, const char *digits, int digits_len) {
    int64_t zeros = s->precision > digits_len ? s->precision - digits_len : 0;
    int64_t body = (int64_t)strlen(sign) + zeros + digits_len;
    int64_t pad = s->width > body ? s->width - body : 0;
    if (!s->left && !(s->zero && s->precision < 0)) put_fill(cx, b, ' ', pad);
    put(cx, b, sign, strlen(sign), strlen(sign));
    if (!s->left && s->zero && s->precision < 0) put_fill(cx, b, '0', pad);
    put_fill(cx, b, '0', zeros);
    put(cx, b, digits, (uint64_t)digits_len, (uint64_t)digits_len);
    if (s->left) put_fill(cx, b, ' ', pad);
}

static void format_integer(rt_ctx *cx, buffer *b, const spec *s, rt_value v) {
    number x = numeric(cx, v);
    uint64_t u;
    int negative = 0;
    if (s->conv == 'd') {
        int64_t n = whole_number(cx, x);
        negative = n < 0;
        u = negative ? -(uint64_t)n : (uint64_t)n;
    } else if (x.is_int) {
        // A negative Int as its 64 bits, as perl has it (T266).
        u = (uint64_t)x.i;
    } else {
        double t = trunc(x.n);
        if (x.split) rt_fault(cx, SPLIT);
        if (t >= TWO_63 && t < 2.0 * TWO_63) u = (uint64_t)t;
        else if (t >= -TWO_63 && t < TWO_63) u = (uint64_t)(int64_t)t;
        else rt_fault(cx, "a number outside 64 bits where a format wants a whole number");
    }
    const char *alphabet = s->conv == 'X' ? "0123456789ABCDEF" : "0123456789abcdef";
    unsigned base = s->conv == 'o' ? 8 : s->conv == 'x' || s->conv == 'X' ? 16 : s->conv == 'b' || s->conv == 'B' ? 2 : 10;
    char digits[72];
    int len = 0;
    char *end = digits + sizeof digits;
    // A precision of 0 and the value 0: no digits at all.
    if (!(u == 0 && s->precision == 0)) {
        uint64_t w = u;
        do {
            *--end = alphabet[w % base];
            len += 1;
            w /= base;
        } while (w != 0);
    }
    const char *sign = "";
    if (s->conv == 'd') sign = negative ? "-" : s->plus ? "+" : s->space ? " " : "";
    else if (s->alt && u != 0 && base == 16) sign = s->conv == 'X' ? "0X" : "0x";
    else if (s->alt && u != 0 && base == 2) sign = s->conv == 'B' ? "0B" : "0b";
    // `#` on `%o`: a leading zero, if the digits and the precision don't
    // already give one.
    if (s->conv == 'o' && s->alt && (len == 0 || *end != '0') && s->precision <= len) {
        *--end = '0';
        len += 1;
    }
    put_number(cx, b, s, sign, end, len);
}

// perl's own `%.0f` (sv.c, S_F0convert): add a half, cut, and step back
// from an odd number the half made, which is not C's rounding at the
// double just above a half (T280). NULL where perl hands it to C.
static char *f0convert(double nv, char *endbuf, int *len) {
    int neg = nv < 0;
    if (neg) nv = -nv;
    if (nv != 0.0 && nv < 18446744073709551615.0) {
        char *p = endbuf;
        uint64_t uv = (uint64_t)nv;
        if ((double)uv != nv) {
            nv += 0.5;
            uv = (uint64_t)nv;
            if (uv & 1 && (double)uv == nv) uv--;
        }
        do {
            *--p = (char)('0' + uv % 10);
        } while (uv /= 10);
        if (neg) *--p = '-';
        *len = (int)(endbuf - p);
        return p;
    }
    return NULL;
}

// A zero with a minus, to `%e`, `%f` or `%g`: perl prints `-0` or `0` by
// what the zero has been used as (T267, T282).
static int negative_zero(rt_ctx *cx, rt_value v, double d) {
    if (d != 0.0) return 0;
    if (v.tag == RT_TAG_NUM) return signbit(v.as.n) != 0;
    if (v.tag != RT_TAG_STR) return 0;
    const rt_str *s = alive(cx, v.as.s);
    uint64_t k = 0;
    while (k < s->len && blank(s->bytes[k])) k++;
    return k < s->len && s->bytes[k] == '-';
}

static void format_float(rt_ctx *cx, buffer *b, const spec *s, rt_value v) {
    double d = as_double(numeric(cx, v));
    if (negative_zero(cx, v, d)) rt_fault(cx, "a negative zero to %e, %f or %g: perl prints 0 or -0 by what the zero was used as");
    if (s->conv == 'f' && !s->left && !s->plus && !s->space && !s->zero && !s->alt && s->width == 0 && s->precision == 0) {
        char end[32];
        int len;
        char *p = f0convert(d, end + sizeof end, &len);
        if (p != NULL) {
            put(cx, b, p, (uint64_t)len, (uint64_t)len);
            return;
        }
    }
    char how[16];
    int k = 0;
    how[k++] = '%';
    if (s->left) how[k++] = '-';
    if (s->plus) how[k++] = '+';
    if (s->space) how[k++] = ' ';
    if (s->zero) how[k++] = '0';
    if (s->alt) how[k++] = '#';
    how[k++] = '*';
    how[k++] = '.';
    how[k++] = '*';
    how[k++] = s->conv;
    how[k] = '\0';
    int width = (int)s->width;
    // C's default precision, where none was given.
    int precision = s->precision < 0 ? 6 : (int)s->precision;
    int n = snprintf(NULL, 0, how, width, precision, d);
    if (n < 0) rt_internal(cx, "snprintf failed");
    if (b->chars + (uint64_t)n > (uint64_t)INT32_MAX) rt_fault(cx, "formatted string too long");
    // The NUL after it falls on the next piece's first byte, or on the
    // string's own NUL.
    if (b->out != NULL) snprintf(b->out + b->len, (size_t)n + 1, how, width, precision, d);
    b->len += (uint64_t)n;
    b->chars += (uint64_t)n;
}

// `%s`: the value made a string as `.` makes one, its width and its
// precision in characters; `0` pads with zeros, as perl does (T268, T269).
static void format_string(rt_ctx *cx, buffer *b, const spec *s, rt_value v) {
    scratch x;
    const rt_str *str = to_str(cx, v, &x);
    uint64_t chars = str->chars;
    if (s->precision >= 0 && (uint64_t)s->precision < chars) chars = (uint64_t)s->precision;
    uint64_t len = offset_of(str, chars);
    int64_t pad = s->width > (int64_t)chars ? s->width - (int64_t)chars : 0;
    if (!s->left) put_fill(cx, b, s->zero ? '0' : ' ', pad);
    put(cx, b, str->bytes, len, chars);
    if (s->left) put_fill(cx, b, ' ', pad);
}

// `%c`: a character by its number, as `chr` takes one (D127).
static void format_character(rt_ctx *cx, buffer *b, rt_value v) {
    number x = numeric(cx, v);
    double t = x.is_int ? (double)x.i : trunc(x.n);
    if (below_zero(x) || t > 0x10FFFF || (t >= 0xD800 && t <= 0xDFFF)) rt_fault(cx, "not a character");
    if (x.split) rt_fault(cx, SPLIT);
    uint32_t c = (uint32_t)t;
    char bytes[4];
    int size = c < 0x80 ? 1 : c < 0x800 ? 2 : c < 0x10000 ? 3 : 4;
    if (size == 1) {
        bytes[0] = (char)c;
    } else {
        bytes[0] = (char)((0xF00 >> size & 0xFF) | c >> 6 * (size - 1));
        for (int k = 1; k < size; k++) bytes[k] = (char)(0x80 | (c >> 6 * (size - 1 - k) & 0x3F));
    }
    put(cx, b, bytes, (uint64_t)size, 1);
}

// Reads one conversion at `p`, just past its `%`; where it ends. `want`
// counts the values it takes, stars and all.
static const char *read_spec(rt_ctx *cx, const char *p, const char *end, spec *s, int *stars_w, int *stars_p) {
    memset(s, 0, sizeof *s);
    s->precision = -1;
    *stars_w = *stars_p = 0;
    for (; p < end; p++) {
        if (*p == '-') s->left = 1;
        else if (*p == '+') s->plus = 1;
        else if (*p == ' ') s->space = 1;
        else if (*p == '0') s->zero = 1;
        else if (*p == '#') s->alt = 1;
        else break;
    }
    if (p < end && *p == '*') {
        *stars_w = 1;
        p++;
    } else {
        while (p < end && *p >= '0' && *p <= '9') s->width = s->width * 10 + (*p++ - '0');
    }
    if (p < end && *p == '.') {
        p++;
        s->precision = 0;
        if (p < end && *p == '*') {
            *stars_p = 1;
            p++;
        } else {
            while (p < end && *p >= '0' && *p <= '9') s->precision = s->precision * 10 + (*p++ - '0');
        }
    }
    if (p >= end || strchr("%scduoxXbBeEfgG", *p) == NULL || s->width > INT32_MAX || s->precision > INT32_MAX) {
        rt_internal(cx, "a format the compiler should have refused");
    }
    s->conv = *p;
    return p + 1;
}

// How many values the format takes (D126), its stars among them.
static uint64_t wanted(rt_ctx *cx, const rt_str *f) {
    const char *p = f->bytes, *end = f->bytes + f->len;
    uint64_t n = 0;
    while (p < end) {
        if (*p++ != '%') continue;
        if (p < end && *p == '%') {
            p++;
            continue;
        }
        spec s;
        int sw, sp;
        p = read_spec(cx, p, end, &s, &sw, &sp);
        n += 1 + (uint64_t)sw + (uint64_t)sp;
    }
    return n;
}

// One pass over the format and the list, counting or writing.
static void run_format(rt_ctx *cx, rt_array *a, buffer *b) {
    scratch fx;
    const rt_str *f = to_str(cx, a->items[0], &fx);
    uint64_t k = 1;
    const char *p = f->bytes, *end = f->bytes + f->len;
    while (p < end) {
        const char *q = p;
        while (q < end && *q != '%') q++;
        if (q > p) put(cx, b, p, (uint64_t)(q - p), chars_in(f, (uint64_t)(q - f->bytes)) - chars_in(f, (uint64_t)(p - f->bytes)));
        if (q >= end) break;
        q++;
        if (*q == '%') {
            put(cx, b, "%", 1, 1);
            p = q + 1;
            continue;
        }
        spec s;
        int sw, sp;
        p = read_spec(cx, q, end, &s, &sw, &sp);
        // A negative width is the `-` flag, and a negative precision
        // none, as in perl and C (T283).
        if (sw) {
            int64_t w = star(cx, a->items[k++]);
            if (w < 0) {
                s.left = 1;
                w = -w;
            }
            s.width = w;
        }
        if (sp) {
            int64_t n = star(cx, a->items[k++]);
            s.precision = n < 0 ? -1 : n;
        }
        rt_value v = a->items[k++];
        if (v.tag == RT_TAG_UNDEF) rt_fault(cx, s.conv == 's' ? "undef where a string is wanted" : "undef where a number is wanted");
        switch (s.conv) {
        case 's': format_string(cx, b, &s, v); break;
        case 'c': format_character(cx, b, v); break;
        case 'e': case 'E': case 'f': case 'g': case 'G': format_float(cx, b, &s, v); break;
        default: format_integer(cx, b, &s, v); break;
        }
    }
}

static rt_value format(rt_ctx *cx, rt_value list, const char *name) {
    rt_array *a = array_of(cx, list);
    if (a->count == 0) rt_internal(cx, "a format with no format");
    scratch fx;
    uint64_t want = wanted(cx, to_str(cx, a->items[0], &fx));
    if (want != a->count - 1) {
        char what[64];
        snprintf(what, sizeof what, "%s argument in %s", want > a->count - 1 ? "missing" : "redundant", name);
        rt_fault(cx, what);
    }
    buffer count = { NULL, 0, 0 };
    run_format(cx, a, &count);
    char *bytes;
    const rt_str *made = str_new(cx, count.len, count.chars, &bytes);
    // (The list is in a slot, and what it holds was kept by the
    // collection; its strings are read again, through `alive`.)
    buffer write = { bytes, 0, 0 };
    run_format(cx, array_of(cx, list), &write);
    if (write.len != count.len) rt_internal(cx, "a format wrote another length than it counted");
    return rt_string(made);
}

rt_value rt_sprintf(rt_ctx *cx, rt_value list) {
    return format(cx, list, "sprintf");
}

// `printf`, to stdout (D128): what `sprintf` makes, printed as `print`
// prints, with its faults for a character past ASCII.
void rt_printf(rt_ctx *cx, rt_value list) {
    rt_value made = format(cx, list, "printf");
    emit(cx, made, 0);
}
