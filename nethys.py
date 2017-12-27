#!python3

class SpellItem(object):
    def __init__(self):
        self.name = None
        self.description = None
        self.attrs = {}
        return

    def consolePrint(self):
        print('Spell Name: "%s"' % self.name)
        print('Spell Description: "%s"' % self.description)
        print('Spell Attributes:')
        print(self.attrs)
        return

    def toJson(self):
        return {
            'Name': self.name,
            'Description': self.description,
            'Attributes': self.attrs
        }
