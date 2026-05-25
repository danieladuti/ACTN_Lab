## Homework requirement
1. Implement multi-prime RSA decryption (i.e., computing y^d mod n, for
n = pqr, where p, q, and r are distinct 700-bit primes) using the Chinese
remainder theorem algorithm discussed in class. Perform time comparisons
between this modular exponentiation algorithm and the regular modular
exponentiation algorithm (the one that is implemented in your large integers
library) (4p)

2. Implement multi-power RSA decryption (i.e., computing y^d mod n, for
n = (p^2)q, where p and q are distinct 700-bit primes) using the Chinese
remainder theorem algorithm and Hensel’s lifting lemma discussed in class.
Perform time comparisons between this modular exponentiation algorithm
and the regular modular exponentiation algorithm (the one that is implemented
in your large integers library) (4p)

3. Combine (1) with constructing short addition chains for the elements
d mod (p-1), d mod (q-1), d mod (r-1) (2p) (this will be discussed in the next course).

## Grading scale:
### Multiprime RSA
- correct generation of parameters (p, q, r, n, e, d, y) using large numbers (e is small, maximum 17 bits) (1p)
- decryption using the Chinese Remainder Theorem (2p)
(you have to implement Garner's algorithm)
- comparisons between the two methods (1p)

### Multipower RSA
- correct generation of parameters (p, q, n, e, d, y) using large numbers (e is small, maximum 17 bits) (1p)
- decryption using the Chinese Remainder Theorem and Hensel's Lemma (2p)
- comparisons between the two methods (1p)

### Additive chains
- using the binary method from left to right (0.5p)
- using the fixed window method from left to right (0.5p)
- using the sliding window method from left to right (0.5p)
- comparisons between the three methods (in terms of length) (0.5p)


## Barem:
(in original, in Romanian)

### Multiprime RSA
- generarea corectă a parametrilor (p, q, r, n, e, d, y) folosind numere mari  (e mic, pe maxim 17 biți) (1p)
- decriptarea folosind Teorema Chineză a Resturilor (2p)
        (trebuie să implementați algoritmul lui Garner)
- comparații între cele două metode (1p)


### Multipower RSA
- generarea corectă a parametrilor (p, q,  n, e, d, y) folosind numere mari  (e mic, pe maxim 17 biti)  (1p)
- decriptarea folosind Teorema Chineză a Resturilor și Lema lui Hensel (2p)
- comparații între cele două metode (1p)


### Lanțuri aditive
- folosind metoda binară de la stânga la dreapta (0.5p)
- folosind metoda ferestrei fixe de la stânga la dreapta (0.5p)
- folosind metoda ferestrei glisante de la stânga la dreapta (0.5p)
- comparații între cele trei metode (din punct de vedere a lungimii) (0.5p)
