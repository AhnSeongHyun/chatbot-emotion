class Message(object):

    def __init__(self):
        self.text_list = []

    def append(self, text):
        self.text_list.append(text)

    def to_dict(self):
        return {
            "messages":  self.text_list
        }