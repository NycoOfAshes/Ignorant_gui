from Serializers import *


class GuiModel:
    def __init__(self, parent):
        self.parent = parent

    def get_objects_models(self, **kwargs):
        """
        First gets documents by opening them and parsing them throw the parser in the Serializer module
        Then deserializes all documents throw the Serializer
        :param kwargs:
        :return: models_dictionary
        """
        documents = self._get_documents(**kwargs)
        models_dictionary = {}
        for key, value in documents.items():
            parser = SerializerFactory().create(key)
            models_dictionary[key] = parser.deserialize_doc(value)
        return models_dictionary

    def _get_documents(self, **kwargs):
        """
        First open the files, then parses the documents throw the parser in the Serializer module
        :param kwargs:
        :return: document
        """
        documents = {}
        for key, value in kwargs.items():
            file = open(file=value, mode="r", encoding="UTF-8")
            document = Parser().parse(file)
            documents[key] = document
        return documents
