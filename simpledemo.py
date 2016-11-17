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


# Cleanup of existing resources
#
# Delete Tenant
tenant1 = Tenant('Test-1')
tenant1.mark_as_deleted()
resp = tenant1.push_to_apic(session)



# Create Tenants
#
# Tenant 1
tenant1 = Tenant('Test-1')

# Configure Networking
#
#
defaultVRF = Context('VRF-1', tenant1)

bd1 = BridgeDomain('BD-1', tenant1)
bd1.add_context(defaultVRF)

bd2 = BridgeDomain('BD-2', tenant1)
bd2.add_context(defaultVRF)

net1 = Subnet('Subnet-1', bd1)
net1.set_addr('10.25.226.1/24')
net1.set_scope('public')

net2 = Subnet('Subnet-2', bd1)
net2.set_addr('10.25.227.1/24')
net2.set_scope('public')

net3 = Subnet('Subnet-3', bd2)
net3.set_addr('10.25.228.1/24')
net3.set_scope('public')

# Cretae Contracts
#
#
contract1 = Contract('contract-1', tenant1)
entry11 = FilterEntry('entry11',
     applyToFrag='no',
     arpOpc='unspecified',
     dFromPort='80',
     dToPort='80',
     etherT='ip',
     prot='tcp',
     sFromPort='1',
     sToPort='65535',
     tcpRules='unspecified',
     parent=contract1)

contract2 = Contract('contract-2', tenant1)
entry21 = FilterEntry('entry11',
     applyToFrag='no',
     arpOpc='unspecified',
     dFromPort='80',
     dToPort='80',
     etherT='ip',
     prot='tcp',
     sFromPort='1',
     sToPort='65535',
     tcpRules='unspecified',
     parent=contract2)
entry22 = FilterEntry('entry12',
     applyToFrag='no',
     arpOpc='unspecified',
     dFromPort='443',
     dToPort='443',
     etherT='ip',
     prot='tcp',
     sFromPort='1',
     sToPort='65535',
     tcpRules='unspecified',
     parent=contract2)


# Define Application Profiles
#
#
app1 = AppProfile('AP-1', tenant1)
epg1 = EPG('EPG-1', app1)
epg1.add_bd(bd1)

epg2 = EPG('EPG-2', app1)
epg2.add_bd(bd1)

epg3 = EPG('EPG-3', app1)
epg3.add_bd(bd2)

# Contract usage
#
#
epg3.provide(contract1)
epg3.provide(contract2)
epg1.consume(contract1)
epg2.consume(contract2)


# Send configuration to APIC
print tenant1.get_json()
resp = tenant1.push_to_apic(session)
if not resp.ok:
    print("%% Oops, something didn't work!")
    sys.exit(0)
