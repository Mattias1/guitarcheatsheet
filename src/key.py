class Key():
    """The key class"""

    def __init__(self, startnote, scale=None):
        self.base = Key.str2note(startnote.upper())
        if scale == None:
            self.scale = Scale.default
        else:
            self.scale = scale

    def __getitem__(i):
        return self.tones[i]

    def __in__(t):
        return t in self.tones

    def getIndex(self, note):
        return Scale.getIndex(self.scale, self.base, note)

    @staticmethod
    def note2str(note):
        if note > 7: note += 1 # F
        if note > 2: note += 1 # C
        return chr(ord('A') + note // 2) + ('' if note % 2 == 0 else '#')
    @staticmethod
    def str2note(s):
        note = (ord(s[0]) - ord('A')) * 2
        if len(s) > 1:
            if s[1] == '#': note += 1
            if s[1] == 'b': note -= 1
        if note > 2: note -= 1 # C
        if note > 7: note -= 1 # F
        return note


class Scale():
    """Some scales"""
    default = [0, 2, 4, 5, 7, 9, 11]
    pentatonic = [0, 2, 4, 7, 9]
    
    @staticmethod
    def getIndex(scale, base, note):
        n = (note + 12 - base) % 12
        for i, offset in enumerate(scale):
            if offset == n:
                print("{}, str({}): {}".format(i, offset, Key.note2str(offset)))
                return i + 1
        return -1

