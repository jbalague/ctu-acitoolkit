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

Tenant.subscribe(session)

while True:
    if Tenant.has_events(session):
        tenant = Tenant.get_event(session)
        if tenant.is_deleted():
            print('Tenant', tenant.name, 'has been deleted.')
        else:
            print('Tenant', tenant.name, 'has been created or modified.')
