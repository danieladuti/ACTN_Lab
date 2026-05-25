from Crypto.Util import number
import random as rand
import math


# ----------------- Setup for Shanks's algorithm
def generate_prime(nr_bits):
    prime = number.getPrime(nr_bits)
    while prime % 2 == 0:
        prime = generate_prime(nr_bits)
    return prime

def generate_alpha(prime):
    alfa = rand.randint(2, prime-2)
    while pow(alfa,(prime-1)//2,prime) == 1:
        alfa = rand.randint(2, prime-2)
    return alfa

# Shanks's algorithm
def alg_shanks(p,alfa):
    eps = rand.randint(0, p-2)
    beta = pow(alfa, eps, p)
    # beta = 11
    m = math.ceil(math.sqrt(p-1))
    print(f"eps = {eps}, beta = {beta}, m = {m}")
    # baby steps
    L = {}
    for j in range(0,m):
        nr = pow(alfa,j,p)
        L[nr] = j
    # print(f"L = {L}")
    # giant steps
    aux = pow(alfa, -m, p)
    for i in range(0, m):
        aux2 = (beta * pow(aux, i, p)) %p
        if aux2 in L:
            j_magic = L[aux2]
            i_magic = i
            rez = i_magic * m + j_magic
            verif = pow(alfa, rez, p)
            return j_magic, i_magic, beta, verif, rez
    return "no j_magic", "no i_magic", "no rez", "no verif"

# ----------------- Setup for Silver-Pohlig-Hellman's algorithm
def generate_p2():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    while True:
        nr = 1
        fact = []
        for q in primes:
            e = rand.randint(20, 30)
            nr *= (q ** e)
            fact.append((q, e))

        p = nr + 1
        if number.isPrime(p):
            print(f"nr of bits for p: {p.bit_length()}")
            return p, fact


def generate_alpha2(p, factor):
    N = p - 1
    while True:
        alpha = rand.randint(2, p - 2)
        is_root = True

        for q, _ in factor:
            if pow(alpha, N // q, p) == 1:
                is_root = False
                break

        if is_root:
            return alpha


def ctr(remainders, moduli):
    suma = 0
    N_total = math.prod(moduli)

    for a, m in zip(remainders, moduli):
        N_i = N_total // m
        inv = pow(N_i, -1, m)
        suma += a * N_i * inv

    return suma % N_total


def shanks_small(alpha, beta, p, q):
    m = math.isqrt(q) + 1
    # baby steps
    L = {}
    for j in range(m):
        L[pow(alpha, j, p)] = j
    # giant steps
    aux = pow(alpha, -m, p)
    for i in range(m):
        aux2 = (beta * pow(aux, i, p)) % p
        if aux2 in L:
            return i * m + L[aux2]

    return None

# Silver-Pohlig-Hellman's algorithm
def alg_pohlig_hellman(p, alpha, beta, factor):
    moduli = []
    remainders = []

    for pi, ei in factor:
        print(f"factorul i: {pi}^{ei} ...")

        alpha_i = pow(alpha, (p - 1) // pi, p)

        S_j = 0

        for j in range(ei):
            exponent = (p - 1) // (pi ** (j + 1))

            beta_part = pow(beta, exponent, p)

            alpha_Sj = pow(alpha, -S_j, p)
            alpha_part = pow(alpha_Sj, exponent, p)

            E = (beta_part * alpha_part) % p

            c_j = shanks_small(alpha_i, E, p, pi)

            if c_j is None:
                raise ValueError(f"no c_{j} for p_i={pi}")

            S_j += c_j * (pi ** j)

        E_i = S_j

        moduli.append(pi ** ei)
        remainders.append(E_i)
        print(f" E_{pi} = {E_i} mod {pi ** ei}")

    print("apply ctr")
    E_final = ctr(remainders, moduli)
    print(f" {pow(alpha,E_final,p)}")
    print(pow(alpha,E_final,p) == beta)

    return E_final

if __name__ == '__main__':
    # ------------------------ 1. Shanks's algorithm
    print("\n# ------------------------ 1. Shanks's algorithm")
    q = generate_prime(32)
    p = 2*q + 1
    # p=13
    while not number.isPrime(p):
        q = generate_prime(32)
        p = 2 * q + 1
    print(f"q = {q}")
    print(f"p = {p}")
    alpha = generate_alpha(p)
    # alpha = 2
    i, j, beta, verif, rez = alg_shanks(p, alpha)
    print(f"i gasit: {i}, j gasit: {j} ")
    print(f"VERIFICARE: {beta} ?= {verif}")
    print(f"rezultat final: {rez}")

    # ------------------------ 2. Silver-Pohlig-Hellman's algorithm
    print("\n\n# ------------------------ 2. Silver-Pohlig-Hellman's algorithm")
    p, fact_p = generate_p2()
    print(f"p = {p}, fact_p = {fact_p}")
    alpha = generate_alpha2(p, fact_p)
    beta = pow(alpha, rand.randint(1, p - 2), p)
    print(f"alpha = {alpha}, beta = {beta}")
    eps_final = alg_pohlig_hellman(p, alpha, beta, fact_p)
    print(f"eps_final = {eps_final}")
