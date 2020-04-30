# vcard utils

Utilities for dealing with `.vcf` files.

## Install

```bash
virtualenv -p $(which python3) $PWD/.venv
```

There are no external dependencies yet.

## Utilities

### Sort

Sort `.vcf` files by certain attributes. Example:

```bash
.venv/bin/python3 -m vcard.sort N FN < your.vcf > new.vcf
```

### Diff

Gives the difference between 2 `.vcf` files, treating 2 records with same values in provided attributes as same.

If you use `diff.sh` script, it will sort the file contents first:

```bash
./diff.sh file1.vcf file2.vcf N FN
```

Sample output:

```diff
--- /dev/fd/63
+++ /dev/fd/62
@@ @@ -["vcard", [["FN", [], "text", "Danielius Russo"], ["N", [], "text", "Russo;Danielius;;;"]]]
-BEGIN:VCARD
-VERSION:3.0
-FN:Danielius Russo
-N:Russo;Danielius;;;
-TEL;TYPE=CELL:+15551234567
-item1.EMAIL;TYPE=INTERNET:Danielius.Russo@example.com
-item1.X-ABLabel:
-END:VCARD
@@ @@  ["vcard", [["FN", [], "text", "Laylah Bains"], ["N", [], "text", "Kavanagh;Ace;;;"]]]
 BEGIN:VCARD
 VERSION:3.0
 FN:Laylah Bains
 N:Kavanagh;Ace;;;
 TEL;TYPE=CELL:+15557654111
 item1.EMAIL;TYPE=INTERNET:Laylah.Bains@example.com
 item1.X-ABLabel:
 END:VCARD
@@ @@ +["vcard", [["FN", [], "text", "Renesmee Dudley"], ["N", [], "text", "Dudley;Renesmee;;;"]]]
+BEGIN:VCARD
+VERSION:3.0
+FN:Renesmee Dudley
+N:Dudley;Renesmee;;;
+TEL;TYPE=CELL:+15550000123
+item1.EMAIL;TYPE=INTERNET:Renesmee.Dudley@example.com
+item1.X-ABLabel:
+END:VCARD
@@ @@  ["vcard", [["FN", [], "text", "Tayyibah Bernal"], ["N", [], "text", "Bernal;Tayyibah;;;"]]]
 BEGIN:VCARD
 VERSION:3.0
 FN:Tayyibah Bernal
 N:Bernal;Tayyibah;;;
-TEL;TYPE=CELL:+15557654321
+TEL;TYPE=CELL:+15558654321
-item1.EMAIL;TYPE=INTERNET:Tayyibah.Bernal@example.com
+item1.EMAIL;TYPE=INTERNET:Tayyibah.Bernal@2.example.com
 item1.X-ABLabel:
 END:VCARD
```

# MIT License

Copyright (c) 2020 Leon Poon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
