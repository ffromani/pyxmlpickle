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



# used as namespace
class Tags(object):
    ROOT = 'pyxmlpickle'
    VALUE = 'value'
    ITEM = 'item'


# used as namespace
class Attrib(object):
    TYPE = 'type'
    INDEX = 'index'
    KEY = 'key'


def _dump_dict(obj, node):
    node.attrib[Attrib.TYPE] = 'dict'
    for key, val in obj.items():
        itemelem = ET.SubElement(node, Tags.ITEM, key=str(key))
        _dump(val, itemelem)
    return node


def _dump_list(obj, node):
    node.attrib[Attrib.TYPE] = 'list'
    for idx, val in enumerate(obj):
        itemelem = ET.SubElement(node, Tags.ITEM, index=str(idx))
        _dump(val, itemelem)
    return node


def _dump(obj, parent):
    if isinstance(obj, dict):
        return _dump_dict(obj, parent)
    elif isinstance(obj, list):
        return _dump_list(obj, parent)
    elif isinstance(obj, bool):
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
    x.attrib[Attrib.TYPE] = tag
    x.text = str(obj)
    return x


def _load_dict(node):
    ret = {}
    for item in node.findall('./item'):
        key = item.attrib.get(Attrib.KEY)
        ntype = item.attrib.get(Attrib.TYPE)
        if key is None or ntype is None:
            raise Malformed()
        ret[str(key)] = _load(item, ntype)
    return ret


def _load_list(node):
    ret = []
    for item in node.findall('./item'):
        idx = item.attrib.get(Attrib.INDEX)
        ntype = item.attrib.get(Attrib.TYPE)
        if idx is None or ntype is None:
            raise Malformed()
        ret.append(_load(item, ntype))
    return ret


def _load(node, ntype):
    ntype = ntype.lower()
    if ntype == 'dict':
        return _load_dict(node)
    elif ntype == 'list':
        return _load_list(node)
    elif ntype == 'bool':
        return bool(node.text.lower() == 'true')
    elif ntype == 'int':
        return int(node.text)
    elif ntype == 'float':
        return float(node.text)
    elif ntype == 'str':
        return str(node.text)
    raise Malformed()


def dump(obj, root=None):
    if root is None:
        root = ET.Element(Tags.ROOT)
    parent = ET.SubElement(root, Tags.VALUE)
    _dump(obj, parent)
    return root


def load(node, root=None):
    if root is None:
        root = Tags.ROOT
    if node.tag != root:
        raise Malformed()
    value = node.find('./%s' % Tags.VALUE)
    if value is None:
        raise Malformed()
    return _load(value, value.attrib.get(Attrib.TYPE))


def dumps(obj):
    return ET.tostring(dump(obj), encoding='UTF-8')


def loads(xml_string, root=None):
    return load(ET.fromstring(xml_string), root=root)
