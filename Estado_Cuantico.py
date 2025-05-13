import math
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
            prob = abs(amp)**2
            probabilidades[f"|{i}⟩"] = float(prob)
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
            if imag and real:
                return f"{real}{sign}{imag}"
            return real or imag

        vector_str = ", ".join(format_complex(amp) for amp in self.vector)
        return f"{self.id}: [{vector_str}] en base {self.base}"

    def __repr__(self) -> str:
        """
        Representación técnica para depuración.
        """
        return f"EstadoCuantico(id='{self.id}', vector={self.vector}, base='{self.base}')"
