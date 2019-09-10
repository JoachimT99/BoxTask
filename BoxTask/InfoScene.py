from psychopy import visual, event, core
import Constants


class InfoScene(object):
    def __init__(self, win, manager, mouse, text, y_offset=0):
        self.mouse = mouse
        self.win = win
        self.manager = manager
        self.text = visual.TextStim(self.win,
                                    text=text,
                                    wrapWidth=Constants.WINDOW_SIZE[0])
        self.next_box_text = visual.TextStim(self.win,
                                             text="Continue to trial",
                                             pos=[0, -200+y_offset])
        self.continue_box = visual.Rect(self.win, pos=[0, -200+y_offset], width=Constants.SQUARE_SIZE+50, height=Constants.SQUARE_SIZE/2, fillColor="black")

    def check_input(self):
        if 'escape' in event.getKeys():
            core.quit()
        if self.mouse.isPressedIn(self.continue_box, buttons=[0]):
            event.clearEvents()
            self.manager.next_trial()
            

        return True
    
    def draw(self):
        self.text.draw()
        self.continue_box.draw()
        self.next_box_text.draw()