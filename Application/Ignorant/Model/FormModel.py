from Framework.DBAPIFactory import DBAPIFactory
from Framework.FrameModel import FrameModel
import re

class GuiModel(FrameModel):
    def __init__(self, parent):
        FrameModel.__init__(self, parent)

    def get_widgets_dict(self, files_api):
        """
        First gets documents by opening them and parsing them throw the parser in the Serializer module
        Then deserializes all documents throw the Serializer
        :param files_api
        :return widgets dictionary
        """
        documents = self._get_documents(files_api)
        widgets_dictionary = {}
        for key, value in documents.items():
            db_api_fact = DBAPIFactory()
            serializer = db_api_fact.get_database_api(key)
            widgets_dictionary[value[0]] = serializer.deserialize_doc(value[1])
        return widgets_dictionary

    def _get_documents(self, files_api):
        """
        First open the files, then parses the documents throw the parser in the Serializer module
        :param files_api:
        :return: document
        """
        documents = {}
        for file_api in files_api:
            file_name, api = file_api
            file = open(file=file_name, mode="r", encoding="UTF-8")
            document = self.parser.parse(file)
            doc_name = self._get_doc_name(file_name)
            documents[api] = (doc_name, document)
        return documents

    def _get_doc_name(self, file_name):

        pattern = re.compile("^([a-zA-Z_\-]*[\\\|/])*([a-zA-Z_\-]*){1}(.json|.xml)$")
        match = pattern.match(file_name)
        if match:
            return match.group(2)
