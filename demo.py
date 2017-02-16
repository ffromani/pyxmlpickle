#!/usr/bin/python


from xml.dom import minidom

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

print(prettify(xmlpickle.dumps(custom)))
print(prettify(xmlpickle.dumps(1)))
print(prettify(xmlpickle.dumps('a')))
