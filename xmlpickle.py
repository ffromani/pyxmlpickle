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


class Error(Exception):
    pass


class Malformed(Error):
    pass


class Unpicklable(Error):
    pass


# used as namespace
class Attrib(object):
    TYPE = 'type'
    INDEX = 'index'
    KEY = 'key'


class Tags(object):
    ROOT = 'pyxmlpickle'
    VALUE = 'value'
    ITEM = 'item'

    def __init__(self, namespace, namespace_uri):
        self._namespace = namespace
        self._namespace_uri = namespace_uri
        if self._namespace_uri is not None:
            if self._namespace is None:
                raise Error('both namespace and namespace_uri must be given')
            ET.register_namespace(self._namespace, self._namespace_uri)

    def _tag(self, text):
        if self._namespace_uri is not None:
            return '{%s}%s' % (self._namespace_uri, text,)
        return text

    @property
    def root(self):
        return self._tag(self.ROOT)

    @property
    def value(self):
        return self._tag(self.VALUE)

    @property
    def item(self):
        return self._tag(self.ITEM)


class Codec(object):

    def __init__(self, namespace, namespace_uri):
        self._namespace = namespace
        self._namespace_uri = namespace_uri
        self._tags = Tags(namespace, namespace_uri)

    def _dump_dict(self, obj, node):
        node.attrib[Attrib.TYPE] = 'dict'
        for key, val in obj.items():
            itemelem = ET.SubElement(node, self._tags.item, key=str(key))
            self._dump(val, itemelem)
        return node

    def _dump_sequence(self, obj, seq_type, node):
        node.attrib[Attrib.TYPE] = seq_type
        for idx, val in enumerate(obj):
            itemelem = ET.SubElement(node, self._tags.item, index=str(idx))
            self._dump(val, itemelem)
        return node

    def _dump(self, obj, node):
        if isinstance(obj, dict):
            return self._dump_dict(obj, node)
        elif isinstance(obj, list):
            return self._dump_sequence(obj, 'list', node)
        elif isinstance(obj, tuple):
            return self._dump_sequence(obj, 'tuple', node)
        elif isinstance(obj, set):
            return self._dump_sequence(obj, 'set', node)
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
        node.attrib[Attrib.TYPE] = tag
        node.text = str(obj)
        return node

    def _load_dict(self, node):
        ret = {}
        for item in node.findall('./%s' % self._tags.item):
            key = item.attrib.get(Attrib.KEY)
            if key is None:
                raise Malformed()
            ret[str(key)] = self._load(item, item.attrib.get(Attrib.TYPE))
        return ret

    def _load_sequence(self, node, seq_class):
        ret = []
        for item in node.findall('./%s' % self._tags.item):
            if item.attrib.get(Attrib.INDEX) is None:
                raise Malformed()
            ret.append(self._load(item, item.attrib.get(Attrib.TYPE)))
        return seq_class(ret)

    def _load(self, node, ntype):
        if ntype is None:
            raise Malformed()
        ntype = ntype.lower()
        if ntype == 'dict':
            return self._load_dict(node)
        elif ntype == 'list':
            return self._load_sequence(node, list)
        elif ntype == 'tuple':
            return self._load_sequence(node, tuple)
        elif ntype == 'set':
            return self._load_sequence(node, set)
        elif ntype == 'bool':
            return bool(node.text.lower() == 'true')
        elif ntype == 'int':
            return int(node.text)
        elif ntype == 'float':
            return float(node.text)
        elif ntype == 'str':
            return str(node.text)
        raise Malformed()

    def dump(self, obj, root=None):
        if root is None:
            root = ET.Element(self._tags.root)
        node = ET.SubElement(root, self._tags.value)
        self._dump(obj, node)
        return root

    def load(self, node, root=None):
        if root is None:
            root = self._tags.root
        if node.tag != root:
            raise Malformed()
        value = node.find('./%s' % self._tags.value)
        if value is None:
            raise Malformed()
        return self._load(value, value.attrib.get(Attrib.TYPE))


def dump(obj, root=None, namespace=None, namespace_uri=None):
    codec = Codec(namespace, namespace_uri)
    return codec.dump(obj, root)


def load(node, root=None, namespace=None, namespace_uri=None):
    codec = Codec(namespace, namespace_uri)
    return codec.load(node, root)


def dumps(obj, namespace=None, namespace_uri=None):
    return ET.tostring(
        dump(obj, namespace=namespace, namespace_uri=namespace_uri),
        encoding='UTF-8'
    )


def loads(xml_string, root=None, namespace=None, namespace_uri=None):
    return load(
        ET.fromstring(xml_string),
        root=root,
        namespace=namespace,
        namespace_uri=namespace_uri
    )
