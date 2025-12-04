# Maryna Korolova Part starts here >:)

class CacheBlock:
    def __init__(self):
        self.tag = None
        self.valid = False
    
    def get_tag(self):
        return self.tag

    def is_valid(self):
        return self.valid

    def set_tag(self, tag):
        self.tag = tag
    
    def set_valid(self):
        self.valid = True

    def reset_valid(self):
        self.valid = False

    def is_never_used(self):
        return self.never_used