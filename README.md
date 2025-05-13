# Simulación de Estados Cuánticos con Programación Orientada a Objetos en Python

Repositorio: https://github.com/RubLAA/Simulaci-n-de-Estados-Cu-nticos-con-Programaci-n-Orientada-a-Objetos-en-Python.git

Este proyecto implementa la gestión de estados cuánticos con funcionalidades de:

- Crear estados cuánticos
- Medir probabilidades de cada base
- Aplicar operadores cuánticos (unitarios)
- Persistir estados en CSV
- Cargar estados desde CSV

Además, incluye una suite de pruebas unitarias con **pytest** para garantizar el correcto funcionamiento.

---

## Estructura del proyecto

```plaintext
src
└── quantum
    ├── __init__.py
    ├── Estado_Cuantico.py
    ├── Operador_Cuantico.py
    ├── RepositorioDeEstados.py
    └── menu.py

test
├── __init__.py
└── test_quantum.py

requirements.txt
README.md
main.py
```

- **src/cuantica/**: paquete Python con las clases principales.
- **tests/**: pruebas unitarias.
- **requirements.txt**: dependencias.
- **README.md**: guía de uso y organización.

---

## Requisitos

- Python 3.8 o superior
- Virtualenv (recomendado)

---

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/RubLAA/Simulaci%C3%B3n-de-Estados-Cu%C3%A1nticos-con-Programaci%C3%B3n-Orientada-a-Objetos-en-Python.git
   cd Simulación-de-Estados-Cuánticos-con-Programación-Orientada-a-Objetos-en-Python
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Linux/Mac
   # o: venv\Scripts\activate  # Windows
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## Uso

### Importación manual

```python
from cuantica.estado_cuantico import EstadoCuantico
from cuantica.operador_cuantico import OperadorCuantico
from cuantica.repositorio import RepositorioDeEstados

repo = RepositorioDeEstados()
repo.agregar_estado("q0", [1, 0])                        # |0⟩
repo.agregar_estado("plus", [1/2**0.5, 1/2**0.5])         # |+⟩

# Medición
probs = repo.medir_estado("plus")

# Operador Hadamard
d = 1/math.sqrt(2)
H = OperadorCuantico("H", [[d, d], [d, -d]])
new_state = repo.aplicar_operador("q0", H, "q0_H")
print(new_state)

# Persistencia
repo.guardar("estados.csv")
new_repo = RepositorioDeEstados()
new_repo.cargar("estados.csv")
```

### Interfaz de línea de comandos (opcional)

Si existe `src/cuantica/main.py`, ejecútalo:
```bash
python src/cuantica/main.py
```
Sigue el menú interactivo para gestionar estados.

---

## Ejecución de pruebas

Con el entorno virtual activo, ejecuta:
```bash
pytest -v
```
Esto correrá todas las pruebas en `tests/`.

---

## Dependencias

```text
numpy==1.24.2
pytest==7.2.0
```
