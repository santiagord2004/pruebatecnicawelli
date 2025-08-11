### 📖 README.md: Sistema de Biblioteca Digital con Tienda

Este proyecto implementa un sistema híbrido que gestiona préstamos de libros y ventas en una tienda digital. [cite\_start]El sistema maneja usuarios [cite: 12][cite\_start], inventario de libros [cite: 27][cite\_start], multas [cite: 45] [cite\_start]y reportes[cite: 49], siguiendo un conjunto de reglas de negocio específicas.

\<br\>

-----

### 🚀 Requisitos y Tecnologías

  * [cite\_start]**Backend:** Python [cite: 7]
  * [cite\_start]**Base de datos:** [cite: 8]
  * **Gestor de paquetes:** `pip`

-----

### 🛠️ Instalación y Configuración

1.  **Clona el repositorio:**
    ```bash
    git clone [URL]
    cd 
    ```
2.  **Crea y activa un entorno virtual(en caso de errores al instalar mysql para python):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Instala las dependencias de Python:**
    ```bash
    pip install mysql-connector-python
    ```
4.  **Configura la base de datos MySQL:**
      * Crea una base de datos con el nombre `LIBRARY`.
      * Ejecuta el script SQL `LIBRARY.sql` para crear todas las tablas necesarias.
5.  **Configura la conexión a la base de datos en `db.py`:**
    Abre el archivo `db.py` y actualiza los detalles de conexión con tus credenciales de MySQL.
    ```python
    db_config = {
        'user': 'tu_usuario',
        'password': 'tu_contraseña',
        'host': '127.0.0.1',
        'database': 'LIBRARY'
    }
    ```

\<br\>

-----

### 🕹️ Guía de Uso

El proyecto se ejecuta a través de un menú interactivo en `main.py`.

Para iniciar el sistema, ejecuta el siguiente comando en tu terminal:

```bash
python3 main.py
```

Al iniciar, se te presentará un menú principal con las siguientes opciones:

1.  **Inicializar datos de usuarios y libros:**
    Esta opción poblará la base de datos con datos de prueba, lo que es necesario para poder probar las demás funcionalidades.

2.  **Gestión de Préstamos:**

      * **Realizar un préstamo:** Ingresa el ID del usuario y del libro. 
      * **Devolver un libro:** Ingresa el ID del préstamo.
      * **Extender un préstamo:** Permite a los profesores extender un préstamo una vez por 15 días adicionales[cite: 25].
      * **Reportar un libro perdido:** Aplica una multa de $5.000 por la pérdida del libro y lo marca como 'Maintenance'.

3.  **Gestión de Compras:**

      * **Realizar una compra:** Permite comprar uno o varios libros en una sola transacción.
      * **Sensibilidad a mayúsculas y minúsculas:** Es **CRÍTICO** que al ingresar el tipo de libro lo hagas con la primera letra en mayúscula y el resto en minúscula: **`Physical`** o **`Digital`**. Un valor incorrecto, como `physical` o `DIGITAL`, resultará en un error.

4.  **Gestión de Stock:**

      * **Ejecutar gestión automática de stock:** Ajusta el stock mínimo de los libros basándose en su popularidad o falta de movimiento.
      * **Verificar auto-reorden de stock:** Genera una alerta si el stock físico de un libro está por debajo de su stock mínimo.

5.  **Generar Reportes:**

      * Muestra diversos informes sobre la actividad del sistema, incluyendo los libros más populares, los usuarios con multas y las ventas por categoría.

6.  **Salir:**
    Cierra la aplicación de manera segura.

\<br\>

