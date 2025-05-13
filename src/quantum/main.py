from src.quantum.RepositorioDeEstados import RepositorioDeEstados
from src.quantum.Operador_Cuantico import OperadorCuantico
import math


# Ejemplos de uso
if __name__ == "__main__":
    repo = RepositorioDeEstados()
    # Agregar y listar
    repo.agregar_estado("psi", [1/math.sqrt(2), 1/math.sqrt(2)], "computacional")  # |+>
    print(repo.listar_estados())

    # Definir operador Hadamard
    h_val = 1/math.sqrt(2)
    opH = OperadorCuantico("H", [[h_val, h_val], [h_val, -h_val]])

    # Aplicar operador generando nuevo id
    psi_H = repo.aplicar_operador("psi", opH, "psi_H")
    print(psi_H)
    print(psi_H.vector)  # Aproximadamente [1.0, 0.0]

    # Verificar error al duplicar id
    try:
        repo.aplicar_operador("psi", opH, "psi_H")
    except ValueError as e:
        print(e)
