import tkinter as tk
from tkinter import ttk
import math
import random
import string
import re

class PasswordEntropyCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Entropy Calculator")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Configure style
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TLabel", background="#f5f5f5", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        self.style.configure("Result.TLabel", font=("Arial", 12))
        
        # Main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(self.main_frame, text="Password Entropy Calculator", 
                 style="Title.TLabel").pack(pady=(0, 20))
        
        # Input frame
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, text="Enter Password:").pack(side=tk.LEFT, padx=(0, 10))
        self.password_entry = ttk.Entry(input_frame, width=40, show="•")
        self.password_entry.pack(side=tk.LEFT)
        self.show_password_var = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="Show", variable=self.show_password_var, 
                        command=self.toggle_password_visibility).pack(side=tk.LEFT, padx=10)
        
        # Calculate button
        ttk.Button(self.main_frame, text="Calculate Entropy", 
                  command=self.calculate_entropy).pack(pady=10)
        
        # Results frame
        self.results_frame = ttk.Frame(self.main_frame)
        self.results_frame.pack(fill=tk.X, pady=10)
        
        # Entropy bar frame
        self.bar_frame = ttk.Frame(self.main_frame)
        self.bar_frame.pack(fill=tk.X, pady=10)
        
        self.bar_canvas = tk.Canvas(self.bar_frame, height=30, bg="white", highlightthickness=1, highlightbackground="#999")
        self.bar_canvas.pack(fill=tk.X)
        
        # Generate password frame
        self.generate_frame = ttk.Frame(self.main_frame)
        self.generate_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(self.generate_frame, text="Password Length:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.length_var = tk.IntVar(value=16)
        self.length_spinbox = ttk.Spinbox(self.generate_frame, from_=8, to=32, textvariable=self.length_var, width=5)
        self.length_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Checkboxes for character types
        self.use_upper_var = tk.BooleanVar(value=True)
        self.use_lower_var = tk.BooleanVar(value=True)
        self.use_digits_var = tk.BooleanVar(value=True)
        self.use_special_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(self.generate_frame, text="Uppercase", variable=self.use_upper_var).grid(
            row=0, column=2, padx=5, pady=5, sticky=tk.W)
        ttk.Checkbutton(self.generate_frame, text="Lowercase", variable=self.use_lower_var).grid(
            row=0, column=3, padx=5, pady=5, sticky=tk.W)
        ttk.Checkbutton(self.generate_frame, text="Digits", variable=self.use_digits_var).grid(
            row=1, column=2, padx=5, pady=5, sticky=tk.W)
        ttk.Checkbutton(self.generate_frame, text="Special", variable=self.use_special_var).grid(
            row=1, column=3, padx=5, pady=5, sticky=tk.W)
        
        ttk.Button(self.generate_frame, text="Generate Strong Password", 
                  command=self.generate_password).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        # Generated password frame
        self.gen_password_frame = ttk.Frame(self.main_frame)
        self.gen_password_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(self.gen_password_frame, text="Generated Password:").pack(side=tk.LEFT, padx=(0, 10))
        self.gen_password_var = tk.StringVar()
        self.gen_password_entry = ttk.Entry(self.gen_password_frame, textvariable=self.gen_password_var, width=40)
        self.gen_password_entry.pack(side=tk.LEFT)
        
        ttk.Button(self.gen_password_frame, text="Use", 
                  command=self.use_generated_password).pack(side=tk.LEFT, padx=10)
        
    def toggle_password_visibility(self):
        """Toggle between showing and hiding the password"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")
    
    def calculate_entropy(self):
        """Calculate and display the entropy of the entered password"""
        password = self.password_entry.get()
        
        if not password:
            self.show_results("Please enter a password.", 0, "red")
            return
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Calculate entropy
        entropy, pool_size = self.get_password_entropy(password)
        entropy_percent = min(100, (entropy / 100) * 100)  # Cap at 100%
        
        # Determine strength level
        strength, color = self.get_strength_level(entropy)
        
        # Display results
        result_text = f"Entropy: {entropy:.2f} bits ({entropy_percent:.1f}%)\n"
        result_text += f"Character pool size: {pool_size}\n"
        result_text += f"Strength: {strength}"
        
        ttk.Label(self.results_frame, text=result_text, style="Result.TLabel").pack(anchor=tk.W)
        
        # Update entropy bar
        self.update_entropy_bar(entropy_percent, color)
        
        # Suggest generating a stronger password if needed
        if entropy < 75:
            ttk.Label(self.results_frame, 
                     text="This password has low entropy. Consider generating a stronger one.", 
                     foreground="red").pack(anchor=tk.W, pady=(10, 0))
    
    def get_password_entropy(self, password):
        """Calculate the entropy of a password"""
        # Determine the character pool size based on what's actually in the password
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'[0-9]', password))
        has_special = bool(re.search(r'[^a-zA-Z0-9]', password))
        
        pool_size = 0
        if has_lower: pool_size += 26
        if has_upper: pool_size += 26
        if has_digit: pool_size += 10
        if has_special: pool_size += 33  # Approximation for special characters
        
        # If we couldn't determine the pool, use a default
        if pool_size == 0:
            pool_size = 26  # Default to lowercase
        
        # Calculate entropy
        entropy = len(password) * math.log2(pool_size)
        
        return entropy, pool_size
    
    def get_strength_level(self, entropy):
        """Determine the strength level based on entropy"""
        if entropy < 40:
            return "Very Weak", "#FF0000"  # Red
        elif entropy < 60:
            return "Weak", "#FF7F00"  # Orange
        elif entropy < 80:
            return "Moderate", "#FFFF00"  # Yellow
        elif entropy < 100:
            return "Strong", "#7FFF00"  # Light green
        else:
            return "Very Strong", "#00FF00"  # Green
    
    def update_entropy_bar(self, entropy_percent, color):
        """Update the entropy visualization bar"""
        width = self.bar_canvas.winfo_width()
        if width <= 1:  # Not properly initialized yet
            # Use the configured width instead
            width = self.bar_canvas.winfo_reqwidth()
            if width <= 1:
                width = 580  # Fallback width
        
        # Clear previous bar
        self.bar_canvas.delete("all")
        
        # Draw the new bar
        bar_width = (width - 4) * (entropy_percent / 100)
        self.bar_canvas.create_rectangle(2, 2, 2 + bar_width, 28, fill=color, outline="")
        
        # Add percentage text
        text_x = width / 2
        self.bar_canvas.create_text(text_x, 15, text=f"{entropy_percent:.1f}%", fill="black")
    
    def generate_password(self):
        """Generate a strong password based on selected options"""
        length = self.length_var.get()
        
        # Define character pools based on selected options
        char_pool = ""
        if self.use_upper_var.get():
            char_pool += string.ascii_uppercase
        if self.use_lower_var.get():
            char_pool += string.ascii_lowercase
        if self.use_digits_var.get():
            char_pool += string.digits
        if self.use_special_var.get():
            char_pool += "!@#$%^&*()-_=+[]{}|;:,.<>?/"
        
        # Ensure at least one character type is selected
        if not char_pool:
            char_pool = string.ascii_lowercase
            self.use_lower_var.set(True)
        
        # Generate password
        password = ''.join(random.choice(char_pool) for _ in range(length))
        
        # Display generated password
        self.gen_password_var.set(password)
        
        # Calculate and display its entropy
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.calculate_entropy()
    
    def use_generated_password(self):
        """Use the generated password and calculate its entropy"""
        password = self.gen_password_var.get()
        if password:
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)
            self.calculate_entropy()
    
    def show_results(self, message, entropy_percent, color):
        """Show results with a specific message"""
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Display message
        ttk.Label(self.results_frame, text=message, foreground=color).pack(anchor=tk.W)
        
        # Update entropy bar
        self.update_entropy_bar(entropy_percent, color)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordEntropyCalculator(root)
    root.mainloop()
