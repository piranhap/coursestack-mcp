COURSE = {
    "title": "Administración de Linux",
    "subtitle": "Administra sistemas Linux con confianza",
    "lab_system": {
        "name": "linuxbox",
        "image_id": "428356ac-de2b-4618-8f1a-f34d7b55001f",
        "size": "micro",
    },
    "modules": [
        # =====================================================================
        # MÓDULO 1
        # =====================================================================
        {
            "name": "Módulo 1: Fundamentos del Sistema",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Bienvenida al curso",
                    "markdown": """# Bienvenida a Administración de Linux

Te damos la bienvenida a este curso práctico. Aquí aprenderás a administrar
sistemas Linux con confianza, trabajando sobre un servidor **Debian 12**
real llamado `linuxbox`.

## ¿Qué vas a aprender?

- La estructura del sistema de archivos (FHS) y el proceso de arranque.
- Gestión de usuarios, grupos y permisos, incluyendo ACLs.
- Control de procesos y servicios con `systemd`.
- Administración de almacenamiento y sistemas de archivos.
- Configuración de red, firewall y SSH.
- Automatización con `cron`, temporizadores de systemd y respaldos.

## Cómo funciona el curso

Cada módulo incluye tres partes:

| Parte | Descripción |
|-------|-------------|
| Conceptos | Teoría concisa con ejemplos de comandos. |
| Lab | Ejercicio práctico sobre `linuxbox`. |
| Quiz | Cuatro preguntas para consolidar lo aprendido. |

En los labs escribirás comandos reales. Cada lab incluye una solución
comentada, pero te recomendamos intentarlo por tu cuenta primero.

## Una nota sobre privilegios

Muchas tareas de administración requieren privilegios de superusuario.
Usarás `sudo` para ejecutarlas:

```bash
sudo whoami
# root
```

¡Empecemos!
""",
                },
                {
                    "kind": "text",
                    "name": "Conceptos: FHS, arranque, shell y ayuda",
                    "markdown": """# Fundamentos del Sistema

## Jerarquía de directorios (FHS)

El *Filesystem Hierarchy Standard* define para qué sirve cada directorio.
Todo cuelga de la raíz `/`.

| Directorio | Propósito |
|-----------|-----------|
| `/bin`, `/usr/bin` | Programas ejecutables esenciales. |
| `/etc` | Archivos de configuración del sistema. |
| `/home` | Directorios personales de los usuarios. |
| `/var` | Datos variables: logs, colas, caché. |
| `/tmp` | Archivos temporales. |
| `/root` | Directorio personal del superusuario. |
| `/proc`, `/sys` | Sistemas de archivos virtuales del kernel. |
| `/dev` | Archivos de dispositivo. |

```bash
ls -l /
cat /etc/os-release   # Identifica la distribución
```

## Proceso de arranque

En Debian 12 la secuencia es, a grandes rasgos:

1. **Firmware (BIOS/UEFI)** ejecuta el gestor de arranque.
2. **GRUB** carga el kernel de Linux y el `initramfs`.
3. El **kernel** monta la raíz e inicia `systemd` (PID 1).
4. **systemd** activa objetivos (*targets*) y servicios.

```bash
systemctl get-default          # Objetivo por defecto
systemd-analyze                # Tiempo de arranque
systemd-analyze blame          # Servicios más lentos
```

## El shell

El shell interpreta tus comandos. En Debian el predeterminado es **Bash**.

```bash
echo $SHELL       # Shell actual
pwd               # Directorio de trabajo
echo $PATH        # Rutas donde se buscan programas
history           # Comandos recientes
```

## Obtener ayuda

Nunca memorices todo: aprende a consultar la documentación.

```bash
man ls            # Manual completo de un comando
ls --help         # Ayuda rápida
apropos network   # Busca páginas de manual por palabra clave
type cd           # ¿Es builtin, alias o programa?
```

Las páginas de `man` se organizan por secciones (1 comandos, 5 formatos de
archivo, 8 administración). Por ejemplo, `man 5 passwd` documenta el
formato del archivo, no el comando.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 01: Explora el sistema",
                    "markdown": """# Lab 01: Explora el sistema

Vas a familiarizarte con `linuxbox` y su estructura.

## Objetivos

1. Identifica la versión de Debian instalada.
2. Muestra el objetivo (target) de arranque por defecto.
3. Encuentra los tres servicios que más tardaron en arrancar.
4. Lee la sección 5 de la página de manual de `passwd`.
5. Crea un archivo `~/notas.txt` con la ruta de tu directorio personal.

## Pistas

- El archivo `/etc/os-release` contiene la versión de la distribución.
- `systemd-analyze` tiene un subcomando para culpar a los servicios lentos.
- Recuerda que `man` acepta un número de sección.

Cuando termines, compara con la solución.
""",
                    "solution_markdown": """# Solución comentada

```bash
# 1. Versión de Debian
cat /etc/os-release
lsb_release -d 2>/dev/null || grep PRETTY_NAME /etc/os-release

# 2. Objetivo de arranque por defecto
systemctl get-default

# 3. Servicios más lentos (los tres primeros)
systemd-analyze blame | head -n 3

# 4. Sección 5 del manual de passwd (formato del archivo)
man 5 passwd

# 5. Guardar la ruta del HOME en un archivo de notas
echo "$HOME" > ~/notas.txt
cat ~/notas.txt
```

## Explicación paso a paso

1. `/etc/os-release` es el estándar moderno para identificar la
   distribución. `PRETTY_NAME` muestra algo como *Debian GNU/Linux 12
   (bookworm)*.
2. `systemctl get-default` normalmente devuelve `graphical.target` o
   `multi-user.target` (típico en servidores sin escritorio).
3. `systemd-analyze blame` ordena los servicios por el tiempo que tardaron
   en inicializarse; `head -n 3` recorta a los tres primeros.
4. `man 5 passwd` abre la página de la **sección 5**, que describe el
   *formato* del archivo `/etc/passwd`, distinta de `man 1 passwd` (el
   comando para cambiar contraseñas).
5. `$HOME` es una variable de entorno que contiene tu directorio personal,
   habitualmente `/home/usuario` o `/root`. La redirección `>` crea o
   sobrescribe el archivo.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 1: Fundamentos",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Qué directorio del FHS contiene los archivos de configuración del sistema?",
                            [
                                ("/etc", True),
                                ("/var", False),
                                ("/bin", False),
                                ("/proc", False),
                            ],
                        ),
                        (
                            "¿Cuál es el primer proceso (PID 1) que inicia el kernel en Debian 12?",
                            [
                                ("systemd", True),
                                ("bash", False),
                                ("grub", False),
                                ("init.d", False),
                            ],
                        ),
                        (
                            "¿Qué comando muestra el formato del archivo /etc/passwd en lugar del comando passwd?",
                            [
                                ("man 5 passwd", True),
                                ("man 1 passwd", False),
                                ("passwd --help", False),
                                ("apropos passwd", False),
                            ],
                        ),
                        (
                            "¿Qué variable de entorno indica las rutas donde el shell busca programas?",
                            [
                                ("PATH", True),
                                ("HOME", False),
                                ("SHELL", False),
                                ("PWD", False),
                            ],
                        ),
                    ],
                },
            ],
        },
        # =====================================================================
        # MÓDULO 2
        # =====================================================================
        {
            "name": "Módulo 2: Usuarios, Grupos y Permisos",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: usuarios, grupos, permisos y ACLs",
                    "markdown": """# Usuarios, Grupos y Permisos

## Usuarios y grupos

Cada usuario tiene un UID y pertenece a uno o varios grupos (GID).

```bash
sudo useradd -m -s /bin/bash ana    # Crea usuario con HOME y shell
sudo passwd ana                      # Asigna contraseña
sudo usermod -aG sudo ana            # Añade al grupo sudo (¡con -aG!)
id ana                               # Muestra UID, GID y grupos
sudo userdel -r ana                  # Elimina usuario y su HOME
```

Importante: usa siempre `-aG` (append) al añadir grupos suplementarios.
Sin la `a`, `-G` reemplaza todos los grupos suplementarios del usuario.

## /etc/passwd y /etc/shadow

| Archivo | Contenido |
|---------|-----------|
| `/etc/passwd` | Usuario, UID, GID, HOME, shell (legible por todos). |
| `/etc/shadow` | Hashes de contraseñas y caducidad (solo root). |
| `/etc/group` | Definición de grupos. |

Una línea de `/etc/passwd` tiene el formato:
`ana:x:1001:1001:Ana:/home/ana:/bin/bash`. La `x` indica que la contraseña
está en `/etc/shadow`.

## Permisos tradicionales

Cada archivo tiene permisos para **usuario (u)**, **grupo (g)** y
**otros (o)**: lectura (r=4), escritura (w=2), ejecución (x=1).

```bash
ls -l archivo.sh                # -rwxr-xr--
chmod 750 archivo.sh            # rwx r-x ---
chmod u+x script.sh            # Añade ejecución al dueño
chown ana:ana archivo.sh       # Cambia dueño y grupo
```

| Octal | Símbolo | Significado |
|-------|---------|-------------|
| 7 | rwx | Leer, escribir, ejecutar |
| 5 | r-x | Leer y ejecutar |
| 4 | r-- | Solo lectura |
| 0 | --- | Sin permisos |

## sudo

`sudo` ejecuta comandos como otro usuario (root por defecto). Su
configuración vive en `/etc/sudoers` y `/etc/sudoers.d/`; edítala siempre
con `visudo` para evitar errores de sintaxis.

```bash
sudo -l           # Qué puedo ejecutar con sudo
sudo visudo       # Editar configuración de forma segura
```

## ACLs

Cuando los permisos u/g/o no bastan, las ACLs otorgan permisos a usuarios
o grupos concretos.

```bash
setfacl -m u:ana:rw archivo.txt   # Da rw a ana
getfacl archivo.txt               # Ver ACLs
setfacl -x u:ana archivo.txt      # Quita la ACL de ana
```

Un `+` al final de `ls -l` (por ejemplo `-rw-r--r--+`) indica que el
archivo tiene ACLs extendidas.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 02: Crea un usuario y ajusta permisos",
                    "markdown": """# Lab 02: Crea un usuario y ajusta permisos

## Objetivos

1. Crea un usuario `devops` con su directorio personal y shell Bash.
2. Añádelo al grupo `sudo` sin borrar sus otros grupos.
3. Crea el directorio `/srv/proyecto` y hazlo propiedad de `devops`.
4. Aplica permisos `750` a `/srv/proyecto`.
5. Concede a `devops` permiso de lectura sobre `/etc/hostname` usando una
   ACL, y verifícalo.

## Pistas

- Recuerda el flag correcto de `usermod` para *añadir* a un grupo.
- `chown` acepta `usuario:grupo`.
- Las ACLs se gestionan con `setfacl` y se consultan con `getfacl`.
""",
                    "solution_markdown": """# Solución comentada

```bash
# 1. Crear el usuario con HOME y shell
sudo useradd -m -s /bin/bash devops

# 2. Añadirlo al grupo sudo sin perder otros grupos
sudo usermod -aG sudo devops
id devops

# 3. Crear el directorio y asignar propietario
sudo mkdir -p /srv/proyecto
sudo chown devops:devops /srv/proyecto

# 4. Permisos 750 (rwx para dueño, r-x para grupo, nada para otros)
sudo chmod 750 /srv/proyecto
ls -ld /srv/proyecto

# 5. ACL de lectura sobre /etc/hostname y verificación
sudo setfacl -m u:devops:r /etc/hostname
getfacl /etc/hostname
```

## Explicación paso a paso

1. `useradd -m` crea el directorio `/home/devops`; `-s /bin/bash` fija el
   shell de inicio de sesión.
2. `usermod -aG sudo` **añade** (`a`) el grupo suplementario `sudo`. Sin la
   `a`, reemplazarías todos los grupos suplementarios del usuario. `id`
   confirma la pertenencia.
3. `mkdir -p` crea el árbol de directorios; `chown devops:devops` transfiere
   la propiedad al nuevo usuario y su grupo primario.
4. `chmod 750` se traduce en `rwxr-x---`: control total para el dueño,
   lectura/ejecución para el grupo y nada para el resto. `ls -ld` muestra
   los permisos del directorio sin listar su contenido.
5. `setfacl -m u:devops:r` añade una ACL que da lectura a `devops` sobre
   `/etc/hostname`. `getfacl` lista las entradas; verás una línea
   `user:devops:r--`. En `ls -l` el archivo aparecerá con un `+` final.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 2: Usuarios y Permisos",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Qué opción de usermod añade un grupo suplementario sin eliminar los existentes?",
                            [
                                ("-aG", True),
                                ("-G", False),
                                ("-g", False),
                                ("-d", False),
                            ],
                        ),
                        (
                            "¿Dónde se almacenan los hashes de las contraseñas en Debian 12?",
                            [
                                ("/etc/shadow", True),
                                ("/etc/passwd", False),
                                ("/etc/group", False),
                                ("/etc/sudoers", False),
                            ],
                        ),
                        (
                            "¿Qué representa el permiso octal 750 en un directorio?",
                            [
                                ("rwx para el dueño, r-x para el grupo, nada para otros", True),
                                ("rwx para todos", False),
                                ("r-x para el dueño y el grupo", False),
                                ("rw- para dueño, grupo y otros", False),
                            ],
                        ),
                        (
                            "¿Qué comando concede a un usuario concreto un permiso adicional mediante ACL?",
                            [
                                ("setfacl -m u:usuario:rw archivo", True),
                                ("chmod u+rw archivo", False),
                                ("chown usuario archivo", False),
                                ("getfacl archivo", False),
                            ],
                        ),
                    ],
                },
            ],
        },
        # =====================================================================
        # MÓDULO 3
        # =====================================================================
        {
            "name": "Módulo 3: Procesos y Servicios",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: procesos, señales y systemd",
                    "markdown": """# Procesos y Servicios

## Observar procesos

Un proceso es un programa en ejecución identificado por su PID.

```bash
ps aux                 # Todos los procesos, formato BSD
ps -ef                 # Todos los procesos, formato System V
top                    # Monitor interactivo en tiempo real
htop                   # Alternativa más amigable (si está instalada)
pgrep -a sshd          # Busca procesos por nombre
```

En `top`, las teclas útiles son: `P` (ordenar por CPU), `M` (por memoria),
`k` (enviar señal) y `q` (salir).

## Señales y kill

Las señales comunican eventos a los procesos.

| Señal | Número | Efecto |
|-------|--------|--------|
| SIGTERM | 15 | Terminación ordenada (por defecto). |
| SIGKILL | 9 | Terminación forzada, no ignorable. |
| SIGHUP | 1 | Recargar configuración. |
| SIGSTOP | 19 | Pausar el proceso. |

```bash
kill 1234              # Envía SIGTERM al PID 1234
kill -9 1234           # SIGKILL (último recurso)
kill -HUP 1234         # Recargar configuración
pkill nginx            # Por nombre
killall firefox        # Todos los procesos con ese nombre
```

Prefiere siempre SIGTERM antes que SIGKILL: da al proceso la oportunidad de
cerrar archivos y liberar recursos limpiamente.

## systemd y systemctl

`systemd` gestiona servicios (unidades `.service`), objetivos y más.

```bash
systemctl status ssh           # Estado de un servicio
sudo systemctl start ssh       # Iniciar
sudo systemctl stop ssh        # Detener
sudo systemctl restart ssh     # Reiniciar
sudo systemctl reload ssh      # Recargar configuración
sudo systemctl enable ssh      # Arrancar en el arranque
sudo systemctl disable ssh     # No arrancar en el arranque
systemctl is-active ssh        # ¿Está activo?
systemctl list-units --type=service
```

La diferencia clave: `start/stop` afectan al estado actual; `enable/disable`
afectan a si el servicio arranca automáticamente al iniciar el sistema.

## journalctl

Los logs de systemd se consultan con `journalctl`.

```bash
journalctl -u ssh              # Logs de un servicio
journalctl -u ssh -f           # Seguir en tiempo real
journalctl -b                  # Desde el último arranque
journalctl -p err              # Solo errores
journalctl --since "10 min ago"
```
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 03: Gestiona un servicio systemd",
                    "markdown": """# Lab 03: Gestiona un servicio systemd

Trabajarás con el servicio de tu elección; usaremos `cron` como ejemplo.

## Objetivos

1. Muestra el estado del servicio `cron` y averigua si está activo.
2. Reinícialo y confirma que sigue activo.
3. Asegúrate de que arranca automáticamente al iniciar el sistema.
4. Consulta los últimos 20 registros del servicio en el journal.
5. Encuentra el PID del proceso `cron` y examina cómo terminarías el
   proceso de forma *ordenada* (no forzada). No es necesario matarlo.

## Pistas

- `systemctl is-active` responde con una sola palabra.
- `enable` no es lo mismo que `start`.
- `journalctl` acepta `-n` para limitar líneas.
- `pgrep` te da el PID rápidamente.
""",
                    "solution_markdown": """# Solución comentada

```bash
# 1. Estado y actividad del servicio cron
systemctl status cron
systemctl is-active cron

# 2. Reiniciar y confirmar
sudo systemctl restart cron
systemctl is-active cron

# 3. Habilitar en el arranque
sudo systemctl enable cron
systemctl is-enabled cron

# 4. Últimos 20 registros del journal
journalctl -u cron -n 20 --no-pager

# 5. Encontrar el PID y ver cómo se terminaría ordenadamente
pgrep -a cron
# Terminación ordenada (SIGTERM, señal 15). NO lo ejecutes si no quieres
# detener el servicio:
#   sudo kill <PID>
#   (equivale a  kill -TERM <PID>)
```

## Explicación paso a paso

1. `systemctl status cron` muestra estado, PID principal y últimas líneas de
   log. `is-active` devuelve `active` o `inactive`, ideal para scripts.
2. `restart` detiene y vuelve a iniciar el servicio; comprobamos de nuevo
   `is-active` para asegurarnos de que quedó `active`.
3. `enable` crea los enlaces necesarios para que el servicio arranque en el
   siguiente inicio del sistema. `is-enabled` lo confirma con `enabled`.
   Recuerda: `enable` NO inicia el servicio ahora, solo en el arranque.
4. `journalctl -u cron -n 20` limita la salida a las 20 líneas más
   recientes del servicio. `--no-pager` evita que se abra un paginador.
5. `pgrep -a cron` lista el PID y la línea de comando. La terminación
   ordenada usa SIGTERM (`kill <PID>`), que permite al proceso cerrar
   limpiamente; reservamos SIGKILL (`kill -9`) para cuando no responde.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 3: Procesos y Servicios",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Qué señal envía kill por defecto y permite una terminación ordenada?",
                            [
                                ("SIGTERM (15)", True),
                                ("SIGKILL (9)", False),
                                ("SIGHUP (1)", False),
                                ("SIGSTOP (19)", False),
                            ],
                        ),
                        (
                            "¿Qué comando hace que un servicio arranque automáticamente al iniciar el sistema?",
                            [
                                ("systemctl enable servicio", True),
                                ("systemctl start servicio", False),
                                ("systemctl status servicio", False),
                                ("systemctl reload servicio", False),
                            ],
                        ),
                        (
                            "¿Cómo consultas en tiempo real los logs de un servicio con systemd?",
                            [
                                ("journalctl -u servicio -f", True),
                                ("tail -f /var/log/servicio", False),
                                ("systemctl logs servicio", False),
                                ("dmesg -w servicio", False),
                            ],
                        ),
                        (
                            "¿Cuál es la diferencia entre start y enable en systemctl?",
                            [
                                ("start afecta al estado actual; enable afecta al arranque automático", True),
                                ("Son sinónimos exactos", False),
                                ("start habilita el arranque; enable inicia ahora", False),
                                ("enable detiene el servicio; start lo reinicia", False),
                            ],
                        ),
                    ],
                },
            ],
        },
        # =====================================================================
        # MÓDULO 4
        # =====================================================================
        {
            "name": "Módulo 4: Almacenamiento y Sistemas de Archivos",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: discos, montaje, fstab y LVM",
                    "markdown": """# Almacenamiento y Sistemas de Archivos

## Uso de espacio

```bash
df -h                  # Espacio por sistema de archivos (legible)
df -i                  # Uso de inodos
du -sh /var/log        # Tamaño total de un directorio
du -h --max-depth=1 /  # Tamaño de cada subdirectorio de /
```

`df` mide el espacio del *sistema de archivos*; `du` suma el tamaño de los
*archivos* de un directorio. A veces difieren (archivos borrados aún
abiertos por un proceso).

## Discos y particiones

```bash
lsblk                  # Árbol de discos y particiones
sudo fdisk -l          # Detalle de particiones
blkid                  # UUID y tipo de cada dispositivo
sudo fdisk /dev/sdb    # Editar particiones (interactivo)
```

Nombres típicos: `/dev/sda` (primer disco), `/dev/sda1` (primera
partición), `/dev/nvme0n1` (disco NVMe).

## Sistemas de archivos y montaje

```bash
sudo mkfs.ext4 /dev/sdb1        # Formatear como ext4
sudo mkdir /mnt/datos
sudo mount /dev/sdb1 /mnt/datos # Montar
mount | grep sdb1              # Ver montajes
sudo umount /mnt/datos         # Desmontar
```

Debian 12 usa habitualmente **ext4**. Otros: `xfs`, `btrfs`, `vfat`.

## /etc/fstab

Define los montajes persistentes. Cada línea tiene seis campos:

| Campo | Ejemplo | Significado |
|-------|---------|-------------|
| dispositivo | `UUID=abc...` | Qué montar (mejor por UUID). |
| punto de montaje | `/mnt/datos` | Dónde. |
| tipo | `ext4` | Sistema de archivos. |
| opciones | `defaults` | Opciones de montaje. |
| dump | `0` | Respaldo (obsoleto). |
| fsck | `2` | Orden de comprobación. |

```bash
blkid /dev/sdb1                # Obtén el UUID
sudo nano /etc/fstab          # Añade la línea
sudo mount -a                 # Prueba sin reiniciar
```

Usa UUID en lugar de `/dev/sdX`: los nombres de dispositivo pueden cambiar
entre arranques, pero el UUID no. Un error en `fstab` puede impedir el
arranque; valida siempre con `mount -a`.

## Nociones de LVM

*Logical Volume Manager* añade una capa flexible sobre las particiones.

- **PV** (Physical Volume): un disco o partición.
- **VG** (Volume Group): agrupa varios PV.
- **LV** (Logical Volume): volumen que formateas y montas.

```bash
sudo pvs        # Volúmenes físicos
sudo vgs        # Grupos de volúmenes
sudo lvs        # Volúmenes lógicos
```

La gran ventaja de LVM es redimensionar volúmenes en caliente y combinar
varios discos en un mismo grupo.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 04: Inspecciona el almacenamiento",
                    "markdown": """# Lab 04: Inspecciona el almacenamiento

## Objetivos

1. Muestra el espacio libre de todos los sistemas de archivos en formato
   legible.
2. Identifica qué subdirectorio de `/var` ocupa más espacio.
3. Lista los discos y particiones en forma de árbol.
4. Muestra el UUID del dispositivo montado en `/`.
5. Guarda en `~/almacenamiento.txt` la salida de `df -h`.

## Pistas

- `df` y `du` son tus herramientas de uso de espacio.
- `du --max-depth=1` resume por subdirectorio; ordénalo con `sort`.
- `lsblk` presenta un árbol claro.
- `findmnt` o `blkid` te ayudan con el UUID de la raíz.
""",
                    "solution_markdown": """# Solución comentada

```bash
# 1. Espacio libre legible
df -h

# 2. Subdirectorio de /var más grande
sudo du -h --max-depth=1 /var 2>/dev/null | sort -rh | head

# 3. Árbol de discos y particiones
lsblk

# 4. UUID del dispositivo montado en /
findmnt -no SOURCE /            # Muestra el dispositivo de la raíz
sudo blkid $(findmnt -no SOURCE /)

# 5. Guardar la salida de df -h
df -h > ~/almacenamiento.txt
cat ~/almacenamiento.txt
```

## Explicación paso a paso

1. `df -h` lista cada sistema de archivos con tamaño, usado, disponible y
   punto de montaje en unidades legibles (`-h` = human readable).
2. `du -h --max-depth=1 /var` suma el tamaño de cada subdirectorio directo
   de `/var`. `sort -rh` ordena de mayor a menor respetando las unidades y
   `head` muestra los primeros. Usamos `sudo` porque algunos directorios
   (como `/var/log`) no son legibles por todos.
3. `lsblk` dibuja un árbol con discos (`disk`) y sus particiones (`part`),
   incluyendo tamaño y punto de montaje.
4. `findmnt -no SOURCE /` devuelve el dispositivo de la raíz (por ejemplo
   `/dev/sda1`). Pasarlo a `blkid` revela su UUID, el identificador estable
   que deberías usar en `/etc/fstab`.
5. La redirección `>` guarda la tabla de `df -h` en un archivo de texto para
   revisarla o adjuntarla a un informe.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 4: Almacenamiento",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Qué comando muestra el espacio libre de cada sistema de archivos?",
                            [
                                ("df -h", True),
                                ("du -sh", False),
                                ("lsblk", False),
                                ("free -h", False),
                            ],
                        ),
                        (
                            "¿Por qué se recomienda usar UUID en /etc/fstab en lugar de /dev/sdX?",
                            [
                                ("Los nombres /dev/sdX pueden cambiar entre arranques; el UUID no", True),
                                ("El UUID ocupa menos espacio en disco", False),
                                ("/dev/sdX no funciona con ext4", False),
                                ("El UUID monta más rápido el disco", False),
                            ],
                        ),
                        (
                            "En la terminología de LVM, ¿qué es un Volume Group (VG)?",
                            [
                                ("Una agrupación de uno o varios volúmenes físicos", True),
                                ("Una partición formateada lista para montar", False),
                                ("El disco físico sin particionar", False),
                                ("El punto de montaje de un volumen lógico", False),
                            ],
                        ),
                        (
                            "¿Qué comando prueba las entradas de /etc/fstab sin reiniciar?",
                            [
                                ("sudo mount -a", True),
                                ("sudo umount -a", False),
                                ("sudo fsck -a", False),
                                ("sudo reboot", False),
                            ],
                        ),
                    ],
                },
            ],
        },
        # =====================================================================
        # MÓDULO 5
        # =====================================================================
        {
            "name": "Módulo 5: Redes",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: IP, puertos, DNS, firewall y SSH",
                    "markdown": """# Redes

## Interfaces y direcciones

La suite moderna es `ip` (del paquete `iproute2`); reemplaza a `ifconfig`.

```bash
ip a                   # Direcciones de todas las interfaces
ip -br a               # Resumen breve
ip route               # Tabla de rutas
ip link set eth0 up    # Activar una interfaz
```

Una dirección como `192.168.1.50/24` combina la IP y la máscara (`/24` =
255.255.255.0).

## Puertos y conexiones

`ss` reemplaza al viejo `netstat`.

```bash
ss -tuln               # Puertos TCP/UDP en escucha, numéricos
ss -tp                 # Conexiones TCP con el proceso dueño
ss -s                  # Resumen estadístico
```

| Opción | Significado |
|--------|-------------|
| `-t` | TCP |
| `-u` | UDP |
| `-l` | Solo en escucha (listening) |
| `-n` | Sin resolver nombres (numérico) |
| `-p` | Muestra el proceso |

## DNS y resolución

```bash
cat /etc/resolv.conf   # Servidores DNS configurados
getent hosts debian.org
host debian.org        # Consulta DNS
dig debian.org         # Consulta DNS detallada
```

El orden de resolución (archivos, DNS...) lo define
`/etc/nsswitch.conf`. `/etc/hosts` permite mapeos estáticos locales.

## Firewall

Debian trae `nftables`; `ufw` es un frontend sencillo muy usado.

```bash
sudo ufw status verbose
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp          # Permitir SSH
sudo ufw allow from 192.168.1.0/24 to any port 80
sudo ufw enable
```

Con `iptables` directamente sería más verboso:

```bash
sudo iptables -L -n -v         # Listar reglas
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

Antes de activar el firewall en un servidor remoto, asegúrate de permitir
el puerto SSH (22): de lo contrario podrías bloquear tu propio acceso.

## SSH

`ssh` da acceso remoto seguro; el servidor es `sshd`.

```bash
ssh usuario@servidor           # Conectar
ssh -p 2222 usuario@servidor   # Puerto no estándar
ssh-keygen -t ed25519          # Generar par de claves
ssh-copy-id usuario@servidor   # Instalar la clave pública
```

La configuración del cliente está en `~/.ssh/config` y la del servidor en
`/etc/ssh/sshd_config`. Autenticar con claves es más seguro que con
contraseña.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 05: Configura el firewall y revisa la red",
                    "markdown": """# Lab 05: Configura el firewall y revisa la red

## Objetivos

1. Muestra las direcciones IP de las interfaces en formato breve.
2. Lista los puertos TCP en escucha (numéricos).
3. Configura `ufw` con política por defecto: denegar entrante, permitir
   saliente.
4. Permite explícitamente el puerto SSH (22/tcp) **antes** de habilitar el
   firewall, y luego habilítalo.
5. Verifica el estado detallado del firewall.

## Pistas

- `ip -br a` da un resumen compacto.
- `ss -tln` muestra los puertos TCP en escucha.
- Permite SSH antes de `ufw enable` para no perder el acceso.
""",
                    "solution_markdown": """# Solución comentada

```bash
# 1. Direcciones IP en formato breve
ip -br a

# 2. Puertos TCP en escucha, numéricos
ss -tln

# 3. Políticas por defecto
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 4. Permitir SSH ANTES de habilitar, y luego habilitar
sudo ufw allow 22/tcp
sudo ufw --force enable

# 5. Estado detallado
sudo ufw status verbose
```

## Explicación paso a paso

1. `ip -br a` (brief) muestra cada interfaz, su estado (UP/DOWN) y sus
   direcciones en una sola línea, ideal para una vista rápida.
2. `ss -tln` lista sockets TCP (`-t`) en escucha (`-l`) sin resolver nombres
   (`-n`). Verás, por ejemplo, `0.0.0.0:22` si SSH está activo.
3. Fijamos las políticas por defecto: bloquear todo el tráfico entrante y
   permitir el saliente. Es la base de un firewall seguro.
4. **El orden importa.** Permitimos `22/tcp` (SSH) antes de activar el
   firewall; si lo habilitáramos primero con la política de denegar, en un
   servidor remoto perderíamos la conexión. `--force enable` evita la
   pregunta interactiva de confirmación.
5. `ufw status verbose` muestra las políticas por defecto y la lista de
   reglas activas, confirmando que SSH está permitido y el firewall activo.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 5: Redes",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Qué comando moderno muestra las direcciones IP de las interfaces?",
                            [
                                ("ip a", True),
                                ("ss -tuln", False),
                                ("route -n", False),
                                ("dig a", False),
                            ],
                        ),
                        (
                            "¿Qué opciones de ss muestran los puertos TCP en escucha de forma numérica?",
                            [
                                ("ss -tln", True),
                                ("ss -u", False),
                                ("ss -p", False),
                                ("ss -r", False),
                            ],
                        ),
                        (
                            "Antes de habilitar ufw en un servidor remoto, ¿qué regla es crítico añadir?",
                            [
                                ("Permitir el puerto SSH (22/tcp)", True),
                                ("Denegar todo el tráfico saliente", False),
                                ("Permitir el puerto 80 (HTTP)", False),
                                ("Bloquear el puerto 22", False),
                            ],
                        ),
                        (
                            "¿Qué archivo contiene los servidores DNS que usa el sistema para resolver nombres?",
                            [
                                ("/etc/resolv.conf", True),
                                ("/etc/hosts", False),
                                ("/etc/hostname", False),
                                ("/etc/ssh/sshd_config", False),
                            ],
                        ),
                    ],
                },
            ],
        },
        # =====================================================================
        # MÓDULO 6
        # =====================================================================
        {
            "name": "Módulo 6: Automatización y Mantenimiento + Capstone",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: cron, timers, apt y respaldos",
                    "markdown": """# Automatización y Mantenimiento

## cron

`cron` ejecuta tareas de forma programada. Cada usuario tiene su crontab.

```bash
crontab -e             # Editar tu crontab
crontab -l             # Listar tus tareas
sudo crontab -e -u ana # Editar el crontab de otro usuario
```

El formato de una línea tiene cinco campos de tiempo más el comando:

```
# min hora dia-mes mes dia-sem  comando
  0   3    *       *   *        /usr/local/bin/respaldo.sh
```

| Campo | Rango |
|-------|-------|
| minuto | 0-59 |
| hora | 0-23 |
| día del mes | 1-31 |
| mes | 1-12 |
| día de la semana | 0-7 (0 y 7 = domingo) |

El ejemplo anterior se ejecuta todos los días a las 3:00. Hay directorios
como `/etc/cron.daily/` para scripts periódicos del sistema.

## Temporizadores de systemd

Alternativa moderna a cron: un par de unidades `.service` + `.timer`.

```bash
systemctl list-timers          # Temporizadores activos
systemctl status mi-tarea.timer
```

Ventajas sobre cron: registro en el journal, dependencias, y `Persistent=true`
para ejecutar tareas perdidas tras un apagado.

## Gestión de paquetes con apt

```bash
sudo apt update                # Actualiza el índice de paquetes
sudo apt upgrade               # Actualiza paquetes instalados
sudo apt install nginx         # Instala un paquete
sudo apt remove nginx          # Elimina (conserva config)
sudo apt purge nginx           # Elimina también la config
sudo apt autoremove            # Quita dependencias huérfanas
apt search palabra            # Busca paquetes
apt show nginx                # Detalles de un paquete
```

`apt update` NO actualiza software; solo refresca la lista de versiones
disponibles. `apt upgrade` es el que instala las actualizaciones.

## Respaldos

Herramientas habituales: `tar`, `rsync`.

```bash
# Respaldo comprimido de /etc
sudo tar czf /respaldos/etc-$(date +%F).tar.gz /etc

# Sincronización incremental con rsync
rsync -av --delete /datos/ /respaldos/datos/
```

| Opción rsync | Significado |
|--------------|-------------|
| `-a` | Modo archivo (preserva permisos, tiempos, enlaces). |
| `-v` | Detallado. |
| `--delete` | Borra en destino lo que ya no está en origen. |

Sigue la regla 3-2-1: tres copias, en dos medios distintos, una fuera del
sitio. Y prueba tus restauraciones periódicamente.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 06: Programa una tarea con cron",
                    "markdown": """# Lab 06: Programa una tarea con cron

## Objetivos

1. Crea el script `/usr/local/bin/registro_disco.sh` que añada la fecha y la
   salida de `df -h /` a `/var/log/registro_disco.log`.
2. Hazlo ejecutable.
3. Programa en el crontab de root que se ejecute cada día a las 6:30.
4. Verifica que la tarea aparece en el crontab.
5. Ejecuta el script manualmente una vez y revisa el log.

## Pistas

- Un script empieza con `#!/bin/bash`.
- `chmod +x` lo hace ejecutable.
- Recuerda el orden de los campos de cron: minuto hora ...
- Usa `sudo crontab -e` para el crontab de root.
""",
                    "solution_markdown": """# Solución comentada

```bash
# 1. Crear el script
sudo tee /usr/local/bin/registro_disco.sh > /dev/null <<'EOF'
#!/bin/bash
echo "=== $(date +'%F %T') ===" >> /var/log/registro_disco.log
df -h / >> /var/log/registro_disco.log
EOF

# 2. Hacerlo ejecutable
sudo chmod +x /usr/local/bin/registro_disco.sh

# 3. Programarlo en el crontab de root (cada día a las 6:30)
#    Abre el editor:  sudo crontab -e   y añade la línea:
#    30 6 * * * /usr/local/bin/registro_disco.sh
#    De forma no interactiva:
( sudo crontab -l 2>/dev/null; echo "30 6 * * * /usr/local/bin/registro_disco.sh" ) | sudo crontab -

# 4. Verificar el crontab de root
sudo crontab -l

# 5. Ejecutar manualmente y revisar el log
sudo /usr/local/bin/registro_disco.sh
sudo cat /var/log/registro_disco.log
```

## Explicación paso a paso

1. `tee` con un *here-document* (`<<'EOF'`) escribe el script. Las comillas
   en `'EOF'` evitan que el shell expanda `$(date)` al crear el archivo, de
   modo que la expansión ocurra al ejecutarse. El script añade (`>>`) una
   marca de tiempo y el uso de disco de la raíz al log.
2. `chmod +x` otorga permiso de ejecución; sin él, cron no podría lanzarlo.
3. La línea de cron `30 6 * * *` significa: minuto 30, hora 6, cualquier día
   del mes, cualquier mes, cualquier día de la semana. El truco
   `crontab -l | ... | crontab -` añade la línea sin abrir el editor.
4. `sudo crontab -l` lista las tareas de root; deberías ver tu nueva línea.
5. Ejecutar el script a mano valida que funciona antes de esperar a las
   6:30. El log mostrará la fecha seguida de la tabla de `df -h /`.
""",
                },
                {
                    "kind": "lab",
                    "name": "Capstone: Configura un servidor web",
                    "markdown": """# Capstone: Configura un servidor web

Este ejercicio final integra todo lo aprendido: usuarios, permisos,
servicios, firewall y automatización. Sobre `linuxbox` (Debian 12),
configura un pequeño servidor web con Nginx.

## Objetivos

1. **Paquetes:** actualiza el índice de apt e instala `nginx`.
2. **Servicio:** asegúrate de que `nginx` está activo y habilitado en el
   arranque.
3. **Contenido:** crea un usuario `webadmin`, dale propiedad del directorio
   `/var/www/capstone` y coloca dentro un `index.html` con un saludo.
4. **Configuración:** crea un *server block* de Nginx que sirva
   `/var/www/capstone` en el puerto 8080 y actívalo.
5. **Firewall:** permite el puerto 8080/tcp en `ufw` (y 22/tcp para no
   perder SSH); habilita el firewall.
6. **Verificación:** comprueba con `curl http://localhost:8080` que
   responde tu página.
7. **Automatización:** programa una tarea de cron que cada domingo a las
   4:00 respalde `/var/www/capstone` en `/var/backups/`.

## Pistas

- Los *server blocks* viven en `/etc/nginx/sites-available/` y se activan
  enlazándolos en `/etc/nginx/sites-enabled/`.
- Valida la configuración de Nginx con `nginx -t` antes de recargar.
- `tar czf` crea un respaldo comprimido.

Tómate tu tiempo. Cuando termines, contrasta con la solución.
""",
                    "solution_markdown": """# Solución comentada

```bash
# 1. Paquetes: actualizar e instalar Nginx
sudo apt update
sudo apt install -y nginx

# 2. Servicio activo y habilitado
sudo systemctl enable --now nginx
systemctl status nginx --no-pager

# 3. Usuario y contenido
sudo useradd -m -s /bin/bash webadmin
sudo mkdir -p /var/www/capstone
sudo chown -R webadmin:webadmin /var/www/capstone
echo "<h1>Hola desde el Capstone</h1>" | sudo tee /var/www/capstone/index.html

# 4. Server block en el puerto 8080
sudo tee /etc/nginx/sites-available/capstone > /dev/null <<'EOF'
server {
    listen 8080;
    server_name _;
    root /var/www/capstone;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
}
EOF
sudo ln -sf /etc/nginx/sites-available/capstone /etc/nginx/sites-enabled/capstone
sudo nginx -t                 # Validar la sintaxis
sudo systemctl reload nginx

# 5. Firewall: permitir SSH y 8080, luego habilitar
sudo ufw allow 22/tcp
sudo ufw allow 8080/tcp
sudo ufw --force enable

# 6. Verificación
curl http://localhost:8080

# 7. Respaldo semanal por cron (domingos a las 4:00)
( sudo crontab -l 2>/dev/null; \\
  echo "0 4 * * 0 tar czf /var/backups/capstone-\\$(date +\\%F).tar.gz /var/www/capstone" ) \\
  | sudo crontab -
sudo crontab -l
```

## Explicación paso a paso

1. `apt update` refresca el índice de paquetes y `apt install -y nginx`
   instala el servidor web sin pedir confirmación.
2. `systemctl enable --now nginx` habilita el servicio en el arranque y lo
   inicia en el mismo comando. `status` confirma que está `active`.
3. Creamos el usuario `webadmin`, el directorio raíz del sitio y le
   transferimos la propiedad con `chown -R`. El `index.html` es la página
   que servirá Nginx.
4. El *server block* le dice a Nginx que escuche en el puerto **8080** y
   sirva archivos desde `/var/www/capstone`. Lo activamos con un enlace
   simbólico en `sites-enabled`. `nginx -t` valida la sintaxis antes de
   aplicar; `reload` recarga sin cortar conexiones. Nota: en el crontab, el
   signo `%` debe escaparse como `\\%` porque cron lo interpreta como salto
   de línea.
5. Abrimos el puerto 8080 en `ufw` y, muy importante, también el 22 para no
   perder el acceso SSH antes de activar el firewall con `--force enable`.
6. `curl http://localhost:8080` debe devolver el HTML del saludo,
   confirmando que todo el conjunto funciona de extremo a extremo.
7. La línea de cron `0 4 * * 0` se ejecuta los domingos (día 0) a las 4:00
   y crea un `tar.gz` fechado del sitio en `/var/backups/`. Con esto cierras
   el ciclo: instalación, servicio, seguridad y automatización.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 6: Automatización",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "En una línea de cron, ¿qué representa el primer campo?",
                            [
                                ("El minuto (0-59)", True),
                                ("La hora (0-23)", False),
                                ("El día del mes (1-31)", False),
                                ("El día de la semana (0-7)", False),
                            ],
                        ),
                        (
                            "¿Qué hace exactamente 'sudo apt update'?",
                            [
                                ("Refresca el índice de paquetes disponibles, sin instalar nada", True),
                                ("Actualiza todos los paquetes instalados", False),
                                ("Elimina paquetes huérfanos", False),
                                ("Instala las últimas versiones de seguridad", False),
                            ],
                        ),
                        (
                            "¿Qué opción de rsync borra en el destino los archivos que ya no existen en el origen?",
                            [
                                ("--delete", True),
                                ("-a", False),
                                ("-v", False),
                                ("--dry-run", False),
                            ],
                        ),
                        (
                            "¿Qué ventaja ofrecen los temporizadores de systemd frente a cron?",
                            [
                                ("Registran su ejecución en el journal y pueden recuperar tareas perdidas con Persistent=true", True),
                                ("Son la única forma de ejecutar tareas cada minuto", False),
                                ("No requieren que el sistema esté encendido", False),
                                ("Se configuran editando /etc/crontab", False),
                            ],
                        ),
                    ],
                },
            ],
        },
    ],
}
