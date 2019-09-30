from psychopy import visual, event, core
import Constants


class InfoScene(object):
    """
    This class is used to display info on the manager instance
    """
    def __init__(self, win, manager, mouse, text, y_offset=0):
        """
        Initializes a InfoScene object.
        Params:
            win: A window object the form should be drawn onto
            manager: an instance of the info scene's manager
            mouse: A mouse object for checking against mouse input
            text: the text string to be displayed
            y_offset: integer of the y_offset for the text
        Returns:
            None
        """
        self.mouse = mouse
        self.win = win
        self.manager = manager
        self.text = visual.TextStim(self.win,
                                    text=text,
                                    wrapWidth=Constants.WINDOW_SIZE[0])
        self.next_box_text = visual.TextStim(self.win,
                                             text="Continue",
                                             pos=[0, -200+y_offset])
        self.continue_box = visual.Rect(self.win, pos=[0, -200+y_offset], width=Constants.SQUARE_SIZE+50, height=Constants.SQUARE_SIZE/2, fillColor="black")

    def check_input(self):
        """
        Checks input on the scene
        Params:
            None
        Returns:
            None
        """
        if 'escape' in event.getKeys():
            core.quit()
        if self.mouse.isPressedIn(self.continue_box, buttons=[0]):
            event.clearEvents()
            self.manager.to_trial()
        return True
    
    def draw(self):
        """
        Draws the info scene to the screen
        Params:
            None
        Returns:
            None
        """
        self.text.draw()
        self.continue_box.draw()
        self.next_box_text.draw()