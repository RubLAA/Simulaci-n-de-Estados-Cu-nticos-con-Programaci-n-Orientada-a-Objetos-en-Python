from .Estado_Cuantico import EstadoCuantico
from .Operador_Cuantico import OperadorCuantico
from typing import List, Union, Dict, Optional
import csv
import os

class RepositorioDeEstados:
    def __init__(self, csv_path: str = "estados.csv"):
        """
        Repositorio con persistencia automática en CSV.
        """
        self.csv_path: str = csv_path
        self.estados: Dict[str, EstadoCuantico] = {}
        # Carga inicial si existe el archivo
        if os.path.exists(self.csv_path):
            self.cargar(self.csv_path)

    def listar_estados(self) -> List[str]:
        return [str(estado) for estado in self.estados.values()]

    def agregar_estado(self, id: str, vector: List[Union[complex, float]], base: str = "computacional") -> None:
        if id in self.estados:
            raise ValueError(f"Error: ya existe un estado con identificador '{id}'")
        estado = EstadoCuantico(id, vector, base)
        self.estados[id] = estado
        self.guardar(self.csv_path)

    def obtener_estado(self, id: str) -> Optional[EstadoCuantico]:
        return self.estados.get(id)

    def aplicar_operador(self, id_estado: str, operador: OperadorCuantico, nuevo_id: Optional[str] = None) -> EstadoCuantico:
        estado_orig = self.obtener_estado(id_estado)
        if estado_orig is None:
            raise KeyError(f"No existe ningún estado con identificador '{id_estado}'")
        target_id = nuevo_id or f"{id_estado}_{operador.nombre}"
        if target_id in self.estados:
            raise ValueError(f"Error: ya existe un estado con identificador '{target_id}'")
        estado_nuevo = operador.aplicar(estado_orig)
        estado_nuevo.id = target_id
        self.estados[target_id] = estado_nuevo
        self.guardar(self.csv_path)
        return estado_nuevo

    def eliminar_estado(self, id: str) -> None:
        if id not in self.estados:
            raise KeyError(f"No existe ningún estado con identificador '{id}'")
        del self.estados[id]
        self.guardar(self.csv_path)
    
    def medir(self) -> Dict[str, float]:
        """
        Calcula las probabilidades de medición para cada estado base.
        """
        return {f"|{i}⟩": float(abs(amp)**2) for i, amp in enumerate(self.vector)}
    
    def guardar(self, archivo: str) -> None:
        """
        Guarda todos los estados en CSV.
        Formato: id;base;vector_serializado (r,i;...)
        """
        with open(archivo, mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['id', 'base', 'vector'])
            for e in self.estados.values():
                vec_str = ';'.join(f"{c.real},{c.imag}" for c in e.vector)
                writer.writerow([e.id, e.base, vec_str])

    def cargar(self, archivo: str) -> None:
        """
        Carga desde CSV, reemplazando el repositorio.
        """
        with open(archivo, mode='r', newline='') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader, None)
            self.estados.clear()
            for row in reader:
                id, base, vec_str = row[0], row[1], row[2]
                comps = vec_str.split(';')
                vector = [complex(*map(float, comp.split(','))) for comp in comps]
                self.estados[id] = EstadoCuantico(id, vector, base)

    def medir_estado(self, id: str) -> Dict[str, float]:
        estado = self.obtener_estado(id)
        if estado is None:
            raise KeyError(f"No existe ningún estado con identificador '{id}'")
        probs = estado.medir()
        print(f"Medición del estado {estado.id} (base {estado.base}):")
        for base_label, p in probs.items():
            print(f"  - Estado base {base_label}: {p*100:.2f}%")
        return probs