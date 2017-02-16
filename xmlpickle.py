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


def dump(obj, root=None):
    if root is None:
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


def _dump_dict(obj, parent):
    node = parent
    node.attrib['type'] = 'dict'
    for key, val in obj.items():
        itemelem = ET.SubElement(node, 'item', key=str(key))
        _dump(val, itemelem)
    return node


def _dump_list(obj, parent):
    node = parent
    node.attrib['type'] = 'list'
    for idx, val in enumerate(obj):
        itemelem = ET.SubElement(node, 'item', index=str(idx))
        _dump(val, itemelem)
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


def load(node):
    return object()


def dumps(obj):
    return ET.tostring(dump(obj), encoding='UTF-8')


def loads(xml_string):
    return load(ET.fromstring(xml_string))
