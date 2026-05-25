## Homework requirement
Implement Reed-Solomon encoding/decoding using the algorithms discussed in class. For simplicity, consider s = 1 (a single error may be corrected). Use as few modular inversions operations as possible. (10p)

## Grading scale:
### ----------------Setup----------------------------------------------------------------------------

- generation of parameter p, large prime number (over 161 bits) (1p)
(familiarization with a library dedicated to large numbers (BigInteger for Java, NTL/GMP for C/C++ etc.))

### ----------------Encoding--------------------------------------------------------------------

- encoding the input (initially specified as a file/string) as a vector of natural numbers smaller than p (1p)
- effective encoding, using Horner's scheme for evaluating the polynomial P(x) at points 1,2,...,n (2p)

### -------------Decoding-------------------------------------------------------------------

- calculation of the free coefficient - maximum (3p), as follows:
- variant using k(k-1) inversions (1p)
- variant using k inversions (1p)
- variant using a single inversion (1p)

### Others
- comparisons in terms of time for the previous variants (1p)
- reconstruction of the polynomial P(x) in the final phase of decoding, creating its own function/procedure for multiplying polynomials with coefficients of natural numbers smaller than p (2p)

## Barem:
(in original, in Romanian)

### ----------------Setup-------------------------------------------------------------------------------
- generarea parametrului p, număr prim mare (peste 161 biti) (1p)
  (familiarizarea cu o bibliotecă dedicată numerelor mari (BigInteger pentru Java, NTL/GMP pentru C/C++ etc.))

### ----------------Codificare--------------------------------------------------------------------------
- codificarea input-ului (specificat inițial ca un fișier/șir de caractere) ca vector de numere naturale mai mici decât p (1p)
- codificarea efectivă, folosind schema lui Horner pentru evaluarea polinomului P(x) în punctele 1,2,...,n (2p)


### ---------------Decodificare-------------------------------------------------------------------------
- calculul coeficientului liber - maxim (3p), după cum urmează:
- varianta folosind k(k-1) inversări (1p)
- varianta folosind k inversări (1p)
- varianta folosind o singură inversare (1p)

### În plus:
- comparații din punct de vedere al timpului pentru variantele precedente (1p)
- reconstrucția polinomului P(x) în faza finală a decodificării, creând propria funcție/procedură pentru înmulțirea de polinoame având coeficienți numere naturale mai mici decât p (2p)
