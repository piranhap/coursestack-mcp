COURSE = {
    "title": "Python para Seguridad",
    "subtitle": "Automatiza tareas de seguridad con Python",
    "lab_system": {
        "name": "linuxbox",
        "image_id": "428356ac-de2b-4618-8f1a-f34d7b55001f",
        "size": "micro",
    },
    "modules": [
        # ============================================================
        # MÓDULO 1
        # ============================================================
        {
            "name": "Módulo 1: Fundamentos de Python",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Bienvenida al curso",
                    "markdown": r"""# Bienvenida a Python para Seguridad

Hola y bienvenido/a. En este curso aprenderás a usar **Python 3** como herramienta
diaria para tareas de seguridad: analizar logs, procesar texto, hablar con la red,
calcular hashes y automatizar comprobaciones repetitivas.

## Por qué Python en seguridad

Python es el lenguaje dominante en el mundo de la seguridad ofensiva y defensiva por
tres razones:

| Ventaja | Qué significa para ti |
| --- | --- |
| Sintaxis clara | Escribes una herramienta útil en pocas líneas |
| Biblioteca estándar enorme | `re`, `socket`, `hashlib`, `subprocess` ya vienen incluidos |
| Ecosistema | Miles de librerías (`requests`, `scapy`, ...) para ampliar |

## Cómo trabajarás

Cada módulo tiene tres piezas:

1. Una lección de **Conceptos** con ejemplos de código.
2. Un **Lab** práctico que ejecutarás en tu máquina Linux (`linuxbox`, Debian 12).
3. Un **Quiz** para consolidar lo aprendido.

En los labs escribirás un archivo `.py` y lo lanzarás así:

```bash
python3 mi_script.py
```

Comprueba que tienes Python disponible:

```bash
python3 --version
```

Deberías ver algo como `Python 3.11.x`. Si es así, ya estás listo/a para empezar.

> Consejo de seguridad: practica siempre en sistemas que te pertenecen o donde tengas
> permiso explícito. Las técnicas aquí son para defender y automatizar, no para atacar.

Pulsa **siguiente** y comencemos con los fundamentos del lenguaje.
""",
                },
                {
                    "kind": "text",
                    "name": "Conceptos: Variables, tipos y strings",
                    "markdown": r"""# Variables, tipos y strings

Python no necesita declarar el tipo de una variable: lo deduce del valor que asignas.

```python
host = "10.0.0.5"        # str (cadena de texto)
puerto = 443             # int (entero)
activo = True            # bool (booleano)
ratio = 0.95             # float (decimal)
```

Consulta el tipo con `type()`:

```python
print(type(puerto))   # <class 'int'>
```

## Tipos básicos

| Tipo | Ejemplo | Uso típico en seguridad |
| --- | --- | --- |
| `str` | `"admin"` | IPs, usuarios, líneas de log |
| `int` | `22` | números de puerto, contadores |
| `float` | `1.5` | tiempos de respuesta |
| `bool` | `False` | ¿está abierto el puerto? |

## Trabajar con strings

Las cadenas son fundamentales: casi todo lo que analizas (logs, cabeceras HTTP,
salidas de comandos) es texto.

```python
linea = "  Failed password for root from 192.168.1.10  "

print(linea.strip())          # quita espacios sobrantes
print(linea.lower())          # todo a minúsculas
print("root" in linea)        # True si contiene la subcadena
print(linea.split())          # lista de palabras
```

Métodos muy usados al parsear logs:

| Método | Qué hace |
| --- | --- |
| `.strip()` | elimina espacios/blancos al inicio y fin |
| `.split(sep)` | divide la cadena en una lista |
| `.startswith(x)` | ¿empieza por `x`? |
| `.replace(a, b)` | sustituye texto |

## f-strings

La forma moderna de construir texto es la **f-string**: pon una `f` antes de la comilla
e inserta variables entre llaves.

```python
usuario = "root"
ip = "192.168.1.10"
print(f"Intento de acceso fallido: usuario={usuario} origen={ip}")
```

## Entrada y salida

`input()` lee texto del usuario (siempre devuelve `str`); `print()` lo muestra.

```python
objetivo = input("Introduce una IP: ")
print(f"Vas a escanear {objetivo}")
```

Si necesitas un número, convierte con `int()`:

```python
puerto = int(input("Puerto: "))
```

Con esto ya puedes leer datos, transformarlos y mostrarlos: la base de cualquier
script de seguridad.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 01: Tu primer script de seguridad",
                    "markdown": r"""# Lab 01: Tu primer script de seguridad

## Objetivo

Escribir un script que pida datos por teclado, los procese y muestre un resumen con
formato. Practicarás variables, tipos, strings, `input()` y `print()`.

## Instrucciones

1. Conéctate a tu máquina `linuxbox` (Debian 12).
2. Crea un archivo llamado `perfil.py` con tu editor favorito (`nano perfil.py`).
3. El programa debe:
   - Pedir un **nombre de usuario** con `input()`.
   - Pedir una **dirección IP** con `input()`.
   - Pedir un **número de puerto** y convertirlo a entero con `int()`.
   - Calcular la longitud del nombre de usuario con `len()`.
   - Mostrar un resumen usando una **f-string**, indicando además si el puerto es un
     puerto "privilegiado" (menor que 1024) o no.

4. Ejecuta tu script:

```bash
python3 perfil.py
```

## Salida esperada (ejemplo)

```
Usuario: admin
IP: 10.0.0.5
Puerto: 22
--- Resumen ---
Usuario 'admin' (5 caracteres) conectando a 10.0.0.5:22
Puerto privilegiado: True
```

## Pistas

- Recuerda que `input()` devuelve texto; para comparar el puerto con 1024 necesitas
  un `int`.
- Usa `len(usuario)` para contar caracteres.
- Una comparación como `puerto < 1024` ya devuelve un `bool`.
""",
                    "solution_markdown": r"""# Solución comentada

```python
# perfil.py
# Pide datos al usuario, los procesa y muestra un resumen de seguridad.

# 1. Leemos texto del teclado. input() SIEMPRE devuelve str.
usuario = input("Usuario: ")
ip = input("IP: ")

# 2. El puerto debe ser numérico para poder compararlo, así que lo convertimos.
puerto = int(input("Puerto: "))

# 3. Calculamos la longitud del nombre de usuario.
longitud = len(usuario)

# 4. Un puerto por debajo de 1024 requiere privilegios de root en Linux.
#    La comparación devuelve directamente un booleano.
privilegiado = puerto < 1024

# 5. Mostramos el resumen con f-strings.
print("--- Resumen ---")
print(f"Usuario '{usuario}' ({longitud} caracteres) conectando a {ip}:{puerto}")
print(f"Puerto privilegiado: {privilegiado}")
```

## Explicación paso a paso

1. **Lectura de datos**: usamos `input()` tres veces. Es clave recordar que devuelve
   siempre una cadena (`str`), aunque el usuario escriba números.
2. **Conversión de tipo**: `int(input("Puerto: "))` transforma el texto en un entero.
   Sin esta conversión, `puerto < 1024` fallaría porque compararíamos texto con número.
3. **Función `len()`**: cuenta cuántos caracteres tiene el nombre de usuario. Es una
   función incorporada muy útil para validar longitudes (contraseñas, tokens, etc.).
4. **Booleano derivado**: `puerto < 1024` produce `True` o `False`. En Linux los
   puertos 0-1023 son "privilegiados" y solo root puede abrirlos, un dato relevante en
   seguridad.
5. **f-strings**: al poner `f` antes de la comilla podemos insertar variables entre
   llaves `{}`, lo que hace el código legible y evita concatenaciones frágiles.

Para ejecutarlo:

```bash
python3 perfil.py
```
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 1: Fundamentos",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Qué tipo de dato devuelve siempre la función input()?",
                            [
                                ("str (una cadena de texto)", True),
                                ("int (un entero)", False),
                                ("bool (un booleano)", False),
                                ("El tipo depende de lo que escriba el usuario", False),
                            ],
                        ),
                        (
                            "¿Cómo conviertes el texto \"22\" en el número entero 22?",
                            [
                                ("int(\"22\")", True),
                                ("str(22)", False),
                                ("\"22\".integer()", False),
                                ("float(\"22\")", False),
                            ],
                        ),
                        (
                            "¿Qué muestra print(\"root\" in \"Failed for root\")?",
                            [
                                ("True", True),
                                ("False", False),
                                ("root", False),
                                ("Un error de sintaxis", False),
                            ],
                        ),
                        (
                            "¿Qué método de string elimina los espacios al principio y al final?",
                            [
                                (".strip()", True),
                                (".split()", False),
                                (".lower()", False),
                                (".replace()", False),
                            ],
                        ),
                    ],
                },
            ],
        },
        # ============================================================
        # MÓDULO 2
        # ============================================================
        {
            "name": "Módulo 2: Estructuras de Datos y Control de Flujo",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: Listas, diccionarios, bucles y funciones",
                    "markdown": r"""# Listas, diccionarios, control de flujo y funciones

## Listas

Una **lista** es una colección ordenada y modificable. Perfecta para guardar IPs,
puertos o líneas de un log.

```python
puertos = [22, 80, 443, 3306]
puertos.append(8080)          # añade al final
print(puertos[0])             # 22 (primer elemento)
print(len(puertos))           # 5
print(puertos[-1])            # 8080 (último)
```

## Diccionarios

Un **diccionario** guarda pares `clave: valor`. Ideal para asociar un puerto con su
servicio.

```python
servicios = {22: "ssh", 80: "http", 443: "https"}
print(servicios[443])         # https
servicios[3306] = "mysql"     # añade un par nuevo
print(23 in servicios)        # False
```

| Estructura | Sintaxis | Uso |
| --- | --- | --- |
| Lista | `[1, 2, 3]` | secuencia ordenada |
| Diccionario | `{"k": "v"}` | búsqueda por clave |

## Condicionales

```python
puerto = 22
if puerto < 1024:
    print("Privilegiado")
elif puerto < 49152:
    print("Registrado")
else:
    print("Dinámico")
```

## Bucles

El bucle `for` recorre cualquier colección:

```python
for p in puertos:
    print(f"Comprobando puerto {p}")
```

El bucle `while` repite mientras se cumpla una condición:

```python
intentos = 0
while intentos < 3:
    print(f"Intento {intentos}")
    intentos += 1
```

Recorrer un diccionario con `.items()`:

```python
for puerto, servicio in servicios.items():
    print(f"{puerto} -> {servicio}")
```

## Funciones

Una **función** encapsula lógica reutilizable. Se define con `def` y devuelve valores
con `return`.

```python
def es_privilegiado(puerto):
    return puerto < 1024

if es_privilegiado(80):
    print("El 80 necesita root")
```

Con parámetros por defecto:

```python
def clasificar(puerto, umbral=1024):
    if puerto < umbral:
        return "bajo"
    return "alto"

print(clasificar(22))        # bajo
print(clasificar(8080))      # alto
```

Combinando listas, diccionarios, condicionales, bucles y funciones ya puedes construir
la lógica de casi cualquier herramienta de seguridad.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 02: Clasificador de puertos",
                    "markdown": r"""# Lab 02: Clasificador de puertos

## Objetivo

Construir un script que recorra una lista de puertos, los clasifique con una función y
genere un informe usando un diccionario. Practicarás listas, diccionarios, bucles,
condicionales y funciones.

## Instrucciones

1. En tu `linuxbox`, crea el archivo `clasificar_puertos.py`.
2. Define una **lista** con estos puertos: `21, 22, 80, 443, 3306, 8080, 9999`.
3. Define un **diccionario** que asocie al menos estos puertos con su servicio conocido:
   `21: "ftp", 22: "ssh", 80: "http", 443: "https", 3306: "mysql"`.
4. Escribe una **función** `nivel_riesgo(puerto)` que devuelva:
   - `"ALTO"` si el puerto es 21 o 23 (protocolos sin cifrar),
   - `"MEDIO"` si es un puerto conocido del diccionario,
   - `"DESCONOCIDO"` en cualquier otro caso.
5. Recorre la lista con un **bucle** e imprime una línea por puerto con: el número, el
   servicio (o `"?"` si no está en el diccionario) y su nivel de riesgo.
6. Al final, imprime cuántos puertos hay en total.

Ejecuta:

```bash
python3 clasificar_puertos.py
```

## Salida esperada (aproximada)

```
21   ftp    ALTO
22   ssh    MEDIO
80   http   MEDIO
443  https  MEDIO
3306 mysql  MEDIO
8080 ?      DESCONOCIDO
9999 ?      DESCONOCIDO
Total de puertos analizados: 7
```

## Pistas

- Para obtener el servicio sin error usa `servicios.get(puerto, "?")`.
- Comprueba pertenencia al diccionario con `if puerto in servicios`.
""",
                    "solution_markdown": r"""# Solución comentada

```python
# clasificar_puertos.py
# Clasifica una lista de puertos por servicio y nivel de riesgo.

# Lista de puertos a analizar.
puertos = [21, 22, 80, 443, 3306, 8080, 9999]

# Diccionario puerto -> servicio conocido.
servicios = {
    21: "ftp",
    22: "ssh",
    80: "http",
    443: "https",
    3306: "mysql",
}


def nivel_riesgo(puerto):
    # Devuelve el nivel de riesgo de un puerto.
    if puerto in (21, 23):
        # FTP y Telnet transmiten credenciales en texto plano.
        return "ALTO"
    elif puerto in servicios:
        return "MEDIO"
    else:
        return "DESCONOCIDO"


# Recorremos la lista e imprimimos el informe.
for p in puertos:
    servicio = servicios.get(p, "?")   # "?" si no está en el diccionario
    riesgo = nivel_riesgo(p)
    print(f"{p:<5}{servicio:<7}{riesgo}")

# len() sobre la lista nos da el total.
print(f"Total de puertos analizados: {len(puertos)}")
```

## Explicación paso a paso

1. **Lista y diccionario**: `puertos` es la colección ordenada que vamos a recorrer;
   `servicios` es la tabla de consulta puerto -> nombre.
2. **La función `nivel_riesgo`**: usa `if/elif/else`. La comprobación `puerto in (21, 23)`
   detecta protocolos sin cifrar (FTP y Telnet) que suponen riesgo ALTO. Si el puerto
   está en el diccionario de servicios conocidos, es MEDIO; en otro caso, DESCONOCIDO.
3. **`servicios.get(p, "?")`**: `.get()` devuelve el valor asociado o, si la clave no
   existe, el segundo argumento (`"?"`). Así evitamos un `KeyError`.
4. **Bucle `for`**: recorre cada puerto y usa formato con anchura (`{p:<5}`) para alinear
   las columnas y que el informe se lea limpio.
5. **`len(puertos)`**: cuenta cuántos elementos tiene la lista para el total final.

Los dos puertos que no están en el diccionario (8080 y 9999) salen como DESCONOCIDO, lo
que en un contexto real señalaría servicios que merece la pena investigar.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 2: Estructuras y control de flujo",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Cómo accedes al valor asociado a la clave 443 en un diccionario llamado servicios?",
                            [
                                ("servicios[443]", True),
                                ("servicios(443)", False),
                                ("servicios.443", False),
                                ("servicios{443}", False),
                            ],
                        ),
                        (
                            "¿Qué palabra clave se usa para definir una función en Python?",
                            [
                                ("def", True),
                                ("function", False),
                                ("func", False),
                                ("define", False),
                            ],
                        ),
                        (
                            "¿Qué método añade un elemento al final de una lista?",
                            [
                                (".append()", True),
                                (".add()", False),
                                (".insert_last()", False),
                                (".push()", False),
                            ],
                        ),
                        (
                            "En la cadena if/elif/else, ¿cuándo se ejecuta el bloque else?",
                            [
                                ("Cuando ninguna de las condiciones anteriores fue verdadera", True),
                                ("Siempre, después del if", False),
                                ("Solo cuando el if fue verdadero", False),
                                ("Cuando todas las condiciones son verdaderas", False),
                            ],
                        ),
                    ],
                },
            ],
        },
        # ============================================================
        # MÓDULO 3
        # ============================================================
        {
            "name": "Módulo 3: Archivos y Procesamiento de Texto/Logs",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: Archivos, líneas y expresiones regulares",
                    "markdown": r"""# Archivos, líneas y expresiones regulares

El pan de cada día del análisis defensivo es leer logs y extraer información. Python lo
hace muy sencillo.

## Abrir y leer archivos

Usa siempre `with`: garantiza que el archivo se cierra aunque haya un error.

```python
with open("/var/log/auth.log") as f:
    contenido = f.read()      # todo el archivo en un str
```

Para procesar línea a línea (lo habitual con logs grandes):

```python
with open("/var/log/auth.log") as f:
    for linea in f:
        linea = linea.strip()          # quita el salto de línea
        if "Failed password" in linea:
            print(linea)
```

| Modo | Significado |
| --- | --- |
| `"r"` | lectura (por defecto) |
| `"w"` | escritura (borra el contenido previo) |
| `"a"` | añadir al final |

## Escribir en un archivo

```python
with open("sospechosos.txt", "w") as f:
    f.write("192.168.1.10\n")
```

## Expresiones regulares con el módulo `re`

Las **regex** describen patrones de texto. Son imprescindibles para extraer IPs,
usuarios o fechas de un log.

```python
import re

linea = "Failed password for root from 192.168.1.10 port 22"

# Buscar una dirección IPv4
ip = re.search(r"\d+\.\d+\.\d+\.\d+", linea)
if ip:
    print(ip.group())        # 192.168.1.10
```

Metacaracteres esenciales:

| Patrón | Coincide con |
| --- | --- |
| `\d` | un dígito (0-9) |
| `\w` | letra, dígito o guion bajo |
| `\s` | un espacio en blanco |
| `+` | una o más repeticiones |
| `.` | cualquier carácter |
| `()` | grupo de captura |

## Grupos de captura

Los paréntesis capturan trozos concretos:

```python
import re

linea = "Failed password for root from 192.168.1.10 port 22"
m = re.search(r"for (\w+) from (\d+\.\d+\.\d+\.\d+)", linea)
if m:
    print(m.group(1))   # root  -> usuario
    print(m.group(2))   # 192.168.1.10 -> IP
```

## Encontrar todas las coincidencias

`re.findall` devuelve una lista con todas las coincidencias:

```python
import re

texto = "hosts: 10.0.0.1, 10.0.0.2, 10.0.0.3"
ips = re.findall(r"\d+\.\d+\.\d+\.\d+", texto)
print(ips)   # ['10.0.0.1', '10.0.0.2', '10.0.0.3']
```

> Nota: usa cadenas "raw" (`r"..."`) para las regex y así no tener que escapar las
> barras invertidas. `r"\d"` es más limpio que `"\\d"`.

Con lectura de archivos + `re` ya tienes el 80% de un analizador de logs.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 03: Analizador de intentos fallidos de SSH",
                    "markdown": r"""# Lab 03: Analizador de intentos fallidos de SSH

## Objetivo

Leer un archivo de log, extraer con expresiones regulares las IPs que fallaron al
autenticarse por SSH y contar cuántos intentos hizo cada una. Esto es la base de la
detección de ataques de fuerza bruta.

## Preparación

Primero crea un log de ejemplo en tu `linuxbox`. Copia y pega este bloque en la terminal:

```bash
cat > auth.log <<'EOF'
Jan 10 10:00:01 srv sshd[1010]: Failed password for root from 192.168.1.10 port 22 ssh2
Jan 10 10:00:03 srv sshd[1011]: Failed password for root from 192.168.1.10 port 22 ssh2
Jan 10 10:00:05 srv sshd[1012]: Accepted password for admin from 10.0.0.5 port 22 ssh2
Jan 10 10:00:07 srv sshd[1013]: Failed password for invalid user test from 203.0.113.9 port 22 ssh2
Jan 10 10:00:09 srv sshd[1014]: Failed password for root from 192.168.1.10 port 22 ssh2
Jan 10 10:00:11 srv sshd[1015]: Failed password for admin from 203.0.113.9 port 22 ssh2
EOF
```

## Instrucciones

1. Crea `analizar_ssh.py`.
2. Abre `auth.log` con `with open(...)` y recórrelo línea a línea.
3. Para cada línea que contenga `"Failed password"`, usa el módulo `re` para extraer la
   dirección IP de origen.
4. Cuenta los intentos por IP usando un **diccionario** (clave = IP, valor = número de
   intentos).
5. Al final, imprime cada IP con su número de intentos fallidos.
6. Marca como **"SOSPECHOSA"** cualquier IP con 2 o más intentos fallidos.

Ejecuta:

```bash
python3 analizar_ssh.py
```

## Salida esperada (aproximada)

```
192.168.1.10 -> 3 intentos fallidos [SOSPECHOSA]
203.0.113.9 -> 2 intentos fallidos [SOSPECHOSA]
```

## Pistas

- El patrón `r"from (\d+\.\d+\.\d+\.\d+)"` captura la IP en el grupo 1.
- Para contar: `conteo[ip] = conteo.get(ip, 0) + 1`.
- Recuerda importar `re` al principio del archivo.
""",
                    "solution_markdown": r"""# Solución comentada

```python
# analizar_ssh.py
# Detecta IPs con intentos fallidos de SSH (posible fuerza bruta).

import re

# Diccionario que acumulará: IP -> número de intentos fallidos.
conteo = {}

# Abrimos el log de forma segura con "with".
with open("auth.log") as f:
    for linea in f:
        # Solo nos interesan los fallos de autenticación.
        if "Failed password" not in linea:
            continue

        # Extraemos la IP que aparece tras "from".
        m = re.search(r"from (\d+\.\d+\.\d+\.\d+)", linea)
        if m:
            ip = m.group(1)
            # get(ip, 0) devuelve 0 si la IP aún no estaba: sumamos 1.
            conteo[ip] = conteo.get(ip, 0) + 1

# Informe final.
for ip, intentos in conteo.items():
    etiqueta = " [SOSPECHOSA]" if intentos >= 2 else ""
    print(f"{ip} -> {intentos} intentos fallidos{etiqueta}")
```

## Explicación paso a paso

1. **`import re`**: cargamos el módulo de expresiones regulares.
2. **Diccionario acumulador**: `conteo` empieza vacío y se irá rellenando con cada IP
   como clave y el número de fallos como valor.
3. **Lectura con `with`**: recorremos el archivo línea a línea. Es eficiente en memoria
   porque no cargamos todo el log de golpe.
4. **Filtro rápido**: `if "Failed password" not in linea: continue` descarta las líneas
   que no nos interesan (como los "Accepted password") antes de aplicar la regex.
5. **La regex `from (\d+\.\d+\.\d+\.\d+)`**: `\d+` significa "uno o más dígitos" y los
   puntos separan los cuatro octetos. Los paréntesis crean un grupo de captura que
   recuperamos con `m.group(1)`.
6. **Conteo idiomático**: `conteo.get(ip, 0) + 1` obtiene el contador actual (o 0 si es
   la primera vez) y le suma 1. Es el patrón estándar para contar en Python.
7. **Umbral de sospecha**: al imprimir, marcamos como `[SOSPECHOSA]` toda IP con 2 o más
   intentos, que es exactamente la señal que buscaría un sistema anti fuerza bruta como
   fail2ban.

La IP `10.0.0.5` no aparece en el informe porque su intento fue `Accepted`, no `Failed`.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 3: Archivos y regex",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Por qué se recomienda abrir archivos con la sentencia 'with'?",
                            [
                                ("Porque cierra el archivo automáticamente, incluso si ocurre un error", True),
                                ("Porque hace la lectura más rápida", False),
                                ("Porque convierte el archivo a JSON", False),
                                ("Porque es la única forma de leer archivos en Python", False),
                            ],
                        ),
                        (
                            "En una expresión regular, ¿qué representa \\d+?",
                            [
                                ("Uno o más dígitos", True),
                                ("Exactamente un dígito", False),
                                ("Cualquier carácter que no sea dígito", False),
                                ("Uno o más espacios en blanco", False),
                            ],
                        ),
                        (
                            "Con m = re.search(r\"for (\\w+)\", linea), ¿cómo obtienes el texto capturado por el grupo?",
                            [
                                ("m.group(1)", True),
                                ("m.capture(1)", False),
                                ("m[group]", False),
                                ("m.match(1)", False),
                            ],
                        ),
                        (
                            "¿Qué devuelve re.findall(r\"\\d+\\.\\d+\\.\\d+\\.\\d+\", texto)?",
                            [
                                ("Una lista con todas las IPs encontradas en el texto", True),
                                ("Solo la primera IP encontrada", False),
                                ("Un booleano indicando si hay coincidencias", False),
                                ("Un diccionario de coincidencias", False),
                            ],
                        ),
                    ],
                },
            ],
        },
        # ============================================================
        # MÓDULO 4
        # ============================================================
        {
            "name": "Módulo 4: Redes con Python",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: Sockets, requests y escaneo de puertos",
                    "markdown": r"""# Redes con Python: sockets, HTTP y escaneo

## El módulo `socket`

Un **socket** es el extremo de una conexión de red. Con `socket` puedes comprobar si un
puerto TCP está abierto: intentas conectarte y ves si tiene éxito.

```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)                       # no esperar más de 1 segundo
resultado = s.connect_ex(("127.0.0.1", 22))
s.close()

if resultado == 0:
    print("Puerto 22 ABIERTO")
else:
    print("Puerto 22 cerrado o filtrado")
```

| Elemento | Significado |
| --- | --- |
| `AF_INET` | IPv4 |
| `SOCK_STREAM` | TCP |
| `settimeout(1)` | evita esperas eternas |
| `connect_ex` | devuelve 0 si conecta, un código de error si no |

`connect_ex` es preferible a `connect` en un escáner porque devuelve un código en lugar
de lanzar una excepción.

## Un escáner de puertos simple

Combina un bucle con sockets para revisar varios puertos:

```python
import socket

objetivo = "127.0.0.1"
for puerto in [22, 80, 443, 8080]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    if s.connect_ex((objetivo, puerto)) == 0:
        print(f"{puerto} abierto")
    s.close()
```

## HTTP con `requests`

Para hablar con servicios web, la librería `requests` es el estándar. Instálala si
hiciera falta:

```bash
pip install requests
```

Una petición GET:

```python
import requests

r = requests.get("https://example.com")
print(r.status_code)          # 200
print(r.headers.get("Server"))  # cabecera del servidor
print(len(r.text))            # tamaño del cuerpo HTML
```

| Atributo | Contiene |
| --- | --- |
| `r.status_code` | código HTTP (200, 404, ...) |
| `r.headers` | diccionario de cabeceras |
| `r.text` | cuerpo como texto |
| `r.json()` | cuerpo parseado como dict (si es JSON) |

Ejemplo defensivo: comprobar cabeceras de seguridad.

```python
import requests

r = requests.get("https://example.com")
if "Strict-Transport-Security" not in r.headers:
    print("Falta cabecera HSTS")
```

## Manejar errores de red

La red falla a menudo. Envuelve las peticiones en `try/except`:

```python
import requests

try:
    r = requests.get("https://example.com", timeout=3)
    print(r.status_code)
except requests.RequestException as e:
    print(f"Error de conexion: {e}")
```

Con sockets para el nivel bajo y `requests` para HTTP, ya puedes automatizar
comprobaciones de red completas.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 04: Escáner de puertos TCP",
                    "markdown": r"""# Lab 04: Escáner de puertos TCP

## Objetivo

Construir un escáner de puertos que revise un rango de puertos en un host y muestre
cuáles están abiertos. Practicarás `socket`, bucles, `try/except` y funciones.

## Instrucciones

1. En tu `linuxbox`, crea `escaner.py`.
2. Define el host objetivo como `"127.0.0.1"` (localhost) y una lista de puertos a
   comprobar, por ejemplo: `[21, 22, 25, 80, 443, 3306, 8080]`.
3. Escribe una **función** `puerto_abierto(host, puerto)` que:
   - Cree un socket TCP.
   - Aplique un `settimeout` corto (por ejemplo 0.5 segundos).
   - Use `connect_ex` y devuelva `True` si el resultado es `0`, `False` en caso
     contrario.
   - Cierre siempre el socket.
4. Recorre la lista de puertos y, por cada uno, imprime si está ABIERTO o cerrado.
5. Al final, muestra una lista con solo los puertos abiertos.

Ejecuta:

```bash
python3 escaner.py
```

## Comprobación

Puedes abrir un puerto de prueba en otra terminal para ver un resultado ABIERTO. Por
ejemplo, arranca un servidor web simple:

```bash
python3 -m http.server 8080
```

Y vuelve a lanzar tu escáner: el puerto 8080 debería salir ABIERTO.

## Salida esperada (aproximada)

```
Puerto 21: cerrado
Puerto 22: ABIERTO
Puerto 25: cerrado
...
Puertos abiertos: [22, 8080]
```

## Pistas

- `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` crea un socket TCP.
- `connect_ex` devuelve 0 cuando el puerto está abierto.
- Guarda los abiertos en una lista con `.append()`.
""",
                    "solution_markdown": r"""# Solución comentada

```python
# escaner.py
# Escáner de puertos TCP simple sobre un host.

import socket


def puerto_abierto(host, puerto):
    # Devuelve True si el puerto TCP está abierto en el host.
    # Creamos un socket TCP/IPv4.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Timeout corto para que el escaneo sea rápido y no se quede colgado.
    s.settimeout(0.5)
    # connect_ex devuelve 0 si la conexión tuvo éxito (puerto abierto).
    resultado = s.connect_ex((host, puerto))
    s.close()
    return resultado == 0


host = "127.0.0.1"
puertos = [21, 22, 25, 80, 443, 3306, 8080]
abiertos = []

for puerto in puertos:
    if puerto_abierto(host, puerto):
        print(f"Puerto {puerto}: ABIERTO")
        abiertos.append(puerto)
    else:
        print(f"Puerto {puerto}: cerrado")

print(f"Puertos abiertos: {abiertos}")
```

## Explicación paso a paso

1. **`import socket`**: el módulo de red de la biblioteca estándar, no requiere instalar
   nada.
2. **La función `puerto_abierto`**: encapsula la lógica de comprobar un único puerto.
   Devolver un booleano hace el código principal muy legible.
3. **Creación del socket**: `AF_INET` indica IPv4 y `SOCK_STREAM` indica TCP.
4. **`settimeout(0.5)`**: sin timeout, un puerto filtrado por un firewall dejaría el
   script bloqueado. Medio segundo es un buen equilibrio entre rapidez y fiabilidad.
5. **`connect_ex`**: a diferencia de `connect`, no lanza una excepción cuando falla;
   devuelve un código numérico. `0` significa éxito, es decir, puerto abierto. Por eso
   comparamos `resultado == 0`.
6. **Cerrar el socket**: `s.close()` libera el recurso. En un escáner que abre muchos
   sockets es importante no dejarlos abiertos.
7. **Bucle e informe**: recorremos la lista, imprimimos el estado de cada puerto y
   guardamos los abiertos en la lista `abiertos` con `.append()` para el resumen final.

Este es exactamente el principio que usan herramientas como `nmap`, aunque en versión
mínima. Recuerda: escanea únicamente sistemas propios o con permiso explícito.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 4: Redes",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "En un escáner de puertos, ¿qué valor devuelve connect_ex cuando el puerto está abierto?",
                            [
                                ("0", True),
                                ("1", False),
                                ("True", False),
                                ("-1", False),
                            ],
                        ),
                        (
                            "¿Para qué sirve s.settimeout(0.5) en un socket?",
                            [
                                ("Para evitar que la conexión se quede bloqueada esperando indefinidamente", True),
                                ("Para cifrar la conexión", False),
                                ("Para aumentar la velocidad de descarga", False),
                                ("Para limitar el número de puertos a escanear", False),
                            ],
                        ),
                        (
                            "Con la librería requests, ¿qué atributo contiene el código HTTP de la respuesta?",
                            [
                                ("r.status_code", True),
                                ("r.code", False),
                                ("r.http_status", False),
                                ("r.response", False),
                            ],
                        ),
                        (
                            "¿Qué combinación de argumentos crea un socket TCP sobre IPv4?",
                            [
                                ("socket.AF_INET, socket.SOCK_STREAM", True),
                                ("socket.AF_INET6, socket.SOCK_DGRAM", False),
                                ("socket.AF_UNIX, socket.SOCK_STREAM", False),
                                ("socket.AF_INET, socket.SOCK_DGRAM", False),
                            ],
                        ),
                    ],
                },
            ],
        },
        # ============================================================
        # MÓDULO 5
        # ============================================================
        {
            "name": "Módulo 5: Automatización de Seguridad",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: subprocess, hashlib, pathlib y APIs",
                    "markdown": r"""# Automatización: subprocess, hashlib, pathlib y APIs

## Ejecutar comandos con `subprocess`

`subprocess` permite lanzar comandos del sistema desde Python y capturar su salida.

```python
import subprocess

resultado = subprocess.run(
    ["ss", "-tuln"],           # comando como lista de argumentos
    capture_output=True,
    text=True,                 # salida como str, no bytes
)
print(resultado.stdout)
print("Código de salida:", resultado.returncode)
```

> Seguridad: pasa el comando como **lista** (`["ls", "-l"]`), nunca como una sola cadena
> con `shell=True` sobre entrada del usuario. Evitas así inyección de comandos.

## Hashing con `hashlib`

Los hashes verifican integridad de archivos y detectan cambios (indicadores de
compromiso).

```python
import hashlib

datos = b"contenido del archivo"
h = hashlib.sha256(datos).hexdigest()
print(h)
```

Hashear un archivo por bloques (para no cargarlo entero en memoria):

```python
import hashlib

h = hashlib.sha256()
with open("/bin/ls", "rb") as f:      # "rb" = modo binario
    for bloque in iter(lambda: f.read(4096), b""):
        h.update(bloque)
print(h.hexdigest())
```

| Algoritmo | Uso recomendado |
| --- | --- |
| `md5` | solo compatibilidad; NO para seguridad |
| `sha1` | obsoleto para firmas |
| `sha256` | estándar actual para integridad |

## Rutas con `os` y `pathlib`

`pathlib` ofrece una forma moderna y limpia de trabajar con rutas y archivos.

```python
from pathlib import Path

carpeta = Path("/etc")
for archivo in carpeta.glob("*.conf"):
    print(archivo.name, archivo.stat().st_size, "bytes")
```

| Operación | pathlib |
| --- | --- |
| ¿Existe? | `Path("x").exists()` |
| ¿Es archivo? | `p.is_file()` |
| Tamaño | `p.stat().st_size` |
| Listar patrón | `p.glob("*.log")` |

Con `os` también puedes leer variables de entorno, útil para secretos:

```python
import os

token = os.environ.get("API_TOKEN", "")
```

## Consumir una API

Automatizar seguridad suele implicar consultar APIs (reputación de IPs, CVEs, etc.).
Con `requests` y JSON:

```python
import requests

r = requests.get("https://api.ejemplo.com/ip/8.8.8.8", timeout=5)
if r.status_code == 200:
    datos = r.json()            # convierte JSON a diccionario
    print(datos.get("reputacion"))
```

Combinando `subprocess`, `hashlib`, `pathlib` y APIs puedes construir automatizaciones
de seguridad completas: desde inventariar archivos hasta enriquecer indicadores.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 05: Verificador de integridad de archivos",
                    "markdown": r"""# Lab 05: Verificador de integridad de archivos

## Objetivo

Crear una herramienta que calcule el hash SHA-256 de todos los archivos de un directorio
usando `pathlib` y `hashlib`. Es la base de un sistema de detección de cambios (FIM,
File Integrity Monitoring).

## Instrucciones

1. En tu `linuxbox`, crea un directorio de prueba con unos archivos:

```bash
mkdir -p ~/vigilar
echo "config uno" > ~/vigilar/a.conf
echo "config dos" > ~/vigilar/b.conf
echo "binario simulado" > ~/vigilar/c.bin
```

2. Crea `integridad.py`.
3. El programa debe:
   - Usar `pathlib.Path` para apuntar al directorio `~/vigilar` (puedes usar
     `Path.home() / "vigilar"`).
   - Recorrer todos los archivos del directorio con `.iterdir()` o `.glob("*")`.
   - Para cada archivo, escribir una **función** `hash_sha256(ruta)` que lea el archivo
     en modo binario por bloques y devuelva su hash hexadecimal.
   - Imprimir una línea por archivo con: nombre, tamaño en bytes y su hash SHA-256.
4. Ejecuta:

```bash
python3 integridad.py
```

## Salida esperada (aproximada)

```
a.conf   11 bytes  9b74c9897b...
b.conf   11 bytes  1a2b3c4d5e...
c.bin    17 bytes  ffee00dd11...
```

## Reto extra

Vuelve a ejecutar el script tras modificar `a.conf`:

```bash
echo "config MODIFICADO" > ~/vigilar/a.conf
python3 integridad.py
```

Observa cómo cambia el hash de `a.conf`: así se detectan alteraciones no autorizadas.

## Pistas

- Abre en binario: `open(ruta, "rb")`.
- Acumula con `h.update(bloque)` y obtén el resultado con `h.hexdigest()`.
- Filtra solo archivos con `if ruta.is_file()`.
""",
                    "solution_markdown": r"""# Solución comentada

```python
# integridad.py
# Calcula el hash SHA-256 de cada archivo de un directorio (base de un FIM).

import hashlib
from pathlib import Path


def hash_sha256(ruta):
    # Devuelve el hash SHA-256 hexadecimal de un archivo.
    h = hashlib.sha256()
    # Modo binario "rb": los hashes se calculan sobre bytes, no texto.
    with open(ruta, "rb") as f:
        # Leemos por bloques de 4096 bytes para no cargar archivos grandes enteros.
        for bloque in iter(lambda: f.read(4096), b""):
            h.update(bloque)
    return h.hexdigest()


# Directorio a vigilar: /home/<usuario>/vigilar
directorio = Path.home() / "vigilar"

for ruta in sorted(directorio.iterdir()):
    # Nos saltamos subdirectorios: solo hasheamos archivos.
    if not ruta.is_file():
        continue
    tamano = ruta.stat().st_size
    digest = hash_sha256(ruta)
    print(f"{ruta.name:<10}{tamano} bytes  {digest}")
```

## Explicación paso a paso

1. **Importaciones**: `hashlib` para el hashing y `Path` de `pathlib` para manejar rutas
   de forma moderna y portable.
2. **La función `hash_sha256`**: crea un objeto hash con `hashlib.sha256()` y lo va
   alimentando con `update()`. Al final, `hexdigest()` devuelve el hash como cadena
   hexadecimal legible.
3. **Modo binario `"rb"`**: los hashes operan sobre bytes. Abrir en binario evita
   problemas de codificación y funciona igual para texto o binarios.
4. **Lectura por bloques**: `iter(lambda: f.read(4096), b"")` lee el archivo en trozos de
   4 KB hasta que `read` devuelve una cadena vacía de bytes (`b""`). Así el script
   funciona incluso con archivos de varios gigabytes sin agotar la memoria.
5. **`Path.home() / "vigilar"`**: construye la ruta al directorio del usuario de forma
   independiente del sistema. El operador `/` une rutas en pathlib.
6. **`iterdir()` + `is_file()`**: recorremos el contenido del directorio y descartamos lo
   que no sea un archivo regular.
7. **`stat().st_size`**: obtiene el tamaño en bytes, un metadato útil junto al hash.

La clave defensiva: si el contenido de un archivo cambia aunque sea un byte, su
SHA-256 cambia por completo. Guardando estos hashes como línea base, cualquier
modificación posterior (por ejemplo, un atacante troyanizando un binario) se detecta al
instante.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 5: Automatización",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Por qué es más seguro pasar el comando a subprocess.run como una lista en lugar de una cadena con shell=True?",
                            [
                                ("Porque evita la inyección de comandos a través de la entrada del usuario", True),
                                ("Porque las listas se ejecutan más rápido", False),
                                ("Porque shell=True no existe en Python", False),
                                ("Porque las cadenas no pueden contener argumentos", False),
                            ],
                        ),
                        (
                            "¿Qué método de un objeto hashlib devuelve el hash como texto hexadecimal?",
                            [
                                (".hexdigest()", True),
                                (".digest()", False),
                                (".hexvalue()", False),
                                (".tohex()", False),
                            ],
                        ),
                        (
                            "¿Qué algoritmo de hashing es el recomendado hoy para verificar integridad?",
                            [
                                ("sha256", True),
                                ("md5", False),
                                ("crc32", False),
                                ("base64", False),
                            ],
                        ),
                        (
                            "Con pathlib, ¿cómo compruebas el tamaño en bytes de un archivo p?",
                            [
                                ("p.stat().st_size", True),
                                ("p.size()", False),
                                ("p.length", False),
                                ("len(p)", False),
                            ],
                        ),
                    ],
                },
            ],
        },
        # ============================================================
        # MÓDULO 6
        # ============================================================
        {
            "name": "Módulo 6: Proyecto Integrador + Capstone",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: Diseño de una herramienta de seguridad",
                    "markdown": r"""# Diseño de una herramienta de seguridad completa

Ha llegado el momento de juntar todo: lectura de archivos, regex, diccionarios, funciones
y hashing en una única herramienta. En este módulo construirás un **analizador de logs de
seguridad** que produce un informe accionable.

## Estructura de una buena herramienta

Divide el programa en funciones con una responsabilidad clara cada una:

| Función | Responsabilidad |
| --- | --- |
| leer/parsear | extraer datos crudos del log |
| analizar | aplicar reglas y contar |
| reportar | mostrar resultados de forma clara |

Este patrón (parsear -> analizar -> reportar) es el corazón de casi cualquier
herramienta defensiva.

```python
def parsear(ruta):
    eventos = []
    with open(ruta) as f:
        for linea in f:
            eventos.append(linea.strip())
    return eventos

def analizar(eventos):
    resumen = {}
    for e in eventos:
        # ... aplicar reglas ...
        pass
    return resumen

def reportar(resumen):
    for clave, valor in resumen.items():
        print(f"{clave}: {valor}")
```

## Datos accionables

Un informe útil no vuelca datos crudos: los prioriza. Piensa en umbrales:

```python
UMBRAL_ALERTA = 5

for ip, intentos in resumen.items():
    if intentos >= UMBRAL_ALERTA:
        print(f"ALERTA: {ip} con {intentos} intentos")
```

## Robustez

Una herramienta real maneja errores: archivos que no existen, líneas mal formadas...

```python
from pathlib import Path

ruta = Path("auth.log")
if not ruta.exists():
    print("No se encuentra el archivo de log")
else:
    print("Analizando...")
```

## Presentar resultados ordenados

Ordena los resultados para destacar lo importante primero, por ejemplo las IPs con más
intentos:

```python
resumen = {"10.0.0.1": 2, "203.0.113.9": 8, "192.168.1.5": 5}

# sorted por valor, de mayor a menor
for ip, n in sorted(resumen.items(), key=lambda par: par[1], reverse=True):
    print(f"{ip}: {n}")
```

## Checklist antes de entregar una herramienta

| Comprobación | ¿Hecho? |
| --- | --- |
| ¿Maneja archivos inexistentes? | |
| ¿Está dividida en funciones claras? | |
| ¿Prioriza lo crítico en el informe? | |
| ¿Los umbrales son configurables? | |

Con estos principios, en el Capstone construirás una herramienta que un analista real
podría usar en su día a día.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 06 (Capstone): Analizador de logs de seguridad",
                    "markdown": r"""# Lab 06 (Capstone): Analizador de logs de seguridad

## Objetivo

Construir la herramienta final del curso: un **analizador de logs de autenticación** que
detecta posibles ataques de fuerza bruta, prioriza las IPs más agresivas y genera un
informe ordenado. Integrarás archivos, regex, diccionarios, funciones, umbrales y
ordenación.

## Preparación

Crea un log de ejemplo más completo en tu `linuxbox`:

```bash
cat > seguridad.log <<'EOF'
Jan 12 08:00:01 srv sshd[2001]: Failed password for root from 203.0.113.9 port 22 ssh2
Jan 12 08:00:02 srv sshd[2002]: Failed password for root from 203.0.113.9 port 22 ssh2
Jan 12 08:00:03 srv sshd[2003]: Failed password for admin from 203.0.113.9 port 22 ssh2
Jan 12 08:00:04 srv sshd[2004]: Failed password for root from 203.0.113.9 port 22 ssh2
Jan 12 08:00:05 srv sshd[2005]: Failed password for root from 203.0.113.9 port 22 ssh2
Jan 12 08:00:06 srv sshd[2006]: Accepted password for carlos from 10.0.0.20 port 22 ssh2
Jan 12 08:00:07 srv sshd[2007]: Failed password for guest from 198.51.100.7 port 22 ssh2
Jan 12 08:00:08 srv sshd[2008]: Failed password for guest from 198.51.100.7 port 22 ssh2
Jan 12 08:00:09 srv sshd[2009]: Failed password for oracle from 192.168.1.50 port 22 ssh2
EOF
```

## Requisitos de la herramienta

Crea `capstone.py` con al menos estas tres funciones:

1. `parsear(ruta)`: abre el archivo y, para cada línea con `"Failed password"`, extrae
   con `re` la **IP** y el **usuario** al que intentaron acceder. Devuelve una lista de
   pares `(usuario, ip)`.
2. `analizar(eventos)`: recibe la lista y devuelve un **diccionario** `ip -> nº de
   intentos fallidos`.
3. `reportar(resumen, umbral)`: imprime las IPs **ordenadas de más a menos intentos**,
   marcando con `ALERTA` las que igualan o superan el `umbral` (usa 3 como umbral).

El programa principal debe:
- Comprobar que el archivo existe (usa `pathlib`).
- Llamar a las tres funciones en orden.
- Al final, imprimir cuántas IPs distintas superaron el umbral.

Ejecuta:

```bash
python3 capstone.py
```

## Salida esperada (aproximada)

```
=== Informe de intentos fallidos SSH ===
203.0.113.9   -> 5 intentos  [ALERTA]
198.51.100.7  -> 2 intentos
192.168.1.50  -> 1 intento
IPs en alerta (>= 3 intentos): 1
```

## Pistas

- Regex útil: `r"for (?:invalid user )?(\w+) from (\d+\.\d+\.\d+\.\d+)"`.
- Para contar: `resumen[ip] = resumen.get(ip, 0) + 1`.
- Para ordenar: `sorted(resumen.items(), key=lambda par: par[1], reverse=True)`.
""",
                    "solution_markdown": r"""# Solución comentada

```python
# capstone.py
# Analizador de logs de autenticación: detecta fuerza bruta y prioriza IPs.

import re
from pathlib import Path

UMBRAL = 3   # nº de fallos a partir del cual una IP se considera en ALERTA


def parsear(ruta):
    # Extrae pares (usuario, ip) de las líneas con 'Failed password'.
    eventos = []
    # La regex captura el usuario (ignorando 'invalid user ') y la IP.
    patron = re.compile(r"for (?:invalid user )?(\w+) from (\d+\.\d+\.\d+\.\d+)")
    with open(ruta) as f:
        for linea in f:
            if "Failed password" not in linea:
                continue
            m = patron.search(linea)
            if m:
                usuario = m.group(1)
                ip = m.group(2)
                eventos.append((usuario, ip))
    return eventos


def analizar(eventos):
    # Cuenta cuántos intentos fallidos hizo cada IP.
    resumen = {}
    for usuario, ip in eventos:
        resumen[ip] = resumen.get(ip, 0) + 1
    return resumen


def reportar(resumen, umbral):
    # Imprime las IPs ordenadas de más a menos intentos.
    print("=== Informe de intentos fallidos SSH ===")
    en_alerta = 0
    # Ordenamos por número de intentos, de mayor a menor.
    for ip, intentos in sorted(resumen.items(), key=lambda par: par[1], reverse=True):
        etiqueta = "  [ALERTA]" if intentos >= umbral else ""
        palabra = "intento" if intentos == 1 else "intentos"
        print(f"{ip:<14}-> {intentos} {palabra}{etiqueta}")
        if intentos >= umbral:
            en_alerta += 1
    return en_alerta


# --- Programa principal ---
ruta = Path("seguridad.log")
if not ruta.exists():
    print("No se encuentra 'seguridad.log'. Crea el log de ejemplo primero.")
else:
    eventos = parsear(ruta)
    resumen = analizar(eventos)
    total_alerta = reportar(resumen, UMBRAL)
    print(f"IPs en alerta (>= {UMBRAL} intentos): {total_alerta}")
```

## Explicación paso a paso

1. **Arquitectura parsear -> analizar -> reportar**: cada función tiene una única
   responsabilidad, lo que hace la herramienta fácil de leer, probar y ampliar.
2. **`parsear`**: precompila la regex con `re.compile` (más eficiente si se usa muchas
   veces). El fragmento `(?:invalid user )?` es un grupo **no capturador** opcional: hace
   coincidir tanto `for root` como `for invalid user test`, capturando siempre el nombre
   real en el grupo 1 y la IP en el grupo 2. Devuelve una lista de tuplas `(usuario, ip)`.
3. **`analizar`**: recorre los eventos y construye el diccionario `ip -> contador` con el
   patrón idiomático `resumen.get(ip, 0) + 1`.
4. **`reportar`**: usa `sorted` con `key=lambda par: par[1]` y `reverse=True` para mostrar
   primero las IPs más agresivas: es lo que un analista quiere ver arriba. Marca con
   `[ALERTA]` las que alcanzan el umbral y cuenta cuántas hay.
5. **Concordancia de singular/plural**: pequeño detalle (`intento` vs `intentos`) que hace
   el informe más profesional.
6. **Robustez con `pathlib`**: antes de nada, `ruta.exists()` comprueba que el log está
   presente, evitando un error feo si el archivo falta.
7. **Umbral configurable**: `UMBRAL` es una constante en la cabecera; cambiarla ajusta la
   sensibilidad sin tocar la lógica.

La IP `203.0.113.9` acumula 5 fallos y salta la alerta: exactamente el comportamiento de
un ataque de diccionario contra SSH. `10.0.0.20` no aparece porque su acceso fue
`Accepted`, no `Failed`. Con esta herramienta cierras el curso habiendo construido algo
que un equipo de seguridad podría usar de verdad.

Para ejecutarla:

```bash
python3 capstone.py
```
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 6: Proyecto integrador",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Qué patrón de diseño se recomienda para estructurar una herramienta de análisis de logs?",
                            [
                                ("Dividirla en funciones: parsear, analizar y reportar", True),
                                ("Escribir todo el código en una sola línea", False),
                                ("Usar únicamente variables globales sin funciones", False),
                                ("Evitar las funciones para que sea más rápida", False),
                            ],
                        ),
                        (
                            "Para ordenar un diccionario resumen de mayor a menor por número de intentos, ¿qué expresión es correcta?",
                            [
                                ("sorted(resumen.items(), key=lambda par: par[1], reverse=True)", True),
                                ("sorted(resumen)", False),
                                ("resumen.sort()", False),
                                ("sorted(resumen.keys(), reverse=True)", False),
                            ],
                        ),
                        (
                            "En la regex 'for (?:invalid user )?(\\w+) from', ¿qué hace el fragmento (?:...)? ",
                            [
                                ("Crea un grupo opcional que NO se captura, para coincidir con o sin 'invalid user'", True),
                                ("Captura obligatoriamente el texto 'invalid user'", False),
                                ("Indica el final de la expresión regular", False),
                                ("Convierte el patrón en insensible a mayúsculas", False),
                            ],
                        ),
                        (
                            "¿Por qué conviene comprobar ruta.exists() antes de abrir el archivo de log?",
                            [
                                ("Para manejar con elegancia el caso de que el archivo no exista, en lugar de fallar con un error", True),
                                ("Porque acelera la lectura del archivo", False),
                                ("Porque es obligatorio en Python para abrir cualquier archivo", False),
                                ("Porque cifra el archivo antes de leerlo", False),
                            ],
                        ),
                    ],
                },
            ],
        },
    ],
}
