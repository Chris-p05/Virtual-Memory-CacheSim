class CacheBlock:
    def __init__(self, tag=None, valid = False):
        self.tag = tag
        self.valid = valid
    
    def get_tag(self):
        return self.tag

    def is_valid(self):
        return self.valid

    def set_tag(self, tag):
        self.tag = tag
    
    def set_valid(self, valid):
        self.valid = valid