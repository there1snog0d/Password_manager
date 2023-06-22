import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from cryptography.fernet import Fernet
import random

class Password_encryptor:

    def __init__(self):
        self.key = None
        self.key_file = None

    def create_key(self, path):
        self.key = Fernet.generate_key()
        self.key_file = path
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        self.key_file = path
        with open(path, 'rb') as f:
            self.key = f.read()

    def encrypt_func(self, password):
        encrypted_data = Fernet(self.key).encrypt(password.encode())
        return encrypted_data.decode()

    def decrypt_func(self, encrypted_password):
        decrypted_data = Fernet(self.key).decrypt(encrypted_password.encode())
        return decrypted_data.decode()

def delete_from_file(fname, dline):
    f = open(fname)
    temp = []
    for line in f:
        if line.split()[0] != dline[0] and line.split()[1] != dline[1]:
            temp.append(line)
    f.close()
    f = open(fname, 'w')
    f.writelines(temp)
    f.close()

class New_tab():

    def __init__(self, nb, c1, c2, c3, fname):
        self.new_key = Password_encryptor()

        try:
            self.new_key.load_key('Temp/crypto.key')
        except FileNotFoundError:
            self.new_key.create_key('Temp/crypto.key')

        self.tab = ttk.Frame(nb)
        self.initialize_user_interface(c1, c2, c3, fname)
        self.insert_data(fname)

        try:
            f = open('Temp/pincode.txt', 'r')
            f.close()
        except:
            self.create_pincode()

    def initialize_user_interface(self, c1, c2, c3, fname):
        self.f_top = ttk.Frame(self.tab)
        self.f_bot = ttk.Frame(self.tab)
        self.f_top.pack(fill=tk.BOTH)
        self.f_bot.pack(expand=True, fill=tk.BOTH)

        self.buttonAdd = tk.Button(self.f_top, text="Добавить", command=lambda: self.add_func(fname))
        self.buttonDelete = tk.Button(self.f_top, text="Удалить", command= lambda: self.delete_func(fname))
        self.buttonAdd.pack(side=tk.LEFT, padx=5, pady=5)
        self.buttonDelete.pack(side=tk.LEFT)


        self.new_list = ttk.Treeview(self.f_bot, show="headings")
        self.new_list['columns'] = (c1, c2, c3)
        self.new_list.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        for col in self.new_list['columns']:
            self.new_list.column(col, anchor='center')
            self.new_list.heading(col, text=col.capitalize())

        self.list = self.new_list
        self.list.bind("<Double-1>", lambda x: self.OnDoubleClick(fname))

    def commit_pincode(self,pin):
        f = open('Temp/pincode.txt', "w+")
        f.write(self.new_key.encrypt_func(pin))
        f.close()

    def create_pincode(self):
        create_window = tk.Tk()
        create_window.title("Придумайте пин-код")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        create_frame = tk.Frame(create_window)
        create_frame .pack(expand=True)

        pincode_entry = tk.Entry(create_frame)
        pincode_entry.grid(row=0, column=1)

        button1 = tk.Button(create_frame, text="Готово",
                            command=lambda: [self.commit_pincode(pincode_entry.get()), create_window.destroy() ])
        button1.grid(row=1, column=1)

        window_width = 250
        window_height = 250
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        create_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        create_window.resizable(width=False, height=False)

    def OnDoubleClick(self, fname):

        check_window = tk.Tk()
        check_window.title("Введите пин-код")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        check_frame = tk.Frame(check_window)
        check_frame.pack(expand=True)

        pincode_entry = tk.Entry(check_frame)
        pincode_entry.grid(row=0, column=1)

        button1 = tk.Button(check_frame, text="Готово",
                                         command=lambda: [self.check_func(pincode_entry, fname), check_window.destroy()])
        button1.grid(row=1, column=1)


        window_width = 250
        window_height = 250
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        check_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        check_window.resizable(width=False, height=False)

    def check_func(self, entry, fname):
        pincode = ''
        with open('Temp/pincode.txt', 'r') as f: pincode = f.read()
        pincode = self.new_key.decrypt_func(pincode)

        if pincode == entry.get():
            self.show_info(fname)
        return 1



    def insert_data(self, fname):
        self.list.delete(*self.list.get_children())
        with open(fname, newline="") as f:
            for contact in f:
                contact = contact.split()[0] + ' ' + contact.split()[1] + ' ' + '*' * len(self.new_key.decrypt_func(contact.split()[2]))
                self.list.insert("", tk.END, values = contact)

    def add_func(self, fname):
        add_window = tk.Tk()
        add_window.title("Добавить")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        add_frame = tk.Frame(add_window)
        add_frame.pack(expand=True)

        label1 = tk.Label(add_frame, text="Название:")
        label1.grid(row=0, column=0)

        site_entry = tk.Entry(add_frame)
        site_entry.grid(row=0, column=1)

        label2 = tk.Label(add_frame, text="Логин:")
        label2.grid(row=1, column=0)

        login_entry = tk.Entry(add_frame)
        login_entry.grid(row=1, column=1)

        label3 = tk.Label(add_frame, text="Пароль:")
        label3.grid(row=2, column=0)

        password_entry = tk.Entry(add_frame)
        password_entry.grid(row=2, column=1)

        button1 = tk.Button(add_frame, text="Готово",
                            command=lambda: [self.commit_func(site_entry, login_entry, password_entry, fname),
                                             self.insert_data(fname),
                                             add_window.destroy()])
        button1.grid(row=3, column=1)
        button2 = tk.Button(add_frame, text="Сгенерировать пароль",
                            command=lambda: [self.generate_func(password_entry)])
        button2.grid(row=4, column=1)

        window_width = 250
        window_height = 250
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        add_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        add_window.resizable(width=False, height=False)

    def generate_func(self, entery):
        chars = '_-*!&$#?=<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        password = ''
        for i in range(10):
            password += random.choice(chars)
        entery.delete(0, tk.END)
        entery.insert(0, password)

    def commit_func(self, entery1, entery2, entery3, fname):
        info1 = entery1.get()
        info2 = entery2.get()
        info3 = entery3.get()
        with open(fname, 'r') as original: temp = original.read()
        with open(fname, 'w+') as modified: modified.write(info1 + " " + info2 + " " + self.new_key.encrypt_func(info3) + '\n' + temp)

    def delete_func(self, fname):
        res = tk.messagebox.askyesno(title="Подтвержение удаления", message="Вы точно хотите удалить пароль?")
        if res:
            selection = self.list.selection()[0]
            print(self.list.item(selection)['values'])
            delete_from_file(fname, self.list.item(selection)['values'])
            self.list.delete(selection)

    def show_info(self, fname):
        selection = self.list.selection()[0]
        f = open(fname)
        #print(self.list.item(selection)['values'])
        selected_line = self.list.item(selection)['values']
        temp = ''
        for line in f:
            if line.split()[0] == selected_line[0] and str(line.split()[1]) == str(selected_line[1]):
                temp = line
        f.close()

        print(temp)

        show_window = tk.Tk()
        show_window.title(selected_line[0])

        show_frame = tk.Frame(show_window)
        show_frame.pack(expand=True)

        label2 = tk.Label(show_frame, text="Логин:")
        label2.grid(row=0, column=0)

        login_entry = tk.Entry(show_frame)
        login_entry.insert(0, temp.split()[1])
        login_entry.grid(row=0, column=1)
        login_entry['state'] = 'disabled'

        button_copy1 = tk.Button(show_frame,
                                 text='Копировать',
                                 command = lambda: [show_window.clipboard_clear(),
                                                                             show_window.clipboard_append(login_entry.get().rstrip()),
                                                                             label4.config(text="Логин скопирован!")])
        button_copy1.grid(row=0,column=2)


        label3 = tk.Label(show_frame, text="Пароль:")
        label3.grid(row=1, column=0)

        password_entry = tk.Entry(show_frame)
        password_entry.insert(0, self.new_key.decrypt_func(temp.split()[2]))
        password_entry.grid(row=1, column=1)
        password_entry['state'] = 'disabled'

        button_copy2 = tk.Button(show_frame,
                                 text='Копировать',
                                 command=lambda: [show_window.clipboard_clear(),
                                                  show_window.clipboard_append(password_entry.get().rstrip()),
                                                  label4.config(text="Пароль скопирован!")])
        button_copy2.grid(row=1, column=2)

        label4 = tk.Label(show_frame)
        label4.grid(row=2, column=1)

        window_width = 260
        window_height = 260

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        show_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        show_window.resizable(width=False, height=False)

root = tk.Tk()
root.resizable(width=False, height=False)

root.title("Менеджер паролей")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 1024
window_height = 720
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

websites_tab = New_tab(notebook, 'Сайт', 'Логин', 'Пароль', "Temp/websites_accounts.txt")
apps_tab = New_tab(notebook, 'Приложение', 'Логин', 'Пароль', "Temp/apps_accounts.txt")

notebook.add(websites_tab.tab, text="Web-сайты")
notebook.add(apps_tab.tab, text="Приложения")

root.mainloop()
