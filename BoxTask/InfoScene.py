from psychopy import visual, event
import Constants


class InfoScene(object):
    def __init__(self, win, manager):
        self.win = win
        self.manager = manager
        self.text = visual.TextStim(self.win, text=f"This trial is not timed and will end after all boxes are shown. It also tests the amount of text one can put into one line and really stretches the amount of information on the screen", wrapWidth=Constants.WINDOW_SIZE[0])

    def check_input(self):
        if 'escape' in event.getKeys():
            return False
        return True
    
    def draw(self):
        self.text.draw()