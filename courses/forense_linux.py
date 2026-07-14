COURSE = {
    "title": "Análisis Forense de Linux (DFIR)",
    "subtitle": "Triage e investigación forense de sistemas Linux comprometidos",
    "lab_system": {
        "name": "linuxbox",
        "image_id": "428356ac-de2b-4618-8f1a-f34d7b55001f",
        "size": "micro",
    },
    "modules": [
        # ==================== MÓDULO 1 ====================
        {
            "name": "Módulo 1: Fundamentos del DFIR en Linux",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Bienvenida al curso",
                    "markdown": """# Bienvenida al curso

Te damos la bienvenida al curso **Análisis Forense de Linux (DFIR)**. A lo largo de seis módulos aprenderás a realizar *triage* e investigación forense sobre sistemas Linux que han sido comprometidos, siguiendo un método riguroso y defendible ante un tribunal.

## ¿Qué vas a aprender?

- El proceso forense completo: identificación, adquisición, análisis y presentación.
- Cómo adquirir evidencia (disco y memoria) preservando su integridad con hashes.
- A reconstruir la **línea de tiempo** de un ataque a partir de los metadatos del sistema de archivos.
- A cazar artefactos de persistencia: `cron`, unidades `systemd`, claves SSH y autostart.
- A analizar logs de autenticación, `journald` y conexiones de red.
- A detectar malware, procesos ocultos y *rootkits*, cerrando con un **laboratorio capstone** de triage completo.

## Tu entorno de trabajo

Dispones de una máquina Linux llamada **linuxbox** (Debian 12) accesible por SSH. Todos los laboratorios se realizan sobre esta máquina. No necesitas instalar nada: las herramientas forenses básicas ya están disponibles o se indican los paquetes necesarios.

## Metodología

Cada módulo incluye una lección de **Conceptos** con teoría y ejemplos de comandos, uno o dos **laboratorios** prácticos con su solución comentada, y un **quiz** para consolidar. Recuerda: en DFIR la disciplina importa tanto como la técnica. Documenta cada paso, calcula hashes y nunca modifiques la evidencia original.

¡Comencemos!
""",
                },
                {
                    "kind": "text",
                    "name": "Conceptos: El proceso forense y el orden de volatilidad",
                    "markdown": """# El proceso forense y el orden de volatilidad

El *Digital Forensics and Incident Response* (DFIR) combina la respuesta a incidentes con la ciencia forense. En Linux esto implica trabajar con evidencia frágil y aplicar un método reproducible.

## Las fases del proceso forense

1. **Identificación**: determinar qué sistemas y datos son relevantes.
2. **Adquisición (preservación)**: copiar la evidencia sin alterarla, calculando hashes.
3. **Análisis**: examinar la evidencia para responder qué, cuándo, cómo y quién.
4. **Presentación**: documentar hallazgos de forma clara y defendible.

## Orden de volatilidad

La evidencia se degrada a distinta velocidad. El **orden de volatilidad** (RFC 3227) indica que debes capturar primero lo más efímero:

| Prioridad | Fuente de evidencia | Se pierde al... |
|-----------|---------------------|-----------------|
| 1 | Registros de CPU y caché | apagar/instante |
| 2 | Memoria RAM (procesos, conexiones) | apagar |
| 3 | Estado de red y tablas ARP | apagar/tiempo |
| 4 | Procesos en ejecución | apagar |
| 5 | Disco (archivos temporales) | reinicio |
| 6 | Discos y medios físicos | destrucción física |
| 7 | Configuración y topología física | rara vez |

En la práctica, en una máquina viva se captura primero la RAM y el estado de red **antes** de tocar el disco:

```bash
# Estado volátil primero (live response)
date
uptime
ps aux
ss -tulpanep
who
last
```

## Cadena de custodia

Toda evidencia debe tener una **cadena de custodia**: quién la recolectó, cuándo, con qué herramienta y cómo se ha almacenado. Cualquier hueco en esa cadena puede invalidar la evidencia. Se acompaña siempre de hashes criptográficos (SHA-256) que demuestran que la copia no ha cambiado.

## Regla de oro

**Nunca trabajes sobre la evidencia original.** Se monta en solo-lectura o se trabaja sobre una imagen. Cada acción del investigador debe ser registrada, justificada y, en lo posible, repetible por un tercero.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 01: Live response y montaje de evidencia en solo-lectura",
                    "markdown": """# Lab 01: Live response y montaje de evidencia en solo-lectura

En este laboratorio practicarás la recolección inicial de estado volátil y aprenderás a montar una imagen de evidencia en **solo-lectura**, garantizando que no la modificas.

## Objetivos

- Recolectar información volátil siguiendo el orden de volatilidad.
- Crear una pequeña imagen de sistema de archivos como "evidencia".
- Montarla en modo solo-lectura y verificar que no se puede escribir.

## Instrucciones

1. Conéctate a **linuxbox** por SSH.
2. Crea una carpeta de trabajo para tus notas: `~/caso01`.
3. Recolecta el estado volátil (fecha, uptime, procesos, red, usuarios conectados) y guárdalo en un archivo dentro de `~/caso01`.
4. Crea un archivo de 20 MB relleno con ceros y formatéalo como `ext4`: esta será tu "imagen de evidencia".
5. Móntala en un punto de montaje en **solo-lectura** (`ro`).
6. Intenta crear un archivo dentro del punto de montaje y confirma que el sistema lo rechaza.
7. Documenta la ruta del archivo de imagen y el resultado del intento de escritura.

## Pistas

- El comando `ss` sustituye al antiguo `netstat` para el estado de red.
- Puedes crear una imagen con `dd if=/dev/zero`.
- La opción de montaje `-o ro,loop` monta un archivo como dispositivo en solo-lectura.
- Necesitarás privilegios de root (`sudo`) para montar.
""",
                    "solution_markdown": """# Solución comentada

```bash
#!/bin/bash
set -e

# 1-2. Carpeta de trabajo para el caso
mkdir -p ~/caso01
cd ~/caso01

# 3. Recolección de estado volátil (orden de volatilidad)
{
  echo "=== FECHA ==="; date
  echo "=== UPTIME ==="; uptime
  echo "=== PROCESOS ==="; ps aux
  echo "=== RED ==="; ss -tulpanep
  echo "=== USUARIOS CONECTADOS ==="; who
  echo "=== ULTIMOS LOGINS ==="; last -n 20
} > live_response.txt

# 4. Crear imagen de evidencia de 20 MB y formatearla como ext4
dd if=/dev/zero of=evidencia.img bs=1M count=20
mkfs.ext4 -q evidencia.img

# 5. Montar en SOLO-LECTURA
sudo mkdir -p /mnt/evidencia
sudo mount -o ro,loop evidencia.img /mnt/evidencia

# 6. Intentar escribir (debe FALLAR)
touch /mnt/evidencia/prueba.txt 2>&1 || echo "CORRECTO: escritura rechazada (read-only file system)"

# 7. Documentar
echo "Imagen: $(pwd)/evidencia.img" >> live_response.txt
mount | grep evidencia >> live_response.txt

# Desmontar al terminar
sudo umount /mnt/evidencia
```

## Explicación paso a paso

1. **Carpeta del caso**: mantener todo bajo `~/caso01` facilita la cadena de custodia; sabemos dónde está cada artefacto.
2. **Estado volátil primero**: recolectamos `date`, `uptime`, `ps aux`, `ss`, `who` y `last`. Esto respeta el orden de volatilidad (RFC 3227): capturamos lo efímero (procesos, red, sesiones) antes de manipular el disco.
3. **`ss -tulpanep`**: muestra sockets TCP/UDP en escucha y establecidos con el proceso propietario, sustituto moderno de `netstat`.
4. **Creación de la imagen**: `dd if=/dev/zero of=evidencia.img bs=1M count=20` genera un archivo de 20 MB. `mkfs.ext4` le da un sistema de archivos para simular un disco.
5. **Montaje `-o ro,loop`**: `loop` asocia el archivo a un dispositivo de bloques virtual; `ro` fuerza **solo-lectura**. Esta es la práctica clave: la evidencia nunca debe montarse en modo escritura.
6. **Verificación**: el `touch` falla con "Read-only file system". Que el sistema **rechace** la escritura demuestra que la evidencia está protegida contra modificación accidental.
7. **Documentación**: registramos la ruta absoluta de la imagen y la salida de `mount`, elementos necesarios para la cadena de custodia.

En un caso real, la imagen provendría de un disco físico y usarías además un *write blocker* de hardware o `blockdev --setro` sobre el dispositivo antes de montarlo.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 1: Fundamentos del DFIR",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "Según el orden de volatilidad (RFC 3227), ¿cuál de estas fuentes de evidencia debe capturarse ANTES?",
                            [
                                ("La memoria RAM y las conexiones de red activas", True),
                                ("El contenido del disco duro", False),
                                ("Los archivos de configuración del sistema", False),
                                ("La topología física de la red", False),
                            ],
                        ),
                        (
                            "¿Cuál es la razón principal para montar una imagen de evidencia con la opción 'ro'?",
                            [
                                ("Evitar cualquier modificación de la evidencia original", True),
                                ("Acelerar la velocidad de lectura del disco", False),
                                ("Comprimir automáticamente los archivos", False),
                                ("Permitir que varios usuarios escriban a la vez", False),
                            ],
                        ),
                        (
                            "¿Qué documenta la cadena de custodia?",
                            [
                                ("Quién manejó la evidencia, cuándo, cómo y dónde se almacenó", True),
                                ("Únicamente el nombre del sistema operativo analizado", False),
                                ("La lista de contraseñas encontradas en el sistema", False),
                                ("El precio del hardware forense utilizado", False),
                            ],
                        ),
                        (
                            "¿Cuál es el orden correcto de las fases del proceso forense?",
                            [
                                ("Identificación, adquisición, análisis, presentación", True),
                                ("Análisis, identificación, presentación, adquisición", False),
                                ("Adquisición, presentación, análisis, identificación", False),
                                ("Presentación, análisis, adquisición, identificación", False),
                            ],
                        ),
                    ],
                },
            ],
        },
        # ==================== MÓDULO 2 ====================
        {
            "name": "Módulo 2: Adquisición de Evidencia",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: Adquisición de disco y memoria, hashing e integridad",
                    "markdown": """# Adquisición de disco y memoria, hashing e integridad

La **adquisición** es el momento más delicado de una investigación: si se hace mal, toda la evidencia posterior queda contaminada. El objetivo es obtener una copia **bit a bit** de la fuente y demostrar matemáticamente que la copia es idéntica al original.

## Live vs. dead acquisition

| Tipo | Sistema | Ventajas | Riesgos |
|------|---------|----------|---------|
| **Live** | Encendido | Captura RAM, procesos, red, discos cifrados montados | Alteras el sistema al tocarlo |
| **Dead** | Apagado | Máxima integridad del disco | Pierdes toda la memoria volátil |

La decisión depende del caso: si hay cifrado de disco activo o malware solo en memoria, la adquisición *live* es imprescindible.

## Imagen de disco con dd

`dd` copia bloques crudos. La variante `dd` clásica y `dcfldd`/`dc3dd` (con hashing integrado) son estándar:

```bash
# Imagen bit a bit de un disco completo
sudo dd if=/dev/sdb of=/evidencia/disco.img bs=4M conv=noerror,sync status=progress

# Con dc3dd calculando el hash durante la copia
sudo dc3dd if=/dev/sdb of=/evidencia/disco.img hash=sha256 log=/evidencia/disco.log
```

- `conv=noerror,sync` continúa ante errores de lectura y rellena bloques dañados para mantener el offset.
- Nunca escribas la imagen sobre el mismo disco que estás copiando.

## Captura de memoria

La RAM contiene procesos, claves, conexiones y malware que nunca toca el disco. En Linux moderno `/dev/mem` está restringido, por lo que se usan herramientas como **AVML** o **LiME**:

```bash
# AVML: volcado de RAM a un archivo
sudo ./avml /evidencia/memoria.lime

# LiME como módulo del kernel
sudo insmod lime.ko "path=/evidencia/mem.lime format=lime"
```

El volcado se analiza después con **Volatility 3**.

## Hashing: la prueba de integridad

Un hash criptográfico produce una huella única. Si un solo bit cambia, el hash cambia por completo:

```bash
# Hash de la evidencia justo después de adquirirla
sha256sum /evidencia/disco.img > /evidencia/disco.img.sha256

# Verificación posterior
sha256sum -c /evidencia/disco.img.sha256
```

Se calcula el hash **de la fuente** y **de la imagen**: si coinciden, la copia es fiel. SHA-256 es el estándar actual; MD5 y SHA-1 se consideran obsoletos por colisiones, aunque se siguen registrando por compatibilidad.

## Buenas prácticas

- Calcula el hash **antes y después** de cualquier manipulación.
- Guarda los logs de adquisición junto a la imagen.
- Usa *write blockers* en discos físicos.
- Etiqueta cada evidencia con un identificador único de caso.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 02: Crear una imagen con dd y verificar su integridad",
                    "markdown": """# Lab 02: Crear una imagen con dd y verificar su integridad

Vas a simular la adquisición de un dispositivo de bloques, generar su imagen con `dd` y demostrar mediante hashes SHA-256 que la copia es idéntica a la fuente.

## Objetivos

- Preparar un "dispositivo" de evidencia (un archivo con datos).
- Adquirir una imagen bit a bit con `dd`.
- Calcular y comparar hashes SHA-256 de fuente e imagen.
- Detectar una alteración provocando un cambio de un solo bit.

## Instrucciones

1. Conéctate a **linuxbox** y crea la carpeta `~/caso02`.
2. Crea un archivo `origen.img` de 10 MB con contenido pseudoaleatorio (será tu fuente de evidencia).
3. Adquiere una copia bit a bit llamada `imagen.img` usando `dd` con `status=progress`.
4. Calcula el hash SHA-256 de la fuente y de la imagen; guárdalos en archivos.
5. Compara ambos hashes y confirma que coinciden.
6. Modifica un único byte de `imagen.img`, recalcula su hash y demuestra que ya NO coincide con el original.
7. Documenta el hash original y el hash tras la alteración.

## Pistas

- `/dev/urandom` genera datos pseudoaleatorios.
- `sha256sum archivo` produce el hash; con `-c` verifica un archivo de sumas.
- Para cambiar un byte puedes usar `dd` con `seek`, `conv=notrunc` y una entrada de un solo carácter.
""",
                    "solution_markdown": """# Solución comentada

```bash
#!/bin/bash
set -e

mkdir -p ~/caso02
cd ~/caso02

# 2. Fuente de evidencia: 10 MB de datos pseudoaleatorios
dd if=/dev/urandom of=origen.img bs=1M count=10 status=progress

# 3. Adquisición bit a bit
dd if=origen.img of=imagen.img bs=4M conv=noerror,sync status=progress

# 4. Hashes de fuente e imagen
sha256sum origen.img  > origen.sha256
sha256sum imagen.img  > imagen.sha256

# 5. Comparar: renombramos la referencia de la imagen a la fuente para verificar
ORIG=$(awk '{print $1}' origen.sha256)
COPIA=$(awk '{print $1}' imagen.sha256)
echo "Fuente: $ORIG"
echo "Imagen: $COPIA"
if [ "$ORIG" = "$COPIA" ]; then
  echo "INTEGRIDAD OK: la imagen es idéntica a la fuente"
else
  echo "ALERTA: los hashes NO coinciden"
fi

# 6. Alterar un solo byte de la imagen (posición 1000)
printf 'X' | dd of=imagen.img bs=1 seek=1000 count=1 conv=notrunc
NUEVO=$(sha256sum imagen.img | awk '{print $1}')
echo "Hash tras alteración: $NUEVO"
if [ "$ORIG" != "$NUEVO" ]; then
  echo "DETECTADO: la imagen fue modificada (hash distinto)"
fi

# 7. Documentar
{
  echo "Hash original de la evidencia: $ORIG"
  echo "Hash tras alterar 1 byte:      $NUEVO"
} > integridad.txt
```

## Explicación paso a paso

1. **Fuente pseudoaleatoria**: `/dev/urandom` crea contenido único e incompresible, imitando un disco real con datos variados.
2. **Adquisición con `dd`**: `bs=4M` mejora el rendimiento; `conv=noerror,sync` es la convención forense que continúa ante errores rellenando con ceros para no desalinear el resto de la imagen. `status=progress` muestra el avance.
3. **Hashing SHA-256**: `sha256sum` genera la huella criptográfica. Se calcula sobre fuente e imagen por separado.
4. **Comparación**: si ambos hashes son iguales, la copia es una réplica exacta bit a bit. Esta igualdad es lo que se presenta como prueba de integridad.
5. **Alteración de un byte**: `dd ... seek=1000 count=1 conv=notrunc` sobrescribe **un solo byte** sin truncar el archivo. Es el punto pedagógico clave: un cambio mínimo produce un hash totalmente distinto (efecto avalancha).
6. **Detección**: al recalcular, el nuevo hash difiere del original, demostrando por qué el hashing detecta cualquier manipulación, por pequeña que sea.
7. **Documentación**: guardamos ambos hashes en `integridad.txt` como registro para la cadena de custodia.

En un caso real, `origen.img` sería `/dev/sdb`, la imagen se guardaría en un medio distinto y usarías `dc3dd` para hashear durante la propia adquisición y ahorrar una pasada de lectura.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 2: Adquisición de Evidencia",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Qué hace la opción 'conv=noerror,sync' en dd durante una adquisición forense?",
                            [
                                ("Continúa ante errores de lectura y rellena los bloques dañados para mantener el offset", True),
                                ("Cifra la imagen resultante con AES", False),
                                ("Comprime la imagen para ahorrar espacio", False),
                                ("Verifica automáticamente el hash SHA-256 al finalizar", False),
                            ],
                        ),
                        (
                            "¿Por qué se prefiere una adquisición 'live' en un sistema con cifrado de disco completo activo?",
                            [
                                ("Porque con el sistema encendido los datos están descifrados y se puede capturar la RAM", True),
                                ("Porque apagar el equipo acelera la copia del disco", False),
                                ("Porque el cifrado desaparece al reiniciar", False),
                                ("Porque 'dead acquisition' no funciona en discos SSD", False),
                            ],
                        ),
                        (
                            "Tras alterar un solo byte de una imagen, su hash SHA-256 cambia por completo. ¿Cómo se llama esta propiedad?",
                            [
                                ("Efecto avalancha", True),
                                ("Compresión sin pérdida", False),
                                ("Colisión de hash", False),
                                ("Suma de verificación paritaria", False),
                            ],
                        ),
                        (
                            "¿Cuál es una razón por la que hoy se prefiere SHA-256 frente a MD5 en forense?",
                            [
                                ("MD5 es vulnerable a colisiones y se considera obsoleto para integridad", True),
                                ("MD5 no puede calcularse en Linux", False),
                                ("SHA-256 produce un hash más corto y rápido de escribir", False),
                                ("MD5 modifica el archivo original al calcularse", False),
                            ],
                        ),
                    ],
                },
            ],
        },
        # ==================== MÓDULO 3 ====================
        {
            "name": "Módulo 3: Sistema de Archivos y Línea de Tiempo",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: Inodos, timestamps MAC y construcción de timelines",
                    "markdown": """# Inodos, timestamps MAC y construcción de timelines

Reconstruir **cuándo** ocurrió cada acción es el corazón del análisis forense. En Linux, el sistema de archivos ext4 guarda metadatos temporales por cada inodo que nos permiten ordenar los eventos.

## El inodo

Cada archivo tiene un **inodo**: una estructura que almacena permisos, propietario, tamaño, punteros a los bloques de datos y las marcas de tiempo. El nombre del archivo NO está en el inodo, sino en el directorio que lo referencia. Por eso pueden existir varios nombres (hard links) para un mismo inodo.

```bash
# Ver el número de inodo
ls -i /etc/passwd

# Metadatos completos del inodo
stat /etc/passwd
```

## Los timestamps MAC(B)

| Marca | Nombre | Se actualiza cuando... |
|-------|--------|------------------------|
| **A** (atime) | Access | se lee el contenido del archivo |
| **M** (mtime) | Modify | cambia el **contenido** del archivo |
| **C** (ctime) | Change | cambian los **metadatos** del inodo (permisos, dueño, nombre) |
| **B** (crtime) | Birth/Create | se crea el archivo (ext4, no siempre expuesto) |

Punto crítico: **ctime no es "creation time"**, es "change time". Un atacante puede falsificar `atime` y `mtime` con `touch -t`, pero **ctime es mucho más difícil de falsear** desde el espacio de usuario, porque se actualiza ante cualquier cambio del inodo. Por eso ctime es un aliado del investigador.

```bash
# Ver los tres tiempos y el birth time
stat archivo_sospechoso

# Manipulación típica de un atacante (anti-forense)
touch -t 202001010000 archivo_malicioso   # cambia atime y mtime, pero ctime revela la manipulación
```

## Encontrar archivos por tiempo

```bash
# Archivos modificados en las últimas 24 horas
find / -xdev -type f -mtime -1 2>/dev/null

# Archivos cuyo inodo cambió en los últimos 10 minutos
find / -xdev -type f -cmin -10 2>/dev/null

# Ordenar por mtime
find /var/www -type f -printf '%T+ %p\\n' | sort
```

`-xdev` evita cruzar a otros sistemas de archivos (como /proc o montajes de red).

## Construir un timeline

Un **timeline** ordena todos los eventos del sistema de archivos cronológicamente. La herramienta clásica es **The Sleuth Kit**:

```bash
# 1. Extraer el "body file" con los tiempos MAC de cada inodo
fls -r -m / /dev/sdb1 > cuerpo.body

# 2. Generar el timeline legible ordenado por fecha
mactime -b cuerpo.body -d > timeline.csv
```

El resultado muestra, minuto a minuto, qué archivos fueron creados, modificados o accedidos, permitiendo situar la intrusión en el tiempo y seguir el rastro del atacante. Un pico de actividad de archivos a una hora inusual suele marcar el momento del compromiso.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 03: Analizar timestamps MAC y detectar timestomping",
                    "markdown": """# Lab 03: Analizar timestamps MAC y detectar timestomping

Practicarás la lectura de los tiempos MAC con `stat` y aprenderás a detectar **timestomping**: la técnica anti-forense de falsear las marcas de tiempo de un archivo.

## Objetivos

- Interpretar atime, mtime y ctime con `stat`.
- Simular un atacante que falsifica timestamps con `touch -t`.
- Demostrar que el **ctime** delata la manipulación.

## Instrucciones

1. Conéctate a **linuxbox** y crea `~/caso03`.
2. Crea un archivo `webshell.php` con contenido cualquiera.
3. Observa sus tres timestamps con `stat`.
4. Como "atacante", usa `touch -t` para retrasar su mtime y atime a una fecha antigua (por ejemplo, año 2019), simulando que el archivo lleva mucho tiempo en el sistema.
5. Vuelve a mirar con `stat`: comprueba que mtime y atime cambiaron pero el ctime sigue reflejando el momento real de la manipulación.
6. Explica por qué el ctime es la marca fiable para el investigador.
7. Documenta ambos estados (antes y después).

## Pistas

- El formato de `touch -t` es `[[CC]YY]MMDDhhmm[.ss]`.
- `stat` muestra Access, Modify y Change.
- No existe una opción de `touch` sencilla para reescribir el ctime al pasado sin manipular el reloj del sistema.
""",
                    "solution_markdown": """# Solución comentada

```bash
#!/bin/bash
set -e

mkdir -p ~/caso03
cd ~/caso03

# 2. Crear el archivo sospechoso
echo '<?php system($_GET["cmd"]); ?>' > webshell.php

# 3. Estado inicial de los timestamps
echo "===== ANTES DE LA MANIPULACION ====="
stat webshell.php | tee estado_antes.txt

# 4. El "atacante" falsifica mtime y atime a 2019
touch -t 201903150900 webshell.php

# 5. Estado tras el timestomping
echo "===== DESPUES DEL TIMESTOMPING ====="
stat webshell.php | tee estado_despues.txt

# 6. Extraer y comparar los tiempos clave
echo "----- Comparativa -----"
echo "Modify (mtime): $(stat -c %y webshell.php)"
echo "Change (ctime): $(stat -c %z webshell.php)"
echo "Access (atime): $(stat -c %x webshell.php)"
```

## Explicación paso a paso

1. **Creación del archivo**: `webshell.php` simula un artefacto malicioso subido por un atacante.
2. **`stat` inicial**: muestra Access, Modify y Change, todos apuntando al momento actual de creación.
3. **Timestomping con `touch -t 201903150900`**: el atacante fija mtime y atime al 15 de marzo de 2019 a las 09:00 para que el archivo parezca antiguo y pase desapercibido en un timeline.
4. **`stat` posterior**: aquí está la clave. Los campos **Modify** y **Access** ahora muestran 2019, PERO el campo **Change (ctime)** muestra la fecha y hora **reales** en que se ejecutó el `touch`. ¿Por qué? Porque `touch` modifica los metadatos del inodo, y cualquier cambio del inodo actualiza automáticamente el ctime, que **no es controlable directamente** desde el espacio de usuario.
5. **Interpretación forense**: cuando el ctime es **posterior** al mtime, es una señal de alarma clásica de timestomping. Un archivo legítimo casi nunca tiene su ctime muy por delante de su mtime; ese desfase indica que alguien tocó los tiempos.
6. **Conclusión**: el investigador confía en el **ctime** y en fuentes externas (logs, journald) para fechar la intrusión, no en mtime/atime que el atacante puede reescribir.

Para falsear también el ctime, el atacante tendría que cambiar el reloj del sistema o manipular el disco a bajo nivel (por ejemplo con `debugfs`), acciones mucho más ruidosas y detectables.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 04: Construir un timeline del sistema de archivos",
                    "markdown": """# Lab 04: Construir un timeline del sistema de archivos

Ahora construirás un **timeline** cronológico de la actividad de archivos en un directorio, la técnica que permite situar un ataque en el tiempo.

## Objetivos

- Recopilar los tiempos MAC de un árbol de directorios.
- Generar un listado cronológico de eventos.
- Identificar un pico de actividad sospechoso.

## Instrucciones

1. Conéctate a **linuxbox** y crea `~/caso04`.
2. Crea un directorio `escenario` con varios archivos "normales" creados en distintos momentos.
3. Simula la actividad de un atacante creando de golpe 3 archivos sospechosos (una webshell, un binario y un script) en un instante concreto.
4. Genera un timeline del directorio `escenario` ordenado por fecha de modificación usando `find -printf` y `sort`.
5. Observa cómo los 3 archivos del atacante aparecen agrupados en el mismo minuto (el "pico" de actividad).
6. Como alternativa profesional, muestra cómo se haría con `fls`/`mactime` de The Sleuth Kit sobre una imagen.
7. Guarda el timeline en un CSV.

## Pistas

- `find dir -printf '%T+ %p\\n'` imprime el mtime en formato ordenable seguido de la ruta.
- `sort` ordena cronológicamente esas líneas.
- Un grupo de archivos con el mismo timestamp exacto es sospechoso.
""",
                    "solution_markdown": """# Solución comentada

```bash
#!/bin/bash
set -e

mkdir -p ~/caso04/escenario
cd ~/caso04/escenario

# 2. Archivos "normales" con tiempos dispersos
echo "config" > app.conf;  touch -t 202601100800 app.conf
echo "datos"  > data.csv;  touch -t 202602050930 data.csv
echo "readme" > README.md; touch -t 202603201200 README.md

# 3. Actividad del atacante: 3 archivos en el mismo instante
ATTACK_TS="202607141530"
echo '<?php system($_GET["c"]); ?>' > shell.php
echo 'binario'                       > backdoor
echo '#!/bin/bash; nc -e /bin/bash'  > persist.sh
touch -t "$ATTACK_TS" shell.php backdoor persist.sh

# 4. Generar el timeline ordenado por mtime
cd ~/caso04
find escenario -type f -printf '%T+ %p\\n' | sort > timeline.txt
echo "===== TIMELINE ====="
cat timeline.txt

# 7. Exportar a CSV
find escenario -type f -printf '%T+,%s,%p\\n' | sort > timeline.csv
echo "CSV generado en ~/caso04/timeline.csv"
```

Alternativa profesional con The Sleuth Kit sobre una imagen de disco:

```bash
# Extraer el body file (tiempos MAC de todos los inodos) y generar el timeline
fls -r -m / /evidencia/disco.img > cuerpo.body
mactime -b cuerpo.body -d > timeline_tsk.csv
```

## Explicación paso a paso

1. **Archivos normales**: creamos `app.conf`, `data.csv` y `README.md` con `touch -t` fijando fechas dispersas en enero, febrero y marzo. Representan la línea base legítima del sistema.
2. **Actividad del atacante**: `shell.php`, `backdoor` y `persist.sh` reciben todos el **mismo** timestamp (`202607141530`, 14/07/2026 15:30). En un ataque real, cuando un intruso despliega su kit de herramientas, muchos archivos aparecen creados o modificados en segundos.
3. **`find -printf '%T+ %p'`**: `%T+` imprime el mtime en formato `AAAA-MM-DD+HH:MM:SS`, directamente ordenable como texto; `%p` es la ruta. Al pasarlo por `sort` obtenemos la secuencia cronológica.
4. **Lectura del timeline**: los tres artefactos del atacante quedan **agrupados** en la misma marca temporal, formando un "pico" que destaca sobre la actividad dispersa normal. Ese pico es la firma de una intrusión y marca el momento del compromiso.
5. **CSV**: añadimos `%s` (tamaño) y separadores por comas para producir un `timeline.csv` que puede abrirse en una hoja de cálculo o cargarse en una herramienta de análisis.
6. **The Sleuth Kit**: `fls -r -m /` recorre recursivamente los inodos de una imagen y emite un *body file*; `mactime` lo convierte en un timeline legible que incluye las cuatro marcas MACB de cada archivo, incluso de archivos borrados cuyos inodos aún existen.

El valor del timeline es que **correlaciona** cientos de eventos: una vez localizado el pico, el investigador examina esos archivos, sus ctimes y los logs de esa franja horaria para reconstruir la cadena completa del ataque.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 3: Sistema de Archivos y Timeline",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Qué representa realmente el 'ctime' de un archivo en Linux?",
                            [
                                ("El momento en que cambiaron los metadatos del inodo (permisos, dueño, nombre)", True),
                                ("El momento en que se creó el archivo por primera vez", False),
                                ("El momento en que se leyó el contenido del archivo", False),
                                ("El momento en que el archivo será borrado automáticamente", False),
                            ],
                        ),
                        (
                            "Un atacante ejecuta 'touch -t 201901010000 malware'. ¿Qué marca de tiempo delata la manipulación?",
                            [
                                ("El ctime, porque refleja el momento real en que se tocó el inodo", True),
                                ("El mtime, porque no se puede modificar con touch", False),
                                ("El atime, porque touch nunca lo altera", False),
                                ("Ninguna, touch reescribe las tres marcas al pasado", False),
                            ],
                        ),
                        (
                            "En 'find / -xdev -type f -mtime -1', ¿qué logra la opción -xdev?",
                            [
                                ("Evita que find cruce a otros sistemas de archivos como /proc o montajes de red", True),
                                ("Incluye también los archivos ocultos", False),
                                ("Ordena los resultados por fecha", False),
                                ("Calcula el hash de cada archivo encontrado", False),
                            ],
                        ),
                        (
                            "Al construir un timeline, ¿qué patrón sugiere típicamente el momento de una intrusión?",
                            [
                                ("Un pico de muchos archivos creados o modificados en el mismo instante inusual", True),
                                ("Un único archivo con atime muy antiguo", False),
                                ("La ausencia total de archivos con mtime reciente", False),
                                ("Que todos los archivos tengan el mismo propietario", False),
                            ],
                        ),
                    ],
                },
            ],
        },
        # ==================== MÓDULO 4 ====================
        {
            "name": "Módulo 4: Artefactos de Usuario y Persistencia",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: Historiales, cron, systemd, SSH y autostart",
                    "markdown": """# Historiales, cron, systemd, SSH y autostart

Tras comprometer un sistema, el atacante busca **persistencia**: sobrevivir a reinicios y logouts. Conocer dónde se esconde la persistencia es esencial en el triage.

## Historiales de shell

`~/.bash_history` guarda los comandos ejecutados por un usuario. Es una mina de oro, aunque el atacante puede borrarlo o desactivarlo:

```bash
# Historial de todos los usuarios
cat /home/*/.bash_history /root/.bash_history 2>/dev/null

# Señales de anti-forense
grep -R "unset HISTFILE\\|history -c\\|export HISTSIZE=0" /home /root 2>/dev/null
```

Ojo: el historial en memoria no se escribe al disco hasta el logout, así que en *live response* conviene revisar también la variable `HISTFILE` y la sesión activa.

## Tareas programadas: cron y at

`cron` es el mecanismo de persistencia más clásico:

| Ubicación | Contenido |
|-----------|-----------|
| `/etc/crontab` | tareas del sistema |
| `/etc/cron.d/` | fragmentos de cron |
| `/etc/cron.{hourly,daily,weekly,monthly}/` | scripts periódicos |
| `/var/spool/cron/crontabs/` | crontabs por usuario |

```bash
# Crontab de cada usuario
for u in $(cut -f1 -d: /etc/passwd); do echo "== $u =="; crontab -l -u "$u" 2>/dev/null; done

# Todo lo relacionado con cron
ls -la /etc/cron* /var/spool/cron/crontabs/ 2>/dev/null
```

## Unidades systemd

systemd permite persistencia mediante *services* y *timers*, a veces en rutas de usuario poco vigiladas:

```bash
# Servicios y timers habilitados
systemctl list-unit-files --state=enabled
systemctl list-timers --all

# Unidades de usuario (persistencia sin root)
ls -la ~/.config/systemd/user/ /etc/systemd/system/ 2>/dev/null
```

Un servicio con `ExecStart` apuntando a `/tmp` o a un binario oculto es muy sospechoso.

## Claves SSH y authorized_keys

Añadir una clave pública a `authorized_keys` da acceso permanente y silencioso:

```bash
# Claves autorizadas de todos los usuarios
find / -name authorized_keys 2>/dev/null -exec echo "== {} ==" \\; -exec cat {} \\;

# Configuración del servidor (¿PermitRootLogin? ¿claves añadidas?)
grep -R "" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/ 2>/dev/null
```

Revisa la fecha de modificación de `authorized_keys`: si es reciente y no coincide con ninguna administración legítima, es una bandera roja.

## Autostart y perfiles

Otros puntos de arranque: `/etc/rc.local`, `/etc/profile.d/`, `~/.bashrc`, `~/.profile`, `/etc/ld.so.preload` (usado por rootkits) y los directorios de autostart de escritorio `~/.config/autostart/`.

```bash
grep -R "" /etc/profile.d/ ~/.bashrc ~/.profile /etc/rc.local /etc/ld.so.preload 2>/dev/null
```

## Estrategia de triage

Revisa cada mecanismo de forma sistemática y correlaciona sus **timestamps** con la ventana del incidente. La persistencia recién creada suele delatarse por un ctime dentro de la franja del ataque.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 05: Cazar mecanismos de persistencia",
                    "markdown": """# Lab 05: Cazar mecanismos de persistencia

Buscarás y documentarás varios mecanismos de persistencia que un atacante habría dejado en el sistema.

## Objetivos

- Inspeccionar bash_history en busca de comandos sospechosos.
- Enumerar tareas cron de sistema y de usuario.
- Revisar servicios y timers de systemd.
- Localizar claves SSH añadidas en authorized_keys.

## Instrucciones

1. Conéctate a **linuxbox** y crea `~/caso05`.
2. Simula la persistencia del atacante (para tener qué encontrar):
   - Añade una tarea cron de usuario que ejecute un script cada 5 minutos.
   - Crea un archivo en `/etc/cron.d/` (con sudo) con una tarea sospechosa.
   - Añade una clave pública a tu propio `~/.ssh/authorized_keys`.
3. Ahora, actuando como investigador, escribe un script de triage que:
   - Vuelque el bash_history buscando comandos peligrosos (`nc`, `wget`, `curl`, `chmod +s`, `history -c`).
   - Liste todos los crontabs de usuario y el contenido de `/etc/cron*`.
   - Liste unidades systemd habilitadas y timers.
   - Muestre todos los `authorized_keys` del sistema con su fecha de modificación.
4. Guarda el informe en `~/caso05/triage_persistencia.txt`.

## Pistas

- `crontab -l -u usuario` lista el crontab de un usuario.
- `find / -name authorized_keys` los localiza todos.
- `stat -c '%y %n'` muestra el mtime junto al nombre.
""",
                    "solution_markdown": """# Solución comentada

```bash
#!/bin/bash
set -e
mkdir -p ~/caso05
cd ~/caso05

# ---- 2. Simular persistencia del atacante ----
echo '#!/bin/bash' > /tmp/beacon.sh; chmod +x /tmp/beacon.sh
( crontab -l 2>/dev/null; echo "*/5 * * * * /tmp/beacon.sh" ) | crontab -
echo "* * * * * root /tmp/beacon.sh" | sudo tee /etc/cron.d/updater >/dev/null
mkdir -p ~/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIATTACKERKEY atacante@evil" >> ~/.ssh/authorized_keys

# ---- 3. Script de triage del investigador ----
REPORT=~/caso05/triage_persistencia.txt
{
  echo "############ TRIAGE DE PERSISTENCIA ############"
  echo; echo "===== 1. BASH_HISTORY (comandos peligrosos) ====="
  grep -REn "nc |ncat|wget |curl |chmod \\+s|history -c|unset HISTFILE|base64 -d" \
       /home/*/.bash_history /root/.bash_history 2>/dev/null

  echo; echo "===== 2. CRON DE USUARIO ====="
  for u in $(cut -f1 -d: /etc/passwd); do
    out=$(crontab -l -u "$u" 2>/dev/null) && [ -n "$out" ] && echo "-- $u --" && echo "$out"
  done

  echo; echo "===== 3. CRON DE SISTEMA ====="
  ls -la /etc/cron.d/ /etc/cron.daily/ /etc/cron.hourly/ 2>/dev/null
  grep -Rh "" /etc/cron.d/ /etc/crontab 2>/dev/null

  echo; echo "===== 4. SYSTEMD HABILITADO Y TIMERS ====="
  systemctl list-unit-files --state=enabled --no-pager 2>/dev/null
  systemctl list-timers --all --no-pager 2>/dev/null

  echo; echo "===== 5. CLAVES SSH AUTORIZADAS ====="
  find / -name authorized_keys 2>/dev/null | while read -r f; do
    echo "-- $(stat -c '%y' "$f") -- $f"
    cat "$f"
  done
} | tee "$REPORT"
```

## Explicación paso a paso

1. **Simulación del atacante**: para que el triage tenga hallazgos, plantamos tres mecanismos reales: una tarea cron de usuario cada 5 minutos, un fragmento en `/etc/cron.d/updater` (nombre que finge legitimidad) y una clave pública ajena en `authorized_keys`.
2. **bash_history**: `grep -REn` con una lista de patrones peligrosos (`nc`, `wget`, `curl`, `chmod +s`, `history -c`, `unset HISTFILE`, `base64 -d`) resalta comandos típicos de descarga de payloads, escalada por SUID y anti-forense. `-n` añade el número de línea.
3. **Cron de usuario**: recorremos cada cuenta de `/etc/passwd` con `crontab -l -u` y solo mostramos las que tienen contenido. Así aparece la tarea `*/5` del beacon.
4. **Cron de sistema**: listamos y volcamos `/etc/cron.d/`, `/etc/crontab` y los directorios periódicos. Aquí sale `updater` apuntando a `/tmp/beacon.sh`, ubicación altamente sospechosa (nada legítimo se ejecuta desde `/tmp`).
5. **systemd**: `list-unit-files --state=enabled` y `list-timers --all` revelan servicios y temporizadores persistentes; buscaríamos `ExecStart` hacia rutas raras.
6. **authorized_keys**: `find` localiza cada archivo, y `stat -c '%y'` muestra su **mtime**. Una clave añadida con fecha dentro de la ventana del incidente y un comentario como `atacante@evil` es una bandera roja inmediata.
7. **Informe**: `tee` guarda todo en `triage_persistencia.txt`, un artefacto documentado para el caso.

La clave metodológica es **correlacionar timestamps**: los mecanismos de persistencia recién plantados comparten fechas cercanas entre sí y con el resto de artefactos del ataque.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 4: Persistencia",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Por qué un servicio systemd con 'ExecStart' apuntando a un binario en /tmp es sospechoso?",
                            [
                                ("Porque el software legítimo no suele ejecutarse desde /tmp, señal de persistencia maliciosa", True),
                                ("Porque /tmp no permite ejecutar binarios en ningún caso", False),
                                ("Porque systemd no puede leer archivos en /tmp", False),
                                ("Porque /tmp se borra cada hora y rompería el servicio", False),
                            ],
                        ),
                        (
                            "Un atacante añade su clave pública a ~/.ssh/authorized_keys. ¿Qué le proporciona esto?",
                            [
                                ("Acceso remoto persistente y silencioso sin necesidad de contraseña", True),
                                ("La capacidad de descifrar el disco completo", False),
                                ("Permisos de root automáticos en el sistema", False),
                                ("Un registro que borra todos los logs de acceso", False),
                            ],
                        ),
                        (
                            "¿Cuál de estos archivos guarda los crontabs específicos de cada usuario?",
                            [
                                ("/var/spool/cron/crontabs/", True),
                                ("/etc/ssh/sshd_config", False),
                                ("/var/log/auth.log", False),
                                ("/proc/self/environ", False),
                            ],
                        ),
                        (
                            "Encontrar 'unset HISTFILE' o 'history -c' en un bash_history sugiere que...",
                            [
                                ("El atacante intentó ocultar o borrar el rastro de sus comandos (anti-forense)", True),
                                ("El usuario estaba optimizando el rendimiento del shell", False),
                                ("Se produjo un fallo automático del sistema de logs", False),
                                ("El sistema tiene el historial cifrado por defecto", False),
                            ],
                        ),
                    ],
                },
            ],
        },
        # ==================== MÓDULO 5 ====================
        {
            "name": "Módulo 5: Análisis de Logs y Red",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: auth.log, journald, wtmp/btmp y conexiones de red",
                    "markdown": """# auth.log, journald, wtmp/btmp y conexiones de red

Los logs cuentan la historia del sistema: quién entró, cuándo, desde dónde y qué falló. En una investigación son la fuente primaria para fechar y atribuir acciones.

## auth.log y journald

En Debian, la autenticación se registra en `/var/log/auth.log`; en sistemas con systemd, también en el **journal** binario:

```bash
# Intentos de login SSH fallidos
grep "Failed password" /var/log/auth.log

# Logins aceptados y desde qué IP
grep "Accepted" /var/log/auth.log

# Uso de sudo
grep "sudo:" /var/log/auth.log

# Con journald (persistente o de un arranque concreto)
journalctl -u ssh --since "2026-07-01" --until "2026-07-14"
journalctl _COMM=sudo -o short-iso
```

Un ataque de **fuerza bruta** aparece como decenas o cientos de "Failed password" desde una misma IP, a menudo seguidos de un "Accepted" que marca el compromiso.

## Registros binarios: wtmp, btmp, lastlog

Estos archivos NO son texto; se leen con utilidades específicas:

| Archivo | Contenido | Herramienta |
|---------|-----------|-------------|
| `/var/log/wtmp` | logins/logouts exitosos | `last` |
| `/var/log/btmp` | intentos de login fallidos | `lastb` |
| `/var/log/lastlog` | último login de cada usuario | `lastlog` |

```bash
last -f /var/log/wtmp        # historial de sesiones
last -f /var/log/wtmp -i     # con IPs numéricas
sudo lastb                   # intentos fallidos (fuerza bruta)
lastlog                      # último acceso por usuario
```

Un atacante avanzado puede editar `wtmp` con herramientas como `utmpdump` para borrar su sesión; comparar `wtmp` con `auth.log` ayuda a detectar esas manipulaciones.

## Análisis de red

En *live response* interesa el estado de las conexiones y los puertos en escucha:

```bash
# Sockets TCP/UDP con proceso y usuario
ss -tulpanep

# Conexiones establecidas (posible C2)
ss -tanp state established

# Equivalente clásico
netstat -tulpan
```

Busca puertos en escucha inesperados, conexiones salientes a IPs desconocidas (posible *command and control*) y procesos de red que no reconozcas. Correlaciona el PID con el binario en `/proc/PID/exe`.

## Correlación

El verdadero análisis surge de **cruzar fuentes**: una IP que aparece en cientos de `Failed password`, luego en un `Accepted`, luego en `last` con una sesión, y a la misma hora un pico de archivos nuevos en el timeline. Esa correlación reconstruye la intrusión de principio a fin.

```bash
# Top de IPs atacantes por fuerza bruta
grep "Failed password" /var/log/auth.log | grep -oE "([0-9]+\\.){3}[0-9]+" | sort | uniq -c | sort -rn | head
```
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 06: Investigar fuerza bruta SSH en los logs",
                    "markdown": """# Lab 06: Investigar fuerza bruta SSH en los logs

Analizarás logs de autenticación para detectar un ataque de fuerza bruta SSH e identificar la IP atacante y el momento del compromiso.

## Objetivos

- Distinguir intentos fallidos de logins aceptados.
- Identificar la IP con más intentos fallidos.
- Determinar si la fuerza bruta tuvo éxito.

## Instrucciones

1. Conéctate a **linuxbox** y crea `~/caso06`.
2. Como no hay un ataque real, genera un `auth.log` de laboratorio: un archivo con muchas líneas "Failed password" desde una IP atacante y, al final, una línea "Accepted password" desde esa misma IP.
3. Escribe comandos de investigación que:
   - Cuenten cuántos intentos fallidos hubo por IP y muestren el ranking.
   - Extraigan la línea "Accepted" para identificar el momento del compromiso y el usuario comprometido.
   - Determinen la ventana temporal del ataque (primer y último fallo).
4. Guarda las conclusiones en `~/caso06/hallazgos.txt`.

## Pistas

- Puedes fabricar el log con un bucle que imprima líneas con `printf`.
- Una expresión regular para IPv4: `([0-9]+\\.){3}[0-9]+`.
- `sort | uniq -c | sort -rn` produce un ranking por frecuencia.
""",
                    "solution_markdown": """# Solución comentada

```bash
#!/bin/bash
set -e
mkdir -p ~/caso06
cd ~/caso06

# 2. Fabricar un auth.log de laboratorio
LOG=auth.log
: > "$LOG"
ATTACKER="203.0.113.66"
for i in $(seq -w 1 40); do
  printf 'Jul 14 03:%02d:%02d linuxbox sshd[%d]: Failed password for invalid user admin from %s port 51%03d ssh2\\n' \
         $((10 + i % 40)) $((i % 60)) $((2000 + i)) "$ATTACKER" "$i" >> "$LOG"
done
# Algo de ruido desde otra IP
printf 'Jul 14 02:15:01 linuxbox sshd[1999]: Failed password for root from 198.51.100.9 port 40000 ssh2\\n' >> "$LOG"
# El compromiso final
printf 'Jul 14 03:51:12 linuxbox sshd[2100]: Accepted password for backup from %s port 51999 ssh2\\n' "$ATTACKER" >> "$LOG"

# 3. Investigación
{
  echo "===== RANKING DE IPs POR INTENTOS FALLIDOS ====="
  grep "Failed password" "$LOG" | grep -oE "([0-9]+\\.){3}[0-9]+" | sort | uniq -c | sort -rn

  echo; echo "===== LOGIN ACEPTADO (COMPROMISO) ====="
  grep "Accepted" "$LOG"

  echo; echo "===== VENTANA TEMPORAL DEL ATAQUE ====="
  echo "Primer intento: $(grep "Failed password" "$LOG" | head -1 | awk '{print $1,$2,$3}')"
  echo "Ultimo intento: $(grep "Failed password" "$LOG" | tail -1 | awk '{print $1,$2,$3}')"

  echo; echo "===== USUARIO COMPROMETIDO ====="
  grep "Accepted" "$LOG" | awk '{for(i=1;i<=NF;i++) if($i=="for") print "Usuario:", $(i+1)}'
} | tee ~/caso06/hallazgos.txt
```

## Explicación paso a paso

1. **Fabricación del log**: generamos 40 líneas `Failed password` desde la IP `203.0.113.66` (rango de documentación), una línea de ruido desde otra IP y, al final, un `Accepted password for backup` desde la IP atacante. Esto reproduce el patrón real de un ataque de fuerza bruta que triunfa.
2. **Ranking de IPs**: `grep "Failed password"` filtra los fallos; `grep -oE` con la regex de IPv4 extrae solo las direcciones; `sort | uniq -c | sort -rn` cuenta y ordena de mayor a menor. La IP atacante emerge en lo alto con 40 intentos frente a 1 del ruido.
3. **Login aceptado**: `grep "Accepted"` revela el instante exacto del compromiso (03:51:12), el usuario afectado (`backup`) y confirma que la misma IP atacante logró entrar: la fuerza bruta tuvo éxito.
4. **Ventana temporal**: comparando el primer y último `Failed password` acotamos la duración del ataque, dato clave para cruzar con el timeline del sistema de archivos y con otras evidencias.
5. **Usuario comprometido**: extraemos con `awk` el nombre que sigue a la palabra `for` en la línea `Accepted`. Saber que la cuenta `backup` fue tomada dirige la siguiente fase: revisar qué hizo ese usuario tras entrar.

En un caso real cruzaríamos estos hallazgos con `last -f /var/log/wtmp -i` (para ver la sesión resultante), con `lastb` (más fallos) y con las conexiones de red de esa franja, construyendo una narrativa completa: reconocimiento, fuerza bruta, acceso y actividad post-explotación.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 07: Sesiones con wtmp/btmp y conexiones de red",
                    "markdown": """# Lab 07: Sesiones con wtmp/btmp y conexiones de red

Trabajarás con los registros binarios de sesión (`wtmp`, `btmp`, `lastlog`) y con el estado de red para identificar sesiones y posibles canales de mando y control (C2).

## Objetivos

- Leer wtmp/btmp/lastlog con las herramientas correctas.
- Enumerar puertos en escucha y conexiones establecidas.
- Reconocer indicadores de una conexión C2.

## Instrucciones

1. Conéctate a **linuxbox** y crea `~/caso07`.
2. Muestra el historial de sesiones exitosas con `last`, incluyendo IPs numéricas.
3. Muestra los intentos fallidos con `lastb` (usa sudo).
4. Muestra el último acceso de cada cuenta con `lastlog`.
5. Enumera todos los sockets TCP/UDP en escucha con su proceso y usuario propietario.
6. Lista las conexiones TCP establecidas (candidatas a C2) e identifica el binario detrás de un PID mediante `/proc/PID/exe`.
7. Guarda toda la salida en `~/caso07/red_y_sesiones.txt`.

## Pistas

- `last -i` fuerza IPs numéricas; `-f` selecciona el archivo.
- `ss -tulpanep` incluye proceso, usuario e información extendida.
- `ss -tanp state established` filtra solo conexiones establecidas.
- `ls -l /proc/<PID>/exe` revela el ejecutable real de un proceso.
""",
                    "solution_markdown": """# Solución comentada

```bash
#!/bin/bash
set -e
mkdir -p ~/caso07
cd ~/caso07

REPORT=~/caso07/red_y_sesiones.txt
{
  echo "===== 1. SESIONES EXITOSAS (wtmp) ====="
  last -i -f /var/log/wtmp | head -30

  echo; echo "===== 2. INTENTOS FALLIDOS (btmp) ====="
  sudo lastb 2>/dev/null | head -30 || echo "(btmp vacío o inaccesible)"

  echo; echo "===== 3. ULTIMO ACCESO POR USUARIO (lastlog) ====="
  lastlog

  echo; echo "===== 4. PUERTOS EN ESCUCHA ====="
  ss -tulpanep

  echo; echo "===== 5. CONEXIONES ESTABLECIDAS (posible C2) ====="
  ss -tanp state established

  echo; echo "===== 6. RESOLVER PID -> BINARIO ====="
  # Para cada PID con socket, mostrar su ejecutable real
  for pid in $(ss -tanp state established 2>/dev/null | grep -oE 'pid=[0-9]+' | cut -d= -f2 | sort -u); do
    echo "PID $pid -> $(sudo ls -l /proc/$pid/exe 2>/dev/null | awk '{print $NF}')"
  done
} | tee "$REPORT"
```

## Explicación paso a paso

1. **`last -i -f /var/log/wtmp`**: lee el archivo binario `wtmp` y muestra las sesiones exitosas (login/logout) con IPs numéricas gracias a `-i`. Aquí se ve desde qué direcciones se ha conectado cada usuario y cuánto duró cada sesión. Una sesión desde una IP externa a una hora inusual es sospechosa.
2. **`lastb`** (requiere root): lee `btmp`, el registro de **intentos fallidos**. Un torrente de fallos confirma la fuerza bruta vista en `auth.log`, aportando una segunda fuente independiente.
3. **`lastlog`**: presenta el último acceso de cada cuenta del sistema. Cuentas de servicio (como `backup` o `www-data`) que normalmente nunca inician sesión pero muestran un login reciente son una señal clara de abuso.
4. **`ss -tulpanep`**: enumera todos los sockets en escucha (`-l`), TCP (`-t`) y UDP (`-u`), con números (`-n`), PID/proceso (`-p`), extendida (`-e`) y usuario. Un puerto en escucha no habitual (por ejemplo un shell en el 4444) delata un backdoor.
5. **`ss -tanp state established`**: filtra las conexiones **establecidas**. Una conexión saliente persistente hacia una IP externa desconocida es el patrón típico de un canal de **mando y control (C2)**.
6. **`/proc/PID/exe`**: para cada PID con conexión, `ls -l /proc/PID/exe` revela la ruta real del binario en ejecución. Si apunta a `/tmp`, a un nombre borrado (`(deleted)`) o a una ruta sospechosa, hemos localizado el proceso malicioso.

La potencia del método está en **triangular**: `wtmp`/`btmp`/`lastlog` sitúan las sesiones, `ss` muestra la actividad de red viva y `/proc` conecta esa actividad con un binario concreto del disco, cerrando el círculo entre acceso, red y ejecución.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 5: Logs y Red",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Qué herramienta lee el archivo binario /var/log/btmp?",
                            [
                                ("lastb", True),
                                ("cat", False),
                                ("journalctl", False),
                                ("lastlog", False),
                            ],
                        ),
                        (
                            "En auth.log, ¿qué patrón indica una fuerza bruta SSH que tuvo éxito?",
                            [
                                ("Muchos 'Failed password' desde una IP seguidos de un 'Accepted' desde esa misma IP", True),
                                ("Un único 'Accepted password' sin ningún fallo previo", False),
                                ("Numerosas líneas 'session opened' de cron", False),
                                ("La ausencia total de líneas con la palabra sshd", False),
                            ],
                        ),
                        (
                            "Una conexión TCP saliente persistente hacia una IP externa desconocida sugiere...",
                            [
                                ("Un posible canal de mando y control (C2) del atacante", True),
                                ("Una actualización rutinaria del kernel", False),
                                ("Que el firewall está funcionando correctamente", False),
                                ("Un fallo del servidor DNS local", False),
                            ],
                        ),
                        (
                            "¿Para qué sirve inspeccionar /proc/<PID>/exe durante el análisis de red?",
                            [
                                ("Para identificar el binario real que respalda un proceso con conexiones sospechosas", True),
                                ("Para reiniciar el proceso de forma segura", False),
                                ("Para cambiar el puerto de escucha del proceso", False),
                                ("Para borrar los logs asociados al proceso", False),
                            ],
                        ),
                    ],
                },
            ],
        },
        # ==================== MÓDULO 6 ====================
        {
            "name": "Módulo 6: Detección de Malware y Rootkits + Capstone",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: Procesos ocultos, /proc, SUID sospechosos y rootkits",
                    "markdown": """# Procesos ocultos, /proc, SUID sospechosos y rootkits

El último eslabón del triage es cazar el propio malware: procesos ocultos, binarios con privilegios abusivos y *rootkits* que manipulan el sistema para esconderse.

## El pseudo-sistema /proc

`/proc` expone el estado del kernel y de cada proceso. Es una fuente forense de primer nivel porque muchas herramientas de usuario mienten, pero el kernel sabe la verdad:

```bash
# Directorio de cada proceso
ls /proc/<PID>/

# Ejecutable real (aunque se haya borrado del disco)
ls -l /proc/<PID>/exe

# Línea de comandos y entorno
tr '\\0' ' ' < /proc/<PID>/cmdline; echo
cat /proc/<PID>/environ | tr '\\0' '\\n'

# Archivos abiertos por el proceso
ls -l /proc/<PID>/fd/
```

Un caso clásico: un binario borrado del disco pero aún en ejecución aparece como `/proc/PID/exe -> /tmp/x (deleted)`. Es malware que se autoeliminó para no dejar rastro en el disco.

## Detectar procesos ocultos

Un rootkit puede alterar `ps` para ocultar sus procesos. Se detecta **comparando** la lista de `ps` con la verdad del kernel en `/proc`:

```bash
# PIDs según ps
ps -eo pid --no-headers | sort -n > /tmp/ps.txt

# PIDs reales según el kernel
ls /proc | grep -E '^[0-9]+$' | sort -n > /tmp/proc.txt

# Diferencia: un PID en /proc que ps NO muestra es sospechoso
comm -13 /tmp/ps.txt /tmp/proc.txt
```

## Binarios SUID/SGID sospechosos

Los binarios con bit **SUID** ejecutan con los privilegios de su dueño (a menudo root). Un atacante puede plantar una copia SUID de `bash` para escalar:

```bash
# Todos los SUID del sistema
find / -xdev -type f -perm -4000 -exec ls -l {} \\; 2>/dev/null

# SGID
find / -xdev -type f -perm -2000 2>/dev/null
```

| Indicador | Ejemplo | Por qué alarma |
|-----------|---------|----------------|
| SUID en ruta rara | `/tmp/sh` con SUID root | ninguna razón legítima |
| SUID reciente | ctime dentro del incidente | plantado por el atacante |
| Copia SUID de shell | `/usr/bin/.bash` SUID root | escalada evidente |

Compara la lista de SUID con una **línea base** conocida de una instalación limpia de Debian: cualquier extra merece investigación.

## Indicadores de rootkit

- Discrepancias entre `ps`/`/proc`, `ss`/`/proc/net`, `ls`/inodos.
- `/etc/ld.so.preload` con librerías desconocidas (rootkits de userland como Azazel).
- Módulos del kernel no firmados o no listados: `lsmod` vs `/proc/modules`.
- Herramientas como **chkrootkit** y **rkhunter** automatizan parte de la búsqueda:

```bash
sudo rkhunter --check --sk
sudo chkrootkit
```

## Metodología final

El triage de malware combina todo lo anterior: procesos y red (`/proc`, `ss`), archivos y tiempos (SUID, timeline, ctime), persistencia (cron, systemd) y logs. Ningún indicador aislado es concluyente; la **correlación** entre varias fuentes construye la certeza.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 08: Cazar binarios SUID y procesos con binario borrado",
                    "markdown": """# Lab 08: Cazar binarios SUID y procesos con binario borrado

Practicarás dos técnicas de detección de malware: localizar binarios SUID sospechosos y encontrar procesos cuyo ejecutable ha sido borrado del disco.

## Objetivos

- Enumerar SUID y compararlos con una línea base.
- Detectar una copia SUID sospechosa.
- Identificar un proceso en ejecución cuyo binario fue borrado.

## Instrucciones

1. Conéctate a **linuxbox** y crea `~/caso08`.
2. Simula al atacante:
   - Crea una copia SUID root de `bash` en una ruta sospechosa (con sudo).
   - Lanza en segundo plano un proceso desde un binario en `/tmp` y luego borra ese binario del disco (el proceso sigue vivo).
3. Como investigador:
   - Enumera todos los SUID del sistema y destaca el sospechoso.
   - Recorre `/proc/*/exe` para encontrar procesos cuyo ejecutable aparezca como `(deleted)`.
   - Para el proceso encontrado, muestra su cmdline y su binario real.
4. Limpia (mata el proceso, elimina el SUID) y guarda los hallazgos en `~/caso08/malware.txt`.

## Pistas

- `chmod u+s` activa el bit SUID.
- `find / -perm -4000` localiza SUID.
- Un proceso con binario borrado se ve en `ls -l /proc/PID/exe` como `... (deleted)`.
""",
                    "solution_markdown": """# Solución comentada

```bash
#!/bin/bash
set -e
mkdir -p ~/caso08
cd ~/caso08

# ---- 2. Simular al atacante ----
# a) Copia SUID root de bash en ruta sospechosa
sudo cp /bin/bash /tmp/.hidden_sh
sudo chown root:root /tmp/.hidden_sh
sudo chmod 4755 /tmp/.hidden_sh

# b) Proceso con binario borrado
cp /bin/sleep /tmp/evil_bin
/tmp/evil_bin 600 &
EVIL_PID=$!
rm -f /tmp/evil_bin          # el binario desaparece del disco, el proceso sigue vivo

# ---- 3. Investigación ----
{
  echo "===== SUID EN EL SISTEMA ====="
  find / -xdev -type f -perm -4000 -exec ls -l {} \\; 2>/dev/null

  echo; echo "===== SUID SOSPECHOSOS (fuera de rutas estándar) ====="
  find / -xdev -type f -perm -4000 2>/dev/null | grep -vE '^/(usr/bin|usr/sbin|bin|sbin|usr/lib)'

  echo; echo "===== PROCESOS CON BINARIO BORRADO ====="
  for p in /proc/[0-9]*; do
    exe=$(sudo readlink "$p/exe" 2>/dev/null || true)
    case "$exe" in
      *"(deleted)"*)
        pid=${p#/proc/}
        echo "PID $pid -> $exe"
        echo "  cmdline: $(sudo tr '\\0' ' ' < $p/cmdline 2>/dev/null)"
        ;;
    esac
  done
} | tee ~/caso08/malware.txt

# ---- 4. Limpieza ----
kill "$EVIL_PID" 2>/dev/null || true
sudo rm -f /tmp/.hidden_sh
```

## Explicación paso a paso

1. **Copia SUID root**: `cp /bin/bash /tmp/.hidden_sh` seguido de `chmod 4755` (el `4` es el bit SUID) crea un shell que, al ejecutarse, otorga privilegios de root. El nombre con punto (`.hidden_sh`) y la ubicación en `/tmp` son señales inequívocas de malware: ningún paquete legítimo coloca binarios SUID ahí.
2. **Proceso con binario borrado**: copiamos `sleep` a `/tmp/evil_bin`, lo ejecutamos en segundo plano y **borramos** el archivo. El proceso sigue vivo en memoria porque el kernel mantiene el inodo abierto; esta es una táctica real de malware que se autoelimina del disco para evadir análisis estático.
3. **Enumeración de SUID**: `find / -xdev -type f -perm -4000` lista todos los binarios SUID. Al filtrar con `grep -vE` las rutas estándar (`/usr/bin`, `/bin`, etc.), aislamos los que están fuera de sitio: aparece `/tmp/.hidden_sh`, el implante del atacante. En un caso real se compara contra una **línea base** de Debian limpio.
4. **Detección del binario borrado**: recorremos `/proc/[0-9]*/exe` con `readlink`; cuando el destino contiene `(deleted)`, hemos encontrado un proceso cuyo ejecutable ya no está en disco. Mostramos su `cmdline` para identificarlo. Este es uno de los hallazgos más valiosos: el proceso está vivo pero no hay archivo que analizar, salvo dumpeándolo desde `/proc/PID/exe`.
5. **Recuperación del binario**: aunque no lo hagamos aquí, se podría recuperar copiando `/proc/PID/exe` a un archivo, ya que el enlace sigue apuntando al inodo en memoria.
6. **Limpieza**: matamos el proceso y eliminamos el SUID para dejar el laboratorio en estado limpio.

La lección clave es que el disco puede mentir (archivo borrado) pero `/proc` y el kernel conservan la verdad del proceso en ejecución.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 09 (Capstone): Triage forense completo de linuxbox",
                    "markdown": """# Lab 09 (Capstone): Triage forense completo de linuxbox

Este es el laboratorio final. Integrarás todo lo aprendido en un **triage forense completo**: un único guion que recolecta evidencia volátil, persistencia, red, SUID, procesos ocultos y logs, produciendo un informe estructurado con integridad garantizada.

## Escenario

Se sospecha que **linuxbox** ha sido comprometida. Como analista DFIR, debes realizar un triage inicial rápido y defendible que capture los principales indicadores de compromiso (IoC) sin alterar la evidencia más de lo imprescindible, y entregar un informe con su hash.

## Objetivos

- Recolectar en un solo informe: estado volátil, red, persistencia, SUID, procesos ocultos y logs de autenticación.
- Respetar el orden de volatilidad.
- Sellar el informe con un hash SHA-256 para la cadena de custodia.

## Instrucciones

1. Conéctate a **linuxbox** y crea la carpeta del caso `~/capstone`.
2. Escribe un script `triage.sh` que recopile, en este orden:
   - Metadatos del sistema (fecha, hostname, uptime, kernel).
   - Estado volátil: procesos (`ps aux`), usuarios conectados (`who`), sesiones (`last`).
   - Red: puertos en escucha y conexiones establecidas (`ss`).
   - Procesos ocultos: comparación `ps` vs `/proc`.
   - Procesos con binario borrado (`/proc/*/exe` -> `(deleted)`).
   - Persistencia: cron de usuario y sistema, servicios/timers systemd, authorized_keys.
   - SUID fuera de rutas estándar.
   - Logs: top de IPs con `Failed password` y logins `Accepted`.
3. Vuelca todo a un archivo con marca temporal, calcula su SHA-256 y guarda el hash.
4. Redacta al final un breve resumen de los IoC que consideres más relevantes.

## Pistas

- Usa `comm -13` para la diferencia entre PIDs de `ps` y de `/proc`.
- Antepón cabeceras claras a cada sección para que el informe sea legible.
- Sella la integridad con `sha256sum informe > informe.sha256`.
""",
                    "solution_markdown": """# Solución comentada

```bash
#!/bin/bash
# triage.sh - Triage forense de linuxbox (capstone DFIR)
set -u

CASO=~/capstone
mkdir -p "$CASO"
STAMP=$(date +%Y%m%d_%H%M%S)
OUT="$CASO/triage_${STAMP}.txt"

section(){ echo; echo "############ $1 ############"; }

{
  section "0. METADATOS DEL SISTEMA"
  date; echo "Hostname: $(hostname)"; uptime; uname -a

  section "1. ESTADO VOLATIL (orden de volatilidad)"
  echo "--- Procesos ---";           ps auxww
  echo "--- Usuarios conectados ---"; who
  echo "--- Sesiones (wtmp) ---";     last -i | head -20

  section "2. RED"
  echo "--- Puertos en escucha ---";      ss -tulpanep
  echo "--- Conexiones establecidas ---"; ss -tanp state established

  section "3. PROCESOS OCULTOS (ps vs /proc)"
  ps -eo pid --no-headers | tr -d ' ' | sort -n > /tmp/_ps.$$
  ls /proc | grep -E '^[0-9]+$' | sort -n     > /tmp/_proc.$$
  DIF=$(comm -13 /tmp/_ps.$$ /tmp/_proc.$$)
  if [ -n "$DIF" ]; then echo "SOSPECHOSO: PIDs en /proc no listados por ps:"; echo "$DIF"
  else echo "Sin discrepancias ps/proc."; fi
  rm -f /tmp/_ps.$$ /tmp/_proc.$$

  section "4. PROCESOS CON BINARIO BORRADO"
  for p in /proc/[0-9]*; do
    exe=$(sudo readlink "$p/exe" 2>/dev/null || true)
    case "$exe" in *"(deleted)"*) echo "PID ${p#/proc/} -> $exe";; esac
  done

  section "5. PERSISTENCIA - CRON"
  for u in $(cut -f1 -d: /etc/passwd); do
    c=$(crontab -l -u "$u" 2>/dev/null) && [ -n "$c" ] && echo "-- $u --" && echo "$c"
  done
  grep -RhH "" /etc/cron.d/ /etc/crontab 2>/dev/null

  section "6. PERSISTENCIA - SYSTEMD"
  systemctl list-unit-files --state=enabled --no-pager 2>/dev/null
  systemctl list-timers --all --no-pager 2>/dev/null

  section "7. PERSISTENCIA - CLAVES SSH"
  find / -name authorized_keys 2>/dev/null | while read -r f; do
    echo "-- $(stat -c '%y' "$f") $f --"; cat "$f"
  done

  section "8. SUID FUERA DE RUTAS ESTANDAR"
  find / -xdev -type f -perm -4000 2>/dev/null \
    | grep -vE '^/(usr/bin|usr/sbin|bin|sbin|usr/lib)'

  section "9. LOGS DE AUTENTICACION"
  echo "--- Top IPs con Failed password ---"
  grep "Failed password" /var/log/auth.log 2>/dev/null \
    | grep -oE "([0-9]+\\.){3}[0-9]+" | sort | uniq -c | sort -rn | head
  echo "--- Logins aceptados ---"
  grep "Accepted" /var/log/auth.log 2>/dev/null
} > "$OUT" 2>&1

# Sellar integridad
sha256sum "$OUT" > "$OUT.sha256"
echo "Informe: $OUT"
echo "Hash:    $(cat "$OUT.sha256")"
```

## Explicación paso a paso

1. **Estructura y marca temporal**: cada ejecución produce `triage_AAAAMMDD_HHMMSS.txt`, de modo que múltiples pasadas no se sobrescriben y quedan fechadas para la cadena de custodia. La función `section` da cabeceras legibles.
2. **Orden de volatilidad**: el script recolecta primero lo efímero (procesos, sesiones, red) antes que lo estático (archivos, logs), respetando el RFC 3227.
3. **Procesos ocultos (sección 3)**: comparamos los PIDs que reporta `ps` con los directorios numéricos reales de `/proc`. `comm -13` muestra los PIDs presentes en `/proc` pero **ausentes** en `ps`: si aparece alguno, es un fortísimo indicador de rootkit que manipula `ps`.
4. **Binario borrado (sección 4)**: `readlink /proc/*/exe` detecta procesos cuyo ejecutable ya no existe en disco (`(deleted)`), táctica típica de malware residente en memoria.
5. **Persistencia (secciones 5-7)**: cubrimos los tres vectores principales -cron (usuario y sistema), unidades/timers systemd y `authorized_keys`- mostrando además el mtime de las claves para correlacionar con la ventana del incidente.
6. **SUID anómalos (sección 8)**: listamos binarios SUID fuera de las rutas del sistema, donde se esconden las puertas traseras de escalada de privilegios.
7. **Logs (sección 9)**: resumimos la fuerza bruta (top de IPs) y los accesos exitosos, enlazando el ataque de red con el compromiso.
8. **Sellado de integridad**: `sha256sum` genera el hash del informe, garantizando que el artefacto entregado no se altera después. Este hash entra en la documentación del caso.

Este capstone es una plantilla de triage real: en un incidente se ejecutaría en los primeros minutos para obtener una foto integral de indicadores de compromiso, priorizar la respuesta y decidir si procede una adquisición forense completa (imagen de disco y memoria) de las vistas en los módulos anteriores. La fortaleza del método reside en la **correlación**: cada sección aislada da pistas, pero juntas y cruzadas por tiempo reconstruyen la historia completa del ataque.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 6: Malware, Rootkits y Capstone",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Cómo se detecta típicamente un proceso ocultado por un rootkit que manipula 'ps'?",
                            [
                                ("Comparando los PIDs de 'ps' con los directorios numéricos reales en /proc", True),
                                ("Reiniciando el sistema y volviendo a ejecutar 'ps'", False),
                                ("Contando las líneas del archivo /etc/passwd", False),
                                ("Ejecutando 'ps' dos veces seguidas y comparando", False),
                            ],
                        ),
                        (
                            "En 'ls -l /proc/1234/exe' el destino aparece como '/tmp/x (deleted)'. ¿Qué significa?",
                            [
                                ("El proceso sigue en ejecución aunque su binario fue borrado del disco", True),
                                ("El proceso ha terminado y su PID es inválido", False),
                                ("El binario está cifrado por el kernel", False),
                                ("El proceso pertenece al usuario root necesariamente", False),
                            ],
                        ),
                        (
                            "¿Por qué alarma encontrar '/tmp/.hidden_sh' con permisos 4755 propiedad de root?",
                            [
                                ("Es una copia SUID de un shell que permite escalar a root; nada legítimo la justifica", True),
                                ("Porque los archivos en /tmp no pueden tener dueño root", False),
                                ("Porque 4755 elimina los permisos de lectura del archivo", False),
                                ("Porque indica que el disco está lleno", False),
                            ],
                        ),
                        (
                            "¿Cuál es el principio metodológico central del triage forense completo (capstone)?",
                            [
                                ("Correlacionar múltiples fuentes (procesos, red, archivos, persistencia, logs) para reconstruir el ataque", True),
                                ("Confiar en un único indicador definitivo como el uso de CPU", False),
                                ("Borrar los artefactos sospechosos en cuanto se encuentran", False),
                                ("Analizar exclusivamente el archivo /var/log/syslog", False),
                            ],
                        ),
                    ],
                },
            ],
        },
    ],
}
