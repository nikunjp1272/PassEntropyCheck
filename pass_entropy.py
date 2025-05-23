import tkinter as tk
from tkinter import ttk
import math
import random # Note: for cryptographically secure generation, 'secrets' module is preferred.
import string
import re

# --- Configuration for Time-to-Crack ---
GUESSES_PER_SECOND = 1_000_000_000  # 1 billion guesses per second
MAX_ENTROPY_FOR_TIME_CALC = 256 # Cap entropy for practical time calculation

class PasswordEntropyCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Entropy Calculator")
        # Increased height to accommodate new info
        self.root.geometry("600x470") # Adjusted height
        self.root.resizable(False, False)

        # Configure style
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TLabel", background="#f5f5f5", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        self.style.configure("Result.TLabel", font=("Arial", 11)) # Slightly smaller for more text
        self.style.configure("Time.TLabel", background="#f5f5f5", font=("Arial", 10, "italic"))


        # Main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(self.main_frame, text="Password Entropy Calculator",
                  style="Title.TLabel").pack(pady=(0, 15)) # Adjusted padding

        # Input frame
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(fill=tk.X, pady=5) # Adjusted padding

        ttk.Label(input_frame, text="Enter Password:").pack(side=tk.LEFT, padx=(0, 10))
        self.password_entry = ttk.Entry(input_frame, width=40, show="•")
        self.password_entry.pack(side=tk.LEFT)
        self.show_password_var = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="Show", variable=self.show_password_var,
                        command=self.toggle_password_visibility).pack(side=tk.LEFT, padx=10)

        # Calculate button
        ttk.Button(self.main_frame, text="Calculate Entropy",
                   command=self.calculate_and_display_all).pack(pady=5) # Adjusted padding

        # Results frame
        self.results_frame = ttk.Frame(self.main_frame)
        self.results_frame.pack(fill=tk.X, pady=5) # Adjusted padding

        # Entropy bar frame
        self.bar_frame = ttk.Frame(self.main_frame)
        self.bar_frame.pack(fill=tk.X, pady=5) # Adjusted padding

        self.bar_canvas = tk.Canvas(self.bar_frame, height=30, bg="white", highlightthickness=1, highlightbackground="#999")
        self.bar_canvas.pack(fill=tk.X)

        # Generate password frame
        self.generate_frame = ttk.Frame(self.main_frame)
        self.generate_frame.pack(fill=tk.X, pady=10) # Adjusted padding

        ttk.Label(self.generate_frame, text="Password Length:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.length_var = tk.IntVar(value=16)
        self.length_spinbox = ttk.Spinbox(self.generate_frame, from_=8, to=32, textvariable=self.length_var, width=5)
        self.length_spinbox.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)

        # Checkboxes for character types
        self.use_upper_var = tk.BooleanVar(value=True)
        self.use_lower_var = tk.BooleanVar(value=True)
        self.use_digits_var = tk.BooleanVar(value=True)
        self.use_special_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(self.generate_frame, text="Uppercase", variable=self.use_upper_var).grid(
            row=0, column=2, padx=5, pady=2, sticky=tk.W)
        ttk.Checkbutton(self.generate_frame, text="Lowercase", variable=self.use_lower_var).grid(
            row=0, column=3, padx=5, pady=2, sticky=tk.W)
        ttk.Checkbutton(self.generate_frame, text="Digits", variable=self.use_digits_var).grid(
            row=1, column=2, padx=5, pady=2, sticky=tk.W)
        ttk.Checkbutton(self.generate_frame, text="Special", variable=self.use_special_var).grid(
            row=1, column=3, padx=5, pady=2, sticky=tk.W)

        ttk.Button(self.generate_frame, text="Generate Strong Password",
                   command=self.generate_password_and_analyze).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

        # Generated password frame
        self.gen_password_frame = ttk.Frame(self.main_frame)
        self.gen_password_frame.pack(fill=tk.X, pady=5) # Adjusted padding

        ttk.Label(self.gen_password_frame, text="Generated Password:").pack(side=tk.LEFT, padx=(0, 10))
        self.gen_password_var = tk.StringVar()
        self.gen_password_entry = ttk.Entry(self.gen_password_frame, textvariable=self.gen_password_var, width=40, state='readonly')
        self.gen_password_entry.pack(side=tk.LEFT)

        ttk.Button(self.gen_password_frame, text="Use This",
                   command=self.use_generated_password).pack(side=tk.LEFT, padx=10)

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")

    @staticmethod
    def format_time_readable(seconds):
        if seconds is None: # For cases where time is astronomical
            return "Astronomical (effectively uncrackable by brute force)"
        if seconds == 0: # Password with 0 or 1 combination (e.g. empty or entropy 0)
            return "Instantly (or less than a microsecond)"
        if seconds < 0.000001: # Microseconds
             return f"{seconds * 1_000_000:.2f} microseconds"
        if seconds < 0.001: # Milliseconds
             return f"{seconds * 1000:.2f} milliseconds"
        if seconds < 1:
            return "less than 1 second" # Or show milliseconds more precisely
        
        time_units = [
            ("year", 31536000),  # 365 days
            ("day", 86400),
            ("hour", 3600),
            ("minute", 60)
        ]
        
        if seconds >= time_units[0][1] * 1000: # Thousands of years or more
             years = seconds / time_units[0][1]
             if years < 1_000_000 : return f"{years/1_000:.2f} thousand years"
             if years < 1_000_000_000 : return f"{years/1_000_000:.2f} million years"
             if years < 1_000_000_000_000 : return f"{years/1_000_000_000:.2f} billion years"
             return f"{years/1_000_000_000_000:.2f} trillion years"

        result_str = []
        remaining_seconds = seconds
        for unit_name, unit_in_seconds in time_units:
            if remaining_seconds >= unit_in_seconds:
                count = math.floor(remaining_seconds / unit_in_seconds)
                result_str.append(f"{count} {unit_name}{'s' if count > 1 else ''}")
                remaining_seconds %= unit_in_seconds
                if len(result_str) >=2: # Show at most 2 largest units for brevity
                    break 
        if remaining_seconds > 0 and len(result_str) < 2 :
             result_str.append(f"{remaining_seconds:.0f} second{'s' if remaining_seconds > 1 else ''}")
        
        return ", ".join(result_str) if result_str else f"{seconds:.2f} seconds"


    def calculate_time_to_crack(self, entropy_bits):
        if entropy_bits <= 0: # Handles empty or single-character-pool passwords
            return 0.0
        if entropy_bits > MAX_ENTROPY_FOR_TIME_CALC:
            return None # Indicates astronomical time

        # Search space = 2^E
        # Using math.ldexp(1.0, entropy_bits) is equivalent to 2**entropy_bits for floats
        # and can be more stable or faster for some interpreter versions.
        try:
            search_space = math.pow(2, entropy_bits)
        except OverflowError:
            return None # Astronomical time

        # Average attempts = search_space / 2
        # Time = average_attempts / guesses_per_second
        time_seconds = (search_space / 2) / GUESSES_PER_SECOND
        return time_seconds

    def calculate_and_display_all(self):
        password = self.password_entry.get()

        if not password:
            self.show_results("Please enter a password.", 0, "red", None)
            return

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        entropy, pool_size = self.get_password_entropy(password)
        # Cap entropy for bar percentage display at 100 bits = 100%
        # This is different from MAX_ENTROPY_FOR_TIME_CALC
        entropy_percent_for_bar = min(100, (entropy / 100.0) * 100.0)

        strength, color = self.get_strength_level(entropy)

        # Calculate time to crack
        time_seconds = self.calculate_time_to_crack(entropy)
        readable_time = self.format_time_readable(time_seconds)

        self.show_results(
            f"Entropy: {entropy:.2f} bits\n"
            f"Character Pool Size: {pool_size}\n"
            f"Strength: {strength}",
            entropy_percent_for_bar,
            color,
            readable_time
        )
        
        # Suggest generating a stronger password if needed
        if entropy < 75: # Using 75 bits as a threshold for "low"
            ttk.Label(self.results_frame,
                      text="This password has low entropy. Consider generating a stronger one.",
                      foreground="red", style="TLabel").pack(anchor=tk.W, pady=(5, 0))


    def get_password_entropy(self, password):
        if not password: return 0, 0
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'[0-9]', password))
        has_special = bool(re.search(r'[^a-zA-Z0-9]', password))

        pool_size = 0
        if has_lower: pool_size += 26
        if has_upper: pool_size += 26
        if has_digit: pool_size += 10
        if has_special: pool_size += 33  # Approximation for special characters from original code

        if pool_size == 0: # e.g. password is all spaces or unknown characters
            pool_size = 1 # Avoid log2(0) or log2(1) issues if only unknown chars. Or default to 26 like original.
                          # Let's stick to original's default if it was truly unclassified.
                          # The original code set pool_size = 26 if all checks failed.
                          # Here, if length > 0 but pool_size is 0, it means unknown chars.
                          # Using pool_size = 1 means 0 entropy from log2(1).
                          # If using 26:
            pool_size = 26 # Defaulting to lowercase as per original logic for unclassified.


        entropy = len(password) * math.log2(pool_size) if pool_size > 0 else 0
        return entropy, pool_size

    def get_strength_level(self, entropy):
        if entropy < 40: return "Very Weak", "#FF0000"  # Red
        elif entropy < 60: return "Weak", "#FF7F00"  # Orange
        elif entropy < 80: return "Moderate", "#FFFF00"  # Yellow (text might be hard to see)
        elif entropy < 100: return "Strong", "#7FFF00"  # Light green
        else: return "Very Strong", "#00FF00"  # Green

    def update_entropy_bar(self, entropy_percent, color):
        # Delay to ensure canvas width is determined
        self.root.after(50, lambda: self._draw_bar(entropy_percent, color))

    def _draw_bar(self, entropy_percent, color):
        width = self.bar_canvas.winfo_width()
        if width <= 1: width = 580 # Fallback

        self.bar_canvas.delete("all")
        bar_fill_width = (width - 4) * (entropy_percent / 100.0)
        self.bar_canvas.create_rectangle(2, 2, 2 + bar_fill_width, 28, fill=color, outline="")
        self.bar_canvas.create_text(width / 2, 15, text=f"{entropy_percent:.1f}%", fill="black", font=("Arial", 10, "bold"))


    def generate_password_and_analyze(self):
        length = self.length_var.get()
        char_pool = ""
        if self.use_upper_var.get(): char_pool += string.ascii_uppercase
        if self.use_lower_var.get(): char_pool += string.ascii_lowercase
        if self.use_digits_var.get(): char_pool += string.digits
        if self.use_special_var.get(): char_pool += "!@#$%^&*()-_=+[]{}|;:,.<>?/" # From original

        if not char_pool:
            char_pool = string.ascii_lowercase # Default
            self.use_lower_var.set(True) # Reflect default in UI

        # Using random.choice as per original. For stronger crypto, use secrets.choice
        password = ''.join(random.choice(char_pool) for _ in range(length))
        self.gen_password_var.set(password)

        # Automatically set this generated password in the entry and analyze
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.calculate_and_display_all()

    def use_generated_password(self):
        password = self.gen_password_var.get()
        if password:
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)
            self.calculate_and_display_all()

    def show_results(self, message, entropy_percent_for_bar, color, readable_time):
        # Clear previous results in results_frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.results_frame, text=message, style="Result.TLabel", justify=tk.LEFT).pack(anchor=tk.W)

        if readable_time is not None:
            time_message = f"Estimated time to crack: {readable_time}"
            ttk.Label(self.results_frame, text=time_message, style="Time.TLabel").pack(anchor=tk.W, pady=(5,0))
            ttk.Label(self.results_frame,
                      text=f"(Assuming {GUESSES_PER_SECOND/1_000_000_000:.0f} billion guesses/sec by attacker)",
                      font=("Arial", 8, "italic"), background="#f5f5f5").pack(anchor=tk.W)


        self.update_entropy_bar(entropy_percent_for_bar, color)


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordEntropyCalculator(root)
    root.mainloop()
