from Crypto.Util import number
import secrets
import random
import time
import itertools


# ----------------- Setup
def generate_p():
    #  -- 1. Generating p prime
    nr_bits = secrets.choice(range(161, 1024)) # chooses a number over 161 (bits)
    p = number.getPrime(nr_bits) # generates numbers of nr_bits bits

    #  -- Verifying the setup is correct
    print(f"p = {p}")
    # print(nr_bits)
    print(f"The number of bits: {p.bit_length()}")
    return p





# ----------------- Codification
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


#  -- 2. Encoding message m in a vector with components < p using mod p
def encoding_to_vector():
    p = generate_p()
    ms=read_message()

    m = []
    temp_ms = ms
    while temp_ms > 0:
        m.append(temp_ms % p)
        temp_ms = temp_ms // p
    m.reverse()
    print(f"m = {m}")

    return m,p


#  -- 2. Encoding message m in a vector with components < p using 20 characters
def encoding_to_vector2():
    p = generate_p()
    ms = read_message()

    temp_ms = str(ms)
    m = [int(temp_ms[i: i + 20]) for i in range(0, len(temp_ms), 20)]

    print(f"m = {m}")
    return m,p


#  -- 3. Encoding from polynom to y = (P(1),P(2),...,P(n))
def encoding_to_polynom():
    m,p = encoding_to_vector()
    k = len(m) + 1  # the vector m has (k-1) components
    s=1
    n=k + 2*s

    y=[] # the real codification of the message m

    for x in range(1, n + 1):
        temp_p_x = 0
        for coef in m:
            temp_p_x = (temp_p_x * x + coef) % p
        temp_p_x = (temp_p_x * x) % p
        y.append(temp_p_x)

    print(f"y = {y}")
    return y,n,p,k





# ----------------- Adding error
def adding_error():
    y,n,p,k = encoding_to_polynom()
    position = random.randint(0,n-1)
    # print(f"position: {position}")

    z=y.copy() # y with error (s=1)
    z[position] = z[position] + 1 % p
    print(f"z = {z}")

    return z,n,p,k





# ----------------- Decodification
def inv_mod(a, p):
    return pow(a, p-2, p)


#  -- 1. calculating the free coefficient with k(k-1) inversions
def calculate_fc_v1(z, k, p, A):
    start_time = time.time()
    fc = 0
    nr_inversions = 0

    for i in A:
        prod_lagrange = 1
        for j in A:
            if i == j:
                continue
            inv = inv_mod(j - i, p)
            nr_inversions += 1
            term = (j * inv) % p
            prod_lagrange = (prod_lagrange * term) % p

        fc = (fc + z[i - 1] * prod_lagrange) % p

    end_time = time.time()
    return fc, end_time - start_time, nr_inversions


#  -- 1. calculating the free coefficient with k inversions
def calculate_fc_v2(z, k, p, A):
    start_time = time.time()
    fc = 0
    nr_inversions = 0

    for i in A:
        num_com = 1
        den_com = 1
        for j in A:
            if i == j:
                continue
            num_com = (num_com * j) % p
            den_com = (den_com * (j - i)) % p

        prod_lagrange = (num_com * inv_mod(den_com, p)) % p
        nr_inversions += 1
        fc = (fc + z[i - 1] * prod_lagrange) % p

    end_time = time.time()
    return fc, end_time - start_time, nr_inversions


#  -- 1. calculating the free coefficient with 1 inversion
def calculate_fc_v3(z, k, p, A):
    start_time = time.time()

    nums = []
    dens = []

    for i in A:
        num_i = 1
        den_i = 1
        for j in A:
            if i == j:
                continue
            num_i = (num_i * j) % p
            den_i = (den_i * (j - i)) % p
        nums.append(num_i)
        dens.append(den_i)

    # The total multiplication of denominators
    prod_total_dens = 1
    for d in dens:
        prod_total_dens = (prod_total_dens * d) % p

    inv_total = inv_mod(prod_total_dens, p)

    fc = 0
    for idx, i in enumerate(A):
        # For each i we eliminate the others inversions
        prod_rest = 1
        for jdx, d in enumerate(dens):
            if idx == jdx: continue
            prod_rest = (prod_rest * d) % p

        prod_lagrange = (nums[idx] * inv_total * prod_rest) % p
        fc = (fc + z[i - 1] * prod_lagrange) % p

    end_time = time.time()
    return fc, end_time - start_time, 1


#  -- 2. Generating an A for which it's possible to reconstruct the message(P(x))
def find_correct_subset(z, k, p, n):
    all_points = list(range(1, n + 1))

    # itertools.combinations it gives us all subsets A possible with k elements
    for subset_A in itertools.combinations(all_points, k):
        A = list(subset_A)
        fc, temp, temp = calculate_fc_v3(z, k, p, A)

        if fc == 0:
            print(f"A = {A}")
            return A

    raise Exception("It's not possible to find a subset without errors.")


#  -- 5. The multiplying of two polynomials
def multiply_polys(poly1, poly2, p):
    n1 = len(poly1)
    n2 = len(poly2)

    res = [0] * (n1 + n2 - 1) # the result has the max grad: (grad1 + grad2)

    for i in range(n1):
        for j in range(n2):
            res[i + j] = (res[i + j] + poly1[i] * poly2[j]) % p
    return res


#  -- 4. the reconstruction of the polynom, of the message / interpolation for the a_i coefficients
def reconstruct_polynom(z, A, p):
    k = len(A)
    final_poly = [0] * k  # the polynom P(x) of grade (k-1)

    for i in A:
        # calculate the denominator of the Lagrange multiplication for the current i
        den_total = 1
        for j in A:
            if i == j: continue
            den_total = (den_total * (i - j)) % p

        # z_i * the inverse of the denominator
        lead_term = (z[i - 1] * inv_mod(den_total, p)) % p

        # calculate the multiplication of the polynomials (x - j)
        current_poly = [lead_term]  # constant polynom
        for j in A:
            if i == j: continue
            # multiply with the polynom (x - j)
            term_poly = [1, -j % p]
            current_poly = multiply_polys(current_poly, term_poly, p)

        # adding the resulted polynom to P(x)
        for idx, coef in enumerate(current_poly):
            final_poly[idx] = (final_poly[idx] + coef) % p

    return final_poly


#  -- 5. The actual decoding
def final_decoding():
    z, n, p, k = adding_error()
    A = find_correct_subset(z, k, p, n)

    print("\n--- Analysis ---")
    f1, t1, inv1 = calculate_fc_v1(z, k, p, A)
    f2, t2, inv2 = calculate_fc_v2(z, k, p, A)
    f3, t3, inv3 = calculate_fc_v3(z, k, p, A)

    print(f"Var 1 [k(k-1) inv]: fc={f1}, Time={t1:.8f}s, Inversions={inv1}")
    print(f"Var 2 [k inv]:      fc={f2}, Time={t2:.8f}s, Inversions={inv2}")
    print(f"Var 3 [1 inv]:      fc={f3}, Time={t3:.8f}s, Inversions={inv3}")

    print("\n--- Reconstruction of the P(x) polynom ---")
    poly_reconstruct = reconstruct_polynom(z, A, p)

    m_reconstruct = poly_reconstruct[:-1]

    print(f"initial m = {m_reconstruct}")

    final_mess = 0
    power_poly = 1
    for coef in reversed(m_reconstruct):
        final_mess += coef * power_poly
        power_poly *= p

    print(f"\n\nInitial message: {final_mess}")

    return final_mess


if __name__ == "__main__":
    final_decoding()