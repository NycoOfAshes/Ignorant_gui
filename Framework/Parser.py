import re
import json
from xml.etree import cElementTree as Tree


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
