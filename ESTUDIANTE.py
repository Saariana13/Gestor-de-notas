class Estudiante:
    def __init__(self, nombre, apellido, cedula, email, celular):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.email = email
        self.celular = celular
        self.notas = {
            "pronunciacion": None,
            "escritura": None,
            "practica": None,
            "teoria": None
        }

    def ingresar_datos(self):
        print("Ingrese los datos del estudiante:")
        self.nombre = input("Nombre: ")
        self.apellido = input("Apellido: ")
        self.cedula = input("Cédula: ")
        self.email = input("Email: ")
        self.celular = input("Celular: ")
        modalidad_valida = False
        while not modalidad_valida:
            modalidad = input("Modalidad (presencial o virtual): ").lower()
            if modalidad in ["presencial", "virtual"]:
                self.modalidad = modalidad
                modalidad_valida = True
            else:
                print("Modalidad inválida. Por favor, ingrese 'presencial' o 'virtual'.")

    def ingresar_notas(self):
        print("Ingrese las notas del estudiante:")
        self.notas["pronunciacion"] = float(input("Pronunciación: "))
        self.notas["escritura"] = float(input("Escritura: "))
        self.notas["practica"] = float(input("Práctica: "))
        self.notas["teoria"] = float(input("Teoría: "))

    def calcular_promedio(self):
        notas_validas = [nota for nota in self.notas.values() if nota is not None]

        if notas_validas:
            promedio = sum(notas_validas) / len(notas_validas)
            print("Promedio de notas:", promedio)
        else:
            print("El estudiante no tiene notas ingresadas.")

    def imprimir_datos(self):
        print("Datos del estudiante:")
        matriz_datos = [
            ["Nombre", self.nombre],
            ["Apellido", self.apellido],
            ["Cédula", self.cedula],
            ["Email", self.email],
            ["Celular", self.celular],
            ["Modalidad", self.modalidad],
            ["Notas"],
            ["Pronunciación", self.notas["pronunciacion"]],
            ["Escritura", self.notas["escritura"]],
            ["Práctica", self.notas["practica"]],
            ["Teoría", self.notas["teoria"]],
            ["Promedio", None]
        ]

        for fila in matriz_datos:
            if len(fila) == 1:
                print(fila[0])
            else:
                print("{:<15}{}".format(fila[0] + ":", fila[1]))