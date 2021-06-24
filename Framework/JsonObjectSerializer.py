from Framework.Serializer import Serializer
import re


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