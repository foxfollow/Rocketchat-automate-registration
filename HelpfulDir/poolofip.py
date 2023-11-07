var = """2
4
5
6
7
9
10
12
14
16
17
18
19
24
26
27
29
31
32
34
35
36
39
40
"""

x = var.split()
ips = []
for i in x:
    ips.append(f"10.122.{i}.113")
print(",".join(ips))

# wget https://repo.zabbix.com/zabbix/6.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_6.4-1+ubuntu22.04_all.deb
# dpkg -i zabbix-release_6.4-1+ubuntu22.04_all.deb
# apt update
# apt install zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts zabbix-agent

