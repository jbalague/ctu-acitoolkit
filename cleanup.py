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
tenant = Tenant('Test-1')
tenant.mark_as_deleted()
resp = tenant.push_to_apic(session)

# Delete Tenant
tenant = Tenant('Test-2')
tenant.mark_as_deleted()
resp = tenant.push_to_apic(session)

# Delete contracts
commonTenant = Tenant('common',)
filter = Filter('entry11_Filter', commonTenant)
filter.mark_as_deleted()

filter = Filter('entry21_Filter', commonTenant)
filter.mark_as_deleted()

filter = Filter('entry31_Filter', commonTenant)
filter.mark_as_deleted()
resp = commonTenant.push_to_apic(session)

# Delete contracts
commonTenant = Tenant('common',)
contract = Contract('contract-1', commonTenant)
contract.mark_as_deleted()

contract = Contract('contract-2', commonTenant)
contract.mark_as_deleted()

contract = Contract('contract-3', commonTenant)
contract.mark_as_deleted()
resp = commonTenant.push_to_apic(session)
