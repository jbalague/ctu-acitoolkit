from acitoolkit.acitoolkit import *

LOGIN = 'admin'
PASSWORD = 'password'
IPADDR = 'one.apic.local'
URL = 'https://' + IPADDR

session = Session(URL, LOGIN, PASSWORD)
resp = session.login()
if not resp.ok:
    print('%% Could not login to APIC')
    sys.exit(0)


# Download all of the interfaces
# and store the data as tuples in a list
data = []
interfaces = Interface.get(session)
for interface in interfaces:
    data.append((interface.attributes['if_name'],
                 interface.attributes['porttype'],
                 interface.attributes['adminstatus'],
                 interface.attributes['operSt'],
                 interface.attributes['operSpeed'],
                 interface.attributes['mtu'],
                 interface.attributes['usage']))

# Display the data downloaded
template = "{0:17} {1:8} {2:^6} {3:^6} {4:7} {5:6} {6:9} "
print(template.format("INTERFACE", "TYPE", "ADMIN", "OPER", "SPEED", "MTU", "USAGE"))
print(template.format("---------", "--------", "------", "------", "-----", "___", "---------"))
for rec in data:
    print(template.format(*rec))
