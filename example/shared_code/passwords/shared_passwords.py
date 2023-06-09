"""Handle the API Key storage used with OpenAI"""

import os
import pickle


class passwords_repo:
    """A class that handles a shared_password

    This class is responsible for storing locally on the hard-disk using pickle on a str object
    """

    def __init__(self) -> None:
        os.makedirs(self.__password_folder(), mode=777, exist_ok=True)

    def __password_folder(self) -> str:
        path = os.getenv('APPDATA')
        return path + "\\shared_repo\\PassKeys"

    def __password_file_path(self) -> str:
        return self.__password_folder() + "\\PASS_KEY"

    def __get_password_key(self, key: str) -> str:
        print(f"Please enter your Password for {key}...")
        password = input()

        return password

    def get_password_key(self, key: str) -> str:
        try:

            load_file = open(self.__password_file_path(), "rb")
            ret = pickle.load(load_file)
            ret = ret[key]
            load_file.close()

        except FileNotFoundError:
            load_file = open(self.__password_file_path(), "wb")
            pickle.dump({}, load_file)
            load_file.close()
            return self.get_password_key(key)

        except KeyError:
            load_file = open(self.__password_file_path(), "rb")
            current_file = pickle.load(load_file)
            load_file.close()

            load_file = open(self.__password_file_path(), "wb")
            password = self.__get_password_key(key)
            pickle.dump(current_file | {key: password}, load_file)
            load_file.close()
            return self.get_password_key(key)

        return ret
