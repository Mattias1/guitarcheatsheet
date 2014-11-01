from tkinter import *
from tkinter.ttk import *
from mattycontrols.MattyControls import *
from .mainwin import MainWin
from .key import Key, Scale
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
        self.canvas.bind('<Motion>', self.onMouseMove)
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

        self.dbScale = Db(self, ['default', 'pentatonic'], 0)
        self.dbScale.locateFrom(self.dbKey.label, H_COPY_LEFT, V_BOTTOM)
        self.dbScale.addLabel('Scale: ')
        self.dbScale.onChange = lambda *args: self.onChangeAnything()

        self.dbPreset = Db(self, ['guitar', 'soprano ukelele', 'tenor ukelele'], 0)
        self.dbPreset.locateFrom(self.dbScale.label, H_COPY_LEFT, V_BOTTOM)
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
        self.getChordDetails(0, 'a') # Get the correct length
        if self.changeWithoutEvent:
            return

        # Scale and key
        scale = Scale.default
        if self.dbScale.selectedValue == 'pentatonic':
            scale = Scale.pentatonic
        key = self.dbKey.selectedValue
        # Necksize and tuning
        necksize = Size(14, 6)
        tuning = ['E','B','G','D','A','E']
        if self.dbPreset.selectedValue == 'soprano ukelele':
            necksize = Size(12, 4)
            tuning = ['A','E','C','G']
        elif self.dbPreset.selectedValue == 'tenor ukelele':
            necksize = Size(14, 4)
            tuning = ['G#', 'Eb', 'B', 'F#']
        # Display notes
        displayNotes = self.cbNotes.checked
        # Chords text and highlight
        self.setChordsText()
        highlightSet = set()
        offset = Key.str2note(key)
        for i in range(self.nrOfChords):
            if self.chordCbs[i].checked:
                highlightSet |= {(j + offset) % 12 for j in self.getChordDetails(i, key)[1]}

        # Update the picture
        self.mainWindow.change(key, scale, necksize, [Key.str2note(c) for c in tuning], highlightSet, displayNotes)

    def getChordDetails(self, i, key):
        helper = Key.str2note(key)
        k = lambda n: Key.note2str((helper + n) % 12)
        if self.cbChordsInKey.checked:
            chords = [
                k(0)  + ' (i)',       [0, 4, 7],     # C
                k(2)  + 'm (ii)',     [2, 5, 9],     # Dm
                k(4)  + 'm (iii)',    [4, 7, 11],    # Em
                k(5)  + ' (iv)',      [5, 9, 12],    # F
                k(7)  + ' (v)',       [7, 11, 2],    # G7
                k(9)  + 'm (vi)',     [9, 12, 4],    # Am
                k(11) + 'dim (vii)',  [11, 2, 5]     # Bdim
            ]
        else:
            chords = [
                key,          [0, 4, 7],     # Major
                key + 'm',    [0, 3, 7],     # Minor
                key + 'dim',  [0, 3, 6],     # dim
                key + '7',    [0, 4, 7, 10], # 7
                key + 'm7',   [0, 3, 7, 10], # Minor 7
                key + 'maj7', [0, 4, 7, 11]  # Major 7
            ]
        self.nrOfChords = len(chords) // 2
        return (chords[2 * i], chords[2 * i + 1])

    def setChordsText(self):
        # Init
        key = self.dbKey.selectedValue
        copy = self.chordCbs
        self.chordCbs = []

        # Add the new cb's
        for i in range(self.nrOfChords):
            self.addChordCb(key, i, i==0)

        # Check the previously checked cb's (and discard old checkbox)
        if copy:
            self.changeWithoutEvent = True
            for i, cb in enumerate(self.chordCbs):
                if len(copy) > i:
                    cb.checked = copy[i].checked
                    copy[i].destroy()
            self.changeWithoutEvent = False

    def addChordCb(self, key, index, first=False):
        columnHeight = 7
        name, noteList = self.getChordDetails(index, key)
        offset = Key.str2note(key)
        text = '{}: '.format(name)
        for i in noteList:
            text += Key.note2str((i + offset) % 12) + ' '

        cb = Cb(self, text=text)
        cb.width = 130
        if first:
            cb.place(x=670, y=self.canvas.y + self.canvas.height + 10)
        elif index % columnHeight == 0:
            cb.locateFrom(self.chordCbs[index - 6], H_RIGHT, V_COPY_TOP, 10)
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

    def onMouseMove(self, event):
        self.mainWindow.onMouseMove(Pos(event.x, event.y), event.num)

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

