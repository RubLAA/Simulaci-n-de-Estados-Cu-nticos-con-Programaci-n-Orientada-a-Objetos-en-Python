from src.quantum.Estado_Cuantico import EstadoCuantico
import numpy as np
from typing import List, Union, Dict

class OperadorCuantico:
    def __init__(self, nombre: str, matriz: List[List[Union[complex, float]]]):
        """
        Inicializa un operador cuántico (matriz) con un nombre y su representación matricial.
        
        Args:
            nombre (str): Identificador o etiqueta del operador (e.g. 'X', 'H')
            matriz (List[List[Union[complex, float]]]): Matriz cuadrada n×n
        """
        self.nombre: str = nombre
        # Convertir la matriz a numpy array de dtype=complex
        self.matriz: np.ndarray = np.array(matriz, dtype=complex)
        # Verificar que la matriz sea cuadrada
        filas, cols = self.matriz.shape        
        if filas != cols:
            raise ValueError("La matriz del operador debe ser cuadrada (n×n)")

    def aplicar(self, estado: EstadoCuantico) -> EstadoCuantico:
        """
        Aplica el operador a un EstadoCuantico, retornando un nuevo EstadoCuantico transformado.
        No modifica el estado original.

        Args:
            estado (EstadoCuantico): Estado sobre el cual aplicar la transformación

        Returns:
            EstadoCuantico: Nuevo estado resultante de la aplicación
        """
        # Verificar dimensión compatible
        if len(estado.vector) != self.matriz.shape[0]:
            raise ValueError("Dimensión del operador y del estado no coinciden")
        # Multiplicación matriz-vector
        vector_np = np.array(estado.vector, dtype=complex)
        resultado_np = self.matriz.dot(vector_np)
        # Convertir de nuevo a lista
        vector_transformado = resultado_np.tolist()
        # Nuevo identificador concatenando
        nuevo_id = f"{estado.id}_{self.nombre}"
        # La base permanece igual
        return EstadoCuantico(nuevo_id, vector_transformado, base=estado.base)