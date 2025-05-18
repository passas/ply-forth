# [Compiler] FORTH

*Framework: [Ply.Yac](https://www.dabeaz.com/ply/ply.html)*


*Programming Language: [Forth](https://www.forth.com/starting-forth/1-forth-stacks-dictionary/)*

# Disclaimer
This work was graded as 19/20.

But that's not the question in here.

This is how you define an unambigous language in order to get processed by the Ply-Yacc. The rest is history.

I'm not proud of the way that I managed to hold the translation to a Virtual Machine Instruction Set, but it is as it says "Os cães ladram, mas a caravana passa." (*Life goes on*).

# 💀

*Example of a wrong program...*

```FORTH
: TABUADA DO 11 1 DO I J * LOOP LOOP ;
TABUADA
```

*... and what we have to say about that?*
```
Erro: 3:4: Falta(m) 2 operando(s)!
   3| TABUADA

STOP: Ficheiro não compilado!
```

[^1]

[^1]: Page 20 of the academic report.
