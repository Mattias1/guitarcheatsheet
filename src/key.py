class Key():
    """The key class"""

    def __init__(self, startnote, scale=None, mode=None):
        self.base = Key.str2note(startnote.upper())
        self.scale = scale or Scale.major
        self.mode = mode or Mode.ionian

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
    major = [0, 2, 4, 5, 7, 9, 11]
    minor = [0, 2, 3, 5, 7, 8, 10]
    pentatonic = [0, 2, 4, 7, 9]
    blues1 = [0, 2, 3, 4, 7, 9]
    blues2 = [0, 3, 5, 6, 7, 10]

    @staticmethod
    def getIndex(scale, base, note):
        n = (note + 12 - base) % 12
        for i, offset in enumerate(scale):
            if offset == n:
                return i + 1
        return -1


class Mode():
    """Some modes"""
    ionian     = [0, 2, 4, 5, 7, 9, 11, 12] # T-T-s-T-T-T-s
    dorian     = [0, 2, 3, 5, 7, 9, 10, 12] # T-s-T-T-T-s-T
    phrygian   = [0, 1, 3, 5, 7, 8, 10, 12] # s-T-T-T-s-T-T
    lydian     = [0, 2, 4, 6, 7, 9, 11, 12] # T-T-T-s-T-T-s
    mixolydian = [0, 2, 4, 5, 7, 9, 10, 12] # T-T-s-T-T-s-T
    aeolian    = [0, 2, 3, 5, 7, 8, 10, 12] # T-s-T-T-s-T-T
    locrian    = [0, 1, 3, 5, 6, 8, 10, 12] # s-T-T-s-T-T-T

    allModes   = [ionian, dorian, phrygian, lydian, mixolydian, aeolian, locrian]


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
        elif l == [0, 2, 4, 7]: ext = '2'
        elif l == [0, 2, 3, 7]: ext = 'm2'

        if ext == '?':
            print('UNKNOWN CHORD - l: {}, notes: {}, transpose: {}'.format(l, self.notes, self.transpose(-self.notes[0]).notes))

        return base + ext

    @staticmethod
    def fromScale(scale, *indices):
        print(list(indices))
        noteList = [scale[i - 1] for i in list(indices)]
        return Chord(*noteList)

    @staticmethod
    def fromMode(mode, *indices):
        noteList = [mode[i - 1] for i in list(indices)]
        return Chord(*noteList)

    def transpose(self, difference):
        noteList = [(n + difference + 12) % 12 for n in self.notes]
        return Chord(*noteList)

    def __str__(self):
        result = self.name + ':'
        for n in self.notes:
            result += ' ' + Key.note2str(n)
        return result

