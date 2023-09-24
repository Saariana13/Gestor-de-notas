import tkinter as tk
from tkinter import simpledialog, messagebox
import pyodbc
from tkinter import ttk
from FORMULARIO_ESTUDIANTE import *
from FORMULARIO_REPORTE import *
from PIL import ImageTk, Image
from LOGIN_SEGURIDAD import*




class Menu:
    root  = None
    conn = None
    
    def __init__(self):
        self.root  = tk.Tk()

        self.root.title("Menú Principal")
        self.root.geometry("426x500") 
        self.conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-KNP8F6B3;'  
                      'Database=GESTOR_DE_NOTAS_clases_koreano;' 
                      'Trusted_Connection=yes;')
        self.datos = None 
        
  

    def configure_show_Main(self):

        imagen = Image.open("BTS.png")
        photo = ImageTk.PhotoImage(imagen)
        fondo = tk.Label(self.root, image=photo)
        fondo.image = photo 
        fondo.pack() 
        
        menubar = tk.Menu(self.root)

        formulario_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu Formularios ", menu=formulario_menu)
        formulario_menu.add_command(label="Ingresar Datos",command=self.abrir_ventana_ingresar_datos)
        formulario_menu.add_command(label="Ingresar Notas", command=self.abrir_ventana_ingresar_notas)
        formulario_menu.add_separator()
        formulario_menu.add_command(label="Consultar Estudiante", command=self.abrir_ventana_consultar_estudiante)
        formulario_menu.add_command(label="Modificar Estudiante", command=self.abrir_modificar_dialog)
        formulario_menu.add_command(label="Eliminar Estudiante", command=self.abrir_ventana_eliminar_estudiante)

        reporte_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu Reportes", menu=reporte_menu)
        reporte_menu.add_command(label="Lista de Estudiantes", command=self.abrir_ventana_lista_estudiante)
        reporte_menu.add_separator()
        reporte_menu.add_command(label="Estadísticas del estudiante", command=self.abrir_ventana_estadistica_estudiante)
        reporte_menu.add_command(label="Estadísticas del curso", command=self.abrir_ventana_estadistica_curso)
      

        self.root.config(menu=menubar)
        self.root.after(100, self.formulario_seguidad_App)
        self.root.mainloop() 
        
    def formulario_seguidad_App(self):
        LoginDialog(self.root, self.conn, self.root)
        
        
    def abrir_ventana_ingresar_datos(self):
        RegistroDatosDialog(self.root, self.conn)

    def abrir_ventana_ingresar_notas(self):
        IngresarNotasDialog(self.root, self.conn)
    
    def abrir_modificar_dialog(self):
        ModificarEstudianteDialog(self.root, self.conn)
        
    def abrir_ventana_eliminar_estudiante(self):
        EliminarEstudianteDialog(self.root, self.conn)
        
    def abrir_ventana_consultar_estudiante(self):
        ConsultarEstudianteDialog(self.root, self.conn)
        
    def abrir_ventana_lista_estudiante(self):
        a=AppListadoEstudiantes(self.root,self.conn)
        a.formulario()
        
        
    def abrir_ventana_estadistica_estudiante(self):
        a=AppestadisticaEstudiantes(self.root,self.conn)
        a.formulario()
        
    def abrir_ventana_estadistica_curso(self):
        ReportePromedio ( self.root, self.conn ).formulario_p ()

 



a=Menu()
a.configure_show_Main()
a.conn.close()
print('cerrada conexion exitosamente, BORAHE')

