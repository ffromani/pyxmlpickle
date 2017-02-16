#
# Copyright 2017 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#
from __future__ import absolute_import


import xml.etree.ElementTree as ET


class Unpicklable(Exception):
    pass


def dump(obj, parent=None):
    if parent is None:
        root = ET.Element('pyxmlpickle')
        parent = ET.SubElement(root, 'value')
    _dump(obj, parent)
    return root


def _dump(obj, parent):
    if isinstance(obj, dict):
        return _dump_dict(obj, parent)
    if isinstance(obj, list):
        return _dump_list(obj, parent)
    if (isinstance(obj, tuple) or isinstance(obj, set) or
        isinstance(obj, frozenset)
    ):
        return _dump_list(obj, parent)
    return _dump_type(obj, parent)


def _dump_dict_pedantic(obj, parent):
    node = ET.SubElement(parent, 'pydict')
    for key, val in obj.items():
        itemelem = ET.SubElement(node, 'item')
        keyelem = ET.SubElement(itemelem, 'key')
        _dump(key, keyelem)
        valelem = ET.SubElement(itemelem, 'value')
        _dump(val, valelem)
    return node


def _dump_dict(obj, parent):
#    node = ET.SubElement(parent, 'pydict')
    node = parent
    node.attrib['type'] = 'dict'
    for key, val in obj.items():
        itemelem = ET.SubElement(node, 'item', key=str(key))
        _dump(val, itemelem)
    return node


def _dump_list(obj, parent):
#    node = ET.SubElement(parent, 'pylist')
    node = parent
    node.attrib['type'] = 'list'
    for idx, val in enumerate(obj):
        itemelem = ET.SubElement(node, 'item', index=str(idx))
        _dump(val, itemelem)
    return node


def _dump_type_pedantic(obj, parent):
    if isinstance(obj, bool):
        tag = "pybool"
    elif isinstance(obj, int):
        tag = "pyint"
    elif isinstance(obj, float):
        tag = "pyfloat"
    elif isinstance(obj, str):
        tag = "pystr"
    else:
        raise Unpicklable(repr(obj))
    x = ET.SubElement(parent, tag)
    x.text = str(obj)
    return x


def _dump_type(obj, parent):
    if isinstance(obj, bool):
        tag = "bool"
    elif isinstance(obj, int):
        tag = "int"
    elif isinstance(obj, float):
        tag = "float"
    elif isinstance(obj, str):
        tag = "str"
    else:
        raise Unpicklable(repr(obj))
#    x = ET.SubElement(parent, 'value')
    x = parent
    x.attrib['type'] = tag
    x.text = str(obj)
    return x


def load(node):
    return object()


def dumps(obj):
    return ET.tostring(dump(obj), encoding='UTF-8')


def loads(xml_string):
    return load(ET.fromstring(xml_string))
