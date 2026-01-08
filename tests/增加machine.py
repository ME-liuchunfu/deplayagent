from data.jpa import jpacompement
from data.jpa.models import ServerMachine

server_machine = ServerMachine()
server_machine.name = 'nginx_gt'
server_machine.host = '192.100.29.131'
server_machine.port = 22
server_machine.username = 'root'
server_machine.password = 'root'
server_machine.remark = 'nginx网关'
jpacompement.JpaServerMachine.add_machine(server_machine)