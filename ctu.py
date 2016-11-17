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


# Create Tenants
#
# Tenant 1
tenant1 = Tenant('Test-1')

# Send configuration to APIC
print tenant1.get_json()
resp = tenant1.push_to_apic(session)
if not resp.ok:
    print("%% Oops, something didn't work!")
    sys.exit(0)
