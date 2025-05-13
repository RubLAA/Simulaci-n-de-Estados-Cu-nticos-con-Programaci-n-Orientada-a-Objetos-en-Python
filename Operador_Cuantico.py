import math
import numpy as np
from typing import List, Union, Dict

class EstadoCuantico:
    def __init__(self, id: str, vector: List[Union[complex, float]], base: str = "computacional"):
        """
        Inicializa un estado cuántico con un identificador único, vector de estado y base.
        
        Args:
            id (str): Identificador único del estado
            vector (List[Union[complex, float]]): Vector de amplitudes complejas o reales
            base (str): Base en la que está expresado el estado (default: "computacional")
        
        Raises:
            ValueError: Si el vector está vacío o no está normalizado
        """
        if not vector:
            raise ValueError("El vector de estado no puede estar vacío")

        # Convertir todos los amplitudes a tipo complex
        self.vector: List[complex] = [complex(amp) for amp in vector]
        self.id: str = id
        self.base: str = base

        # Validar normalización: suma de módulos al cuadrado debe ser 1
        suma_cuadrados = sum(abs(amp)**2 for amp in self.vector)
        if not math.isclose(suma_cuadrados, 1.0, rel_tol=1e-9):
            raise ValueError(f"El vector no está normalizado (suma de cuadrados = {suma_cuadrados:.6f})")

    def medir(self) -> Dict[str, float]:
        """
        Calcula las probabilidades de medición para cada estado base.
        No colapsa el estado original, solo retorna la distribución.

        Returns:
            Dict[str, float]: Diccionario que mapea cada estado base a su probabilidad.
        """
        probabilidades: Dict[str, float] = {}
        for i, amp in enumerate(self.vector):
            probabilidades[f"|{i}⟩"] = float(abs(amp)**2)
        return probabilidades

    def __str__(self) -> str:
        """
        Representación legible del estado cuántico.
        """
        def format_complex(c: complex) -> str:
            # Formatea números complejos con tres decimales
            real = f"{c.real:.3f}" if abs(c.real) > 1e-9 else "0.000"
            imag = f"{abs(c.imag):.3f}j" if abs(c.imag) > 1e-9 else ""
            sign = '+' if c.imag >= 0 else '-'
            if imag and real != "0.000":
                return f"{real}{sign}{imag}"
            return real or imag

        vector_str = ", ".join(format_complex(amp) for amp in self.vector)
        return f"{self.id}: [{vector_str}] en base {self.base}"

    def __repr__(self) -> str:
        """
        Representación técnica para depuración.
        """
        return f"EstadoCuantico(id='{self.id}', vector={self.vector}, base='{self.base}')"

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
        filas, cols = self.matriz.shapen        
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