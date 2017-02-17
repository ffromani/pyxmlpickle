pyxmlpickle
============
(c) 2017 Red Hat inc.


Overview
--------

python2 module to pickle objects to/from XML.
Works under the key assumption that dictionary keys are always and only strings.

The supported objects are actually a subset of picklable objects:

- dict
- list
- set
- frozenset
- tuple
- int
- float
- bool
- str

TODO
----

Roughly ordered in decreasing priority

0. finalize the format
1. ~~load functions~~
2. namespace handling
3. ~~tests (100% coverage)~~
4. docs
5. ~~proper python packaging~~
6. PyPI entry


Examples
--------

object:
  
    custom = {
      'containerType': [
        'docker',
        'rkt'
      ],
      'containerImage': 'redis',
        'driveMap': {
          'vda': '/data',
        },
    }
    

XML:

    
    <?xml version="1.0" ?>
    <pyxmlpickle>
      <value type="dict">
        <item key="containerType" type="list">
          <item index="0" type="str">docker</item>
          <item index="1" type="str">rkt</item>
        </item>
        <item key="containerImage" type="str">redis</item>
        <item key="driveMap" type="dict">
          <item key="vda" type="str">/data</item>
        </item>
      </value>
    </pyxmlpickle>
    

check demo.py for more


License
-------

GPLv2 (perhaps dual MIT/GPL in the future)
