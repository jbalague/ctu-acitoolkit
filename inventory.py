from acitoolkit.acitoolkit import *
from acitoolkit.aciphysobject import *

LOGIN = 'admin'
PASSWORD = 'password'
IPADDR = 'one.apic.local'
URL = 'https://' + IPADDR

session = Session(URL, LOGIN, PASSWORD)
resp = session.login()
if not resp.ok:
    print('%% Could not login to APIC')
    sys.exit(0)

def print_inventory(item):
    """
    Display routine
    :param item: Object to print
    :return: None
    """
    for child in item.get_children():
        print_inventory(child)
    print(item.info())

# Print the inventory of each Pod
pods = Pod.get(session)
for pod in pods:
    pod.populate_children(deep=True)
    pod_name = 'Pod: %s' % pod.name
    print(pod_name)
    print('=' * len(pod_name))
    print_inventory(pod)
