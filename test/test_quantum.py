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

class TestOperadorCuantico:
    @pytest.fixture
    def estado_base(self):
        return EstadoCuantico("q0", [1, 0])

    def test_puerta_x(self, estado_base):
        X = OperadorCuantico("X", [[0, 1], [1, 0]])
        out = X.aplicar(estado_base)
