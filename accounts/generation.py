import hashlib 
import random
import string


class GenerationToken:

    def __init__(self):
        self.randomstr = self.randomString(15)

    def randomString(self, stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    def make_token(self):
        h = hashlib.md5(self.randomstr.encode())
        return h.hexdigest()