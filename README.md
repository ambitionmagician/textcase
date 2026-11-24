# textcase

Convert text between naming and writing cases — camelCase, PascalCase, snake_case, kebab-case, CONSTANT_CASE, Title Case, and more — for programmers normalizing identifiers and writers normalizing headings. One file, no dependencies.

## Quickstart

```
python3 textcase.py --help
python3 textcase.py --to snake "parseHTTPResponse now"
```

## Usage

```
usage: textcase.py [-h] --to CASE [--keep-acronyms] [text ...]

  --to {camel,pascal,snake,kebab,constant,title,sentence,lower,upper,dot,path,train}
  --keep-acronyms       Preserve all-caps words in camel/pascal output.
  text                  Text to convert. If omitted, reads lines from stdin.
```

Words are split on spaces, underscores, hyphens, dots, and slashes, and at camel humps — including acronym boundaries, so `HTTPServer` splits as `HTTP` + `Server`. Digits stay attached to the word they follow.

## Examples

```
$ python3 textcase.py --to snake "parseHTTPResponse now"
parse_http_response_now
$ python3 textcase.py --to camel "user_id_value"
userIdValue
$ python3 textcase.py --to title "the quick-brown_fox"
The Quick Brown Fox
$ python3 textcase.py --to constant "max retry count"
MAX_RETRY_COUNT
$ printf 'hello world\n' | python3 textcase.py --to pascal
HelloWorld
```

## Configuration

None — all options are command-line flags.

## Limitations

Title Case capitalizes every word (no small-word exceptions). Word splitting is heuristic: ambiguous strings like `utf8encoder` stay one word. It converts identifiers and short headings, not prose grammar.

## License

MIT — see `LICENSE`.

By Dr. Brent Allen Jensen, Radical Blueprinting Research.

## Support this work

If this tool saved you time, you can support more open work like it:

- **BTC:** `15McijPo79Zx58NGyEf2PvaPtGqGmpztWn`
- **ETH:** `0x8C25164E9234E6A30b8E44485B79c5cE8419cF2B`

Thank you.
