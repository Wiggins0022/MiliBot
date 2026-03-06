from abc import ABC

class BaseModel(ABC):
    def __init__(self,model_name):
        self.model_name = model_name

    def generator(self):
        pass