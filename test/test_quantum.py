import math
import pytest
from src.quantum.Estado_Cuantico import EstadoCuantico
from src.quantum.Operador_Cuantico import OperadorCuantico
from src.quantum.RepositorioDeEstados import RepositorioDeEstados

class TestEstadoCuantico:
    def test_creacion_str_y_atributos(self):
        e = EstadoCuantico("q0", [1, 0], "computacional")
        assert e.id == "q0"
        assert str(e).startswith("q0:")

    def test_error_normalizacion(self):
        with pytest.raises(ValueError):
            EstadoCuantico("bad", [1, 1], "computacional")

    def test_medicion_puro(self):
        e = EstadoCuantico("q1", [0, 1])
        probs = e.medir()
        assert probs["|0⟩"] == pytest.approx(0.0)
        assert probs["|1⟩"] == pytest.approx(1.0)

    def test_medicion_superposicion(self):
        amp = 1 / math.sqrt(2)
        e = EstadoCuantico("plus", [amp, amp])
        probs = e.medir()
        assert probs["|0⟩"] == pytest.approx(0.5)
        assert probs["|1⟩"] == pytest.approx(0.5)
    
    def test_guardar_y_cargar_con_integridad(self, tmp_path):
        repo = RepositorioDeEstados()
        repo.agregar_estado("q0", [1, 0])
        repo.agregar_estado("q1", [0, 1])
        path = tmp_path / "repo.csv"
        repo.guardar(str(path))

        # Eliminar en memoria y recargar
        repo = None
        nuevo_repo = RepositorioDeEstados()
        nuevo_repo.cargar(str(path))
        estados = nuevo_repo.listar_estados()
        assert any("q0" in s for s in estados)
        assert any("q1" in s for s in estados)

class TestOperadorCuantico:
    @pytest.fixture
    def estado_base(self):
        return EstadoCuantico("q0", [1, 0])

    def test_estado_vector_vacio(self):
        with pytest.raises(ValueError):
            EstadoCuantico("vacío", [], "computacional")


    def test_puerta_x(self, estado_base):
        X = OperadorCuantico("X", [[0, 1], [1, 0]])
        out = X.aplicar(estado_base)

    def test_puerta_hadamard(self, estado_base):
        h = 1 / math.sqrt(2)
        H = OperadorCuantico("H", [[h, h], [h, -h]])
        plus = H.aplicar(estado_base)
        assert plus.vector[0] == pytest.approx(h, rel=1e-6)
        assert plus.vector[1] == pytest.approx(h, rel=1e-6)

        # H aplicado dos veces vuelve a q0
        q0_again = H.aplicar(plus)
        assert q0_again.vector[0] == pytest.approx(1, rel=1e-6)
        assert q0_again.vector[1] == pytest.approx(0, rel=1e-6)

