from Serializers import *

class GuiModel:
    def __init__(self, parent):
        self.parent = parent

    def get_objects_models(self, **kwargs):
        documents = self._get_documents(**kwargs)
        models_dictionary = {}
        for key, value in documents.items():
            parser = SerializerFactory().create(key)
            models_dictionary[key] = parser.deserialize_doc(value)
        return models_dictionary

    def _get_documents(self, **kwargs):
        documents = {}
        for key, value in kwargs.items():
            file = open(file=value, mode="r", encoding="UTF-8")
            document = Parser().parse(file)
            documents[key] = document
        return documents