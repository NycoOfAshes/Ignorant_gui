import re
import json
from xml.etree import cElementTree as Tree


class SerializerFactory:

    def create(self, key):
        """
        Returns the right serializer according to key
        :param key:
        :return: the right serializer
        """
        if key == "doc":
            return XmlTreeSerializer()
        elif key == "dic":
            return JsonSerializer()


class Serializer:
    """
    Interface Serializer
    """
    def deserialize_doc(self, doc):
        pass


class XmlTreeSerializer(Serializer):
    def __init__(self):
        self._dict = {}
        self._xml_tree = None
        self._root = None

    def deserialize_doc(self, tree):
        """
        Deserialize an xml document into a dictionary with the xml.etree api
        :param tree:
        :return: a dictionary
        """
        self._xml_tree = tree
        self._root = self._xml_tree.getroot()
        self._dict = {self._root.tag: {}}
        self._crawl_in_node(self._root, self._dict)
        return self._dict

    def _crawl_in_node(self, tree_level, dictionary=None):
        """
        Builds the dictionary by scraping the xml document
        :param tree_level:
        :param dictionary:
        :return: Non
        """
        if dictionary is None:
            dictionary = {}

        node_name = tree_level.tag
        dict_to_add = dictionary[node_name]
        if tree_level.attrib:
            dict_to_add["attribs"] = tree_level.attrib

        for i, e in enumerate(tree_level):
            if e.text:
                pattern = re.compile('^\W*$')
                match = pattern.match(e.text)
            else:
                match = True

            node_name = self._get_node_dict_name(e, dict_to_add, i)
            e.tag = node_name

            if not match:
                if e.attrib:
                    dict_to_add[node_name] = {"attribs": e.attrib}
                    dict_to_add[node_name].update({"text": e.text})
                else:
                    dict_to_add[node_name] = e.text
            else:
                dict_to_add[node_name] = {}
                self._crawl_in_node(e, dict_to_add)

    def _get_node_dict_name(self, node, dictionary, i):
        """
        Adds a number to a node tag if already exists as a dictionary key
        :param node:
        :param dictionary:
        :param i:
        :return: node tag
        """
        if node.tag in dictionary.keys():
            return node.tag + str(i)
        else:
            return node.tag


class JsonSerializer(Serializer):

    def deserialize_doc(self, dictionary):
        """
        Hydrates config text instances with the input dictionary keys, transformed keys and values
        stocks config texts in the objects_dict and returns this dictionary
        :param dictionary:
        :return: dictionary of configtext objects
        """
        objects_dict = {}
        if dictionary["object_type"] == "ConfigText":
            for key, value in dictionary.items():
                if key != "object_type":
                    pattern = re.compile('^(\w+)(_+)(\w+)$')
                    mod_key = ""
                    match = pattern.match(key)
                    if match:
                        mod_key = match.group(1)
                        mod_key = mod_key.capitalize()
                    config_text = ConfigText(key, mod_key, value)
                    objects_dict[key] = config_text

        return objects_dict


class ConfigText:
    def __init__(self, name, select_name, cnf={}):
        self.name = name
        self.select_name = select_name
        self.texts = cnf

class Parser:

    def parse(self, file):
        """
        choose the right parser according to the file extension detected
        Returns the right parsed document
        :param file:
        :return: a parsed document
        """
        file_format = self._get_file_format(file.name)
        if file_format == ".json":
            return self._parse_json(file)
        elif file_format == ".xml":
            return self._parse_xml(file)

    def _get_file_format(self, file_name):
        """
        Detects and returns a file extension
        :param file_name:
        :return: a file extension
        """
        pattern = re.compile("^([a-zA-Z_\-]*[\\\|/])*([a-zA-Z_\-]*){1}(.json|.xml)$")
        match = pattern.match(file_name)
        if match:
            return match.group(3)

    def _parse_json(self, file):
        return json.load(file)

    def _parse_xml(self, file):
        return Tree.parse(file)