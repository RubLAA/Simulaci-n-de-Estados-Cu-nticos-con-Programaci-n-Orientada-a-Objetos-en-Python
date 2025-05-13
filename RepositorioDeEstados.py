from Estado_Cuantico import EstadoCuantico
from Operador_Cuantico import OperadorCuantico
from typing import List, Union, Dict, Optional

class RepositorioDeEstados:
    def __init__(self):
        """
        Repositorio para almacenar y gestionar múltiples EstadosCuantico.
        """
        self.estados: Dict[str, EstadoCuantico] = {}

    def listar_estados(self) -> List[str]:
        """
        Retorna una lista con la representación de cada estado almacenado.
        """
        if not self.estados:
            return []
        return [str(estado) for estado in self.estados.values()]

    def agregar_estado(self, id: str, vector: List[Union[complex, float]], base: str = "computacional") -> None:
        """
        Crea y agrega un nuevo EstadoCuantico al repositorio.
        """
        if id in self.estados:
            raise ValueError(f"Error: ya existe un estado con identificador '{id}'")
        estado = EstadoCuantico(id, vector, base)
        self.estados[id] = estado

    def obtener_estado(self, id: str) -> Optional[EstadoCuantico]:
        """
        Retorna el EstadoCuantico con el identificador dado, o None si no existe.
        """
        return self.estados.get(id)

    def aplicar_operador(self, id_estado: str, operador: OperadorCuantico, nuevo_id: Optional[str] = None) -> EstadoCuantico:
        """
        Aplica un OperadorCuantico a un EstadoCuantico existente en el repositorio.

        Args:
            id_estado (str): Identificador del estado a transformar.
            operador (OperadorCuantico): Operador a aplicar.
            nuevo_id (Optional[str]): Identificador para el nuevo estado. Si no se proporciona,
                                      se genera como '{id_estado}_{operador.nombre}'.

        Returns:
            EstadoCuantico: El nuevo estado transformado.

        Raises:
            KeyError: Si no existe el estado original.
            ValueError: Si el nuevo_id ya está en uso o dimensiones incompatibles.
        """
        # Obtener estado original
        estado_orig = self.obtener_estado(id_estado)
        if estado_orig is None:
            raise KeyError(f"No existe ningún estado con identificador '{id_estado}'")

        # Generar identificador del nuevo estado
        target_id = nuevo_id or f"{id_estado}_{operador.nombre}"
        if target_id in self.estados:
            raise ValueError(f"Error: ya existe un estado con identificador '{target_id}'")

        # Aplicar operador
        estado_nuevo = operador.aplicar(estado_orig)
        # Ajustar el id si se proporcionó nuevo_id
        estado_nuevo.id = target_id
        
        # Almacenar sin borrar el original
        self.estados[target_id] = estado_nuevo
        return estado_nuevo

    def eliminar_estado(self, id: str) -> None:
        """
        Elimina el estado con el identificador dado del repositorio.
        """
        if id not in self.estados:
            raise KeyError(f"No existe ningún estado con identificador '{id}'")
        del self.estados[id]