import tkinter as tk
from tkinter import simpledialog, messagebox
import pyodbc

class LoginDialog(simpledialog.Dialog):
    def __init__(self, parent, conn, main_window):
        self.conn = conn
        self.main_window = main_window
        super().__init__(parent, "Inicio de Sesión")

    def body(self, master):
        tk.Label(master, text="Nombre de usuario:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(master, text="Contraseña:").grid(row=1, column=0, sticky=tk.W)

        self.username_entry = tk.Entry(master)
        self.password_entry = tk.Entry(master, show='*')

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

    def buttonbox(self):
        box = tk.Frame(self)

        self.login_button = tk.Button(box, text="Iniciar Sesión", width=15, command=self.login)
        self.register_button = tk.Button(box, text="Registrarse", width=15, command=self.register)
        self.cancel_button = tk.Button(box, text="Cancelar", width=15, command=self.cancel)

        self.login_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.register_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

        box.pack()

    def cancel(self):
        self.destroy()  # Cerrar la ventana de inicio de sesión
        self.main_window.destroy()  # Cerrar la ventana del menú principal

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Realizar la validación en la base de datos
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        cursor.close()

        if result:
            self.result = (username, password)
            self.destroy()  # Cerrar la ventana de inicio de sesión (solo esta ventana)
        else:
            messagebox.showerror("Inicio de Sesión", "Nombre de usuario o contraseña incorrectos.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Verificar si el nombre de usuario ya existe en la base de datos
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result:
            messagebox.showerror("Registro", "El nombre de usuario ya está en uso. Por favor, elija otro.")
            cursor.close()
        else:
            # Insertar el nuevo usuario en la base de datos
            cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            cursor.close()
            messagebox.showinfo("Registro", "Registro exitoso. Ahora puede iniciar sesión.")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)


