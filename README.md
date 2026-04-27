Para correr el backend es necesario ejecutar estos comandos

```bash
# 1: Crear el entorno virtual
python -m venv venv

# 2: Activar el entorno virtual 
# En Windows:
venv\Scripts\activate
# En mac o linux
source venv/bin/activate

# 3: Instalar todas las dependencias
pip install -r requirements.txt

# 4: Iniciar el servidor de FastAPI
uvicorn app.main:app --reload

# 5: Y al terminar se desactiva el entorno virtual
deactivate

# Si agregas nuevas dependencias utiliza el siguiente comando para actualizar el requirements.txt
pip freeze > requirements.txt


```

Para nombrar cualquier cosa aqui en el backend se debe seguir este formato:

| Tipo de elemento                        | Estilo recomendado                        | Ejemplo correcto                | Ejemplo incorrecto        |
| --------------------------------------- | ----------------------------------------- | ------------------------------- | ------------------------  |
| **Clases**                              | `PascalCase`                              | `class UserModel:` ✅             | `class user_model:` ❌    |
| **Funciones / métodos**                 | `snake_case`                              | `def get_all_users():`  ✅         | `def GetAllUsers():` ❌   |
| **Variables**                           | `snake_case`                              | `user_name = "Juan"` ✅           | `UserName = "Juan"` ❌    |
| **Constantes**                          | `UPPER_CASE`                              | `DB_HOST = "localhost"` ✅        | `dbHost = "localhost"` ❌ |
| **Módulos (archivos .py)**              | `snake_case`                              | `user_model.py`    ✅             | `UserModel.py` ❌         |
| **Paquetes (carpetas con **init**.py)** | `snake_case`                              | `core`, `models`, `controllers` | `Core`, `Models` ❌       |
