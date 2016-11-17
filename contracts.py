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

all_contracts = []
consuming = {}
providing = {}
    tenants = Tenant.get_deep(session)
for tenant in sorted(tenants):
    print 'Tenant', tenant.name
    contracts = tenant.get_children(Contract)
    for contract in sorted(contracts):
        all_contracts.append(contract.name)
        print '  Owns Contract', contract.name
        for subject in contract.get_children(ContractSubject):
            print '    With ContractSubject', subject.name
            for filter in subject.get_filters():
                print '      Filter', filter.name
                for entry in filter.get_children(FilterEntry):
                    print '        Entry', entry.name, entry.etherT, entry.prot, entry.sFromPort, entry.sToPort, entry.dFromPort, entry.dToPort
    app_profiles = tenant.get_children(AppProfile)
    for app_profile in sorted(app_profiles):
        epgs = app_profile.get_children(EPG)
        for epg in sorted(epgs):
            contracts = epg.get_all_consumed()
            for contract in sorted(contracts):
                if contract.name in consuming:
                    consuming[contract.name].append(tenant.name + '/' + app_profile.name + '/' + epg.name)
                else:
                    consuming[contract.name] = [tenant.name + '/' + app_profile.name + '/' + epg.name]
                print '  EPG', epg.name, 'in AppProfile', app_profile.name, 'consumes Contract', contract.name
            contracts = epg.get_all_provided()
            for contract in sorted(contracts):
                if contract.name in providing:
                    providing[contract.name].append(tenant.name + '/' + app_profile.name + '/' + epg.name)
                else:
                    providing[contract.name] = [tenant.name + '/' + app_profile.name + '/' + epg.name]
                print '  EPG', epg.name, 'in AppProfile', app_profile.name, 'provides Contract', contract.name

print ' '
print 'Contracts not used'
for contract in all_contracts:
    if contract not in providing.keys() and contract not in consuming.keys():
        print ' ', contract

print ' '
print 'Contracts not provided but consumed'
for contract in all_contracts:
    if contract not in providing.keys() and contract in consuming.keys():
        print ' ', contract

print ' '
print 'Contracts provided but not consumed'
for contract in all_contracts:
    if contract in providing.keys() and contract not in consuming.keys():
        print ' ', contract

print ' '
print '+-{0:50}-+-{1:50}-+-{2:50}-+'.format('-'*50, '-'*50, '-'*50)
print '| {0:50} | {1:50} | {2:50} |'.format('Consumer', 'Contract', 'Provider')
print '+-{0:50}-+-{1:50}-+-{2:50}-+'.format('-'*50, '-'*50, '-'*50)
for contract in sorted(consuming.keys()):
    for consumer in sorted(consuming[contract]):
        if contract in providing:
            for provider in sorted(providing[contract]):
                print '| {0:50} | {1:50} | {2:50} |'.format(consumer, contract, provider)
        else:
            print '| {0:50} | {1:50} | {2:50} |'.format(consumer, contract, '')
                # print consumer, 'is consuming contract', contract, 'provided by', provider
print '+-{0:50}-+-{1:50}-+-{2:50}-+'.format('-'*50, '-'*50, '-'*50)

print ' '
print '+-{0:50}-+-{1:50}-+-{2:50}-+'.format('-'*50, '-'*50, '-'*50)
print '| {0:50} | {1:50} | {2:50} |'.format('Provider', 'Contract', 'Consumer')
print '+-{0:50}-+-{1:50}-+-{2:50}-+'.format('-'*50, '-'*50, '-'*50)
for contract in sorted(providing.keys()):
    for provider in sorted(providing[contract]):
        if contract in consuming:
            for consumer in sorted(consuming[contract]):
                print '| {0:50} | {1:50} | {2:50} |'.format(provider, contract, consumer)
        else:
            print '| {0:50} | {1:50} | {2:50} |'.format(provider, contract, '')
                # print provider, 'is providing contract', contract, 'consumed by', consumer
print '+-{0:50}-+-{1:50}-+-{2:50}-+'.format('-'*50, '-'*50, '-'*50)
