#!/usr/bin/python

import sys
import unittest

import pytest

import xmlpickle

        
class _DummyClass(object):
    pass


class XMLPickleTests(unittest.TestCase):

    def test_pod_object_roundtrip1(self):
        obj = {
            'containerType': [
                'docker',
                'rkt'
            ],
            'enabled': True,
            'containerImage': 'redis',
            'driveMap': {
                'vda': '/data',
            },
            'memoryMegs': 4096,
            'maxLoad': 0.99,
        }
        serialized = xmlpickle.dumps(obj)
        rebuilt = xmlpickle.loads(serialized)
        assert obj == rebuilt

    def test_pod_object_roundtrip2(self):
        obj = [
            1,
            {
                'foo': 'bar',
            },
            False,
        ]
        serialized = xmlpickle.dumps(obj)
        rebuilt = xmlpickle.loads(serialized)
        assert obj == rebuilt

    def test_dumps_user_defined_objects(self):
        inst = _DummyClass()
        with pytest.raises(xmlpickle.Unpicklable):
            xmlpickle.dumps(inst)

    def test_dumps_nested_user_defined_objects(self):
        obj = [
            1,
            {
                'foo': 'bar',
            },
            False,
            _DummyClass(),
        ]

        with pytest.raises(xmlpickle.Unpicklable):
            xmlpickle.dumps(obj)

    def test_load_wrong_root(self):
        XML = u"""<?xml version='1.0' encoding='UTF-8'?>
        <pyxmlpickle>
          <value type="dict">
            <item key="maxLoad" type="float">0.99</item>
          </value>
        </pyxmlpickle>
        """
        with pytest.raises(xmlpickle.Malformed):
            obj = xmlpickle.loads(XML, root="foobar")

    def test_load_no_value(self):
        XML = u"""<?xml version='1.0' encoding='UTF-8'?>
        <pyxmlpickle>
          <foobar type="dict">
            <item key="memoryMegs" type="int">4096</item>
          </foobar>
        </pyxmlpickle>
        """
        with pytest.raises(xmlpickle.Malformed):
            obj = xmlpickle.loads(XML)

    def test_load_unknown_type(self):
        XML = u"""<?xml version='1.0' encoding='UTF-8'?>
        <pyxmlpickle>
          <value type="dict">
            <item key="memoryMegs" type="megs">4096</item>
          </value>
        </pyxmlpickle>
        """
        with pytest.raises(xmlpickle.Malformed):
            obj = xmlpickle.loads(XML)

    def test_load_dict_without_key(self):
        XML = u"""<?xml version='1.0' encoding='UTF-8'?>
        <pyxmlpickle>
          <value type="dict">
            <item type="float">0.99</item>
            <item key="containerType" type="list">
              <item index="0" type="str">docker</item>
              <item index="1" type="str">rkt</item>
            </item>
            <item key="memoryMegs" type="int">4096</item>
            <item key="driveMap" type="dict">
              <item key="vda" type="str">/data</item>
            </item>
            <item key="containerImage" type="str">redis</item>
            <item key="enabled" type="bool">True</item>
          </value>
        </pyxmlpickle>
        """
        with pytest.raises(xmlpickle.Malformed):
            obj = xmlpickle.loads(XML)

    def test_load_dict_without_type(self):
        XML = u"""<?xml version='1.0' encoding='UTF-8'?>
        <pyxmlpickle>
          <value type="dict">
            <item key="maxLoad" type="float">0.99</item>
            <item key="memoryMegs">4096</item>
          </value>
        </pyxmlpickle>
        """
        with pytest.raises(xmlpickle.Malformed):
            obj = xmlpickle.loads(XML)

    def test_load_list_without_index(self):
        XML = u"""<?xml version='1.0' encoding='UTF-8'?>
        <pyxmlpickle>
          <value type="list">
            <item type="float">0.99</item>
          </value>
        </pyxmlpickle>
        """
        with pytest.raises(xmlpickle.Malformed):
            obj = xmlpickle.loads(XML)

    def test_load_list_without_type(self):
        XML = u"""<?xml version='1.0' encoding='UTF-8'?>
        <pyxmlpickle>
          <value type="list">
            <item index="0" type="float">0.99</item>
            <item index="1">4096</item>
          </value>
        </pyxmlpickle>
        """
        with pytest.raises(xmlpickle.Malformed):
            obj = xmlpickle.loads(XML)
