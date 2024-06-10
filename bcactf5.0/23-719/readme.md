# 23-719

This is was a forensics challenge.

*Given*

- a PDF with very boring content
- the flag is probably hidden in the PDF

*Idea*

- search the PDF. How?
- use `pdfgrep`

```
$ sudo apt update && sudo apt install pdfgrep
```

**First try**

```
$ pdfgrep -nr 'bcactf' # this sub-string is always present in the flag
```
No output. This pattern is not present in the PDF

**Next try**

The character `{` is also always present in the flag. Let's search for that(also it is very unlikely that `{` will be present anywhere other than flag in such a boring government document)

```
$ pdfgrep -nr '\{' .
```

This time we get some output. Also it looks like the beginning of the flag. The string `bcactf` is present but with some space in between the letters.

Great. Now let's look for the end

```
$ pdfgrep -nr '\}' .
```

With this we get the second half of the flag and we're done!

