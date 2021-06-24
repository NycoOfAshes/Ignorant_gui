from Framework.XmlTreeSerializer import XmlTreeSerializer
from Framework.JsonObjectSerializer import JsonSerializer


class DBAPIFactory:

    def get_database_api(self, api_name):

        if api_name == "JsonObjectSerializer":
            return JsonSerializer()
        elif api_name == "XmlTreeSerializer":
            return XmlTreeSerializer()

