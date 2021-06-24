from abc import abstractmethod


class Serializer:

    @abstractmethod
    def deserialize_doc(self, doc):
        pass