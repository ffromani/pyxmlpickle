#!/usr/bin/python

from xml.dom import minidom
import pprint

import xmlpickle


def prettify(s):
    return minidom.parseString(s).toprettyxml(indent="  ")


custom = {
        'containerType': ['docker', 'rkt'],
        'containerImage': 'redis',
        'driveMap': {
            'vda': '/data',
        },
}

for obj in (custom, 1, 'a'):
    print('-' * 42)
    print "* demo object: %s" % pprint.pformat(obj)
    x = xmlpickle.dumps(obj)
    print('  as XML:\n%s' % prettify(x))
    y = xmlpickle.loads(x)
    print('  back  : %s' % pprint.pformat(y))
    print('  status: %s' % ('OK' if obj == y else 'FAIL'))
