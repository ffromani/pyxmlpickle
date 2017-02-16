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


ROOT = 'pyxmlpickle'


class Malformed(Exception):
    pass


class Unpicklable(Exception):
    pass


def dump(obj, strict=False, root=None):
    if root is None:
        root = ET.Element(ROOT)
    parent = ET.SubElement(root, 'value')
    _dump(obj, parent, strict=strict)
    return root


def _dump(obj, parent, strict=False):
    if isinstance(obj, dict):
        return _dump_dict(obj, parent)
    if isinstance(obj, list):
        return _dump_list(obj, parent)
    if (isinstance(obj, tuple) or isinstance(obj, set) or
        isinstance(obj, frozenset)
    ):
        if strict:
            raise Unpicklable()
        return _dump_list(obj, parent, strict=strict)
    return _dump_type(obj, parent)


def _dump_dict(obj, parent, strict=False):
    node = parent
    node.attrib['type'] = 'dict'
    for key, val in obj.items():
        itemelem = ET.SubElement(node, 'item', key=str(key))
        _dump(val, itemelem, strict=strict)
    return node


def _dump_list(obj, parent, strict=False):
    node = parent
    node.attrib['type'] = 'list'
    for idx, val in enumerate(obj):
        itemelem = ET.SubElement(node, 'item', index=str(idx))
        _dump(val, itemelem, strict=strict)
    return node


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
    x = parent
    x.attrib['type'] = tag
    x.text = str(obj)
    return x


def _load_dict(node):
    ret = {}
    for item in node.findall('./item'):
        key = item.attrib.get('key')
        ntype = item.attrib.get('type')
        if key is None or ntype is None:
            raise Malformed()
        ret[str(key)] = _load(item, ntype)
    return ret


def _load_list(node):
    ret = []
    for item in node.findall('./item'):
        idx = item.attrib.get('index')
        ntype = item.attrib.get('type')
        if idx is None or ntype is None:
            raise Malformed()
        ret.append(_load(item, ntype))
    return ret


def _load_type(node, ntype):
    if ntype is None:
        raise Malformed()
    ntype = ntype.lower()
    if ntype == 'bool':
        return bool(node.text.lower() == 'true')
    elif ntype == 'int':
        return int(node.text)
    elif ntype == 'float':
        return float(node.text)
    elif ntype == 'str':
        return str(node.text)
    return Malformed()


def _load(node, ntype):
    if ntype == 'dict':
        return _load_dict(node)
    elif ntype == 'list':
        return _load_list(node)
    return _load_type(node, node.attrib.get('type'))


def load(node, root=None):
    if root is None:
        root = ROOT
    if node.tag != root:
        raise Malformed()
    value = node.find('./value')
    if value is None:
        raise Malformed()
    return _load(value, value.attrib.get('type'))


def dumps(obj):
    return ET.tostring(dump(obj), encoding='UTF-8')


def loads(xml_string):
    return load(ET.fromstring(xml_string))
