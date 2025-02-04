#PC1
#Mateo Sarria Franco de Sarabia
#Rafael Bueno Castro
#Jacobo España-Heredia Beteta
import logging
import subprocess

# Configuración del logger
log = logging.getLogger('manage-p2')

class VM:
    def __init__(self, name):
        self.name = name
        # Inicialización de la VM con el nombre especificado.
        # Descomentar si se necesita traza de depuración
        # log.debug('init VM ' + self.name + " ejecutado con exito")

    def create_vm(self, nServ, debug):
        # Crear la máquina virtual
        if debug:
            log.debug("Inicio create_vm " + self.name)

        # Crear imagen de disco utilizando qemu-img
        subprocess.call([f"qemu-img create -F qcow2 -f qcow2 -b cdps-vm-base-pc1.qcow2 {self.name}.qcow2"], shell=True)

        # Crear archivo XML para la VM, basado en una plantilla
        f1 = open("plantilla-vm-pc1.xml", 'r')
        f2 = open(f"{self.name}.xml", 'w')

        # Modificar el archivo XML dependiendo del nombre de la VM
        if self.name == "lb":  # XML para el balanceador de carga (lb)
            if debug:
                log.debug("Entra XML lb")
            for line in f1:
                if "<name>XXX</name>" in line:
                    f2.write(f"<name>{self.name}</name>\n")
                elif "<source file='/mnt/tmp/XXX/XXX.qcow2'/>" in line:
                    f2.write(f"<source file='/mnt/tmp/msarria/{self.name}.qcow2'/>\n")
                elif "<source bridge='XXX'/>" in line:
                    f2.write("<source bridge='LAN1'/>\n")
                elif "</interface>" in line:
                    f2.write("</interface>\n<interface type='bridge'>\n<source bridge='LAN2'/>\n<model type='virtio'/>\n</interface>\n")
                else:
                    f2.write(line)
        else:  # XML para otras máquinas como c1, s1, s2...
            if debug:
                log.debug("Entra XML OTROS")
            for line in f1:
                if "<name>XXX</name>" in line:
                    f2.write(f"<name>{self.name}</name>\n")
                elif "<source file='/mnt/tmp/XXX/XXX.qcow2'/>" in line:
                    f2.write(f"<source file='/mnt/tmp/msarria/{self.name}.qcow2'/>\n")
                elif "<source bridge='XXX'/>" in line:
                    if self.name[0] == "s":
                        f2.write("<source bridge='LAN2'/>\n")
                    else:
                        f2.write("<source bridge='LAN1'/>\n")
                else:
                    f2.write(line)
            
        f1.close()
        f2.close()

        # Crear y copiar el hostname a la VM
        f = open("temp/hostname", 'w')
        f.write(self.name)
        f.close()
        subprocess.call([f"sudo virt-copy-in -a {self.name}.qcow2 /etc/hostname /etc"], shell=True)

        # Modificar /etc/hosts en la VM
        f2 = open("temp/hosts", 'w')
        f2.write(f"127.0.1.1 {self.name}\n127.0.0.1 localhost")
        f2.close()
        subprocess.call([f"sudo virt-copy-in -a {self.name}.qcow2 temp/hosts /etc"], shell=True)

        # Crear y copiar interfaces
        f = open("temp/interfaces", 'w')
        if self.name[0] == "s":
            ff = open("temp/index.html", 'w')
            ff.write(f"{self.name}\n")
            ff.close()
            subprocess.call([f"sudo virt-copy-in -a {self.name}.qcow2 temp/index.html /var/www/html"], shell=True)
            
            f.write(f"auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.1.2.1{self.name[1]}\nnetwork 10.1.2.0\nnetmask 255.255.255.0\ngateway 10.1.2.1")
            
            ff = open("temp/rc.local", 'w')
            ff.write("#!/bin/bash\nsudo /etc/init.d/apache2 restart\nexit 0\n")
            ff.close()
            subprocess.call([f"chmod 755 temp/rc.local"], shell=True)
            subprocess.call([f"sudo virt-copy-in -a {self.name}.qcow2 temp/rc.local /etc"], shell=True)
            
        elif self.name == "c1":
            f.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.1.1.2\nnetwork 10.1.1.0\nnetmask 255.255.255.0\ngateway 10.1.1.1")
        
        elif self.name == "lb":
            f.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.1.1.1\nnetwork 10.1.1.0\nnetmask 255.255.255.0\n\nauto eth1\niface eth1 inet static\naddress 10.1.2.1\nnetwork 10.1.2.0\nnetmask 255.255.255.0\n")
            subprocess.call(["sudo virt-edit -a lb.qcow2 /etc/sysctl.conf -e 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/'"], shell=True)
            
            # Configuración de HAProxy para el balanceador de carga
            subprocess.call([f"sudo virt-copy-out -a {self.name}.qcow2 /etc/haproxy/haproxy.cfg ."], shell=True)
            subprocess.call([f"cp haproxy.cfg temp/haproxy.cfg"], shell=True)
            subprocess.call([f"rm -f haproxy.cfg"], shell=True)
            ff=open("temp/haproxy.cfg",'a')
            ff.write("\nfrontend lb\n\tbind *:80\n\tmode http\n\tdefault_backend webservers\n\nbackend webservers\n\tmode http\n\tbalance roundrobin\n")
            for i in range(1, nServ + 1):
                ff.write(f"\tserver s{i} 10.1.2.1{i}:80 check\n")
            ff.close()
            
            ff=open("temp/rc.local",'w')
            ff.write("#!/bin/bash\nsudo /etc/init.d/apache2 stop\nsudo /etc/init.d/haproxy restart\nexit 0\n")
            ff.close()
            
            subprocess.call([f"chmod 755 temp/rc.local"], shell=True)
            subprocess.call([f"sudo virt-copy-in -a {self.name}.qcow2 temp/haproxy.cfg /etc/haproxy"], shell=True)
            subprocess.call([f"sudo virt-copy-in -a {self.name}.qcow2 temp/rc.local /etc"], shell=True)
            
        f.close()
        subprocess.call([f"sudo virt-copy-in -a {self.name}.qcow2 temp/interfaces /etc/network"], shell=True)
        subprocess.call([f"sudo virsh define {self.name}.xml"], shell=True)
        log.debug("create_vm " + self.name + " ejecutado con exito")

    def start_vm(self, debug):
        if debug:
            log.debug("Inicio start_vm " + self.name)
        subprocess.call([f"sudo virsh start {self.name}"], shell=True)
        subprocess.call([f"xterm -rv -sb -rightbar -fa monospace -fs 10 -title {self.name}_monitor -e watch -t 'sudo virsh dominfo {self.name}' &"], shell=True)
        log.debug("start_vm " + self.name + " ejecutado con exito")

    def show_console_vm(self, debug):
        if debug:
            log.debug("Inicio show_console_vm " + self.name)
        subprocess.call([f"xterm -rv -sb -rightbar -fa monospace -fs 10 -title {self.name}_console -e sudo virsh console {self.name} &"], shell=True)
        #subprocess.call([f'xterm -e "sudo virsh console {self.name}"&'], shell=True)
        log.debug("show_console_vm " + self.name + " ejecutado con exito")
    
    def stop_vm(self, debug):
        if debug:
            log.debug("Inicio stop_vm " + self.name)
        subprocess.call([f"sudo virsh shutdown {self.name}"], shell=True)
        subprocess.call([f"pkill -f 'xterm.*{self.name}'"], shell=True)
        log.debug("stop_vm " + self.name + " ejecutado con exito")
    
    def destroy_vm(self, debug):
        if debug:
            log.debug("Inicio destroy_vm " + self.name)
        subprocess.call([f"sudo virsh undefine {self.name}"], shell=True)
        subprocess.call([f"sudo virsh destroy {self.name}"], shell=True)
        subprocess.call([f"rm -f {self.name}.qcow2"], shell=True)
        subprocess.call([f"rm -f {self.name}.xml"], shell=True)
        subprocess.call([f"pkill -f 'xterm.*{self.name}'"], shell=True)
        log.debug("destroy_vm " + self.name + " ejecutado con exito")

class NET:
    def __init__(self, name):
        self.name = name
        # Inicialización de la red
        # Descomentar si se necesita traza de depuración
        # log.debug('init net ' + self.name + " ejecutado con exito")

    def create_net(self, debug):
        if debug:
            log.debug('Inicio create_net ' + self.name)
        # Crear bridge de red
        subprocess.call([f"sudo brctl addbr {self.name}"], shell=True)
        subprocess.call([f"sudo ifconfig {self.name} up"], shell=True)
        #subprocess.call([f"sudo ovs-vsctl add-br {self.name}"], shell=True)
        log.debug('create_net ' + self.name + " ejecutado con exito")

    def destroy_net(self, debug):
        if debug:
            log.debug('Inicio destroy_net ' + self.name)
        subprocess.call([f"sudo ifconfig {self.name} down"], shell=True)
        subprocess.call([f"sudo brctl delbr {self.name}"], shell=True)
        #subprocess.call([f"sudo ovs-vsctl del-br {self.name}"], shell=True)
        log.debug('destroy_net ' + self.name + " ejecutado con exito")
