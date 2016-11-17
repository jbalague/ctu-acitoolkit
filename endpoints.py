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
endpoints = Endpoint.get(session)
for ep in endpoints:
    epg = ep.get_parent()
    app_profile = epg.get_parent()
    tenant = app_profile.get_parent()
    data.append((ep.mac, ep.ip, ep.if_name, ep.encap,
                 tenant.name, app_profile.name, epg.name))

# Display the data downloaded
col_widths = [19, 17, 20, 10, 20, 20, 20]
template = ''
for idx, width in enumerate(col_widths):
    template += '{%s:%s} ' % (idx, width)
print(template.format("MACADDRESS", "IPADDRESS", "INTERFACE",
                      "ENCAP", "TENANT", "APP PROFILE", "EPG"))
fmt_string = []
for i in range(0, len(col_widths)):
    fmt_string.append('-' * (col_widths[i] - 2))
print(template.format(*fmt_string))
for rec in data:
    print(template.format(*rec))
