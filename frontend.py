"""
ImageShield - Secure Image Encryption Tool
Frontend GUI Implementation
Built with Tkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

class ImageEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ImageShield - Secure Image Encryption Tool")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f5f7fa")
        
        # State variables
        self.selected_file_path = None
        self.encrypted_data = None
        self.is_locked_out = False
        self.failed_attempts = 0
        self.lockout_time_remaining = 0
        
        # Create main UI
        self.create_header()
        self.create_main_content()
        self.create_status_bar()
        
    def create_header(self):
        """Create the top header section"""
        header_frame = tk.Frame(self.root, bg="#667eea", height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🔐 ImageShield",
            font=("Arial", 32, "bold"),
            bg="#667eea",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Secure PNG/JPG Image Encryption Tool",
            font=("Arial", 12),
            bg="#667eea",
            fg="white"
        )
        subtitle_label.pack()
        
    def create_main_content(self):
        """Create the main content area"""
        # Main container
        main_container = tk.Frame(self.root, bg="#f5f7fa")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Encrypt/Decrypt
        self.encrypt_decrypt_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.encrypt_decrypt_tab, text="  Encrypt / Decrypt  ")
        self.create_encrypt_decrypt_ui()
        
        # Tab 2: Gallery
        self.gallery_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.gallery_tab, text="  Gallery  ")
        self.create_gallery_ui()
        
    def create_encrypt_decrypt_ui(self):
        """Create the encrypt/decrypt interface"""
        # Top section - Operation selection
        operation_frame = tk.Frame(self.encrypt_decrypt_tab, bg="white", pady=20)
        operation_frame.pack(fill=tk.X, padx=30)
        
        tk.Label(
            operation_frame,
            text="Select Operation:",
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(anchor=tk.W)
        
        # Radio buttons for operation
        self.operation_var = tk.StringVar(value="encrypt")
        
        radio_frame = tk.Frame(operation_frame, bg="white")
        radio_frame.pack(anchor=tk.W, pady=10)
        
        tk.Radiobutton(
            radio_frame,
            text="🔒 Encrypt Image",
            variable=self.operation_var,
            value="encrypt",
            font=("Arial", 12),
            bg="white",
            command=self.on_operation_change
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Radiobutton(
            radio_frame,
            text="🔓 Decrypt Image",
            variable=self.operation_var,
            value="decrypt",
            font=("Arial", 12),
            bg="white",
            command=self.on_operation_change
        ).pack(side=tk.LEFT, padx=10)
        
        # File selection section
        file_frame = tk.Frame(self.encrypt_decrypt_tab, bg="white", pady=10)
        file_frame.pack(fill=tk.X, padx=30)
        
        tk.Label(
            file_frame,
            text="Select File:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W)
        
        file_select_frame = tk.Frame(file_frame, bg="white")
        file_select_frame.pack(fill=tk.X, pady=10)
        
        self.file_path_var = tk.StringVar(value="No file selected")
        tk.Entry(
            file_select_frame,
            textvariable=self.file_path_var,
            font=("Arial", 10),
            state="readonly",
            width=60
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            file_select_frame,
            text="📂 Browse",
            command=self.browse_file,
            font=("Arial", 10, "bold"),
            bg="#667eea",
            fg="white",
            padx=20,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            file_select_frame,
            text="🗂️ From Gallery",
            command=self.select_from_gallery,
            font=("Arial", 10, "bold"),
            bg="#43e97b",
            fg="white",
            padx=20,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT)
        
        # Password section
        password_frame = tk.Frame(self.encrypt_decrypt_tab, bg="white", pady=10)
        password_frame.pack(fill=tk.X, padx=30)
        
        tk.Label(
            password_frame,
            text="Enter Password:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W)
        
        password_input_frame = tk.Frame(password_frame, bg="white")
        password_input_frame.pack(fill=tk.X, pady=10)
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            password_input_frame,
            textvariable=self.password_var,
            font=("Arial", 12),
            show="●",
            width=40
        )
        self.password_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        self.show_password_var = tk.BooleanVar()
        tk.Checkbutton(
            password_input_frame,
            text="Show Password",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
            font=("Arial", 10),
            bg="white"
        ).pack(side=tk.LEFT)
        
        # Lockout warning label
        self.lockout_label = tk.Label(
            password_frame,
            text="",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#ff4444"
        )
        self.lockout_label.pack(anchor=tk.W, pady=5)
        
        # Attempts remaining label
        self.attempts_label = tk.Label(
            password_frame,
            text="",
            font=("Arial", 9),
            bg="white",
            fg="#ff9800"
        )
        self.attempts_label.pack(anchor=tk.W)
        
        # Action buttons
        action_frame = tk.Frame(self.encrypt_decrypt_tab, bg="white", pady=20)
        action_frame.pack(fill=tk.X, padx=30)
        
        self.execute_button = tk.Button(
            action_frame,
            text="🔒 ENCRYPT IMAGE",
            command=self.execute_operation,
            font=("Arial", 14, "bold"),
            bg="#667eea",
            fg="white",
            padx=40,
            pady=15,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.execute_button.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            action_frame,
            text="🔄 Reset",
            command=self.reset_form,
            font=("Arial", 12),
            bg="#e0e0e0",
            fg="#333",
            padx=30,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT)
        
        # Save options (for encryption)
        self.save_options_frame = tk.Frame(self.encrypt_decrypt_tab, bg="white", pady=10)
        self.save_options_frame.pack(fill=tk.X, padx=30)
        
        tk.Label(
            self.save_options_frame,
            text="Save encrypted file to:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack(anchor=tk.W)
        
        self.save_location_var = tk.StringVar(value="database")
        
        save_radio_frame = tk.Frame(self.save_options_frame, bg="white")
        save_radio_frame.pack(anchor=tk.W, pady=5)
        
        tk.Radiobutton(
            save_radio_frame,
            text="💾 Database (with gallery)",
            variable=self.save_location_var,
            value="database",
            font=("Arial", 10),
            bg="white"
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Radiobutton(
            save_radio_frame,
            text="📁 File System (.enc file)",
            variable=self.save_location_var,
            value="file",
            font=("Arial", 10),
            bg="white"
        ).pack(side=tk.LEFT, padx=10)
        
        # Preview section
        preview_frame = tk.Frame(self.encrypt_decrypt_tab, bg="white", pady=20)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=30)
        
        tk.Label(
            preview_frame,
            text="Preview:",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W)
        
        # Image preview containers
        preview_container = tk.Frame(preview_frame, bg="white")
        preview_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Original image preview
        original_frame = tk.Frame(preview_container, bg="#f0f4ff", relief=tk.RIDGE, bd=2)
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(
            original_frame,
            text="Original Image",
            font=("Arial", 10, "bold"),
            bg="#f0f4ff"
        ).pack(pady=5)
        
        self.original_image_label = tk.Label(
            original_frame,
            text="No image loaded",
            bg="#f0f4ff",
            fg="#999"
        )
        self.original_image_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Result preview
        result_frame = tk.Frame(preview_container, bg="#e8f5e9", relief=tk.RIDGE, bd=2)
        result_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.result_title_label = tk.Label(
            result_frame,
            text="Encrypted / Decrypted Result",
            font=("Arial", 10, "bold"),
            bg="#e8f5e9"
        )
        self.result_title_label.pack(pady=5)
        
        self.result_image_label = tk.Label(
            result_frame,
            text="No result yet",
            bg="#e8f5e9",
            fg="#999"
        )
        self.result_image_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
    def create_gallery_ui(self):
        """Create the gallery interface"""
        # Header
        header_frame = tk.Frame(self.gallery_tab, bg="white", pady=15)
        header_frame.pack(fill=tk.X, padx=20)
        
        tk.Label(
            header_frame,
            text="📂 Encrypted Files Gallery",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(side=tk.LEFT)
        
        tk.Button(
            header_frame,
            text="🔄 Refresh",
            command=self.refresh_gallery,
            font=("Arial", 10, "bold"),
            bg="#43e97b",
            fg="white",
            padx=15,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.RIGHT)
        
        # Search bar
        search_frame = tk.Frame(self.gallery_tab, bg="white", pady=10)
        search_frame.pack(fill=tk.X, padx=20)
        
        tk.Label(
            search_frame,
            text="🔍 Search:",
            font=("Arial", 10),
            bg="white"
        ).pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 10),
            width=40
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            search_frame,
            text="Search",
            command=self.search_gallery,
            font=("Arial", 10),
            bg="#667eea",
            fg="white",
            padx=15,
            pady=2,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Gallery list with scrollbar
        list_frame = tk.Frame(self.gallery_tab, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for gallery items
        columns = ("Filename", "Format", "Size", "Encrypted Date", "Tags")
        self.gallery_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Configure columns
        self.gallery_tree.heading("Filename", text="Filename")
        self.gallery_tree.heading("Format", text="Format")
        self.gallery_tree.heading("Size", text="Size")
        self.gallery_tree.heading("Encrypted Date", text="Encrypted Date")
        self.gallery_tree.heading("Tags", text="Tags")
        
        self.gallery_tree.column("Filename", width=250)
        self.gallery_tree.column("Format", width=80)
        self.gallery_tree.column("Size", width=100)
        self.gallery_tree.column("Encrypted Date", width=180)
        self.gallery_tree.column("Tags", width=200)
        
        self.gallery_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.gallery_tree.yview)
        
        # Double-click to select
        self.gallery_tree.bind("<Double-1>", self.on_gallery_item_double_click)
        
        # Action buttons
        button_frame = tk.Frame(self.gallery_tab, bg="white", pady=15)
        button_frame.pack(fill=tk.X, padx=20)
        
        tk.Button(
            button_frame,
            text="🔓 Decrypt Selected",
            command=self.decrypt_from_gallery,
            font=("Arial", 11, "bold"),
            bg="#667eea",
            fg="white",
            padx=25,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="🗑️ Delete Selected",
            command=self.delete_from_gallery,
            font=("Arial", 11, "bold"),
            bg="#ff4444",
            fg="white",
            padx=25,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Load sample data
        self.load_gallery_data()
        
    def create_status_bar(self):
        """Create the bottom status bar"""
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 9),
            bg="#e0e0e0",
            fg="#333",
            anchor=tk.W,
            padx=10,
            pady=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    # ==================== EVENT HANDLERS ====================
    
    def on_operation_change(self):
        """Handle operation radio button change"""
        if self.operation_var.get() == "encrypt":
            self.execute_button.config(text="🔒 ENCRYPT IMAGE", bg="#667eea")
            self.result_title_label.config(text="Encrypted Result (Noise)")
            self.save_options_frame.pack(fill=tk.X, padx=30)
        else:
            self.execute_button.config(text="🔓 DECRYPT IMAGE", bg="#43e97b")
            self.result_title_label.config(text="Decrypted Result")
            self.save_options_frame.pack_forget()
        
        self.update_status("Operation changed to: " + self.operation_var.get().upper())
    
    def browse_file(self):
        """Open file dialog to select image or encrypted file"""
        if self.operation_var.get() == "encrypt":
            filetypes = [("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")]
            title = "Select Image to Encrypt"
        else:
            filetypes = [("Encrypted files", "*.enc"), ("All files", "*.*")]
            title = "Select Encrypted File to Decrypt"
        
        filename = filedialog.askopenfilename(
            title=title,
            filetypes=filetypes
        )
        
        if filename:
            self.selected_file_path = filename
            self.file_path_var.set(filename)
            self.update_status(f"Selected: {os.path.basename(filename)}")
            
            # Show preview if it's an image
            if self.operation_var.get() == "encrypt":
                self.show_image_preview(filename)
    
    def select_from_gallery(self):
        """Switch to gallery tab to select file"""
        self.notebook.select(1)  # Switch to gallery tab
        self.update_status("Select a file from the gallery")
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="●")
    
    def execute_operation(self):
        """Execute encryption or decryption"""
        # Validation
        if not self.selected_file_path:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        password = self.password_var.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password!")
            return
        
        if len(password) < 8:
            messagebox.showwarning("Warning", "Password should be at least 8 characters for better security!")
        
        # Check lockout status
        if self.is_locked_out:
            messagebox.showerror("Locked Out", f"Too many failed attempts. Try again in {self.lockout_time_remaining} seconds.")
            return
        
        # Execute operation
        operation = self.operation_var.get()
        
        if operation == "encrypt":
            self.perform_encryption()
        else:
            self.perform_decryption()
    
    def perform_encryption(self):
        """Perform encryption (placeholder - connects to backend)"""
        self.update_status("Encrypting image...")
        
        # PLACEHOLDER: This is where you'd call your encryption backend
        # For now, simulate success
        
        # Simulate encrypted noise preview
        self.show_encrypted_noise_preview()
        
        # Show success message
        save_location = self.save_location_var.get()
        if save_location == "database":
            message = "Encryption successful!\n\nEncrypted file saved to database.\nView it in the Gallery tab."
        else:
            message = "Encryption successful!\n\nEncrypted file saved as:\n" + self.selected_file_path.replace(".jpg", "_encrypted.enc").replace(".png", "_encrypted.enc")
        
        messagebox.showinfo("Success", message)
        self.update_status("Encryption completed successfully")
        
        # Add to gallery if database option selected
        if save_location == "database":
            self.add_to_gallery_sample()
    
    def perform_decryption(self):
        """Perform decryption (placeholder - connects to backend)"""
        self.update_status("Attempting decryption...")
        
        # PLACEHOLDER: This is where you'd call your decryption backend
        # Simulate success or failure based on random
        
        import random
        success = random.choice([True, False])  # Simulate 50% success rate for demo
        
        if success:
            # Reset failed attempts on success
            self.failed_attempts = 0
            self.attempts_label.config(text="")
            
            # Show decrypted image
            self.show_decrypted_preview()
            
            messagebox.showinfo("Success", "Decryption successful!\n\nOriginal image restored.")
            self.update_status("Decryption completed successfully")
        else:
            # Increment failed attempts
            self.failed_attempts += 1
            remaining = 3 - self.failed_attempts
            
            if self.failed_attempts >= 3:
                # Trigger lockout
                self.trigger_lockout()
            else:
                self.attempts_label.config(text=f"⚠️ Attempts remaining: {remaining}")
                messagebox.showerror("Error", f"Invalid password!\n\nAttempts remaining: {remaining}")
                self.update_status(f"Decryption failed - {remaining} attempts remaining")
    
    def trigger_lockout(self):
        """Trigger 30-second lockout"""
        self.is_locked_out = True
        self.lockout_time_remaining = 30
        self.password_entry.config(state="disabled")
        self.execute_button.config(state="disabled")
        
        self.update_lockout_timer()
        
        messagebox.showerror(
            "Locked Out",
            "Too many failed attempts!\n\nYou are locked out for 30 seconds."
        )
    
    def update_lockout_timer(self):
        """Update lockout countdown timer"""
        if self.lockout_time_remaining > 0:
            self.lockout_label.config(
                text=f"🔒 LOCKED OUT - Try again in {self.lockout_time_remaining} seconds"
            )
            self.lockout_time_remaining -= 1
            self.root.after(1000, self.update_lockout_timer)
        else:
            # Lockout expired
            self.is_locked_out = False
            self.lockout_label.config(text="")
            self.attempts_label.config(text="⚠️ Attempts remaining: 1 (Next wrong attempt = immediate lockout)")
            self.password_entry.config(state="normal")
            self.execute_button.config(state="normal")
            self.update_status("Lockout expired - 1 attempt remaining")
    
    def reset_form(self):
        """Reset the form"""
        self.selected_file_path = None
        self.file_path_var.set("No file selected")
        self.password_var.set("")
        self.original_image_label.config(image="", text="No image loaded")
        self.result_image_label.config(image="", text="No result yet")
        self.update_status("Form reset")
    
    def show_image_preview(self, image_path):
        """Display image preview"""
        try:
            img = Image.open(image_path)
            img.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(img)
            self.original_image_label.config(image=photo, text="")
            self.original_image_label.image = photo  # Keep reference
        except Exception as e:
            self.original_image_label.config(text=f"Error loading image:\n{str(e)}")
    
    def show_encrypted_noise_preview(self):
        """Show encrypted noise visualization"""
        # Create a noise image to simulate encrypted data
        import numpy as np
        
        noise = np.random.randint(0, 256, (300, 300, 3), dtype=np.uint8)
        noise_img = Image.fromarray(noise, 'RGB')
        photo = ImageTk.PhotoImage(noise_img)
        
        self.result_image_label.config(image=photo, text="")
        self.result_image_label.image = photo
    
    def show_decrypted_preview(self):
        """Show decrypted image preview (uses original for demo)"""
        if self.selected_file_path:
            # For demo, just show a placeholder
            self.result_image_label.config(text="✅ Decrypted image\n(Original restored)")
    
    # ==================== GALLERY FUNCTIONS ====================
    
    def load_gallery_data(self):
        """Load gallery data from database (placeholder)"""
        # PLACEHOLDER: This would query the SQLite database
        # For now, add sample data
        
        sample_data = [
            ("vacation_photo.jpg", "JPG", "2.3 MB", "2026-04-10 15:30", "vacation, beach"),
            ("document_scan.png", "PNG", "1.1 MB", "2026-04-09 10:20", "work, important"),
            ("family_portrait.jpg", "JPG", "3.8 MB", "2026-04-08 20:00", "family, memories"),
        ]
        
        for item in sample_data:
            self.gallery_tree.insert("", tk.END, values=item)
    
    def refresh_gallery(self):
        """Refresh gallery data"""
        # Clear existing items
        for item in self.gallery_tree.get_children():
            self.gallery_tree.delete(item)
        
        # Reload data
        self.load_gallery_data()
        self.update_status("Gallery refreshed")
    
    def search_gallery(self):
        """Search gallery based on search term"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.refresh_gallery()
            return
        
        # Clear and filter
        for item in self.gallery_tree.get_children():
            self.gallery_tree.delete(item)
        
        # Re-add matching items (placeholder logic)
        self.load_gallery_data()  # In real app, would filter database query
        self.update_status(f"Searching for: {search_term}")
    
    def on_gallery_item_double_click(self, event):
        """Handle double-click on gallery item"""
        selection = self.gallery_tree.selection()
        if selection:
            item = self.gallery_tree.item(selection[0])
            filename = item['values'][0]
            
            # Switch to decrypt tab and populate
            self.notebook.select(0)
            self.operation_var.set("decrypt")
            self.on_operation_change()
            self.file_path_var.set(f"[From Gallery] {filename}")
            self.update_status(f"Selected from gallery: {filename}")
    
    def decrypt_from_gallery(self):
        """Decrypt selected item from gallery"""
        selection = self.gallery_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a file from the gallery first!")
            return
        
        item = self.gallery_tree.item(selection[0])
        filename = item['values'][0]
        
        # Switch to decrypt tab
        self.notebook.select(0)
        self.operation_var.set("decrypt")
        self.on_operation_change()
        self.file_path_var.set(f"[From Gallery] {filename}")
        self.update_status(f"Ready to decrypt: {filename}")
    
    def delete_from_gallery(self):
        """Delete selected item from gallery"""
        selection = self.gallery_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a file to delete!")
            return
        
        item = self.gallery_tree.item(selection[0])
        filename = item['values'][0]
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{filename}' from the database?\n\nThis action cannot be undone!"
        )
        
        if confirm:
            # PLACEHOLDER: Delete from database
            self.gallery_tree.delete(selection[0])
            self.update_status(f"Deleted: {filename}")
            messagebox.showinfo("Deleted", f"'{filename}' has been removed from the gallery.")
    
    def add_to_gallery_sample(self):
        """Add newly encrypted file to gallery (sample)"""
        if self.selected_file_path:
            filename = os.path.basename(self.selected_file_path)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # Get file size (placeholder)
            file_size = "2.5 MB"
            file_format = filename.split('.')[-1].upper()
            
            # Insert into gallery
            self.gallery_tree.insert(
                "",
                0,  # Insert at top
                values=(filename, file_format, file_size, current_time, "new")
            )
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.config(text=f"Status: {message}")


# ==================== MAIN ====================

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptionApp(root)
    root.mainloop()