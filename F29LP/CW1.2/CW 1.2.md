# Yoav Levi - H00347035

## Language processing cw 1.2, grammar and parse trees.

Notes:

* For every grammar, $S$ is the start symbol.
* $T$ is the set of terminals in every grammar.
* $N$ is the set of non-terminals in every grammar.

### 1. $/a*b*/$

$$
\begin{gather*}
	\{a^nb^m|n,m\in
	\mathbb{N}\}
\end{gather*}
$$

### 2.

$$
\begin{gather*}
	N = \{S,A\},\,
	T = \{a,b\}\\\\
	S \rightarrow a S|bA\\
	A \rightarrow b A| \epsilon
\end{gather*}
$$

### 3. $/(ab)*/$

$$
\begin{gather*}
	\{(ab)^n|n\in\mathbb{N}\}
\end{gather*}
$$

### 4.

$$
\begin{gather*}\\
	N = \{S,A\},\,
	T = \{a,b\}\\\\
	S\rightarrow aA \, | \, \epsilon \\
	A\rightarrow bA
\end{gather*}
$$

### 5.$/Whiske?y/$

$$
\begin{gather*}
	\{W^nh^ni^ns^nk^ne^my^n |n=1|m\leq1|m\geq0\}
\end{gather*}
$$

### 6.

$$
\begin{gather*}
	N = \{S,B,C,D,E,F,G\}\,,
	T = \{h,i,s,k,e,y\}\\\\
	\tiny\text{Notice: "W" is terminal!}\\
	\normalsize S \rightarrow WB\\
	B \rightarrow hC\\
	C \rightarrow iD\\
	D \rightarrow sE\\
	E \rightarrow kF\\
	F \rightarrow eG\, | \, y\\
	G \rightarrow y
\end{gather*}
$$

### 7.

$$
\begin{gather*}
	N = \{S,B,C\},\,
	T = \{0,1,2,3,4,5,6,7,8,9,.\}\\\\
	S \rightarrow 1 B | 2 B | 3 B | 4 B | 5 B | 6 B | 7 B | 8 B | 9 B | 0 B\\
	B \rightarrow 1 B | 2 B | 3 B | 4 B | 5 B | 6 B | 7 B | 8 B | 9 B\\
	\tiny\text{Notice: "." is terminal}\\
	B \rightarrow . C | \epsilon\\
	C \rightarrow 0 C | 1 C | 2 C | 3 C | 4 C | 5 C | 6 C | 7 C | 8 C | 9 C\\
	C \rightarrow 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
\end{gather*}
$$

<div style="page-break-after: always; visibility: hidden">
\pagebreak
</div>

### 8.  $\{ aⁿ bⁿ | n ∈ ℕ\} \text{ - Context free}$

$$
\begin{gather*}
	N = \{S\},\,
	T = \{a,b\}\\\\
S \rightarrow aSb\\\
S \rightarrow \epsilon
\end{gather*}
$$

### 9.

$$
\begin{gather*}\\
	N = \{S\},\,
	T = \{(,),0\}\\\\
\tiny\text{Notice: "(" and ")" are terminal}\\
S \rightarrow (\, S \,)\\
S \rightarrow 0
\end{gather*}
$$

### 10.

$$
\begin{gather*}
	N = \{S,A,D,B,E\},\,
	T = \{0,1,2,3,4,5,6,7,8,9,+,*,(,)\}\\\\
	S \to ( A ) | A\\
	D \to 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9\\
	A \to D B\\
	B \to E D B\\
	B \to \epsilon\\
	E \to + | *
\end{gather*}
$$

### 11. $\text{palindromes with \{a,b\}}$

$$
\begin{gather*}
	N = \{S\},\,
	T = \{a,b\}\\\\
	S \to aSa|bSb\\
	S \to a | b\\
	S \to \epsilon
\end{gather*}
$$

### 12. $\text{parity seq}$

$$
\begin{gather*}
	N = \{S,A,B\},\,
	T = \{0,1\}\\\\
	S \to 0 S | 1 A\\
	A \to 0 A | 1 B\\
	B \to 0 B | 1 A | \epsilon
\end{gather*}
$$

### 13. $\text{numbers divsable by 4.}$

$$
\begin{gather*}
	N = \{S,A,B,C\},\,
	T = \{0,1,2,3,4,5,6,7,8,9\}\\\\
	S → 0C | 1B | 2C | 3B | 4C | 5B | 6C | 7B | 8C | 9B | A\\  
	A → 0 | 4 | 8  \\
	B → 2 | 6 | 0E | 1B | 2C | 3B | 4C | 5B | 6C | 7B | 8C | 9B \\ 
	C → 0 | 4 | 8 | 0E | 1B | 2C | 3B | 4C | 5B | 6C | 7B | 8C | 9B \\ 
	E → 0 | 0E
\end{gather*}
$$

### 16.

$$
\begin{gather*}
1.\text{ none}\\
2.\text{ Context-free}\\
3.\text{ Left-recursive and left-regular}\\
4.\text{ Context-free, left-recursive and right-recursive}\\
\end{gather*}
$$

<div style="page-break-after: always; visibility: hidden">
\pagebreak
</div>

### 17.

$$
\begin{gather*}
X\to Xa\text{ is not an object language, it's part of the meta language }\\
\text{as X is a non terminal and therefore not part of the object language.}
\end{gather*}
$$

### 18.

1.$(ab|ba)*$

$$
\begin{gather*}
	N = \{S\},\,
	T = \{a,b\}\\\\
	S\to abS | baS|\epsilon
\end{gather*}
$$

2.$\{(ab)^n a^n| n≥1\}$

$$
\begin{gather*}
	N = \{S,A\},\,
	T = \{a,b\}\\\\
	S \to abA\\
	A \to aS |a
\end{gather*}
$$

$$
\begin{gather*}
	N = \{S\},\,
	T = \{a,b\}\\\\
	S \to aSa|bSb\\
	S \to a | b\\
	S \to \epsilon
\end{gather*}
$$

$$
\begin{gather*}\\
	N = \{S,A\},\,
	T = \{a,b\}\\\\
	S \to b b A| \epsilon \\
	A \to a A | \epsilon
\end{gather*}
$$

$$
\begin{gather*}
	N = \{S\},\,
	T = \{a,b\}\\\\
	S \to a S b | a S b b | \epsilon
\end{gather*}
$$

### 20.

1.Is ambiguous as there are two or more different ways to parse the sentence "aaabaaa"

| Step | Application        | Outcome            | Production Rule |
| ---- | ------------------ | ------------------ | --------------- |
| 1    | **S**        | **aSbSa**    | S → aSbSa      |
| 2    | a**S**bSa    | a**aSa**bSa  | S → aSa        |
| 3    | aa**S**abSa  | abSa               | S → ɛ         |
| 4    | aaab**S**a   | aaab**aSa**a | S → aSa        |
| 5    | aaaba**S**aa | aaabaaa            | S → ɛ         |

and

| Step | Application         | Outcome             | Production Rule |
| ---- | ------------------- | ------------------- | --------------- |
| 1    | **S**         | **aSa**       | S → aSa        |
| 2    | a**S**a       | a**aSa**a     | S → aSa        |
| 3    | aa**S**aa     | aa**aSbSa**aa | S → aSbSa      |
| 4    | aaa**S**bSaaa | aaabSaaa            | S → ɛ         |
| 5    | aaab**S**aaa  | aaabaaa             | S → ɛ         |

2.The problem of finding ambiguousy is unsolved, meaning no one can compute ambiguousy, meaning this grammar with these production rules can very possibly be ambiguous, but we simply do not have a straight answer.

### 23.

Consider the following grammar:

$$
\begin{gather*}
〈exp〉 ::= 〈digit〉|〈exp〉∗〈digit〉|〈digit〉+〈exp〉\\
〈digit〉 ::= 2 |3 |4
\end{gather*}
$$

With the following parse trees:
![[Pasted image 20220210142446.png]]
Both parse trees accept and present the string $2+3*4$ however, they will be evaluated
quite differently as one(to the right) would be evaluated as $2 + ( 3 * 4 ) = 14$.
While the other one(to the left) would be incorrectly evaluated as $(2+3) * 4 = 20$.
