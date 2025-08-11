from users import User
def create():
    estudiante = User.create("Juan Perez", "Student")
    if estudiante:
        print(f"Se ha creado un nuevo estudiante: {estudiante.name}")

    profesor = User.create("Ana Gomez", "Professor")
    if profesor:
        print(f"Se ha creado un nuevo profesor: {profesor.name}")

    visitante = User.create("Maria Lopez", "Visitor")
    if visitante:
        print(f"Se ha creado un nuevo visitante: {visitante.name}")

if __name__ == '__main__':
    create()