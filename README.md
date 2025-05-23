# 🔐 Password Entropy Calculator

A desktop GUI application built using Python and Tkinter to analyze the strength of passwords based on entropy and estimate how long they would take to crack using brute-force methods.

## 🚀 Features

- **Password Entropy Calculation**  
  Enter any password to see its entropy in bits, character pool size, strength category, and estimated time to crack.

- **Visual Feedback**  
  An interactive entropy strength bar visualizes password strength with color-coded feedback (Very Weak to Very Strong).

- **Time-to-Crack Estimation**  
  Based on entropy and assuming 1 billion guesses per second, it estimates how long a brute-force attack would take.

- **Password Generator**  
  Generate strong passwords of customizable length and character types (uppercase, lowercase, digits, special characters).

- **One-Click Use**  
  Easily insert a generated password into the entropy analyzer with one click.

## 📊 How Entropy and Crack Time Are Calculated

1. **Entropy Formula:**  
Entropy (bits) = Length × log2(Pool Size)
- Pool Size is determined by which character types are used.
- For example, using uppercase + lowercase + digits = 26 + 26 + 10 = 62.

2. **Search Space:**  
2^Entropy = Total possible combinations

3. **Crack Time Estimate:**  
- Average attempts needed = 2^Entropy / 2
- Time to crack = Average attempts / 1,000,000,000 guesses per second

4. **Output:**  
Time is presented in human-readable format (e.g., hours, years, centuries).

## 🖥️ User Interface

- **Input Field** for entering passwords.
- **Entropy Bar** showing password strength visually.
- **Password Generator Options** to toggle:
- Uppercase letters
- Lowercase letters
- Digits
- Special characters
- **Result Display** showing:
- Entropy
- Strength label (e.g., Weak, Moderate)
- Estimated time to crack

## 🛠️ Requirements

- Python 3.x
- No external libraries required (uses built-in `tkinter`, `math`, `random`, `string`, `re`)
