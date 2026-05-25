import secrets
from sympy import factorint
from sympy import isprime
import time


# calculate the jacobi symbol
def jacobi(a,n):
    # rule 2. (a/n) = (a mod n/n)
    a = a % n

    # rule 1. (1/n) = 1 and (0/n) = 0
    if a == 1:
        return 1
    if a == 0:
        return 0

    # rule 5. a=2: (2/n) = 1 daca n mod 8 = 1sau7 || -1 daca n mod 8 = 3sau5
    if a == 2:
        if n % 8 == 1 or n % 8 == 7:
            return 1
        if n % 8 == 3 or n % 8 == 5:
            return -1

    # rule 4. (a*b/n) = (a/n)*(b/n)
    temp = factorint(a)
    rez = 1
    for baza, exponent in temp.items():
        if exponent % 2 != 0:
            if baza == 2:
                # rule 5. a=2
                sub_rez = 1 if n % 8 in [1, 7] else -1
            else:
                # rule 3. a,n impare: (a/n) = -(n/a) daca a mod 4= 3 si n mod 4 = 3 altfel (n/a)
                if baza % 4 == 3 and n % 4 == 3:
                    sub_rez = -jacobi(n, baza)
                else:
                    sub_rez = jacobi(n, baza)
            rez *= sub_rez

    return rez


# the algorithm for Solovay-Strassen primality test
def solovay_strassen(n, nr_iter):
    for i in range(nr_iter):
        a = secrets.choice(range(2, n-2))
        temp = pow(a,(n-1)//2,n)
        if temp != 1 and temp != n-1:
            return "n compus"
        temp2 = jacobi(a,n)
        if (temp-temp2)%n!=0:
            return "n compus"
    return "n prim"


# function for verifying that a nr has the length of a multiple of n
# def multiple_n(n, length):
#     if length % n == 0:
#         return True, 0
#     else:
#         next_multiple = ((length // n) + 1) * n
#         to_add = next_multiple - length
#         return False, to_add


# # the algorithm for Lucas-Lehmer primality test for Mersenne numbers
# def lucas_lehmer1(n):
#     prim = isprime(n)
#     if not prim:
#         return "n compus deci si nr Mersenne este compus"
#     m_n = 2**n - 1
#     u = 4
#     for k in range(1,n-1):
#         temp = u**2 - 2
#         if temp < m_n:
#             u = temp % m_n
#         else:
#             bin_temp = bin(temp)[2:]
#             nr_bits = len(bin_temp)
#             flag,bits_add = multiple_n(n,nr_bits)
#             if flag:
#                 binar = bin_temp
#             else:
#                 binar = '0'*bits_add + bin_temp
#             lung = len(binar)
#             jum = lung//2
#             jum1=binar[:jum]
#             jum2=binar[jum:]
#             if int(jum1,2)+int(jum2,2)<m_n:
#                 u = int(jum1,2)+int(jum2,2)
#             else:
#                 u = int(jum1,2)+int(jum2,2)-m_n
#     if u == 0:
#         return "nr Mersenne este prim"
#     return "nr Mersenne compus"


# the algorithm for Lucas-Lehmer primality test for Mersenne numbers
def lucas_lehmer1(n):
    prim = isprime(n)
    if not prim:
        return "n compus deci si nr Mersenne este compus"
    m_n = (1<<n)-1
    u = 4
    for k in range(1,n-1):
        temp = u*u - 2
        jum2 = temp & m_n
        jum1 = temp >> n
        u = jum1 + jum2
        if u >= m_n:
            u -= m_n
    if u == 0:
        return "nr Mersenne este prim"
    return "nr Mersenne compus"


def lucas_lehmer2(n):
    prim = isprime(n)
    if not prim:
        return "n compus deci si nr Mersenne este compus"
    m_n = 2**n - 1
    u = 4
    for k in range(1,n-1):
        temp = u*u - 2
        u = temp % m_n
    if u == 0:
        return "nr Mersenne este prim"
    return "nr Mersenne compus"


if __name__ == '__main__':
    # ------------------------ 1. Solovay-Strassen primality test
    nr = int(input("n = "))
    nr_i = int(input("How many iterations for Solovay-Strassen primality test?\nnr = "))
    result= solovay_strassen(nr,nr_i)
    print(result)

    # testing the jacobi simbol
    print(jacobi(10, 53))
    print(jacobi(2,53))
    print(jacobi(5,53))

    # ------------------------ 2. Lucas-Lehmer primality test for Mersenne numbers
    put_M_n = int(input("The power of 2 for the Mersenne number?\nn = "))
    print(f"nr Mersenne: {2**put_M_n - 1}")

    # Lucas-Lehmer Optimal
    start_time = time.time()
    print(lucas_lehmer1(put_M_n))
    end_time = time.time()
    print(f'OPTIM Determined in  {end_time - start_time:.8f} seconds')

    # Lucas-Lehmer Normal
    start_time = time.time()
    print(lucas_lehmer2(put_M_n))
    end_time = time.time()
    print(f'NORMAL Determined in {end_time - start_time:.8f} seconds')