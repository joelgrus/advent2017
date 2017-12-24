import math

def is_prime(x: int) -> bool:
    for divisor in range(2, int(math.sqrt(x)) + 1):
        if x % divisor == 0:
            return False
    return True

b = 105_700
c = 122_700
h = 0


while b != c:
    if not is_prime(b):
        h = h + 1

    b = b + 17

print(h)
