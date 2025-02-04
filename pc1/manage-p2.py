#PC1
#Mateo Sarria Franco de Sarabia
#Rafael Bueno Castro
#Jacobo España-Heredia Beteta

from lib_vm import VM, NET
import logging, sys, json
import subprocess
from subprocess import run, PIPE

def init_log():
    # Creación y configuración del logger
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('auto_p2')
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.propagate = False

def pause():
    input("-- Press <ENTER> to continue...")

# Main
init_log()
print('CDPS - PC1')
print('Mateo Sarria Franco de Sarabia')
print('Rafael Bueno Castro')
print('Jacobo España-Heredia Beteta')

# Llamada al script prepare-vnx-debian, que prepara el entorno Debian (se ejecuta antes de cualquier operación)
subprocess.call(["/lab/cnvr/bin/prepare-vnx-debian"], shell=True)

# Obtener la orden proporcionada como argumento
orden = str(sys.argv[1])

def getNServers():
    # Obtener el número de servidores desde el archivo de configuración
    nServ = 2  # Valor por defecto si no se encuentra el parámetro en el archivo de configuración
    with open("manage-p2.json") as f:
        config = json.load(f)
    
    # Verificar si la clave "number_of_servers" existe en el archivo de configuración
    if "number_of_servers" in config:
        n_serv = config["number_of_servers"]
        try:
            temp = float(n_serv)
        except ValueError:
            sys.exit("Error: el número de servidores debe ser un entero entre 1 y 5\n")
        
        # Validar que el número de servidores esté en el rango de 1 a 5
        if temp.is_integer() and 1 <= temp <= 5:
            nServ = int(temp)
        else:
            sys.exit("Error: el número de servidores debe ser un entero entre 1 y 5\n")
    return nServ

def get_debug():
    # Obtener la configuración de depuración desde el archivo
    with open("manage-p2.json") as f:
        config = json.load(f)
    
    # Retornar el valor de la clave "debug", o False si no existe
    return config.get("debug", False)

# Procesar la orden proporcionada como argumento
if orden == "create":
    # Crear recursos y redes
    debug = get_debug()
    subprocess.call(["mkdir -p temp"], shell=True)  # Crear la carpeta temporal (si no existe)

    # Crear las redes LAN1 y LAN2
    LAN1 = NET("LAN1")
    LAN1.create_net(debug)
    LAN2 = NET("LAN2")
    LAN2.create_net(debug)

    # Obtener el número de servidores desde el archivo de configuración
    nServ = getNServers()

    # Crear las máquinas virtuales de los servidores
    for i in range(1, nServ + 1):
        s = VM(f"s{str(i)}")
        s.create_vm(nServ, debug)

    # Crear las máquinas virtuales c1 y lb
    c1 = VM("c1")
    c1.create_vm(nServ, debug)
    lb = VM("lb")
    lb.create_vm(nServ, debug)

    # Configurar la red en el host (con la dirección IP y ruta especificadas)
    subprocess.call(["sudo ifconfig LAN1 10.1.1.3/24"], shell=True)
    subprocess.call(["sudo ip route add 10.0.0.0/16 via 10.1.1.1"], shell=True)

    # Limpiar la carpeta temporal creada
    subprocess.call(["rm -rf temp"], shell=True)

elif orden == "start":
    # Iniciar las máquinas virtuales
    debug = get_debug()
    nServ = getNServers()
    names = ["c1", "lb"]  # Lista de nombres de máquinas virtuales básicas (c1 y lb)

    # Añadir las máquinas virtuales de los servidores a la lista de nombres
    for i in range(1, nServ + 1):
        names.append(f"s{str(i)}")
    
    # Si se proporcionan parámetros adicionales en la línea de comandos, validar su existencia
    if len(sys.argv) > 2:
        params = sys.argv[2:len(sys.argv)]
        for param in params:
            if param in names:
                # Verificar que no haya nombres duplicados
                if params.count(param) > 1:
                    sys.exit("Error: no introduzca nombres duplicados")
            else:
                # Si algún parámetro no es un nombre válido, se muestra un mensaje de error
                sys.exit(f"Error: {param} no es nombre valido")
    else:
        params = names  # Si no se proporcionan parámetros adicionales, usar la lista predeterminada

    # Verificar que las máquinas virtuales no estén ya en ejecución antes de intentar iniciar
    running = []
    for name in params:
        state = run(["sudo", "virsh", "domstate", name], stdout=PIPE).stdout.decode('utf-8').strip()
        if state == "ejecutando":
            running.append(name)
        if len(running) >= 1:
            sys.exit("Error: La MV " + ", ".join(running) + " ya está encendida")

    # Iniciar las máquinas virtuales que no estén en ejecución
    for name in params:
        mv = VM(name)
        mv.start_vm(debug)
        mv.show_console_vm(debug)

elif orden == "stop":
    # Detener las máquinas virtuales
    debug = get_debug()
    nServ = getNServers()
    names = ["c1", "lb"]  # Lista de nombres de máquinas virtuales básicas (c1 y lb)

    # Añadir las máquinas virtuales de los servidores a la lista de nombres
    for i in range(1, nServ + 1):
        names.append(f"s{str(i)}")
    
    # Si se proporcionan parámetros adicionales en la línea de comandos, validar su existencia
    if len(sys.argv) > 2:
        params = sys.argv[2:len(sys.argv)]
        for param in params:
            if param in names:
                # Verificar que no haya nombres duplicados
                if params.count(param) > 1:
                    sys.exit("Error: no introduzca nombres duplicados")
            else:
                # Si algún parámetro no es un nombre válido, se muestra un mensaje de error
                sys.exit(f"Error: {param} no es nombre valido")
    else:
        params = names  # Si no se proporcionan parámetros adicionales, usar la lista predeterminada

    # Verificar que las máquinas virtuales no estén ya apagadas antes de intentar detenerlas
    stopped = []
    for name in params:
        state = run(["sudo", "virsh", "domstate", name], stdout=PIPE).stdout.decode('utf-8').strip()
        if state == "apagado":
            stopped.append(name)
        if len(stopped) >= 1:
            sys.exit("Error: La MV " + ", ".join(stopped) + " ya está apagada")

    # Detener las máquinas virtuales que estén en ejecución
    for name in params:
        mv = VM(name)
        mv.stop_vm(debug)

elif orden == "destroy":
    # Destruir las máquinas virtuales y redes
    debug = get_debug()
    nServ = getNServers()

    # Destruir las máquinas virtuales de los servidores
    for i in range(1, nServ + 1):
        s = VM(f"s{str(i)}")
        s.destroy_vm(debug)

    # Destruir las máquinas virtuales c1 y lb
    c1 = VM("c1")
    c1.destroy_vm(debug)
    lb = VM("lb")
    lb.destroy_vm(debug)

    # Destruir las redes LAN1 y LAN2
    LAN1 = NET("LAN1")
    LAN1.destroy_net(debug)
    LAN2 = NET("LAN2")
    LAN2.destroy_net(debug)

else:
    # Si la orden no es válida, mostrar un mensaje de error
    print("Orden inválida")
    sys.exit(1)