from Framework.Serializer import Serializer
import re


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