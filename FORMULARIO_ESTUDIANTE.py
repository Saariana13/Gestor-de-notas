import tkinter as tk
from tkinter import simpledialog, messagebox
import pyodbc
from tkinter import ttk
from ESTUDIANTE import *



class RegistroDatosDialog(tk.Toplevel):
    def __init__(self, parent, conn):
        super().__init__(parent)
        self.parent = parent
        self.conn = conn
        self.title("Ingresar Registro")
        self.configure(bg="#E8DAEF")
        self.cedula_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.celular_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.modalidad_var = tk.StringVar()

        self.ventana_ingresar_datos()

    def ventana_ingresar_datos(self):
        tk.Label(self, text="Cédula:", bg="#E8DAEF").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self, text="Nombre:", bg="#E8DAEF").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(self, text="Apellido:", bg="#E8DAEF").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(self, text="Celular:", bg="#E8DAEF").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(self, text="Email:", bg="#E8DAEF").grid(row=4, column=0, padx=5, pady=5)
        tk.Label(self, text="Modalidad:", bg="#E8DAEF").grid(row=5, column=0, padx=5, pady=5)

        self.cedula_entry = tk.Entry(self, textvariable=self.cedula_var)
        self.cedula_entry.grid(row=0, column=1, padx=5, pady=5)

        self.nombre_entry = tk.Entry(self, textvariable=self.nombre_var)
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5)

        self.apellido_entry = tk.Entry(self, textvariable=self.apellido_var)
        self.apellido_entry.grid(row=2, column=1, padx=5, pady=5)

        self.celular_entry = tk.Entry(self, textvariable=self.celular_var)
        self.celular_entry.grid(row=3, column=1, padx=5, pady=5)

        self.email_entry = tk.Entry(self, textvariable=self.email_var)
        self.email_entry.grid(row=4, column=1, padx=5, pady=5)

        self.modalidad_combobox = ttk.Combobox(self, values=["Presencial", "Virtual"], textvariable=self.modalidad_var)
        self.modalidad_combobox.grid(row=5, column=1, padx=5, pady=5)

        tk.Button(self, text="Guardar", bg="#A569BD", command=self.guardar_registro).grid(row=6, column=0, columnspan=2, padx=5, pady=10)

    def guardar_registro(self):
        cedula = self.cedula_var.get()
        nombre = self.nombre_var.get()
        apellido = self.apellido_var.get()
        celular = self.celular_var.get()
        email = self.email_var.get()
        modalidad = self.modalidad_var.get()

        if not cedula:
            tk.messagebox.showerror("Error", "La cédula no puede estar vacía.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO tabla_registros (cedula, nombre, apellido, celular, email, modalidad) VALUES (?, ?, ?, ?, ?, ?)",
                           (cedula, nombre, apellido, celular, email, modalidad))
            self.conn.commit()
            cursor.close()
            tk.messagebox.showinfo("Éxito", "Registro guardado exitosamente.")
            self.destroy()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Ha ocurrido un error al guardar el registro: {str(e)}")



class IngresarNotasDialog(tk.Toplevel):
    def __init__(self, parent, conn):
        super().__init__(parent)
        self.parent = parent
        self.conn = conn
        self.title("Ingresar Notas del Estudiante")
        self.configure(bg="#E8F8F5")

        self.cedula_var = tk.StringVar()
        self.pronunciacion_var = tk.StringVar()
        self.escritura_var = tk.StringVar()
        self.practica_var = tk.StringVar()
        self.teoria_var = tk.StringVar()

        self.ventana_ingresar_notas()

    def ventana_ingresar_notas(self):
        tk.Label(self, text="Cédula Estudiante:", bg="#E8F8F5").grid(row=0, column=0, padx=5, pady=5)
        self.cedula_entry = tk.Entry(self, textvariable=self.cedula_var)
        self.cedula_entry.grid(row=0, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        self.configure(bg="#E8F8F5")

        tk.Button(btn_frame, text="Buscar Estudiante", bg="#A9DFBF", command=self.buscar_estudiante).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Guardar Notas", bg="#A9DFBF", command=self.guardar_notas).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancelar", bg="#A9DFBF", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def buscar_estudiante(self):
        cedula_estudiante = self.cedula_var.get()
        if not cedula_estudiante:
            messagebox.showerror("Error", "Ingrese la cédula del estudiante.")
            return

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tabla_registros WHERE cedula = ?", cedula_estudiante)
        estudiante = cursor.fetchone()

        if estudiante is None:
            messagebox.showerror("Error", "El número de cédula no existe en la base de datos.")
        else:
            tk.Label(self, text=f"Ingrese las notas para el estudiante: {estudiante[1]} {estudiante[2]}", bg="#A2D9CE").grid(row=2, column=0, columnspan=2, pady=5)
            self.configure(bg="#E8F8F5")

            notas_frame = tk.Frame(self)
            notas_frame.grid(row=3, column=0, columnspan=2)

            tk.Label(notas_frame, text="Pronunciación:").grid(row=0, column=0, padx=10, pady=5)
            tk.Label(notas_frame, text="Escritura:").grid(row=1, column=0, padx=10, pady=5)
            tk.Label(notas_frame, text="Práctica:").grid(row=2, column=0, padx=10, pady=5)
            tk.Label(notas_frame, text="Teoría:").grid(row=3, column=0, padx=10, pady=5)

            tk.Entry(notas_frame, textvariable=self.pronunciacion_var).grid(row=0, column=1, padx=10, pady=5)
            tk.Entry(notas_frame, textvariable=self.escritura_var).grid(row=1, column=1, padx=10, pady=5)
            tk.Entry(notas_frame, textvariable=self.practica_var).grid(row=2, column=1, padx=10, pady=5)
            tk.Entry(notas_frame, textvariable=self.teoria_var).grid(row=3, column=1, padx=10, pady=5)

    def guardar_notas(self):
        cedula_estudiante = self.cedula_var.get()
        try:
            pronunciacion = float(self.pronunciacion_var.get())
            escritura = float(self.escritura_var.get())
            practica = float(self.practica_var.get())
            teoria = float(self.teoria_var.get())
        except ValueError:
            messagebox.showwarning("Error", "Las notas deben ser valores numéricos.")
            return


        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO tabla_notas (cedula_estudiante, pronunciacion, escritura, practica, teoria) VALUES (?, ?, ?, ?, ?)",
                       cedula_estudiante, pronunciacion, escritura, practica, teoria)
        self.conn.commit()

        # Calculate the average
        self.calcular_promedio(cedula_estudiante)

        # Display the success message with the average
        messagebox.showinfo("Éxito", f"Notas del estudiante guardadas correctamente.\nPromedio de notas del estudiante : {self.promedio:.2f}")
        self.destroy()

    def calcular_promedio(self, cedula_estudiante):
        cursor = self.conn.cursor()
        cursor.execute("SELECT pronunciacion, escritura, practica, teoria FROM tabla_notas WHERE cedula_estudiante = ?", cedula_estudiante)
        notas = cursor.fetchone()
        cursor.close()

        notas_validas = [nota for nota in notas if nota is not None]

        if notas_validas:
            self.promedio = sum(notas_validas) / len(notas_validas)
        else:
            self.promedio = 0
            
            
class EliminarEstudianteDialog(tk.Toplevel):
    def __init__(self, parent, conn):
        super().__init__(parent)
        self.parent = parent
        self.conn = conn
        self.title("Eliminar Estudiante")
        self.cedula_var = tk.StringVar()        
        self.create_eliminar_interface()

    def create_eliminar_interface(self):
        # Configurar colores
        pastel_colors = ["#B0E57C", "#C3B1E1", "#F9CB9C", "#A6DCEF", "#F4C2C2", "#B2D8B2", "#FFD700", "#D5A6BD"]
        background_color = pastel_colors[1]
        label_color = pastel_colors[0]
        entry_color = pastel_colors[2]
        button_color = pastel_colors[4]

        self.configure(bg=background_color)

        tk.Label(self, text="Cédula del Estudiante:", bg=background_color, fg="black").pack(pady=10)
        self.cedula_entry = tk.Entry(self, textvariable=self.cedula_var, bg=entry_color)
        self.cedula_entry.pack(pady=5)
        tk.Button(self, text="Eliminar Estudiante", command=self.eliminar_estudiante, bg=button_color).pack(pady=10)

    def eliminar_estudiante(self):
        cedula_estudiante = self.cedula_var.get()

        try:
            cursor = self.conn.cursor()
            delete_notas_query = "DELETE FROM tabla_notas WHERE cedula_estudiante = ?"
            cursor.execute(delete_notas_query, cedula_estudiante)
            cursor.close()

            cursor = self.conn.cursor()
            delete_estudiante_query = "DELETE FROM tabla_registros WHERE cedula = ?"
            cursor.execute(delete_estudiante_query, cedula_estudiante)
            self.conn.commit()
            cursor.close()

            messagebox.showinfo("Éxito", "Estudiante y sus notas han sido eliminados correctamente.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error al eliminar el estudiante: {str(e)}")


            
import tkinter as tk
from tkinter import ttk, messagebox

class ModificarEstudianteDialog(tk.Toplevel):
    def __init__(self, parent, conn):
        super().__init__(parent)
        self.parent = parent
        self.conn = conn
        self.title("Modificar Estudiante")
        self.cedula_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.celular_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.modalidad_var = tk.StringVar()
        self.pronunciacion_var = tk.DoubleVar()
        self.escritura_var = tk.DoubleVar()
        self.practica_var = tk.DoubleVar()
        self.teoria_var = tk.DoubleVar()
        
        self.create_modificar_interface()
        
    def create_modificar_interface(self):
        # Configurar colores
        pastel_colors = ["#F2E8DF", "#E6E6FA", "#FFDAB9", "#D1E8E2", "#F5CBA7", "#B2D8B2", "#FFE4B5", "#D5A6BD"]
        background_color = pastel_colors[1]
        label_color = "black"
        entry_color = pastel_colors[3]
        button_color = pastel_colors[5]
        
        self.configure(bg=background_color)

        tk.Label(self, text="Cédula del Estudiante:", bg=background_color, fg=label_color).grid(row=0, column=0, padx=5, pady=5)
        self.cedula_entry = tk.Entry(self, textvariable=self.cedula_var, bg=entry_color)
        self.cedula_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self, text="Notas:", bg=background_color, fg=label_color).grid(row=6, column=0, padx=5, pady=5)
        
        tk.Label(self, text="Pronunciación:", bg=background_color, fg=label_color).grid(row=7, column=0, padx=5, pady=5)
        self.pronunciacion_entry = tk.Entry(self, textvariable=self.pronunciacion_var, bg=entry_color)
        self.pronunciacion_entry.grid(row=7, column=1, padx=5, pady=5)
        
        tk.Label(self, text="Escritura:", bg=background_color, fg=label_color).grid(row=8, column=0, padx=5, pady=5)
        self.escritura_entry = tk.Entry(self, textvariable=self.escritura_var, bg=entry_color)
        self.escritura_entry.grid(row=8, column=1, padx=5, pady=5)
        
        tk.Label(self, text="Práctica:", bg=background_color, fg=label_color).grid(row=9, column=0, padx=5, pady=5)
        self.practica_entry = tk.Entry(self, textvariable=self.practica_var, bg=entry_color)
        self.practica_entry.grid(row=9, column=1, padx=5, pady=5)
        
        tk.Label(self, text="Teoría:", bg=background_color, fg=label_color).grid(row=10, column=0, padx=5, pady=5)
        self.teoria_entry = tk.Entry(self, textvariable=self.teoria_var, bg=entry_color)
        self.teoria_entry.grid(row=10, column=1, padx=5, pady=5)
        
        tk.Button(self, text="Buscar Estudiante", command=self.buscar_estudiante, bg=button_color).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(self, text="Guardar Cambios", command=self.guardar_cambios, bg=button_color).grid(row=11, column=0, columnspan=2, padx=5, pady=10)
        
        tk.Label(self, text="Nombre:", bg=background_color, fg=label_color).grid(row=1, column=0, padx=5, pady=5)
        tk.Label(self, text="Apellido:", bg=background_color, fg=label_color).grid(row=2, column=0, padx=5, pady=5)
        tk.Label(self, text="Celular:", bg=background_color, fg=label_color).grid(row=3, column=0, padx=5, pady=5)
        tk.Label(self, text="Email:", bg=background_color, fg=label_color).grid(row=4, column=0, padx=5, pady=5)
        tk.Label(self, text="Modalidad:", bg=background_color, fg=label_color).grid(row=5, column=0, padx=5, pady=5)
        
        self.nombre_entry = tk.Entry(self, textvariable=self.nombre_var, bg=entry_color)
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5)
        self.apellido_entry = tk.Entry(self, textvariable=self.apellido_var, bg=entry_color)
        self.apellido_entry.grid(row=2, column=1, padx=5, pady=5)
        self.celular_entry = tk.Entry(self, textvariable=self.celular_var, bg=entry_color)
        self.celular_entry.grid(row=3, column=1, padx=5, pady=5)
        self.email_entry = tk.Entry(self, textvariable=self.email_var, bg=entry_color)
        self.email_entry.grid(row=4, column=1, padx=5, pady=5)
        self.modalidad_combobox = ttk.Combobox(self, values=["Presencial", "Virtual"], textvariable=self.modalidad_var, state="readonly")
        self.modalidad_combobox.grid(row=5, column=1, padx=5, pady=5)
    
    def buscar_estudiante(self):
        cedula_estudiante = self.cedula_var.get()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tabla_registros WHERE cedula = ?", cedula_estudiante)
        estudiante = cursor.fetchone()
        cursor.close()
        if estudiante is None:
            messagebox.showerror("Error", "El número de cédula no existe en la base de datos.")
        else:
            self.nombre_var.set(estudiante[1])
            self.apellido_var.set(estudiante[2])
            self.celular_var.set(estudiante[3])
            self.email_var.set(estudiante[4])
            self.modalidad_var.set(estudiante[5])
            
            cursor_notas = self.conn.cursor()
            cursor_notas.execute("SELECT * FROM tabla_notas WHERE cedula_estudiante = ?", cedula_estudiante)
            notas = cursor_notas.fetchone()
            cursor_notas.close()
            
            if notas is not None:
                self.pronunciacion_var.set(notas[2])
                self.escritura_var.set(notas[3])
                self.practica_var.set(notas[4])
                self.teoria_var.set(notas[5])
    
    def guardar_cambios(self):
        nombre = self.nombre_var.get()
        apellido = self.apellido_var.get()
        celular = self.celular_var.get()
        email = self.email_var.get()
        modalidad = self.modalidad_var.get()
        cedula_estudiante = self.cedula_var.get()
        
        pronunciacion = self.pronunciacion_var.get()
        escritura = self.escritura_var.get()
        practica = self.practica_var.get()
        teoria = self.teoria_var.get()
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE tabla_registros SET nombre=?, apellido=?, celular=?, email=?, modalidad=? WHERE cedula=?", 
                           (nombre, apellido, celular, email, modalidad, cedula_estudiante))
            
            cursor_notas = self.conn.cursor()
            cursor_notas.execute("UPDATE tabla_notas SET pronunciacion=?, escritura=?, practica=?, teoria=? WHERE cedula_estudiante=?", 
                                (pronunciacion, escritura, practica, teoria, cedula_estudiante))
            
            self.conn.commit()
            cursor.close()
            cursor_notas.close()
            
            messagebox.showinfo("Éxito", "Cambios guardados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error al guardar los cambios: {str(e)}")





class ConsultarEstudianteDialog(tk.Toplevel):
    def __init__(self, parent, conn):
        super().__init__(parent)
        self.parent = parent
        self.conn = conn
        self.title("Consultar Estudiante")
        self.cedula_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.celular_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.modalidad_var = tk.StringVar()
        self.notaspronunciacion_var = tk.StringVar()
        self.notasescritura_var = tk.StringVar()
        self.notaspractica_var = tk.StringVar()
        self.notasteoria_var = tk.StringVar()
 
        self.create_consultar_interface()

    def create_consultar_interface(self):
        # Configurar colores
        pastel_colors = ["#F2E8DF", "#E6E6FA", "#FFDAB9", "#D1E8E2", "#F5CBA7", "#B2D8B2", "#FFE4B5", "#D5A6BD"]
        background_color = pastel_colors[1]
        label_color = "black"
        
        self.configure(bg=background_color)

        tk.Label(self, text="Cédula del Estudiante:", bg=background_color, fg=label_color).grid(row=0, column=0, padx=5, pady=5)
        self.cedula_entry = tk.Entry(self, textvariable=self.cedula_var, bg="white")
        self.cedula_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="Consultar Estudiante", command=self.consultar_estudiante, bg="lightblue").grid(row=0, column=2, padx=5, pady=5)
        
        tk.Label(self, text="Nombre:", bg=background_color, fg=label_color).grid(row=1, column=0, padx=5, pady=5)
        tk.Label(self, text="Apellido:", bg=background_color, fg=label_color).grid(row=2, column=0, padx=5, pady=5)
        tk.Label(self, text="Celular:", bg=background_color, fg=label_color).grid(row=3, column=0, padx=5, pady=5)
        tk.Label(self, text="Email:", bg=background_color, fg=label_color).grid(row=4, column=0, padx=5, pady=5)
        tk.Label(self, text="Modalidad:", bg=background_color, fg=label_color).grid(row=5, column=0, padx=5, pady=5)
        tk.Label(self, text="Pronunciación:", bg=background_color, fg=label_color).grid(row=7, column=0, padx=5, pady=5)
        tk.Label(self, text="Escritura:", bg=background_color, fg=label_color).grid(row=8, column=0, padx=5, pady=5)
        tk.Label(self, text="Práctica:", bg=background_color, fg=label_color).grid(row=9, column=0, padx=5, pady=5)
        tk.Label(self, text="Teoría:", bg=background_color, fg=label_color).grid(row=10, column=0, padx=5, pady=5)

        self.nombre_label = tk.Label(self, textvariable=self.nombre_var, bg=background_color, fg="black")
        self.nombre_label.grid(row=1, column=1, padx=5, pady=5)
        self.apellido_label = tk.Label(self, textvariable=self.apellido_var, bg=background_color, fg="black")
        self.apellido_label.grid(row=2, column=1, padx=5, pady=5)
        self.celular_label = tk.Label(self, textvariable=self.celular_var, bg=background_color, fg="black")
        self.celular_label.grid(row=3, column=1, padx=5, pady=5)
        self.email_label = tk.Label(self, textvariable=self.email_var, bg=background_color, fg="black")
        self.email_label.grid(row=4, column=1, padx=5, pady=5)
        self.modalidad_label = tk.Label(self, textvariable=self.modalidad_var, bg=background_color, fg="black")
        self.modalidad_label.grid(row=5, column=1, padx=5, pady=5)
        
        self.notaspronunciacion_label = tk.Label(self, textvariable=self.notaspronunciacion_var, bg=background_color, fg="black")
        self.notaspronunciacion_label.grid(row=7, column=1, padx=5, pady=5)
        self.notasescritura_label = tk.Label(self, textvariable=self.notasescritura_var, bg=background_color, fg="black")
        self.notasescritura_label.grid(row=8, column=1, padx=5, pady=5)
        self.notaspractica_label = tk.Label(self, textvariable=self.notaspractica_var, bg=background_color, fg="black")
        self.notaspractica_label.grid(row=9, column=1, padx=5, pady=5)
        self.notasteoria_label = tk.Label(self, textvariable=self.notasteoria_var, bg=background_color, fg="black")
        self.notasteoria_label.grid(row=10, column=1, padx=5, pady=5)             

    def consultar_estudiante(self):
        cedula_estudiante = self.cedula_var.get()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tabla_registros WHERE cedula = ?", cedula_estudiante)
        estudiante = cursor.fetchone()
        cursor.close()

        if estudiante is None:
            messagebox.showerror("Error", "El número de cédula no existe en la base de datos.")
        else:
            self.nombre_var.set(estudiante[1])
            self.apellido_var.set(estudiante[2])
            self.celular_var.set(estudiante[3])
            self.email_var.set(estudiante[4])
            self.modalidad_var.set(estudiante[5])

            cursor_notas = self.conn.cursor()
            cursor_notas.execute("SELECT pronunciacion, escritura, practica, teoria FROM tabla_notas WHERE cedula_estudiante = ?", cedula_estudiante)
            notas = cursor_notas.fetchone()
            cursor_notas.close()

            if notas is not None:
                pronunciacion, escritura, practica, teoria = notas
                self.notaspronunciacion_var.set(pronunciacion)
                self.notasescritura_var.set(escritura)
                self.notaspractica_var.set(practica)
                self.notasteoria_var.set(teoria)
            else:
                self.notaspronunciacion_var.set("N/A")
                self.notasescritura_var.set("N/A")
                self.notaspractica_var.set("N/A")
                self.notasteoria_var.set("N/A")
