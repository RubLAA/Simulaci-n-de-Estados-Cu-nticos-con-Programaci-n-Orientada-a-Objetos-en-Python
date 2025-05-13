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
        amp = 1/math.sqrt(2)
        e = EstadoCuantico("plus", [amp, amp])
        probs = e.medir()
        assert probs["|0⟩"] == pytest.approx(0.5)
        assert probs["|1⟩"] == pytest.approx(0.5)

class TestOperadorCuantico:
    @pytest.fixture
    def estado_base(self):
        return EstadoCuantico("q0", [1, 0])

    def test_puerta_x(self, estado_base):
        X = OperadorCuantico("X", [[0,1],[1,0]])
        out = X.aplicar(estado_base)
        assert out.vector[0] == pytest.approx(0)
        assert out.vector[1] == pytest.approx(1)

    def test_puerta_hadamard(self, estado_base):
        h = 1/math.sqrt(2)
        H = OperadorCuantico("H", [[h, h], [h, -h]])
        plus = H.aplicar(estado_base)
        assert plus.vector[0] == pytest.approx(h, rel=1e-6)
        assert plus.vector[1] == pytest.approx(h, rel=1e-6)
        # H aplicado dos veces vuelve a q0
        q0_again = H.aplicar(plus)
        assert q0_again.vector[0] == pytest.approx(1, rel=1e-6)
        assert q0_again.vector[1] == pytest.approx(0, rel=1e-6)

class TestRepositorioDeEstados:
    @pytest.fixture
    def repo(self):
        return RepositorioDeEstados()

    def test_agregar_y_listar(self, repo):
        assert repo.listar_estados() == []
        repo.agregar_estado("q0", [1, 0])
        repo.agregar_estado("q1", [0, 1])
        lst = repo.listar_estados()
        assert any(s.startswith("q0:") for s in lst)
        assert any(s.startswith("q1:") for s in lst)

    def test_agregar_duplicado(self, repo):
        repo.agregar_estado("q0", [1, 0])
        with pytest.raises(ValueError):
            repo.agregar_estado("q0", [1, 0])

    def test_aplicar_operador(self, repo):
        repo.agregar_estado("q0", [1, 0])
        X = OperadorCuantico("X", [[0,1],[1,0]])
        q1 = repo.aplicar_operador("q0", X, "q1")
        assert q1.id == "q1"
        assert q1.vector[0] == pytest.approx(0)
        assert q1.vector[1] == pytest.approx(1)

    def test_medir_estado_impresion_y_retorno(self, repo, capsys):
        repo.agregar_estado("q0", [1, 0])
        probs = repo.medir_estado("q0")
        captured = capsys.readouterr()
        assert "Medición del estado q0" in captured.out
        assert probs["|0⟩"] == pytest.approx(1.0)

    def test_persistencia_csv(self, repo, tmp_path):
        repo.agregar_estado("q0", [1, 0])
        amp = 1/math.sqrt(2)
        repo.agregar_estado("plus", [amp, amp])
        file = tmp_path / "estados.csv"
        repo.guardar(str(file))
        # Nuevo repositorio y carga
        repo2 = RepositorioDeEstados()
        repo2.cargar(str(file))
        lst = repo2.listar_estados()
        assert any(s.startswith("q0:") for s in lst)
        assert any(s.startswith("plus:") for s in lst)

if __name__ == "__main__":
    pytest.main()