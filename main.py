import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import itertools
import threading
import time
import os


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ARSEC Dictionary Based Password Generation")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        header = ttk.Label(self.main_frame, text="ARSEC DBPG", style='Header.TLabel')
        header.pack(pady=(0, 20))

        keywords_frame = ttk.Frame(self.main_frame)
        keywords_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(keywords_frame, text="Anahtar Kelimeler (virgülle ayırın):").pack(anchor=tk.W)
        self.keywords_entry = tk.Text(keywords_frame, height=5, width=50, font=('Arial', 10))
        self.keywords_entry.pack(fill=tk.X)

        options_frame = ttk.Frame(self.main_frame)
        options_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(options_frame, text="Şifre Üretme Seçenekleri:").pack(anchor=tk.W)

        self.leet_var = tk.IntVar(value=1)
        leet_check = ttk.Checkbutton(
            options_frame,
            text="Leet Speak Dönüşümü (ör: a->@, e->3)",
            variable=self.leet_var
        )
        leet_check.pack(anchor=tk.W)

        self.numbers_var = tk.IntVar(value=1)
        numbers_check = ttk.Checkbutton(
            options_frame,
            text="Sayı Ekle (0-99, 123, 2023 vb.)",
            variable=self.numbers_var
        )
        numbers_check.pack(anchor=tk.W)

        self.special_var = tk.IntVar(value=1)
        special_check = ttk.Checkbutton(
            options_frame,
            text="Özel Karakter Ekle (!@#$%^&*)",
            variable=self.special_var
        )
        special_check.pack(anchor=tk.W)

        self.case_var = tk.IntVar(value=1)
        case_check = ttk.Checkbutton(
            options_frame,
            text="Büyük/Küçük Harf Kombinasyonları",
            variable=self.case_var
        )
        case_check.pack(anchor=tk.W)

        self.combine_var = tk.IntVar(value=0)
        combine_check = ttk.Checkbutton(
            options_frame,
            text="Kelimeleri Birlikte Kullan (kombinasyonlar oluştur)",
            variable=self.combine_var
        )
        combine_check.pack(anchor=tk.W)

        output_frame = ttk.Frame(self.main_frame)
        output_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(output_frame, text="Çıktı Dosyası:").pack(anchor=tk.W)

        self.output_path = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.output_path, width=50)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        browse_btn = ttk.Button(output_frame, text="Gözat", command=self.browse_file)
        browse_btn.pack(side=tk.RIGHT, padx=(5, 0))

        self.progress = ttk.Progressbar(self.main_frame, orient=tk.HORIZONTAL, mode='determinate')

        self.status_var = tk.StringVar()
        self.status_var.set("Hazır")
        status_label = ttk.Label(self.main_frame, textvariable=self.status_var)

        start_btn = ttk.Button(
            self.main_frame,
            text="Şifreleri Üret",
            command=self.start_generation
        )
        start_btn.pack(pady=(10, 0))

        status_label.pack(pady=(5, 0))
        self.progress.pack(fill=tk.X, pady=(5, 0))

    def browse_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Çıktı dosyasını seçin"
        )
        if filename:
            self.output_path.set(filename)

    def start_generation(self):
        keywords_text = self.keywords_entry.get("1.0", tk.END).strip()
        if not keywords_text:
            messagebox.showerror("Hata", "Lütfen en az bir anahtar kelime girin.")
            return

        output_path = self.output_path.get()
        if not output_path:
            messagebox.showerror("Hata", "Lütfen bir çıktı dosyası seçin.")
            return

        keywords = [k.strip() for k in keywords_text.split(",") if k.strip()]

        thread = threading.Thread(
            target=self.generate_passwords,
            args=(keywords, output_path),
            daemon=True
        )
        thread.start()

    def generate_passwords(self, keywords, output_path):
        self.status_var.set("Şifreler üretiliyor...")
        self.progress["value"] = 0
        self.root.update()

        try:
            passwords = set()

            for keyword in keywords:
                self.process_keyword(keyword, passwords)

            if self.combine_var.get() and len(keywords) > 1:
                self.process_combinations(keywords, passwords)

            self.progress["maximum"] = len(passwords)

            with open(output_path, 'w', encoding='utf-8') as f:
                for i, pwd in enumerate(passwords, 1):
                    f.write(pwd + '\n')
                    if i % 100 == 0:
                        self.progress["value"] = i
                        self.status_var.set(f"Şifreler yazılıyor: {i}/{len(passwords)}")
                        self.root.update()

            self.progress["value"] = len(passwords)
            self.status_var.set(f"Tamamlandı! {len(passwords)} şifre üretildi.")
            messagebox.showinfo("Başarılı", f"{len(passwords)} şifre başarıyla üretildi ve kaydedildi.")

        except Exception as e:
            self.status_var.set("Hata oluştu")
            messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")
        finally:
            self.progress["value"] = 0

    def process_keyword(self, keyword, passwords):
        passwords.add(keyword)

        if self.leet_var.get():
            leet_map = {
                'a': ['@', '4'],
                'e': ['3'],
                'i': ['1', '!'],
                'o': ['0'],
                's': ['5', '$'],
                't': ['7']
            }

            for i in range(1, min(3, len(keyword)) + 1):  # 1-2 karakter dönüşümü
                for letters in itertools.combinations(range(len(keyword)), i):
                    temp_pwd = list(keyword)
                    for pos in letters:
                        char = temp_pwd[pos].lower()
                        if char in leet_map:
                            temp_pwd[pos] = leet_map[char][0]
                    passwords.add(''.join(temp_pwd))

        if self.case_var.get():
            passwords.add(keyword.capitalize())
            passwords.add(keyword.upper())
            passwords.add(keyword.lower())

        if self.numbers_var.get():
            for num in ['', '1', '12', '123', '0', '00', '000', '01', '007', '69', '21', '2020', '2021', '2022',
                        '2023']:
                passwords.add(keyword + num)
                if self.case_var.get():
                    passwords.add(keyword.capitalize() + num)
                    passwords.add(keyword.upper() + num)

        if self.special_var.get():
            for char in ['', '!', '@', '#', '$', '%', '^', '&', '*', '?']:
                passwords.add(keyword + char)
                if self.case_var.get():
                    passwords.add(keyword.capitalize() + char)
                    passwords.add(keyword.upper() + char)

            for char in ['!', '@', '#', '$']:
                passwords.add(char + keyword + char)
                if self.case_var.get():
                    passwords.add(char + keyword.capitalize() + char)
                    passwords.add(char + keyword.upper() + char)

    def process_combinations(self, keywords, passwords):
        for r in range(2, min(4, len(keywords) + 1)):
            for combo in itertools.permutations(keywords, r):
                combined = ''.join(combo)
                passwords.add(combined)


                if self.case_var.get():
                    passwords.add(combined.capitalize())
                    passwords.add(combined.upper())


                if self.numbers_var.get():
                    for num in ['', '1', '12', '123', '0', '00', '000', '01', '007', '69', '21']:
                        passwords.add(combined + num)

                if self.special_var.get():
                    for char in ['', '!', '@', '#', '$', '%', '^', '&', '*', '?']:
                        passwords.add(combined + char)

                    for char in ['!', '@', '#', '$']:
                        passwords.add(char + combined + char)


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()