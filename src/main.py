from tkinter import *
from tkinter.ttk import *
from mattycontrols.MattyControls import *
from .mainwin import MainWin
from .key import Key, Scale, Mode, Chord
from .settings import Settings, Pos, Size


class Application(Frame):
    def __init__(self, settings, master=None):
        """The constructor"""
        frame_init(self, master)
        master.title('Guitar cheat sheet')

        self.ctrl, self.shift, self.alt, self.superkey = False, False, False, False
        self.changeWithoutEvent = False

        self.canvas = Cnvs(master, bd=-2)
        self.canvas.bind('<Button>', self.onMouseDown)
        self.canvas.bind('<Motion>', self.createOnMouseMove(0))
        self.canvas.bind('<B1-Motion>', self.createOnMouseMove(1))
        self.canvas.bind('<B2-Motion>', self.createOnMouseMove(2))
        self.canvas.bind('<B3-Motion>', self.createOnMouseMove(3))
        self.canvas.bind('<ButtonRelease>', self.onMouseUp)
        self.master.bind('<Key>', self.onKeyDown)
        self.master.bind('<KeyRelease>', self.onKeyUp)
        self.resize_bind_id = self.master.bind('<Configure>', self.onResizeOrMove)
        self.canvas.highlightthickness = 0
        self.canvas.width = settings.size.w
        self.canvas.height = settings.canvasheight
        self.canvas.locateInside(self, d=0)

        self.dbKey = Db(self, [Key.note2str(i) for i in range(12)], 3)
        self.dbKey.locateFrom(self.canvas, H_COPY_LEFT, V_BOTTOM)
        self.dbKey.x = 10
        self.dbKey.addLabel('Key: ')
        self.dbKey.onChange = lambda *args: self.onChangeAnything()

        self.dbScale = Db(self, ['Major', 'Minor', 'Pentatonic', 'Blues'], 0)
        self.dbScale.locateFrom(self.dbKey.label, H_COPY_LEFT, V_BOTTOM)
        self.dbScale.addLabel('Scale: ')
        self.dbScale.onChange = lambda *args: self.onChangeAnything()

        modes = ['I. Ionian', 'II. Dorian', 'III. Phrygian', 'IV. Lydian', 'V. Mixolydian', 'VI. Aeolian', 'VII. Locrian' ];
        self.dbMode = Db(self, modes, 0)
        self.dbMode.locateFrom(self.dbScale.label, H_COPY_LEFT, V_BOTTOM)
        self.dbMode.addLabel('Mode: ')
        self.dbMode.onChange = lambda *args: self.onChangeAnything()

        self.dbPreset = Db(self, ['Guitar', 'Soprano ukelele', 'Tenor ukelele'], 0)
        self.dbPreset.locateFrom(self.dbMode.label, H_COPY_LEFT, V_BOTTOM)
        self.dbPreset.addLabel('Preset: ')
        self.dbPreset.onChange = lambda *args: self.onChangeAnything()

        self.cbNotes = Cb(self, text='Display notes')
        self.cbNotes.width = 130
        self.cbNotes.locateFrom(self.canvas, H_COPY_RIGHT, V_BOTTOM)
        self.cbNotes.checked = settings.displayNotes
        self.cbNotes.onChange = lambda _, *args: self.onChangeAnything()

        self.cbChordsInKey = Cb(self, text='Chords in key')
        self.cbChordsInKey.locateFrom(self.cbNotes, H_COPY_LEFT, V_BOTTOM)
        self.cbChordsInKey.checked = True
        self.cbChordsInKey.onChange = lambda _, *args: self.onChangeAnything()

        self.checkMultiple = Cb(self, text='Multiple highlights')
        self.checkMultiple.width = self.cbNotes.width
        self.checkMultiple.locateFrom(self.cbChordsInKey, H_COPY_LEFT, V_BOTTOM)
        self.checkMultiple.onChange = lambda _, *args: self.onChangeAnything()

        self.btnQuit = Btn(self, text='Quit', command=self.quit)
        self.btnQuit.locateInside(self, H_RIGHT, V_BOTTOM)

        self.chordCbs = []

        self.settings = settings

        self.mainWindow = MainWin(settings, self)
        self.nrOfChords = 0
        self.onChangeAnything()

        self.master.after(int(self.settings.fps_inv * 1000), self.loop)

    def onChangeAnything(self):
        """This method is called whenever a control changed value"""
        self.getChordDetails(0, 'a', Mode.ionian) # Set the correct length
        if self.changeWithoutEvent:
            return

        # Key, scale and mode
        key = self.dbKey.selectedValue
        scale = Scale.major
        if self.dbScale.selectedValue == 'Minor':
            scale = Scale.minor
        elif self.dbScale.selectedValue == 'Pentatonic':
            scale = Scale.pentatonic
        elif self.dbScale.selectedValue == 'Blues':
            scale = Scale.blues
        mode = Mode.allModes[self.dbMode.selectedIndex]
        # Necksize and tuning
        necksize = Size(14, 6)
        tuning = ['E','B','G','D','A','E']
        if self.dbPreset.selectedValue == 'Soprano ukelele':
            necksize = Size(12, 4)
            tuning = ['A','E','C','G']
        elif self.dbPreset.selectedValue == 'Tenor ukelele':
            necksize = Size(14, 4)
            tuning = ['G#', 'Eb', 'B', 'F#']
        # Chords text and highlight
        displayNotes = self.cbNotes.checked
        self.updateChordCheckboxes(mode)
        highlightSet = set()
        for i in range(self.nrOfChords):
            if self.chordCbs[i].checked:
                highlightSet |= set(self.getChordDetails(i, key, mode).notes)

        # Update the picture
        self.mainWindow.change(key, scale, mode, necksize, [Key.str2note(c) for c in tuning], highlightSet, displayNotes)

    def getChordDetails(self, i, key, mode):
        def chord(*indices):
            return Chord.fromMode(mode, *list(indices))

        if self.cbChordsInKey.checked:
            chords = [
                chord(1, 3, 5),     # C
                chord(2, 4, 6),     # Dm
                chord(3, 5, 7),     # Em
                chord(4, 6, 8),     # F
                chord(5, 7, 2),     # G
                chord(6, 8, 3),     # Am
                chord(7, 2, 4),     # Bdim
                chord(5, 7, 2, 4),  # G7
                chord(6, 8, 3, 5),  # Am7
                chord(1, 3, 5, 7),  # Cmaj7
                chord(4, 6, 8, 3),  # Fmaj7
                chord(6, 8, 3, 7),  # Am2
                chord(2, 4, 6, 3)   # Dm2
            ]
        else:
            chords = [
                Chord(0, 4, 7),     # Major
                Chord(0, 3, 7),     # Minor
                Chord(0, 3, 6),     # dim
                Chord(0, 5, 7),     # sus 4
                Chord(0, 2, 7),     # sus 2
                Chord(0, 4, 7, 10), # 7
                Chord(0, 3, 7, 10), # Minor 7
                Chord(0, 4, 7, 11), # Major 7
                Chord(0, 4, 7, 14), # Major 2
                Chord(0, 3, 7, 14)  # Minor 2
            ]
        self.nrOfChords = len(chords)

        base = Key.str2note(key)
        return chords[i].transpose(base)

    def updateChordCheckboxes(self, mode):
        # Init
        key = self.dbKey.selectedValue
        copy = self.chordCbs
        self.chordCbs = []

        # Add the new cb's
        for i in range(self.nrOfChords):
            self.addChordCb(key, i, mode, i==0)

        # Check the previously checked cb's (and discard old checkbox)
        if copy:
            self.changeWithoutEvent = True
            for i, cb in enumerate(copy):
                if len(self.chordCbs) > i:
                    self.chordCbs[i].checked = cb.checked
                cb.destroy()
            self.changeWithoutEvent = False

    def addChordCb(self, key, index, mode, first=False):
        columnHeight = 7
        chord = self.getChordDetails(index, key, mode)

        cb = Cb(self, text=str(chord))
        cb.width = 130
        if first:
            cb.place(x=670, y=self.canvas.y + self.canvas.height + 10)
        elif index % columnHeight == 0:
            cb.locateFrom(self.chordCbs[index - columnHeight], H_RIGHT, V_COPY_TOP, 10)
        else:
            cb.locateFrom(self.chordCbs[-1], H_COPY_LEFT, V_BOTTOM, 2)
        cb.onChange = self.chordCbOnChange
        self.chordCbs.append(cb)

    def chordCbOnChange(self, cbMe, *args):
        if self.changeWithoutEvent:
            return

        temp = self.changeWithoutEvent
        self.changeWithoutEvent = True

        if not self.checkMultiple.checked:
            for cb in self.chordCbs:
                if cb != cbMe:
                    cb.checked = False

        self.changeWithoutEvent = temp

        self.onChangeAnything()

    def onMouseDown(self, event):
        self.mainWindow.onMouseDown(Pos(event.x, event.y), event.num)

    def createOnMouseMove(self, btnNr):
        return lambda event: self.mainWindow.onMouseMove(Pos(event.x, event.y), btnNr)

    def onMouseUp(self, event):
        self.mainWindow.onMouseUp(Pos(event.x, event.y), event.num)

    def onKeyDown(self, event):
        if self.setModifyKeys(event, True):
            self.mainWindow.onKeyDown(self.getchar(event))

    def onKeyUp(self, event):
        self.setModifyKeys(event, False)

    def setModifyKeys(self, event, value):
        # Set the modify keys and return whether or not something has to be done still.
        if event.keysym_num in {65505, 65506}:
            self.shift = value
        elif event.keysym_num in {65507, 65508}:
            self.ctrl = value
        elif event.keysym_num in {65513, 65514}:
            self.alt = value
        elif event.keysym_num in {65371, 65372, 65515, 65516}:
            self.superkey = value
        else:
            return True
        return False

    def onResizeOrMove(self, event):
        # s = Size(event.width, event.height)
        # if s != self.settings.size:
        #     self.settings.size = s
        #     self.canvas.width, self.canvas.height = s.w, self.settings.canvasheight
        #     self.mainWindow.resize(Size(s.w, self.settings.canvasheight))
        pass

    def loop(self):
        """Private method to manage the loop method"""
        self.mainWindow.loop()
        self.master.after(int(self.settings.fps_inv * 1000), self.loop)

    def getchar(self, e):
        """Convert a tkinter event (given these three different representations of the same char)"""
        # Get prefixes
        prefix = ('Ctrl-' if self.ctrl else '') + ('Alt-' if self.alt else '') + ('Super-' if self.superkey else '')

        # Some basic key mapping
        num = e.keysym_num
        name = e.keysym
        if 31 < num < 256:
            c = chr(num)
        else:
            c = name

        # Some exceptopns
        if num == 65307: c = 'Esc'
        elif num == 65288: c = '\b'
        elif num == 65293: c = '\n'
        elif num == 65289: c = 'Backtab' if self.shift else '\t'

        return prefix + c


def main():
    """The main entrypoint for this application"""
    root = Tk()
    settings = Settings()
    root.configure()
    root.geometry('{}x{}'.format(settings.size.w, settings.size.h))
    app = Application(settings, master=root)
    app.mainloop()

