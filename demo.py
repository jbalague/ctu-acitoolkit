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


# Create contracts in tenant common
#
#
commonTenant = Tenant('common',)
commonTenant_defaultVRF = Context('default', commonTenant)

commonTenant = Tenant('common',)
contract1 = Contract('contract-1', commonTenant)
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

contract2 = Contract('contract-2', commonTenant)
entry21 = FilterEntry('entry21',
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

contract3 = Contract('contract-3', commonTenant)
entry31 = FilterEntry('entry31',
                     applyToFrag='no',
                     arpOpc='unspecified',
                     dFromPort='3306',
                     dToPort='3306',
                     etherT='ip',
                     prot='tcp',
                     sFromPort='1',
                     sToPort='65535',
                     tcpRules='unspecified',
                     parent=contract3)

# Send configuration to APIC
resp = commonTenant.push_to_apic(session)

# Create Tenants
#
# Tenant 1
tenant1 = Tenant('Test-1')

# Networking
bd1 = BridgeDomain('BD-1', tenant1)
bd1.add_context(commonTenant_defaultVRF)

bd2 = BridgeDomain('BD-2', tenant1)
bd2.add_context(commonTenant_defaultVRF)

net1 = Subnet('Subnet-1', bd1)
net1.set_addr('10.25.226.1/24')
net1.set_scope('public')

net1 = Subnet('Subnet-2', bd1)
net1.set_addr('10.25.227.1/24')
net1.set_scope('public')

# Application
app1 = AppProfile('AP-1', tenant1)
epg1 = EPG('EPG-1', app1)
epg1.add_bd(bd1)

app2 = AppProfile('AP-2', tenant1)
epg2 = EPG('EPG-2', app2)
epg2.add_bd(bd1)

app3 = AppProfile('AP-3', tenant1)
epg3 = EPG('EPG-3', app3)
epg3.add_bd(bd2)

# Tenant 2
tenant2 = Tenant('Test-2')

# Networking
bd21 = BridgeDomain('BD-1', tenant2)
bd21.add_context(commonTenant_defaultVRF)

net21 = Subnet('Subnet-1', bd21)
net21.set_addr('10.25.228.1/24')
net21.set_scope('public')

# Application
app21 = AppProfile('AP-1', tenant2)
epg21 = EPG('EPG-1', app21)
epg21.add_bd(bd21)

epg22 = EPG('EPG-2', app21)
epg22.add_bd(bd21)

# Contract usage
#
# Contract 1
epg21.provide(contract1)
epg1.consume(contract1)
epg2.consume(contract1)
epg22.consume(contract1)

# Contract 2
epg1.provide(contract2)
epg22.consume(contract2)

# Contract 3
epg21.provide(contract3)
epg1.consume(contract3)


# Send configuration to APIC
#print tenant1.get_json()
resp = tenant1.push_to_apic(session)
resp = tenant2.push_to_apic(session)
