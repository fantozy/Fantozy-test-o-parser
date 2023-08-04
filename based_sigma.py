import json


class Client:

    client_id: int = None

    @staticmethod
    def read_chat():
        with open('chat.json', 'r') as f:
            chat = json.load(f)
        return chat

    @classmethod
    def save_client_id(cls, client_id: int):
        cls.client_id = client_id
        chat = cls.read_chat()
        chat['client_id'] = cls.client_id
        with open('chat.json', 'w') as f:
            json.dump(chat, f)

    @classmethod
    def get_client_id(cls):
        chat = cls.read_chat()
        return chat['client_id']


    @classmethod
    def clear_chat(cls):
        with open('chat.json', 'w') as f:
            json.dump({}, f)
