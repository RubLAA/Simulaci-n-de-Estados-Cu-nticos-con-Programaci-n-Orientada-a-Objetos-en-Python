# Simulaci-n-de-Estados-Cu-nticos-con-Programaci-n-Orientada-a-Objetos-en-Python

Este proyecto implementa la gestión de estados cuánticos con funcionalidades de:
- Crear estados cuánticos
- Medir probabilidades de cada base
- Aplicar operadores cuánticos (unitarios)
- Persistir estados en CSV
- Cargar estados desde CSV

Además, incluye una suite de pruebas unitarias con pytest para garantizar el correcto funcionamiento.

## Estructura del proyecto

```plaintext
├── src
│   └── cuantica
│       ├── __init__.py
│       ├── estado_cuantico.py
│       ├── operador_cuantico.py
│       ├── repositorio.py
│       └── main.py       # (opcional) CLI
├── tests
│   ├── __init__.py
│   └── test_quantum.py
├── requirements.txt
└── README.md
```

- **src/cuantica/**: código fuente organizado como paquete Python.
- **tests/**: pruebas unitarias usando pytest.
- **requirements.txt**: dependencias necesarias.
- **README.md**: documentación del proyecto.

## Requisitos

- Python 3.8+
- Virtualenv (recomendado)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone <url-repositorio>
   cd <nombre-proyecto>
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Linux/Mac
   # o venv\Scripts\activate   # Windows
   ```
3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Importación manual

Puedes usar las clases desde un intérprete o script:

```python
from cuantica.estado_cuantico import EstadoCuantico
from cuantica.operador_cuantico import OperadorCuantico
from cuantica.repositorio import RepositorioDeEstados

# Crear repositorio y estados
repo = RepositorioDeEstados()
repo.agregar_estado("q0", [1, 0])             # |0⟩
repo.agregar_estado("plus", [1/2**0.5, 1/2**0.5])  # |+⟩

# Medir estado
probs = repo.medir_estado("plus")

# Definir operador Hadamard y aplicar
H = OperadorCuantico("H", [[1/2**0.5, 1/2**0.5], [1/2**0.5, -1/2**0.5]])
new_state = repo.aplicar_operador("q0", H, "q0_H")
print(new_state)

# Guardar y cargar
repo.guardar("estados.csv")
new_repo = RepositorioDeEstados()
new_repo.cargar("estados.csv")
```

### CLI (si existe `main.py`)

```bash
python src/cuantica/main.py
```

Sigue las indicaciones en pantalla para gestionar estados interactivamente.

## Ejecutar pruebas

Con el entorno virtual activado, en la raíz del proyecto:

```bash
pytest -v
```

Esto ejecuta todos los tests en `tests/` y reporta resultados detallados.

## Dependencias

Contenido de `requirements.txt`:

```text
numpy==1.24.2
pytest==7.2.0
```  
