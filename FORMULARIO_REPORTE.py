import tkinter as tk
from tkinter import messagebox, ttk

import tkinter as tk
import pyodbc
from tkinter import ttk

import tkinter as tk
from tkinter import ttk
import pyodbc

def cargar_modalidad(conn, cb_modalidad, cod_buscar):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT modalidad FROM tabla_registros")
    modalidades = cursor.fetchall()
    modalidad_values = [modalidad[0] for modalidad in modalidades]

    cb_modalidad['values'] = modalidad_values
    if cod_buscar in modalidad_values:
        cb_modalidad.set(cod_buscar)

class AppListadoEstudiantes:
    listado_estudiantes = None
    root = None
    conn = None

    v_criterio = None
    v_orden = None
    tree = None

    def __init__(self, root, conn):
        self.root = root
        self.conn = conn

    def formulario(self):
        self.listado_estudiantes = tk.Toplevel(self.root)
        self.listado_estudiantes.title("Listado")
        self.listado_estudiantes.grab_set()
        self.listado_estudiantes.geometry("1000x400")

        frame = tk.Frame(self.listado_estudiantes)

        et_criterio = tk.Label(frame, text="Criterio:")
        et_criterio.grid(row=0, column=0)
        self.v_criterio = tk.StringVar()
        r_ci = tk.Radiobutton(frame, text="Cédula", variable=self.v_criterio, value="C")
        r_apellido = tk.Radiobutton(frame, text="Apellido", variable=self.v_criterio, value="A")
        r_ci.grid(row=0, column=1)
        r_apellido.grid(row=0, column=2)
        self.v_criterio.set("A")

        et_orden = tk.Label(frame, text="Orden:")
        et_orden.grid(row=1, column=0)
        self.v_orden = tk.StringVar()
        r_ascendente = tk.Radiobutton(frame, text="Ascendente", variable=self.v_orden, value="A")
        r_descendente = tk.Radiobutton(frame, text="Descendente", variable=self.v_orden, value="D")
        r_ascendente.grid(row=1, column=1)
        r_descendente.grid(row=1, column=2)
        self.v_orden.set("A")

        et_modalidad = tk.Label(frame, text="Modalidad:")
        et_modalidad.grid(row=2, column=0)
        self.v_modalidad = tk.StringVar()
        cb_modalidad = ttk.Combobox(frame, textvariable=self.v_modalidad, state="readonly")
        cb_modalidad.grid(row=2, column=1)
        cargar_modalidad(self.conn, cb_modalidad, "Presencial")

        b_mostrar = tk.Button(frame, text="Mostrar", command=self.mostrar_datos)
        b_tabla_completa = tk.Button(frame, text="Mostrar Tabla Completa", command=self.mostrar_tabla_completa)
        b_mostrar.grid(row=0, column=3, padx=10, pady=10)
        b_tabla_completa.grid(row=1, column=3, padx=10, pady=10)

        frame.pack()

        self.tree = ttk.Treeview(self.listado_estudiantes)

        self.tree["columns"] = (
            "columna1", "columna2", "columna3", "columna4", "columna5", "columna6", "columna7", "columna8", "columna9"
        )
        self.tree.column("#0", width=50)
        self.tree.column("columna1", anchor="w", width=100)
        self.tree.column("columna2", anchor="w", width=100)
        self.tree.column("columna3", anchor="w", width=100)
        self.tree.column("columna4", anchor="w", width=100)
        self.tree.column("columna5", anchor="w", width=100)
        self.tree.column("columna6", anchor="w", width=100)
        self.tree.column("columna7", anchor="w", width=100)
        self.tree.column("columna8", anchor="w", width=100)
        self.tree.column("columna9", anchor="w", width=100)

        self.tree.heading("#0", text="No")
        self.tree.heading("columna1", text="Cédula")
        self.tree.heading("columna2", text="Apellido")
        self.tree.heading("columna3", text="Nombre")
        self.tree.heading("columna4", text="Modalidad")
        self.tree.heading("columna5", text="Pronunciación")
        self.tree.heading("columna6", text="Escritura")
        self.tree.heading("columna7", text="Práctica")
        self.tree.heading("columna8", text="Teoría")
        self.tree.heading("columna9", text="Promedio")

        self.tree.pack(fill="both", expand=True)

    def mostrar_datos(self):
        try:
            modalidad_id = self.v_modalidad.get()
        except ValueError:
            modalidad_id = None

        cursor = self.conn.cursor()
        order = "apellido" if self.v_criterio.get() == "A" else "nombre"
        if self.v_orden.get() == "D":
            order += " DESC"

        self.tree.delete(*self.tree.get_children())
        sentencia = """
        SELECT r.cedula, r.nombre, r.apellido, r.modalidad,
        n.pronunciacion, n.escritura, n.practica, n.teoria 
        FROM tabla_registros r 
        INNER JOIN tabla_notas n ON r.cedula = n.cedula_estudiante
        """

        if modalidad_id:
            sentencia += f"WHERE r.modalidad = '{modalidad_id}'"

        cursor.execute(sentencia + " ORDER BY " + order)
        rows = cursor.fetchall()
        for i, row in enumerate(rows):
            promedio = (row[4] + row[5] + row[6] + row[7]) / 4.0
            self.tree.insert(
                "",
                i,
                text=str(i + 1),
                values=(
                    row[0],
                    str(row[2]),
                    row[1],
                    row[3],
                    str(row[4]),
                    str(row[5]),
                    "{0:.2f}".format(row[6]),
                    "{0:.2f}".format(row[7]),
                    "{0:.2f}".format(promedio)
                ),
            )

    def mostrar_tabla_completa(self):
        self.v_modalidad.set("")
        self.mostrar_datos()





        
import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
from tkinter import ttk

def cargar_modalidad(conn, cb_modalidad, cod_buscar):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT modalidad FROM tabla_registros")
    modalidades = cursor.fetchall()
    modalidad_values = [modalidad[0] for modalidad in modalidades]

    cb_modalidad['values'] = modalidad_values
    if cod_buscar in modalidad_values:
        cb_modalidad.set(cod_buscar)

class AppestadisticaEstudiantes:
    listado_estudiantes = None
    root = None
    conn = None

    v_criterio = None
    v_orden = None
    tree = None

    def __init__(self, root, conn):
        self.root = root
        self.conn = conn

    def formulario(self):
        self.listado_estudiantes = tk.Toplevel(self.root)
        self.listado_estudiantes.title("Estadistica de estudiantes")
        self.listado_estudiantes.grab_set()
        self.listado_estudiantes.geometry("650x320")

        frame = tk.Frame(self.listado_estudiantes)
        
        et_modalidad = tk.Label(frame, text="Modalidad:")
        et_modalidad.grid(row=0, column=0)
        self.v_modalidad = tk.StringVar()
        cb_modalidad = ttk.Combobox(frame, textvariable=self.v_modalidad, state="readonly")
        cb_modalidad.grid(row=0, column=1)
        cargar_modalidad(self.conn, cb_modalidad, "Presencial")

        b_mostrar = tk.Button(frame, text="Mostrar", command=self.mostrar_datos)
        b_mostrar.grid(row=0, column=2, padx=10)

        b_tabla_completa = tk.Button(frame, text="Mostrar Tabla Completa de Estudiantes", command=self.mostrar_tabla_completa)
        b_tabla_completa.grid(row=0, column=3, padx=10)

        frame.pack(side="top", padx=10, pady=10, fill="x")

        self.tree = ttk.Treeview(self.listado_estudiantes)

        self.tree["columns"] = (
            "columna1", "columna2", "columna3", "columna4", "columna5")
        self.tree.column("#0", width=50)
        self.tree.column("columna1", anchor="w", width=100)
        self.tree.column("columna2", anchor="w", width=100)
        self.tree.column("columna3", anchor="w", width=100)
        self.tree.column("columna4", anchor="w", width=100)
        self.tree.column("columna5", anchor="w", width=100)

        self.tree.heading("#0", text="No")
        self.tree.heading("columna1", text="Cédula")
        self.tree.heading("columna2", text="Nombre")
        self.tree.heading("columna3", text="Apellido")
        self.tree.heading("columna4", text="Modalidad")
        self.tree.heading("columna5", text="Promedio")  

        self.tree.pack(fill="both", expand=True)

    def mostrar_datos(self):
        try:
            modalidad_id = self.v_modalidad.get()
        except ValueError:
            modalidad_id = None

        cursor = self.conn.cursor()
        order = " DESC"

        self.tree.delete(*self.tree.get_children())
        sentencia = """
        SELECT r.cedula, r.nombre, r.apellido, r.modalidad, (n.pronunciacion + n.escritura + n.practica + n.teoria) / 4 as promedio FROM tabla_registros r INNER JOIN tabla_notas n ON r.cedula = n.cedula_estudiante
        """

        if modalidad_id:
            sentencia += f"WHERE r.modalidad = '{modalidad_id}'"

        cursor.execute(sentencia + " ORDER BY promedio" + order)
        rows = cursor.fetchall()
        
        i = 0
        for row in rows:
            self.tree.insert("", i, text=str(i + 1), values=(row[0], row[1], str(row[2]), row[3], row[4], '{0:.2f}'.format))
            i += 1

    def mostrar_tabla_completa(self):
        self.v_modalidad.set("")  # Vaciar la selección de modalidad
        #self.v_criterio.set("N")   # Establecer el criterio a "Nombre"
        self.mostrar_datos()
##################################################################
import pyodbc
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ReportePromedio:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.promedio_materias = None
        self.vop_modalidad = None
        self.tree = None

    def formulario_p(self):
        self.promedio_materias = tk.Toplevel(self.root)
        self.promedio_materias.title('Promedios del Curso')
        self.promedio_materias.grab_set()
        self.promedio_materias.geometry('300x275')

        frame = tk.Frame(self.promedio_materias)

        et_opmodalidad = tk.Label(frame, text="Modalidad:")
        et_opmodalidad.grid(row=0, column=0)

        self.vop_modalidad = tk.StringVar()

        cbop_modalidad = ttk.Combobox(frame, textvariable=self.vop_modalidad, values=['Presencial', 'Virtual', 'General'], state='readonly')
        cbop_modalidad.grid(row=0, column=1)

        self.vop_modalidad.set('Seleccione...')

        b_mostrar = tk.Button(frame, text="Mostrar", command=self.mostrar_datos_p)
        b_mostrar.grid(row=0, column=2)
        frame.pack()

        self.tree = ttk.Treeview(self.promedio_materias)

        self.tree['columns'] = ('columna1',)
        self.tree.column('columna1', anchor='e', width=60)
        self.tree.heading('#0', text='Asignaturas')
        self.tree.heading('columna1', text='Promedio')

        self.tree.pack()

    def mostrar_datos_p(self):
        cursor = self.conn.cursor()

        self.tree.delete(*self.tree.get_children())

        modalidad = self.vop_modalidad.get()

        asignaturas = ['Pronunciacion', 'Teoria', 'Practica', 'Escritura']

        if modalidad == 'General':
            promedios_generales = []

            for asignatura in asignaturas:
                sentencia = f"""
                SELECT AVG({asignatura.lower()}) AS Promedio
                FROM tabla_notas AS tn INNER JOIN tabla_registros AS tr
                ON (tn.cedula_estudiante = tr.cedula)
                """

                cursor.execute(sentencia)
                row = cursor.fetchone()
                promedios_generales.append(row[0])

            promedio_general_total = sum(promedios_generales) / len(promedios_generales)

            for i, asignatura in enumerate(asignaturas):
                self.tree.insert("", 'end', text=asignatura, values=('{0:.2f}'.format(promedios_generales[i])))
            
            self.tree.insert("", 'end', text='Promedio General', values=('{0:.2f}'.format(promedio_general_total)))

        else:
            sentencia = f"""
            SELECT 'Pronunciacion', AVG(pronunciacion) AS Promedio
            FROM tabla_notas AS tn INNER JOIN tabla_registros AS tr
            ON (tn.cedula_estudiante = tr.cedula)
            WHERE modalidad = '{modalidad}'
            GROUP BY modalidad
            UNION
            SELECT 'Teoria', AVG(teoria) AS Promedio
            FROM tabla_notas AS tn INNER JOIN tabla_registros AS tr
            ON (tn.cedula_estudiante = tr.cedula)
            WHERE modalidad = '{modalidad}'
            GROUP BY modalidad
            UNION
            SELECT 'Practica', AVG(practica) AS Promedio
            FROM tabla_notas AS tn INNER JOIN tabla_registros AS tr
            ON (tn.cedula_estudiante = tr.cedula)
            WHERE modalidad = '{modalidad}'
            GROUP BY modalidad
            UNION
            SELECT 'Escritura', AVG(escritura) AS Promedio
            FROM tabla_notas AS tn INNER JOIN tabla_registros AS tr
            ON (tn.cedula_estudiante = tr.cedula)
            WHERE modalidad = '{modalidad}'
            GROUP BY modalidad
            ORDER BY Promedio DESC
            """

            cursor.execute(sentencia)
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert("", 'end', text=row[0], values=('{0:.2f}'.format(row[1])))



