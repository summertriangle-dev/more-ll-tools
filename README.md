### Programs

`cardstacker4x.py`: Generate SIF 4.x card images from cache.

As described, pastes layers together to make new-style cards.
Sample output: https://icebluenoshunkan.kirara.ca/card/card_960_t.png

A full cache is required; all files must be decrypted and cut.

`detable.py`: Encrypted sqlite3 fixer-upper.

Fixes SQLite3 tables that have partial encrypted columns. Rows are decrypted and
written back to the same file. Then the database can be used as if it never had
encrypted rows.

This program can safely be run multiple times on the same file,
or on files without encrypted rows.

A keybag is required. Sample keybag file:

```json
{"11037": {"key": "AAAAAAAAAAAAAAAAAAAAAA=="}}
```

### License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
