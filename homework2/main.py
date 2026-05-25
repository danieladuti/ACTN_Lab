from Crypto.Util import number
import time


# ----------------- Setup
def generate_prime(nr_bits):
    prime = number.getPrime(nr_bits)

    #  -- Verifying the setup is correct
    # print(f"nr = {prime}")
    # print(f"nr_bits = {nr_bits}")
    # print(f"The number of bits: {prime.bit_length()}")

    return prime


def verify_pqr_distincts(p,q,r):
    while p == q or q == r or r == p:
        if p == q:
            q = generate_prime(700)
        if q == r:
            r = generate_prime(700)
        if r == p:
            p =generate_prime(700)
    return p,q,r

# function for finding out the modular inverse of a number, mod p
def inv_mod(a, p):
    return pow(a, -1, p)

# ----------------- Simple Encryption & Decryption (without TCR)
def read_message():
    #  -- 1. Reading message m from input
    try:
        m = int(input("Enter the message: "))
        if m < 0:
            raise Exception("ERROR! Please enter a positive integer")
    except ValueError:
        print("ERROR! Please enter a positive integer")
    except Exception:
        print("ERROR! Please enter a positive integer")
    else:
        return m


def encrypt(message, exp, mod):
    return pow(message, exp, mod)


def decrypt(message, exp, mod):
    return pow(message, exp, mod)


# ----------------- Encryption & Decryption with TCR
# x = x_p mod p
# x = x_q mod q
# x = x_r mod r
def garner_multiprime(x_p,x_q,x_r, p,q,r):
    mod= [p,q,r]
    solutie = []
    b = [x_p,x_q,x_r]
    x = x_p % p
    solutie.append(x)
    m = 1
    for i in range(1,len(b)):
        m*=mod[i-1]
        alfa = (b[i] - solutie[i-1])*(inv_mod(m,mod[i])) % mod[i]
        x = solutie[i-1] + alfa*m
        solutie.append(x)
    return solutie[len(solutie)-1]

# ----------------- Encryption & Decryption with Hensel's Lemma
def hensel_lemma(y, p, d, e):
    # x_p^2 = (x1x0)p
    x0 = pow((y % p), d % (p - 1), p)
    temp = (e*pow(x0,e-1,p**2) % p)
    x1 = (((y - pow(x0, e, p**2))%p) /p) * (inv_mod(temp, p))
    x_p2 = x0 + x1*p
    return x_p2

# ----------------- Encryption & Decryption with TCR
# x = x_p2 mod p
# x = x_q2 mod q
def garner_multipower(x_p,x_q, p,q):
    mod= [p,q]
    solutie = []
    b = [x_p,x_q]
    x = x_p % p
    solutie.append(x)
    m = 1
    for i in range(1,len(b)):
        m*=mod[i-1]
        alfa = (b[i] - solutie[i-1])*(inv_mod(m,mod[i])) % mod[i]
        x = solutie[i-1] + alfa*m
        solutie.append(x)
    return solutie[len(solutie)-1]


def binary_method(x, n, m):
    bits =bin(n)[2:]

    y = x
    lant = [1]

    for i in range(1, len(bits)):
        ult_exp = lant[-1]
        nou_exp = ult_exp + ult_exp # (y * y) mod m
        lant.append(nou_exp)
        y = (y * y) % m

        if bits[i] == '1':
            nou_exp = lant[-1] + 1
            lant.append(nou_exp)
            y = (y * x) % m

    return lant


def beta_ary_method(n, k):
    beta = 2 ** k
    lant = []

    for i in range(1, beta):
        lant.append(i)

    cifre = []
    temp_n = n
    while temp_n > 0:
        cifre.insert(0, temp_n % beta)
        temp_n //= beta

    exp_crt = cifre[0]

    for i in range(1, len(cifre)):
        # y = y^beta
        for _ in range(k):
            exp_crt = exp_crt * 2
            lant.append(exp_crt)

        val_cifr = cifre[i]
        if val_cifr > 0:
            exp_crt = exp_crt + val_cifr
            lant.append(exp_crt)

    return lant


def sliding_window_method(n, w):
    bits = bin(n)[2:]
    k = len(bits)
    lant = []

    lant.append(1)
    lant.append(2)

    for exp_imp in range(3, 2 ** w, 2):
        lant.append(exp_imp)

    exp_crt = 0
    i = 0

    while i < k:
        if bits[i] == '0':
            if exp_crt > 0:
                exp_crt = exp_crt * 2
                lant.append(exp_crt)
            i += 1
        else:
            lung_window = 1
            val_window = 1
            pas_final = 1

            for j in range(1, w):
                if i + j < k:
                    if bits[i + j] == '1':
                        lung_window = j + 1
                        val_window = int(bits[i:i + j + 1], 2)
                        pas_final = j + 1

            for _ in range(lung_window):
                if exp_crt > 0:
                    exp_crt = exp_crt * 2
                    lant.append(exp_crt)
                else:
                    # special case for the first found window
                    pass

            if exp_crt== 0:
                exp_crt = val_window
            else:
                exp_crt = exp_crt + val_window
                lant.append(exp_crt)

            i += lung_window

    return sorted(list(set([x for x in lant if x > 0])))



if __name__ == '__main__':
    # ------------------------ 1. Multiprime RSA
    p = generate_prime(700)
    q = generate_prime(700)
    r = generate_prime(700)

    p,q,r = verify_pqr_distincts(p,q,r)
    n= p*q*r
    fi_n = (p-1)*(q-1)*(r-1)
    print("\n The parameters for Multiprime RSA:")
    print(f' p = {p} \n q = {q} \n r = {r} \n n = {n} \n fi_n = {fi_n}')

    e = pow(2,16) + 1 # frequent choice of e
    print(f' e = {e}')
    # e = number.getPrime(secrets.choice(range(1, 17)))  # generates numbers of 1-17 bits
    # print(f' e = {e}')

    d = inv_mod(e, fi_n)
    print(f' d = {d}')

    # little verification of the property: d = e^(-1) mod fi_n => fi_n | (e*d - 1)
    print(f'verify the property - fi_n | (e*d - 1), fi_n * {(e*d - 1)//fi_n} = (e*d - 1)')

    x = read_message()
    # -------------------- Basic encryption & decryption
    start_time = time.time()
    y = encrypt(x, e, n)
    x_decrypted = decrypt(y, d, n)
    end_time = time.time()

    print(f' x = {x} \n y = {y}\n x_decrypted = {x_decrypted}\n in {end_time-start_time:.8f} seconds')

    # -------------------- Encryption & decryption with TCR
    start_time = time.time()
    d_p = d % (p - 1)
    d_q = d % (q - 1)
    d_r = d % (r - 1)
    x_p = pow((y % p), d_p, p)
    x_q = pow((y % q), d_q, q)
    x_r = pow((y % r), d_r, r)
    initial_message = garner_multiprime(x_p,x_q,x_r, p,q,r)
    end_time = time.time()
    print(f' initial_message = {initial_message} obtained\n in {end_time-start_time:.8f} seconds')

    # ------------------------ 2. Multipower RSA
    n = pow(p,2)*q
    fi_n = p*(p-1)*(q-1)
    d_pw = inv_mod(e, fi_n)
    print("\n\n\n The parameters for Multipower RSA:")
    print(f' p = {p} \n q = {q} \n n = {n} \n fi_n = {fi_n}')
    print(f' e = {e}')
    print(f' d = {d_pw}')

    # -------------------- Basic encryption & decryption
    start_time = time.time()
    y = encrypt(x, e, n)
    x_decrypted = decrypt(y, d_pw, n)
    end_time = time.time()
    print(f' x = {x} \n y = {y}\n x_decrypted = {x_decrypted}\n in {end_time - start_time:.8f} seconds')

    # -------------------- Encryption & decryption with TCR
    start_time = time.time()
    x_q2 = pow((y % q), d_pw % (q - 1), q)
    x_p2 = hensel_lemma(y, p, d_pw, e)
    initial_message = garner_multipower(x_p2, x_q2,p, q)
    end_time = time.time()
    print(f' initial_message = {initial_message} obtained\n in {end_time - start_time:.8f} seconds')


    # -------------------- 3. Optimization with addition chains


    lant_b_dp = binary_method(1, d_p, p)
    lant_beta_dp = beta_ary_method(d_p, 4)
    lant_sliding_dp = sliding_window_method(d_p,4)
    print(f"\n lant d mod p-1 = {d_p} \n -- BINARY  lung:{len(lant_b_dp)}, \n ult elem = {lant_b_dp[-1]} \n -- BETA-ARY lung:{len(lant_beta_dp)}, \n ult elem = {lant_beta_dp[-1]} \n -- SLIDING lung:{len(lant_sliding_dp)}, \n ult elem = {lant_sliding_dp[-1]}")


    lant_b_dq = binary_method(1, d_q, q)
    lant_beta_dq = beta_ary_method(d_q, 4)
    lant_sliding_dq = sliding_window_method(d_q, 4)
    print(f"\n lant d mod q-1 = {d_q} \n -- BINARY lung:{len(lant_b_dq)}, \n ult elem = {lant_b_dq[-1]} \n -- BETA-ARY lung:{len(lant_beta_dq)}, \n ult elem = {lant_beta_dq[-1]} \n -- SLIDING lung:{len(lant_sliding_dq)}, \n ult elem = {lant_sliding_dq[-1]}")

    lant_b_dr = binary_method(1, d_r, r)
    lant_beta_dr = beta_ary_method(d_r, 4)
    lant_sliding_dr = sliding_window_method(d_r, 4)
    print(f"\n lant d mod r-1 = {d_r} \n -- BINARY  lung:{len(lant_b_dr)}, \n ult elem = {lant_b_dr[-1]} \n -- BETA-ARY lung:{len(lant_beta_dr)}, \n ult elem = {lant_beta_dr[-1]} \n -- SLIDING lung:{len(lant_sliding_dr)}, \n ult elem = {lant_sliding_dr[-1]}")



