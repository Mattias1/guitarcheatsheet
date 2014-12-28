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
                return i + 1
        return -1


class Chord():
    """The class representing a chord"""
    def __init__(self, *notes):
        # The notes are supposed to be a series of integers in [0, 11] with the base note as first element
        assert len(notes) > 2 
        self.notes = list(notes)
        self._name = None

    @property
    def name(self):
        if not self._name:
            self._name = self.getName()
        return self._name

    def getName(self):
        """Find the name of a chord"""
        base = Key.note2str(self.notes[0])
        l = sorted(self.transpose(-self.notes[0]).notes)

        ext = '?'
        if l == [0, 4, 7]: ext = ''
        elif l == [0, 3, 7]: ext = 'm'
        elif l == [0, 3, 6]: ext = 'dim'
        elif l == [0, 5, 7]: ext = 'sus4'
        elif l == [0, 2, 7]: ext = 'sus2'
        elif l == [0, 4, 7, 10]: ext = '7'
        elif l == [0, 3, 7, 10]: ext = 'm7'
        elif l == [0, 4, 7, 11]: ext = 'maj7'
        elif l == [0, 2, 3, 7]: ext = 'm2'

        if ext == '?':
            print('UNKNOWN CHORD - l: {}, notes: {}, transpose: {}'.format(l, self.notes, self.transpose(-self.notes[0]).notes))

        return base + ext

    @staticmethod
    def fromScale(scale, *indices):
        noteList = [scale[i] for i in list(*indices)]
        return Chord(*noteList)

    def transpose(self, difference):
        noteList = [(n + difference + 12) % 12 for n in self.notes]
        return Chord(*noteList)

    def __str__(self):
        result = self.name + ':'
        for n in self.notes:
            result += ' ' + Key.note2str(n)
        return result

