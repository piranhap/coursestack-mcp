COURSE = {
    "title": "Introducción a la Ciberseguridad",
    "subtitle": "Fundamentos de seguridad defensiva para principiantes",
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
            "name": "Módulo 1: Fundamentos de la Seguridad",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Bienvenida al curso",
                    "markdown": """# Bienvenida a *Introducción a la Ciberseguridad*

Hola y bienvenido/a. Este curso está diseñado para personas **principiantes** que quieren
entender cómo se protege la información y los sistemas en el mundo real. No necesitas
experiencia previa en seguridad, solo curiosidad y ganas de practicar.

## ¿Qué vas a aprender?

A lo largo de 6 módulos construirás una base sólida de **seguridad defensiva** (Blue Team):

| Módulo | Tema principal |
|--------|----------------|
| 1 | Fundamentos: tríada CIA, amenazas, vulnerabilidades y riesgo |
| 2 | Criptografía básica: hashing, cifrado y TLS |
| 3 | Seguridad de redes: puertos, protocolos y firewalls |
| 4 | Autenticación y control de acceso |
| 5 | Amenazas comunes y defensa |
| 6 | Blue Team, hardening y proyecto final (Capstone) |

## Cómo funciona cada módulo

Cada módulo tiene la misma estructura:

1. Una lección de **conceptos** para entender la teoría.
2. Un **laboratorio práctico** en una máquina Linux real (Debian 12).
3. Un **cuestionario** para comprobar lo aprendido.

## Tu laboratorio

Tendrás acceso a una máquina Linux llamada `linuxbox`. Allí practicarás comandos reales.
Para comprobar que todo funciona, conéctate y ejecuta:

```bash
whoami
hostname
cat /etc/os-release | grep PRETTY_NAME
```

Deberías ver el nombre de usuario, el nombre del equipo y la versión de Debian.

## Una nota sobre ética

Todo lo que aprenderás aquí es para **defender** sistemas y **entender** cómo piensan los
atacantes. Practica siempre en tus propios equipos o en laboratorios autorizados como este.
Usar estas técnicas contra sistemas ajenos sin permiso es ilegal.

¡Empecemos!
""",
                },
                {
                    "kind": "text",
                    "name": "Conceptos: La tríada CIA y el vocabulario del riesgo",
                    "markdown": """# La tríada CIA y el vocabulario del riesgo

La ciberseguridad se puede resumir en una idea central: proteger la información. Pero
¿protegerla de qué exactamente? Para responder usamos la **tríada CIA**, tres propiedades
que toda información valiosa debe mantener.

## La tríada CIA

| Propiedad | En inglés | Qué significa | Ejemplo de fallo |
|-----------|-----------|---------------|------------------|
| Confidencialidad | Confidentiality | Solo las personas autorizadas pueden ver la información | Una filtración de contraseñas |
| Integridad | Integrity | La información no se altera sin autorización | Un atacante modifica un saldo bancario |
| Disponibilidad | Availability | La información y los servicios están accesibles cuando se necesitan | Un ataque DDoS tira un sitio web |

Cada medida de seguridad que veremos (cifrado, firewalls, copias de seguridad, control de
acceso) sirve para reforzar una o varias de estas tres propiedades.

## Amenaza, vulnerabilidad y riesgo

Estos tres términos se confunden a menudo, pero son distintos:

- **Vulnerabilidad**: una debilidad en un sistema. Ejemplo: un software sin actualizar.
- **Amenaza** (threat): algo o alguien que puede aprovechar esa debilidad. Ejemplo: un
  atacante o un malware.
- **Riesgo**: la probabilidad de que una amenaza aproveche una vulnerabilidad y el impacto
  que causaría. Una forma sencilla de recordarlo:

```
Riesgo ≈ Amenaza × Vulnerabilidad × Impacto
```

Si eliminas la vulnerabilidad (por ejemplo, actualizando el software), el riesgo baja aunque
la amenaza siga existiendo.

## Superficie de ataque

La **superficie de ataque** es el conjunto de todos los puntos por donde un atacante podría
intentar entrar: puertos de red abiertos, formularios web, cuentas de usuario, dispositivos
USB, etc. Un principio clave de la defensa es **reducir la superficie de ataque**: cuanto
menos expongas, menos podrán atacar.

Por ejemplo, en un servidor Linux puedes ver qué servicios están escuchando en la red (parte
de tu superficie de ataque) con:

```bash
ss -tulpn
```

Cada línea es un puerto abierto: un posible punto de entrada. Si un servicio no se usa, lo
mejor es desactivarlo.

## Defensa en profundidad

Nunca confíes en una sola medida. La **defensa en profundidad** consiste en apilar varias
capas (firewall + contraseñas fuertes + cifrado + monitorización) para que, si una falla, las
demás sigan protegiendo. Es la idea que guiará todo el curso.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 01: Explorando la superficie de ataque de linuxbox",
                    "markdown": """# Lab 01: Explorando la superficie de ataque

En este primer laboratorio vas a inspeccionar tu máquina `linuxbox` para identificar
elementos de su **superficie de ataque** y relacionarlos con la tríada CIA.

## Objetivos

1. Identificar el sistema operativo y su versión.
2. Listar los usuarios del sistema.
3. Ver qué servicios de red están escuchando.
4. Reflexionar sobre qué propiedad de la tríada CIA protege cada hallazgo.

## Instrucciones

**Paso 1.** Conéctate a `linuxbox` y averigua la versión del sistema:

```bash
cat /etc/os-release
uname -a
```

**Paso 2.** Mira cuántas cuentas de usuario existen. Los usuarios con shell de login son los
más interesantes desde el punto de vista de seguridad:

```bash
cat /etc/passwd
grep -E "/bin/bash|/bin/sh" /etc/passwd
```

**Paso 3.** Descubre qué puertos están abiertos (tu superficie de ataque en red):

```bash
ss -tulpn
```

**Paso 4.** Cuenta cuántos puertos están en estado de escucha:

```bash
ss -tuln | grep -c LISTEN
```

## Preguntas para reflexionar

- ¿Qué usuarios tienen una shell interactiva? ¿Por qué eso importa?
- Si un servicio innecesario estuviera escuchando, ¿qué propiedad de la CIA pondría en riesgo?
- ¿Cómo reducirías la superficie de ataque de esta máquina?

Cuando termines, compara tu razonamiento con la solución.
""",
                    "solution_markdown": """# Solución comentada

```bash
# Paso 1: identificar el sistema
cat /etc/os-release        # Debería mostrar Debian GNU/Linux 12 (bookworm)
uname -a                   # Kernel, arquitectura y hostname

# Paso 2: enumerar usuarios con shell de login
grep -E "/bin/bash|/bin/sh" /etc/passwd

# Paso 3: servicios en escucha (superficie de ataque de red)
ss -tulpn

# Paso 4: contar puertos en escucha
ss -tuln | grep -c LISTEN
```

## Explicación paso a paso

1. **`/etc/os-release`** es el archivo estándar donde Debian y otras distribuciones declaran
   su nombre y versión. Conocer la versión exacta es el primer paso de cualquier análisis:
   te dice qué vulnerabilidades conocidas (CVE) podrían aplicar.

2. **`/etc/passwd`** contiene una línea por cuenta. El último campo es la shell. Las cuentas
   con `/bin/bash` o `/bin/sh` pueden iniciar sesión de forma interactiva; las cuentas de
   servicio suelen tener `/usr/sbin/nologin` o `/bin/false` precisamente para reducir riesgo.
   Cada cuenta de login es un punto de la superficie de ataque (alguien podría intentar
   adivinar su contraseña).

3. **`ss -tulpn`** muestra los sockets TCP (`-t`) y UDP (`-u`) que están escuchando (`-l`),
   con el número de puerto (`-n`) y el proceso propietario (`-p`). Cada puerto en escucha es
   una puerta abierta hacia la máquina.

4. **`ss -tuln | grep -c LISTEN`** filtra solo las líneas en estado `LISTEN` y las cuenta con
   `grep -c`. Cuantos menos puertos, menor es la superficie de ataque.

## Relación con la tríada CIA

- Un servicio de red innecesario amenaza sobre todo la **confidencialidad** y la
  **integridad** (un atacante podría entrar y leer o modificar datos), y a veces la
  **disponibilidad** (podría saturarlo).
- Reducir la superficie de ataque = desactivar servicios que no uses, deshabilitar cuentas de
  login que no necesites y cerrar puertos. Es un ejemplo directo del principio de
  **defensa en profundidad**.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 1: Fundamentos",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Qué propiedad de la tríada CIA se ve comprometida cuando un atacante logra ver información que no debería?",
                            [
                                ("Confidencialidad", True),
                                ("Integridad", False),
                                ("Disponibilidad", False),
                                ("Autenticidad", False),
                            ],
                        ),
                        (
                            "¿Cuál es la diferencia correcta entre vulnerabilidad y amenaza?",
                            [
                                ("La vulnerabilidad es una debilidad del sistema; la amenaza es lo que puede aprovecharla", True),
                                ("Son sinónimos exactos", False),
                                ("La amenaza es una debilidad del sistema; la vulnerabilidad es quien la aprovecha", False),
                                ("La vulnerabilidad solo existe en el software y la amenaza solo en el hardware", False),
                            ],
                        ),
                        (
                            "¿Qué describe mejor la 'superficie de ataque' de un sistema?",
                            [
                                ("El conjunto de todos los puntos por los que un atacante podría intentar entrar", True),
                                ("El número de discos duros instalados", False),
                                ("La cantidad de memoria RAM disponible", False),
                                ("El color del tema del escritorio", False),
                            ],
                        ),
                        (
                            "¿Qué comando permite ver los puertos de red que están en escucha en un servidor Linux?",
                            [
                                ("ss -tulpn", True),
                                ("cat /etc/hostname", False),
                                ("uptime", False),
                                ("df -h", False),
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
            "name": "Módulo 2: Criptografía Básica",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: Hashing, cifrado y TLS",
                    "markdown": """# Hashing, cifrado y TLS

La criptografía es la caja de herramientas que usamos para proteger la
**confidencialidad** y la **integridad** de los datos. Vamos a distinguir sus piezas
fundamentales.

## Hashing (funciones resumen)

Una **función hash** convierte cualquier entrada en una cadena de longitud fija. Tiene tres
propiedades clave:

- **Determinista**: la misma entrada siempre produce el mismo hash.
- **Unidireccional**: no se puede volver del hash a la entrada original.
- **Sensible**: cambiar un solo bit cambia por completo el hash (efecto avalancha).

Sirve para verificar **integridad** (¿el archivo cambió?) y para almacenar contraseñas.
Ejemplo con SHA-256:

```bash
echo -n "hola" | sha256sum
echo -n "Hola" | sha256sum   # cambia una letra y el hash es totalmente distinto
```

Importante: MD5 y SHA-1 están **rotos** para seguridad; usa SHA-256 o superior.

## Cifrado simétrico vs asimétrico

El **cifrado** sí es reversible: transforma datos en algo ilegible que se puede recuperar con
una clave. Hay dos familias:

| Tipo | Claves | Velocidad | Uso típico |
|------|--------|-----------|------------|
| Simétrico | Una misma clave cifra y descifra | Muy rápido | Cifrar archivos y discos (AES) |
| Asimétrico | Par de claves: pública y privada | Más lento | Intercambio de claves y firmas (RSA, ECC) |

En el cifrado **simétrico** (por ejemplo AES) las dos partes comparten un secreto. El
problema es: ¿cómo se ponen de acuerdo en ese secreto sin que nadie lo intercepte?

Ahí entra el cifrado **asimétrico**: cada usuario tiene una **clave pública** (que reparte
libremente) y una **clave privada** (que guarda en secreto). Lo que se cifra con una solo se
descifra con la otra.

## TLS/HTTPS: lo mejor de ambos mundos

Cuando visitas un sitio con `https://`, tu navegador usa **TLS**. TLS combina las dos
familias de forma inteligente:

1. Usa cifrado **asimétrico** al inicio para acordar de forma segura una clave de sesión.
2. Luego usa cifrado **simétrico** (rápido) con esa clave para toda la conversación.

Así consigues seguridad y velocidad. El candado del navegador significa que la conexión está
cifrada y que el certificado del servidor fue validado por una autoridad de certificación.

Puedes inspeccionar un certificado TLS desde la terminal:

```bash
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -subject -dates
```

## Firmas digitales

Una **firma digital** invierte el uso de las claves asimétricas para garantizar
**integridad** y **autenticidad**:

1. El autor calcula un hash del mensaje y lo cifra con su **clave privada** → esa es la firma.
2. Cualquiera puede usar la **clave pública** del autor para verificar la firma.

Si la verificación funciona, sabes dos cosas: el mensaje no fue alterado (integridad) y
proviene realmente del autor (autenticidad, porque solo él tiene la clave privada). Es la base
de la firma de software, correos y certificados.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 02: Verificar integridad con hashes y firmas",
                    "markdown": """# Lab 02: Verificar integridad con hashes

En este laboratorio comprobarás en la práctica las propiedades de las funciones hash y
generarás un par de claves para entender el cifrado asimétrico.

## Objetivos

1. Calcular hashes SHA-256 y observar el efecto avalancha.
2. Detectar la manipulación de un archivo mediante su hash.
3. Generar un par de claves asimétricas con OpenSSL.

## Instrucciones

**Paso 1.** Crea un archivo y calcula su hash:

```bash
echo "Transferencia: 100 euros" > pago.txt
sha256sum pago.txt
```

Guarda (copia) el hash que aparece.

**Paso 2.** Modifica el archivo mínimamente y vuelve a calcular el hash:

```bash
echo "Transferencia: 900 euros" > pago.txt
sha256sum pago.txt
```

Compara: aunque solo cambió un dígito, el hash es completamente diferente. Así se detecta un
cambio no autorizado (una violación de **integridad**).

**Paso 3.** Observa que el hashing es determinista:

```bash
echo -n "clave123" | sha256sum
echo -n "clave123" | sha256sum   # idéntico
```

**Paso 4.** Genera un par de claves asimétricas (privada y pública):

```bash
openssl genrsa -out privada.pem 2048
openssl rsa -in privada.pem -pubout -out publica.pem
ls -l privada.pem publica.pem
```

## Preguntas para reflexionar

- ¿Por qué un pequeño cambio en el archivo cambia todo el hash?
- ¿Qué archivo (privada o pública) nunca debes compartir?
- ¿Cómo usarías estas claves para firmar un documento?
""",
                    "solution_markdown": """# Solución comentada

```bash
# Paso 1: hash del archivo original
echo "Transferencia: 100 euros" > pago.txt
sha256sum pago.txt

# Paso 2: modificar y recalcular -> hash totalmente distinto
echo "Transferencia: 900 euros" > pago.txt
sha256sum pago.txt

# Paso 3: el hashing es determinista (mismo input -> mismo hash)
echo -n "clave123" | sha256sum
echo -n "clave123" | sha256sum

# Paso 4: par de claves asimétricas
openssl genrsa -out privada.pem 2048          # clave PRIVADA (secreta)
openssl rsa -in privada.pem -pubout -out publica.pem   # clave PÚBLICA (se comparte)

# Extra: firmar y verificar el archivo
openssl dgst -sha256 -sign privada.pem -out pago.sig pago.txt
openssl dgst -sha256 -verify publica.pem -signature pago.sig pago.txt
```

## Explicación paso a paso

1. **`sha256sum`** calcula el resumen SHA-256 del contenido del archivo. El hash es una huella
   digital única del contenido en ese instante.

2. Al cambiar `100` por `900`, el **efecto avalancha** hace que el nuevo hash no se parezca en
   nada al anterior. Por eso los hashes sirven para detectar manipulación: si el hash
   almacenado no coincide con el recalculado, el archivo cambió. Eso es control de
   **integridad**.

3. Ejecutar dos veces `sha256sum` con la misma entrada da el mismo resultado: propiedad
   **determinista**. Es lo que permite comparar hashes de forma fiable.

4. **`openssl genrsa`** crea la clave **privada** (jamás debe compartirse) y
   **`openssl rsa -pubout`** deriva la clave **pública** (sí se puede repartir).

5. En el paso extra, `-sign` con la clave privada crea una **firma digital** del archivo, y
   `-verify` con la clave pública comprueba tanto que el archivo no cambió (integridad) como
   que lo firmó el dueño de la privada (autenticidad). Si modificas `pago.txt` después de
   firmar, la verificación fallará.

## Idea clave

- Nunca compartas `privada.pem`. Reparte solo `publica.pem`.
- Hash = integridad. Firma (hash + clave privada) = integridad + autenticidad.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 2: Criptografía",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Cuál es una propiedad fundamental de una función hash criptográfica?",
                            [
                                ("Es unidireccional: no se puede recuperar la entrada a partir del hash", True),
                                ("Siempre se puede descifrar con la clave correcta", False),
                                ("Produce una salida de longitud variable según la entrada", False),
                                ("Dos entradas distintas siempre producen el mismo hash", False),
                            ],
                        ),
                        (
                            "En el cifrado asimétrico, ¿qué clave debes mantener siempre en secreto?",
                            [
                                ("La clave privada", True),
                                ("La clave pública", False),
                                ("Ambas por igual, no importa cuál", False),
                                ("Ninguna, ambas se comparten", False),
                            ],
                        ),
                        (
                            "¿Por qué TLS combina cifrado asimétrico y simétrico?",
                            [
                                ("Usa el asimétrico para acordar una clave de forma segura y el simétrico, más rápido, para el resto de la comunicación", True),
                                ("Porque el asimétrico es inseguro y hay que reforzarlo", False),
                                ("Porque el simétrico no puede cifrar datos", False),
                                ("Para no tener que usar certificados", False),
                            ],
                        ),
                        (
                            "Una firma digital verificada con la clave pública del autor garantiza que...",
                            [
                                ("El mensaje no fue alterado y proviene realmente del autor", True),
                                ("El mensaje está cifrado y nadie puede leerlo", False),
                                ("El mensaje se enviará más rápido", False),
                                ("El autor no puede volver a firmar nada más", False),
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
            "name": "Módulo 3: Seguridad de Redes",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: Modelos de red, puertos, protocolos y firewalls",
                    "markdown": """# Modelos de red, puertos, protocolos y firewalls

Para defender una red primero hay que entender cómo viajan los datos. Usamos modelos por
**capas**: cada capa se ocupa de una parte del problema.

## Modelo OSI y modelo TCP/IP

El modelo **OSI** tiene 7 capas; el modelo **TCP/IP** (el que se usa en Internet) las agrupa
en 4. Una comparación simplificada:

| OSI (7 capas) | TCP/IP (4 capas) | Ejemplo |
|---------------|------------------|---------|
| Aplicación / Presentación / Sesión | Aplicación | HTTP, DNS, SSH |
| Transporte | Transporte | TCP, UDP |
| Red | Internet | IP, ICMP |
| Enlace / Física | Acceso a red | Ethernet, Wi-Fi |

La idea clave para seguridad: los ataques y las defensas ocurren en distintas capas. Un
firewall clásico trabaja en las capas de red y transporte (IP y puertos); un WAF trabaja en la
capa de aplicación (HTTP).

## Puertos y protocolos

En la capa de transporte, **TCP** y **UDP** identifican los servicios mediante **puertos**
(números del 0 al 65535). Algunos que debes conocer:

| Puerto | Protocolo | Servicio |
|--------|-----------|----------|
| 22 | TCP | SSH (acceso remoto) |
| 53 | UDP/TCP | DNS |
| 80 | TCP | HTTP |
| 443 | TCP | HTTPS |
| 3306 | TCP | MySQL |

**TCP** es orientado a conexión y fiable (garantiza el orden y la entrega). **UDP** es más
rápido pero sin garantías (útil para DNS, streaming, juegos).

Puedes ver los puertos abiertos en tu propia máquina con:

```bash
ss -tulpn
```

## Firewalls

Un **firewall** filtra el tráfico según reglas: decide qué paquetes pasan y cuáles se bloquean
basándose en direcciones IP, puertos y protocolos. La estrategia recomendada es
**denegar por defecto**: bloquear todo y permitir solo lo necesario.

En Debian se suele usar `nftables` o la herramienta sencilla `ufw`:

```bash
sudo ufw default deny incoming
sudo ufw allow 22/tcp     # permitir SSH
sudo ufw enable
sudo ufw status verbose
```

## Escaneo con nmap

**nmap** es la herramienta estándar para descubrir qué puertos están abiertos en un host. Los
defensores la usan para auditar sus propios sistemas y comprobar que no hay servicios
inesperados expuestos:

```bash
nmap -sT localhost          # escaneo TCP connect de tu propia máquina
nmap -sV -p 22,80,443 localhost   # además intenta identificar la versión del servicio
```

Recuerda: escanear máquinas ajenas sin permiso es ilegal. Practica siempre contra `localhost`
o laboratorios autorizados como este. Comparar el resultado de `nmap` con lo que esperas es una
excelente forma de detectar servicios de más en tu superficie de ataque.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 03: Escaneo de puertos con nmap en localhost",
                    "markdown": """# Lab 03: Escaneo de puertos con nmap

Vas a auditar tu propia máquina `linuxbox` como lo haría un miembro del Blue Team: descubrir
qué puertos están abiertos y contrastarlos con los servicios que deberían estar corriendo.

## Objetivos

1. Listar los puertos en escucha con `ss`.
2. Escanear `localhost` con `nmap`.
3. Comparar ambos resultados e identificar servicios.

## Instrucciones

**Paso 1.** Observa los puertos en escucha directamente desde el sistema:

```bash
ss -tulpn
```

**Paso 2.** Ejecuta un escaneo TCP básico contra tu propia máquina:

```bash
nmap -sT localhost
```

Si `nmap` no está instalado, instálalo con `sudo apt-get update && sudo apt-get install -y nmap`.

**Paso 3.** Intenta identificar la versión de los servicios encontrados:

```bash
nmap -sV localhost
```

**Paso 4.** Escanea solo un rango concreto de puertos comunes:

```bash
nmap -p 1-1024 localhost
```

## Preguntas para reflexionar

- ¿Coinciden los puertos que ve `nmap` con los que muestra `ss`?
- ¿Hay algún puerto abierto que no reconozcas? ¿Qué harías al respecto?
- ¿Por qué es importante escanear tus propios sistemas periódicamente?
""",
                    "solution_markdown": """# Solución comentada

```bash
# Paso 1: puertos en escucha vistos desde dentro del sistema
ss -tulpn

# Paso 2: escaneo TCP connect contra la propia máquina
nmap -sT localhost

# (si falta nmap)
sudo apt-get update && sudo apt-get install -y nmap

# Paso 3: detección de versiones de los servicios
nmap -sV localhost

# Paso 4: escaneo del rango de puertos "bien conocidos"
nmap -p 1-1024 localhost
```

## Explicación paso a paso

1. **`ss -tulpn`** muestra la verdad desde dentro: qué procesos escuchan en qué puertos. Es tu
   referencia base.

2. **`nmap -sT localhost`** hace un escaneo TCP *connect*: intenta completar la conexión a cada
   puerto para ver cuáles responden. Como es tu propia máquina, verás los mismos puertos que
   `ss`, más los detalles de "abierto/cerrado/filtrado".

3. **`nmap -sV`** va un paso más allá: interroga cada puerto abierto para deducir qué software
   y versión lo atiende (por ejemplo `OpenSSH 9.2`). Conocer la versión es clave porque enlaza
   con vulnerabilidades conocidas (CVE).

4. **`nmap -p 1-1024`** limita el escaneo a los puertos "bien conocidos" (0-1023), donde viven
   la mayoría de servicios estándar. Acelera el escaneo cuando solo te interesan esos.

## Cómo interpretar los resultados

- Idealmente, `nmap` y `ss` **coinciden**. Una diferencia puede indicar reglas de firewall
  (puertos filtrados) o un servicio que arrancó/paró entre escaneos.
- Un puerto abierto que **no reconoces** es una señal de alerta: podría ser un servicio de más
  (aumenta la superficie de ataque) o incluso una puerta trasera. La respuesta correcta es
  investigar el proceso (columna de `ss -tulpn`) y, si no se necesita, desactivarlo.
- Auditar tus sistemas con regularidad te permite detectar cambios inesperados antes que un
  atacante.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 3: Seguridad de Redes",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Qué puerto TCP se asocia por defecto al servicio HTTPS?",
                            [
                                ("443", True),
                                ("22", False),
                                ("80", False),
                                ("53", False),
                            ],
                        ),
                        (
                            "¿Cuál es la estrategia recomendada al configurar un firewall?",
                            [
                                ("Denegar todo por defecto y permitir solo lo necesario", True),
                                ("Permitir todo por defecto y bloquear solo lo peligroso", False),
                                ("Abrir todos los puertos para evitar problemas de conexión", False),
                                ("Desactivar el firewall en servidores de producción", False),
                            ],
                        ),
                        (
                            "¿En qué se diferencian TCP y UDP?",
                            [
                                ("TCP es orientado a conexión y fiable; UDP es más rápido pero sin garantías de entrega", True),
                                ("UDP cifra los datos y TCP no", False),
                                ("TCP solo funciona en redes locales y UDP en Internet", False),
                                ("No hay ninguna diferencia práctica entre ellos", False),
                            ],
                        ),
                        (
                            "¿Para qué se usa nmap desde el punto de vista de un defensor (Blue Team)?",
                            [
                                ("Auditar los propios sistemas para descubrir qué puertos y servicios están expuestos", True),
                                ("Cifrar el disco duro del servidor", False),
                                ("Crear copias de seguridad automáticas", False),
                                ("Editar el archivo /etc/passwd", False),
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
            "name": "Módulo 4: Autenticación y Control de Acceso",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: Contraseñas, MFA y mínimo privilegio",
                    "markdown": """# Contraseñas, MFA y mínimo privilegio

La **autenticación** responde a la pregunta "¿quién eres?" y el **control de acceso** a
"¿qué puedes hacer?". Juntos protegen la **confidencialidad** y la **integridad**.

## Factores de autenticación

Existen tres tipos de factores:

| Factor | Ejemplo |
|--------|---------|
| Algo que sabes | Contraseña, PIN |
| Algo que tienes | Teléfono, token, llave física |
| Algo que eres | Huella, cara, iris |

## Contraseñas y su almacenamiento

Las contraseñas **nunca** deben guardarse en texto plano. Se almacenan como **hashes** con un
valor aleatorio único llamado **sal** (salt) que impide ataques con tablas precalculadas
(rainbow tables). En Linux, los hashes de las contraseñas viven en `/etc/shadow`, no en
`/etc/passwd`:

```bash
sudo cat /etc/shadow | head
```

Un campo típico se ve como `$6$sal$hash`, donde `$6$` indica el algoritmo SHA-512. Los
sistemas modernos prefieren algoritmos lentos y con sal como **bcrypt**, **scrypt** o
**Argon2**, diseñados para que probar contraseñas por fuerza bruta sea costoso.

Buenas prácticas de contraseñas:

- Largas (una frase de paso es mejor que una palabra corta con símbolos).
- Únicas por servicio (usa un gestor de contraseñas).
- Nunca reutilizadas ni compartidas.

## MFA: autenticación multifactor

La **MFA** exige dos o más factores distintos. Aunque roben tu contraseña (algo que sabes), el
atacante necesitaría además tu segundo factor (algo que tienes). Los códigos temporales
**TOTP** de apps como Google Authenticator son un ejemplo común. La MFA es una de las defensas
más efectivas contra el robo de credenciales.

## Principio de mínimo privilegio

El **principio de mínimo privilegio** dice que cada usuario o proceso debe tener **solo** los
permisos que necesita para su tarea, ni uno más. Así, si una cuenta se ve comprometida, el daño
es limitado.

En Linux esto se refleja en el modelo de permisos y en el uso de `sudo`:

```bash
id                      # ver tus grupos y UID
sudo -l                 # ver qué comandos puedes ejecutar como administrador
```

## sudo en lugar de root

Trabajar siempre como `root` es peligroso: cualquier error o programa malicioso tendría control
total. La práctica correcta es trabajar como usuario normal y elevar privilegios puntualmente
con `sudo`. Ventajas:

- Cada acción con `sudo` queda **registrada** (auditoría).
- Se puede limitar **qué** comandos concretos puede ejecutar cada usuario.

La configuración vive en `/etc/sudoers` y se edita de forma segura con `visudo`, que valida la
sintaxis antes de guardar para no dejarte fuera del sistema:

```bash
sudo visudo
```

Combinar contraseñas fuertes, MFA y mínimo privilegio es una de las mejores inversiones de
seguridad que puedes hacer.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 04: Revisar cuentas, permisos y sudoers",
                    "markdown": """# Lab 04: Cuentas, permisos y sudo

Vas a auditar las cuentas y los privilegios de `linuxbox` aplicando el principio de
**mínimo privilegio**.

## Objetivos

1. Revisar usuarios y dónde se almacenan sus contraseñas.
2. Identificar qué cuentas pueden usar `sudo`.
3. Entender cómo se configuran los privilegios en `/etc/sudoers`.

## Instrucciones

**Paso 1.** Mira las cuentas del sistema y separa las de servicio de las de personas:

```bash
cat /etc/passwd
awk -F: '$3 >= 1000 {print $1, $3}' /etc/passwd   # usuarios "humanos" (UID >= 1000)
```

**Paso 2.** Comprueba dónde están los hashes de contraseña (necesita privilegios):

```bash
sudo head -n 5 /etc/shadow
```

Observa el formato `$6$...` (SHA-512) y la sal.

**Paso 3.** Averigua quién pertenece al grupo `sudo`:

```bash
getent group sudo
```

**Paso 4.** Consulta qué puedes ejecutar como administrador y revisa la configuración:

```bash
sudo -l
sudo cat /etc/sudoers
ls -l /etc/sudoers.d/
```

## Preguntas para reflexionar

- ¿Cuántos usuarios humanos hay frente a cuentas de servicio?
- ¿Por qué las contraseñas están en /etc/shadow y no en /etc/passwd?
- ¿Cómo aplicarías el principio de mínimo privilegio a una cuenta nueva?
""",
                    "solution_markdown": """# Solución comentada

```bash
# Paso 1: usuarios del sistema
cat /etc/passwd
awk -F: '$3 >= 1000 {print $1, $3}' /etc/passwd   # solo cuentas humanas

# Paso 2: dónde viven los hashes de contraseña
sudo head -n 5 /etc/shadow

# Paso 3: miembros del grupo sudo
getent group sudo

# Paso 4: privilegios y configuración de sudo
sudo -l
sudo cat /etc/sudoers
ls -l /etc/sudoers.d/
```

## Explicación paso a paso

1. **`/etc/passwd`** es legible por todos y lista todas las cuentas. El tercer campo es el UID.
   Por convención en Debian, los UID **>= 1000** son cuentas de personas, y los menores son
   cuentas de sistema/servicio. El `awk` filtra solo las humanas: normalmente habrá muy pocas.

2. **`/etc/shadow`** solo lo puede leer root (por eso usamos `sudo`). Guarda los hashes de las
   contraseñas separados del `/etc/passwd` público. El formato `$6$sal$hash` indica algoritmo
   SHA-512 con **sal** aleatoria, de modo que dos usuarios con la misma contraseña tendrán
   hashes distintos. Separar los hashes en un archivo protegido es una defensa clave: aunque
   alguien lea `/etc/passwd`, no obtiene las contraseñas.

3. **`getent group sudo`** muestra qué usuarios pertenecen al grupo `sudo`, es decir, quién
   puede elevar privilegios. Cuantas menos cuentas ahí, mejor (mínimo privilegio).

4. **`sudo -l`** lista exactamente qué comandos puede ejecutar tu usuario como administrador.
   **`/etc/sudoers`** (y los fragmentos en `/etc/sudoers.d/`) definen esas reglas. Editarlo
   siempre con `visudo` evita errores de sintaxis que podrían bloquear el acceso.

## Aplicar mínimo privilegio a una cuenta nueva

- No la añadas al grupo `sudo` salvo que lo necesite.
- Si necesita solo un comando concreto con privilegios, dale una regla específica en
  `/etc/sudoers.d/` (por ejemplo, permitir solo `systemctl restart nginx`) en lugar de acceso
  total.
- Usa una shell de login solo si de verdad va a iniciar sesión; si es de servicio, usa
  `/usr/sbin/nologin`.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 4: Autenticación y Control de Acceso",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Dónde se almacenan los hashes de las contraseñas de los usuarios en un sistema Linux moderno?",
                            [
                                ("/etc/shadow", True),
                                ("/etc/passwd", False),
                                ("/etc/hosts", False),
                                ("/etc/motd", False),
                            ],
                        ),
                        (
                            "¿Qué es la autenticación multifactor (MFA)?",
                            [
                                ("Exigir dos o más factores de distinto tipo (algo que sabes, tienes o eres)", True),
                                ("Usar la misma contraseña en varios servicios a la vez", False),
                                ("Cambiar la contraseña cada día", False),
                                ("Cifrar el disco duro dos veces", False),
                            ],
                        ),
                        (
                            "¿Qué establece el principio de mínimo privilegio?",
                            [
                                ("Cada usuario o proceso debe tener solo los permisos necesarios para su tarea, ni uno más", True),
                                ("Todos los usuarios deben ser administradores para trabajar cómodos", False),
                                ("El administrador debe tener menos permisos que los usuarios", False),
                                ("Nadie debe tener contraseña para agilizar el acceso", False),
                            ],
                        ),
                        (
                            "¿Por qué es preferible usar sudo en lugar de iniciar sesión siempre como root?",
                            [
                                ("Porque cada acción con sudo queda registrada y se puede limitar qué comandos ejecuta cada usuario", True),
                                ("Porque sudo hace que los comandos se ejecuten más rápido", False),
                                ("Porque root no puede instalar software", False),
                                ("Porque sudo desactiva el firewall automáticamente", False),
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
            "name": "Módulo 5: Amenazas Comunes y Defensa",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: Phishing, malware, ingeniería social y OWASP",
                    "markdown": """# Phishing, malware, ingeniería social y OWASP

La mayoría de los incidentes no empiezan con un hackeo sofisticado, sino engañando a una
persona o explotando un fallo común en una aplicación. Conocer estas amenazas es el primer paso
para defenderse.

## Ingeniería social

La **ingeniería social** manipula a las personas para que revelen información o realicen
acciones inseguras. Explota emociones como la urgencia, el miedo o la confianza. No importa lo
buena que sea tu tecnología: si alguien convence a un empleado de entregar su contraseña, las
defensas técnicas se saltan.

## Phishing

El **phishing** es la forma más común de ingeniería social: correos, mensajes o sitios web
falsos que suplantan a una entidad legítima para robar credenciales o dinero. Variantes:

| Tipo | Descripción |
|------|-------------|
| Phishing | Masivo, enviado a muchas víctimas |
| Spear phishing | Dirigido y personalizado a una persona concreta |
| Smishing | A través de SMS |
| Vishing | Por llamada de voz |

Señales de alerta de un correo de phishing:

- Sensación de urgencia ("tu cuenta será bloqueada en 24h").
- Remitente o dominio sospechoso (mira la dirección real, no el nombre mostrado).
- Enlaces que no coinciden con el sitio oficial (pasa el ratón por encima sin hacer clic).
- Adjuntos inesperados.

Puedes inspeccionar un enlace o cabeceras de forma segura desde la terminal sin abrirlos en el
navegador:

```bash
# Ver a dónde redirige realmente una URL sin descargar la página
curl -sI https://example.com | grep -i location
```

## Malware

**Malware** es cualquier software malicioso. Tipos frecuentes:

- **Virus/gusano**: se replica y propaga.
- **Troyano**: se disfraza de programa legítimo.
- **Ransomware**: cifra tus archivos y pide un rescate (ataca la **disponibilidad**).
- **Spyware/keylogger**: roba información (ataca la **confidencialidad**).

Defensas básicas: mantener el software actualizado, usar antivirus, no ejecutar adjuntos
desconocidos y aplicar mínimo privilegio para limitar el alcance.

## OWASP: fallos comunes en aplicaciones web

**OWASP** es una organización que publica el **OWASP Top 10**, la lista de los riesgos más
críticos en aplicaciones web. Algunos que debes conocer como principiante:

| Riesgo | Idea básica | Defensa |
|--------|-------------|---------|
| Inyección (SQL injection) | El atacante envía datos que la app ejecuta como código | Validar entradas y usar consultas parametrizadas |
| Cross-Site Scripting (XSS) | Inyectar scripts que se ejecutan en el navegador de otros | Escapar/validar la salida |
| Control de acceso roto | Acceder a recursos sin autorización | Verificar permisos en el servidor |
| Configuración insegura | Servicios con valores por defecto o de más | Hardening y quitar lo innecesario |

El hilo conductor de OWASP es simple: **nunca confíes en la entrada del usuario** y valida
todo del lado del servidor.

## La capa humana

Recuerda: la mejor defensa combina tecnología y **concienciación**. Formar a las personas para
reconocer phishing y reportarlo es tan importante como cualquier firewall.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 05: Analizar correos y enlaces sospechosos",
                    "markdown": """# Lab 05: Analizar indicadores de phishing

En este laboratorio actuarás como analista: examinarás un correo simulado y sus enlaces desde
la terminal, sin exponerte, para decidir si es phishing.

## Objetivos

1. Crear y examinar una cabecera de correo simulada.
2. Analizar una URL sospechosa sin abrirla en un navegador.
3. Extraer indicadores de compromiso (IoC) básicos.

## Instrucciones

**Paso 1.** Crea un archivo con un correo de ejemplo para analizarlo:

```bash
cat > correo.txt << 'EOF'
From: "Banco Seguro" <alertas@secure-banco-login.example>
Subject: URGENTE: verifique su cuenta en 24 horas
Reply-To: cobros@correo-raro.example

Estimado cliente, su cuenta sera bloqueada.
Acceda ya: http://secure-banco-login.example/verify?id=123
EOF
cat correo.txt
```

**Paso 2.** Extrae el remitente real y el dominio con herramientas de texto:

```bash
grep -i "^From:" correo.txt
grep -ioE "[a-z0-9.-]+@[a-z0-9.-]+" correo.txt
```

**Paso 3.** Extrae las URLs que contiene el mensaje:

```bash
grep -oE "https?://[^ ]+" correo.txt
```

**Paso 4.** Comprueba señales de alerta: dominio que imita a uno legítimo, urgencia en el
asunto y un `Reply-To` distinto del `From`.

```bash
grep -i "urgente\\|bloquead\\|24 horas" correo.txt
grep -i "reply-to" correo.txt
```

## Preguntas para reflexionar

- ¿El dominio del remitente parece legítimo o imita a un banco real?
- ¿Por qué el `Reply-To` diferente es una señal de alerta?
- ¿Qué harías con este correo en una organización real?
""",
                    "solution_markdown": """# Solución comentada

```bash
# Paso 1: crear un correo de ejemplo para el análisis
cat > correo.txt << 'EOF'
From: "Banco Seguro" <alertas@secure-banco-login.example>
Subject: URGENTE: verifique su cuenta en 24 horas
Reply-To: cobros@correo-raro.example

Estimado cliente, su cuenta sera bloqueada.
Acceda ya: http://secure-banco-login.example/verify?id=123
EOF

# Paso 2: remitente y direcciones de correo
grep -i "^From:" correo.txt
grep -ioE "[a-z0-9.-]+@[a-z0-9.-]+" correo.txt

# Paso 3: extraer las URLs sin abrirlas
grep -oE "https?://[^ ]+" correo.txt

# Paso 4: buscar indicadores de phishing
grep -i "urgente\\|bloquead\\|24 horas" correo.txt
grep -i "reply-to" correo.txt
```

## Explicación paso a paso

1. Creamos un correo de laboratorio con `cat > ... << 'EOF'`. El uso de comillas en `'EOF'`
   evita que la shell interprete el contenido: se guarda tal cual.

2. **`grep`** con `-oE` (solo lo coincidente, expresión extendida) extrae las direcciones de
   correo. La clave está en el **dominio**: `secure-banco-login.example` imita a un banco pero
   no es su dominio oficial. Los atacantes registran dominios parecidos (typosquatting).

3. Extraer las URLs con `grep -oE "https?://[^ ]+"` te permite **leer** el destino sin hacer
   clic. Aquí la URL usa `http://` (sin cifrar) y un dominio sospechoso: dos señales de alerta.

4. Buscamos palabras de **urgencia** ("URGENTE", "bloqueada", "24 horas"), una táctica clásica
   para que la víctima actúe sin pensar. Además, el **`Reply-To`** apunta a un dominio distinto
   del `From`: las respuestas irían a los atacantes, no al supuesto banco. Es un indicador
   fuerte de phishing.

## Veredicto y respuesta

Este correo es phishing: dominio que suplanta a un banco, `http` sin cifrar, urgencia y
`Reply-To` inconsistente. En una organización real:

- **No** hagas clic ni respondas.
- Repórtalo al equipo de seguridad (SOC) o a la dirección de abuso interna.
- Los IoC extraídos (dominio, dirección de correo, URL) se pueden bloquear en el firewall y en
  el filtro de correo para proteger a los demás.
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 5: Amenazas Comunes y Defensa",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Qué es el phishing?",
                            [
                                ("Un intento de robar información suplantando a una entidad legítima mediante mensajes o sitios falsos", True),
                                ("Un tipo de firewall de nueva generación", False),
                                ("Un algoritmo de cifrado simétrico", False),
                                ("Una técnica para acelerar la red", False),
                            ],
                        ),
                        (
                            "¿Qué tipo de malware cifra los archivos de la víctima y pide un rescate, atacando la disponibilidad?",
                            [
                                ("Ransomware", True),
                                ("Keylogger", False),
                                ("Adware", False),
                                ("Rootkit de solo lectura", False),
                            ],
                        ),
                        (
                            "Según OWASP, ¿cuál es la defensa principal contra la inyección SQL?",
                            [
                                ("Validar las entradas y usar consultas parametrizadas, sin confiar en la entrada del usuario", True),
                                ("Aumentar la memoria RAM del servidor", False),
                                ("Usar contraseñas más cortas", False),
                                ("Desactivar el registro de eventos", False),
                            ],
                        ),
                        (
                            "¿Cuál de estas es una señal de alerta típica de un correo de phishing?",
                            [
                                ("Un dominio del remitente que imita al de una entidad legítima y un mensaje de urgencia", True),
                                ("Que el correo esté firmado digitalmente por la entidad", False),
                                ("Que use HTTPS con un certificado válido", False),
                                ("Que provenga de un contacto verificado y esperado", False),
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
            "name": "Módulo 6: Blue Team, Hardening y Capstone",
            "lessons": [
                {
                    "kind": "text",
                    "name": "Conceptos: Logging, detección, hardening y respuesta a incidentes",
                    "markdown": """# Logging, detección, hardening y respuesta a incidentes

El **Blue Team** es el equipo defensivo: su trabajo es prevenir, detectar y responder a
ataques. Este módulo reúne todo lo aprendido en una mentalidad práctica de defensa.

## Logging: los registros lo son todo

Sin registros no puedes saber qué pasó. En Linux moderno, la mayoría de eventos se consultan
con **journald**, y algunos servicios aún escriben en `/var/log`:

```bash
journalctl -xe                 # eventos recientes del sistema
journalctl -u ssh              # eventos del servicio SSH
sudo tail -n 50 /var/log/auth.log   # intentos de autenticación (si existe)
```

Los registros de autenticación son especialmente valiosos: muchos intentos fallidos de login
pueden indicar un ataque de fuerza bruta.

## Detección

**Detectar** es buscar señales de actividad maliciosa en esos registros y en el sistema.
Ejemplos de indicadores:

- Múltiples fallos de login seguidos (fuerza bruta).
- Usuarios o procesos inesperados.
- Puertos abiertos que no reconoces.
- Cambios en archivos críticos.

```bash
# Contar intentos fallidos de SSH
sudo grep -c "Failed password" /var/log/auth.log 2>/dev/null

# Procesos que más CPU consumen (posible actividad anómala)
ps aux --sort=-%cpu | head
```

Herramientas como **fail2ban** automatizan la detección: bloquean IPs tras varios fallos.

## Hardening (fortalecimiento)

**Hardening** es reducir la superficie de ataque y reforzar la configuración por defecto.
Principios prácticos en Linux:

| Área | Acción de hardening |
|------|---------------------|
| Servicios | Desactivar los que no uses |
| SSH | Deshabilitar login de root y autenticación por contraseña; usar claves |
| Actualizaciones | Aplicar parches con regularidad |
| Cuentas | Mínimo privilegio, contraseñas fuertes, sin cuentas huérfanas |
| Firewall | Denegar por defecto |

Un ejemplo clásico de hardening de SSH en `/etc/ssh/sshd_config`:

```bash
# Recomendado
PermitRootLogin no
PasswordAuthentication no
```

Tras editar, se recarga el servicio:

```bash
sudo systemctl restart ssh
```

## Respuesta a incidentes

Cuando algo pasa, un proceso ordenado evita el caos. Un marco muy usado (SANS/NIST) tiene estas
fases:

1. **Preparación**: tener registros, copias de seguridad y un plan antes del incidente.
2. **Identificación**: confirmar que hay un incidente y su alcance.
3. **Contención**: aislar los sistemas afectados para frenar el daño.
4. **Erradicación**: eliminar la causa (malware, cuenta comprometida).
5. **Recuperación**: restaurar servicios de forma segura y vigilar.
6. **Lecciones aprendidas**: documentar y mejorar para el futuro.

La idea central del Blue Team: la seguridad no es un producto que se instala una vez, sino un
**proceso continuo** de vigilancia y mejora. En el laboratorio final (Capstone) pondrás en
práctica varias de estas técnicas de hardening sobre `linuxbox`.
""",
                },
                {
                    "kind": "lab",
                    "name": "Lab 06 (Capstone): Hardening y detección en linuxbox",
                    "markdown": """# Lab 06 (Capstone): Hardening de linuxbox

Este es el laboratorio final: reúne todo lo aprendido. Actuarás como analista del Blue Team
para **auditar, detectar y fortalecer** tu máquina `linuxbox`.

## Objetivos

1. Auditar la superficie de ataque (puertos, usuarios, sudo).
2. Revisar registros en busca de indicios de ataque.
3. Aplicar hardening al servicio SSH.
4. Verificar los cambios.

## Parte A — Auditoría

**Paso 1.** Revisa puertos abiertos y usuarios con privilegios:

```bash
ss -tulpn
getent group sudo
awk -F: '$3 >= 1000 {print $1}' /etc/passwd
```

## Parte B — Detección

**Paso 2.** Busca intentos de autenticación fallidos y procesos sospechosos:

```bash
sudo grep -c "Failed password" /var/log/auth.log 2>/dev/null
journalctl -u ssh --no-pager | tail -n 20
ps aux --sort=-%cpu | head
```

## Parte C — Hardening de SSH

**Paso 3.** Haz una copia de seguridad de la configuración antes de tocarla:

```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
```

**Paso 4.** Aplica dos medidas de hardening: deshabilitar el login de root por SSH y validar la
configuración:

```bash
sudo sed -i 's/^#\\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sshd -t && echo "Config OK"
```

## Parte D — Verificación

**Paso 5.** Confirma el cambio y recarga el servicio:

```bash
grep -i "^PermitRootLogin" /etc/ssh/sshd_config
sudo systemctl restart ssh
```

## Entregable

Escribe un breve informe (mentalmente o en un archivo) que responda:

- ¿Qué elementos de la superficie de ataque encontraste?
- ¿Viste indicios de intentos de acceso no autorizados?
- ¿Qué medida de hardening aplicaste y cómo la verificaste?
""",
                    "solution_markdown": """# Solución comentada

```bash
# ---------- Parte A: Auditoría ----------
ss -tulpn                                   # puertos en escucha (superficie de ataque)
getent group sudo                           # quién puede elevar privilegios
awk -F: '$3 >= 1000 {print $1}' /etc/passwd # cuentas humanas

# ---------- Parte B: Detección ----------
sudo grep -c "Failed password" /var/log/auth.log 2>/dev/null  # fuerza bruta SSH
journalctl -u ssh --no-pager | tail -n 20                     # eventos recientes de SSH
ps aux --sort=-%cpu | head                                    # procesos que más consumen

# ---------- Parte C: Hardening de SSH ----------
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak         # copia de seguridad
sudo sed -i 's/^#\\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sshd -t && echo "Config OK"                              # validar sintaxis

# ---------- Parte D: Verificación ----------
grep -i "^PermitRootLogin" /etc/ssh/sshd_config               # confirmar el valor
sudo systemctl restart ssh                                    # aplicar el cambio
```

## Explicación paso a paso

**Parte A — Auditoría.** Recuperamos las técnicas de los módulos 1, 3 y 4: `ss -tulpn` lista la
superficie de ataque en red, `getent group sudo` muestra las cuentas con privilegios (mínimo
privilegio) y el `awk` aísla las cuentas de personas. Es la foto inicial del sistema.

**Parte B — Detección.** `grep -c "Failed password"` cuenta los intentos fallidos de login: un
número alto sugiere un ataque de fuerza bruta. `journalctl -u ssh` da contexto reciente del
servicio y `ps aux --sort=-%cpu` revela procesos anómalos que consuman muchos recursos (posible
malware o minería). Es la fase de identificación de la respuesta a incidentes.

**Parte C — Hardening.** Primero hacemos una **copia de seguridad** (`.bak`): nunca modifiques
configuración crítica sin poder volver atrás. El `sed` reemplaza la línea `PermitRootLogin`
(esté comentada o no) por `PermitRootLogin no`, de modo que la cuenta root no pueda entrar
directamente por SSH: obliga a usar una cuenta normal y luego `sudo` (auditoría y mínimo
privilegio). **`sshd -t`** valida la sintaxis *antes* de reiniciar; si hay un error, lo detectas
sin romper el acceso.

**Parte D — Verificación.** Confirmamos con `grep` que el valor quedó aplicado y recargamos el
servicio con `systemctl restart ssh` para que surta efecto. Verificar siempre el resultado es
parte esencial del trabajo del Blue Team.

## Cómo ampliar el hardening

- `PasswordAuthentication no` y usar **claves SSH** en lugar de contraseñas.
- Instalar **fail2ban** para bloquear IPs tras varios fallos.
- Activar un firewall con `ufw default deny incoming` y permitir solo lo necesario.
- Mantener el sistema actualizado con `sudo apt-get update && sudo apt-get upgrade`.

Si algo sale mal, restaura la copia: `sudo cp /etc/ssh/sshd_config.bak /etc/ssh/sshd_config`.

Con esto cierras el ciclo completo del Blue Team: auditar, detectar, fortalecer y verificar.
¡Enhorabuena por completar el curso!
""",
                },
                {
                    "kind": "quiz",
                    "name": "Quiz Módulo 6: Blue Team y Hardening",
                    "passing_percent": 70,
                    "questions": [
                        (
                            "¿Por qué son fundamentales los registros (logs) para el Blue Team?",
                            [
                                ("Permiten detectar y reconstruir lo que ocurrió durante un ataque", True),
                                ("Sirven para acelerar el arranque del sistema", False),
                                ("Cifran automáticamente el disco duro", False),
                                ("Reemplazan la necesidad de un firewall", False),
                            ],
                        ),
                        (
                            "¿Qué es el 'hardening' de un sistema?",
                            [
                                ("Reducir la superficie de ataque y reforzar la configuración por defecto", True),
                                ("Instalar tantos servicios como sea posible", False),
                                ("Dar permisos de administrador a todos los usuarios", False),
                                ("Desactivar los registros para ahorrar espacio", False),
                            ],
                        ),
                        (
                            "En la configuración de SSH, ¿qué opción de hardening evita que la cuenta root inicie sesión directamente?",
                            [
                                ("PermitRootLogin no", True),
                                ("PermitRootLogin yes", False),
                                ("PasswordAuthentication yes", False),
                                ("X11Forwarding yes", False),
                            ],
                        ),
                        (
                            "En la respuesta a incidentes, ¿qué se hace en la fase de 'contención'?",
                            [
                                ("Aislar los sistemas afectados para frenar la propagación del daño", True),
                                ("Documentar las lecciones aprendidas al final del proceso", False),
                                ("Instalar el sistema operativo por primera vez", False),
                                ("Publicar el incidente en redes sociales de inmediato", False),
                            ],
                        ),
                    ],
                },
            ],
        },
    ],
}
