# Estimating Password Cracking Time ⏱️

The estimation of how long it might take a hacker to crack a password involves a few key steps and assumptions. Here's a breakdown of the calculations used in the scripts:

---

## 1. Determine the Password's Entropy (E)

**What it is:** Entropy is a measure of a password's randomness or unpredictability. It's expressed in bits. A higher entropy means a more secure password.

**Calculation:**  
**E = L × log₂(N)**

Where:  
- `L` = Length of the password (number of characters)  
- `N` = Number of possible unique characters in the character set used (pool size).  

Example values for N:  
- Lowercase letters (a–z): N = 26  
- Lowercase + Uppercase: N = 26 + 26 = 52  
- Lowercase + Uppercase + Digits: N = 52 + 10 = 62  
- Lowercase + Uppercase + Digits + Special Characters: N = 62 + 32 = 94

**Example:** For the password `"Hello123"`  
- L = 8  
- Character set includes uppercase (26), lowercase (26), digits (10)  
- So, N = 62  
- E ≈ 8 × log₂(62) ≈ 8 × 5.95 ≈ **47.6 bits**

---

## 2. Calculate the Total Search Space (S)

**What it is:** Total number of unique password combinations an attacker would theoretically try.

**Calculation:**  
**S = 2^E**  
Alternatively: **S = N^L**

Both yield the same result. Using 2^E is often more direct once entropy is known.

**Example:**  
- E ≈ 47.6  
- S ≈ 2^47.6 ≈ **2.4 × 10¹⁴ combinations**

---

## 3. Determine the Average Number of Guesses (A)

**What it is:** On average, an attacker will guess the password halfway through all combinations.

**Calculation:**  
**A = S / 2**

**Example:**  
- S ≈ 2.4 × 10¹⁴  
- A ≈ **1.2 × 10¹⁴ guesses**

---

## 4. Define the Attacker's Guessing Rate (R)

**What it is:** Number of guesses per second an attacker can make.

**Assumption in Scripts:**  
- R = **1,000,000,000 guesses/second (1 billion)**

This rate reflects a moderately powerful offline attack (e.g., using MD5 or SHA1 hashes).  
For stronger hashes like bcrypt, or online attacks, this rate would be drastically lower.

---

## 5. Calculate the Estimated Time to Crack (T)

**What it is:** Average time it would take to brute-force the password.

**Calculation:**  
**T (seconds) = A / R = (S / 2) / R**

**Example:**  
- A ≈ 1.2 × 10¹⁴ guesses  
- R = 10⁹ guesses/second  
- T ≈ **1.2 × 10⁵ seconds = 120,000 seconds**

---

## 6. Convert Time to Human-Readable Format

**Example:**  
- 120,000 seconds  
- ≈ 2,000 minutes  
- ≈ 33.33 hours  
- ≈ **1.39 days**

---

## Practical Limitations and Considerations

- **Guessing Rate (R)** is a rough estimate. It varies based on:
  - Attack method (offline vs online)
  - Hashing algorithm
  - Hardware capability

- **Max Entropy Cap:** Scripts use a cap like `MAX_ENTROPY_FOR_TIME_CALC = 256` bits.
  - Passwords exceeding this entropy are considered **"effectively uncrackable"** via brute-force.

- **Brute-Force Only:** This estimation ignores:
  - Dictionary attacks
  - Rainbow tables
  - Phishing or social engineering
  - Reused passwords
  - System or algorithm weaknesses

---

This explanation outlines the logic used to estimate password cracking time in the scripts.
