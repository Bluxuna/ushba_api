# aq gaiwereba funqcionali sxvadasxva damatebiti sachiroebebistvis

# functionality for hashing

def get_hash(s: str):
    # hashing functiont

    MOD = 10000007
    p = 29

    prime_powers = [1] * len(s)
    for i in range(1, len(s)):
        prime_powers[i] = (prime_powers[i-1] * p) % MOD

    ans = 0
    for i, char in enumerate(s):
        ans = (ans + (ord(char) + 1) * prime_powers[i]) % MOD  # Use ord(char) + 1

    return str(ans)







