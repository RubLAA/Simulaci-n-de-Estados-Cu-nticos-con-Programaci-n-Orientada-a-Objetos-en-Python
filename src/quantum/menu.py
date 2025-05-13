import sys
from .Operador_Cuantico import OperadorCuantico
from .RepositorioDeEstados import RepositorioDeEstados

MENU = '''
=== Gestor de Estados Cuánticos ===
1. Listar estados
2. Agregar estado
3. Medir estado
4. Definir operador y aplicar
5. Guardar estados en CSV
6. Cargar estados desde CSV
7. Salir
Elige una opción: '''

def main():
    repo = RepositorioDeEstados()
    while True:
        choice = input(MENU).strip()
        if choice == '1':
            estados = repo.listar_estados()
            if not estados:
                print("No hay estados registrados.")
            else:
                print("Estados:")
                for s in estados:
                    print(" -", s)
        elif choice == '2':
            id = input("ID del nuevo estado: ").strip()
            vec_str = input("Vector (e.g. 1,0 or 0.707,0.707): ")
            try:
                comps = [complex(*map(float,p.split(','))) for p in vec_str.split()]
                base = input("Base (por defecto 'computacional'): ") or "computacional"
                repo.agregar_estado(id, comps, base)
                print(f"Estado '{id}' agregado.")
            except Exception as e:
                print("Error al agregar estado:", e)
        elif choice == '3':
            id = input("ID del estado a medir: ").strip()
            try:
                repo.medir_estado(id)
            except Exception as e:
                print("Error al medir estado:", e)
        elif choice == '4':
            id = input("ID del estado origen: ").strip()
            name = input("Nombre del operador (e.g. H, X): ").strip()
            mat_rows = int(input("Dimensión del operador (n para n×n): "))
            print("Introduce cada fila separada por punto y coma, e.g. '0,1;1,0':")
            rows = input().strip().split(';')
            try:
                matrix = [[complex(*map(float, val.split(','))) for val in row.split()] for row in rows]
                op = OperadorCuantico(name, matrix)
                new_id = input("Nuevo ID para resultado (dejar vacío autogenera): ") or None
                estado = repo.aplicar_operador(id, op, new_id)
                print("Operador aplicado:", estado)
            except Exception as e:
                print("Error al aplicar operador:", e)
        elif choice == '5':
            path = input("Ruta CSV para guardar: ").strip() or "estados.csv"
            try:
                repo.guardar(path)
            except Exception as e:
                print("Error al guardar:", e)
        elif choice == '6':
            path = input("Ruta CSV para cargar: ").strip() or "estados.csv"
            try:
                repo.cargar(path)
            except Exception as e:
                print("Error al cargar:", e)
        elif choice == '7':
            print("Saliendo...")
            sys.exit(0)
        else:
            print("Opción no válida.")

if __name__ == '__main__':
    main()
