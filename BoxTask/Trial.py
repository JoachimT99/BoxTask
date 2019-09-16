import Constants
from psychopy import visual, event, core
from Scale import Scale
from InfoScene import InfoScene

class Trial():
    """
    A class specifying a Trial and methods related to a trial. when a trial is created, it only needs to be drawn and checked for input.
    """
    def __init__(self, win, colours, sequence, mouse, output_stream, clock, location_sequence, manager, override_text=None):
        """
        Initializes a Trial object.
        Params:
            win: A window object the form should be drawn onto
            colours: A tuple of colour strings. (names, hex, or rgb)
            sequence: A sequence string containing only 0's and 1's
            mouse: A mouse object for checking against mouse input
            output_stream: A dictionary object containing lists for writing data into
            clock: A clock object to get the current time
        """
        self.manager = manager
        self.clock = clock
        self.win = win
        self.mouse = mouse
        self.output = output_stream
        self.colours = colours
        self.sequence = sequence
        self.location_sequence = location_sequence
        self.place_boxes()
        info_text = "This NOT a practice trial. "
        if override_text is not None:
            info_text = override_text
        else:
            if self.manager.failed_last == True:
                info_text += "You failed the trial because too many boxes were opened! "
            else:
                info_text += "You completed the trial! "
        if len(sequence) != Constants.MATRIX[0] * Constants.MATRIX[1]:
            info_text += "The next trial is a timed trial. "
            banner = "This is a timed trial "
        else:
            info_text += "The next trial is NOT a timed trial. "
            banner = "This is not a timed trial "
        self.manager.scene = InfoScene(self.win, self, self.mouse, info_text)
        self.create_stimuli(banner)


    def to_trial(self):
        self.manager.scene = self

    def place_boxes(self):
        """
        Places a centered grid of box stimuli and returns a list of the created grid.
        Params:
            None
        Returns:
            A python list containing all the boxes that was created for the grid

        """
        boxes = []
        y_offset = (Constants.WINDOW_SIZE[1] / 2) - 2*Constants.SQUARE_SIZE # The starting offset of the first square. (Upper-left)
        y_spacing = abs(y_offset * 2 / (Constants.MATRIX[1]-1)) #Has the value for the spacing between the squares. The formula calculates even distribution on all monitors
        
        #Places the squares in two-dimensional array structure
        for _ in range(Constants.MATRIX[1]):
            x_offset = (-Constants.WINDOW_SIZE[0] / 2) + 2*Constants.SQUARE_SIZE
            x_spacing = abs(x_offset * 2 / (Constants.MATRIX[0]-1))
            for _ in range(Constants.MATRIX[0]):
                box = visual.Rect(self.win,
                                  width=Constants.SQUARE_SIZE,
                                  height=Constants.SQUARE_SIZE,
                                  pos=[x_offset + Constants.CENTER_OFFSET[0], y_offset + Constants.CENTER_OFFSET[1]], # Sets the position to the offset values in addition to adding a global offset to each box to control grid location
                                  fillColor="#BEBEBE")
                boxes.append(box)
                x_offset += x_spacing
            y_offset -= y_spacing
        self.grid = boxes

    """
    Creates the confidence scales
    """
    def create_stimuli(self, banner):
        """
        Creates all stimuli that is to be drawn by the Trial class and stores them as attributes and into lists for easy drawing.
        Params:
            None
        Returns:
            None
        """
        banner_text = visual.TextStim(self.win, text=banner, pos=[0, 500], height=40, wrapWidth=Constants.WINDOW_SIZE[0])
        next_box_text = visual.TextStim(self.win,
                               text="Show next box",
                               pos=[0, -300])
        choice_text0 = visual.TextStim(self.win,
                                       text='Press the circle if you believe it is the dominant colour:',
                                       pos=[-600, -300]
                                       )
        choice_text1 = visual.TextStim(self.win,
                                       text='Press the circle if you believe it is the dominant colour:',
                                       pos=[600, -300])
        self.button0 = visual.Circle(self.win,
                                        radius=50,
                                        pos=[-600, -400],
                                        fillColor=self.colours[0]
                                        )
        self.button1 = visual.Circle(self.win,
                                     radius=50,
                                     pos= [600, -400],
                                     fillColor=self.colours[1]
                                     )
        self.continue_box = visual.Rect(self.win, pos=[0, -300], width=Constants.SQUARE_SIZE, height=Constants.SQUARE_SIZE/2, fillColor="black")
        rating_text0 = visual.TextStim(self.win, text=f"More \n{self.colours[2]}", pos=[-800, -400], color=self.colours[0])
        rating_text1 = visual.TextStim(self.win, text=f"More \n{self.colours[3]}", pos=[800, -400], color=self.colours[1])
        self.rating_scale = Scale(self.win, self.colours)
        self.rating_stims = [rating_text0, rating_text1, banner_text] + self.grid
        self.drawables = [self.continue_box, next_box_text, banner_text] + self.grid
        self.choice_stims = [self.button0, self.button1, choice_text0, choice_text1]
        self.boxes_revealed = 0

    def check_input(self):
        """
        Checks input for all components of the trial on screen except for the rating scale. It also writes to the output if a trial is failed.
        Params:
            None    
        Returns:
            bool: indicating wether the Trial has ended. A true value indicates the trial has ended
        """
        if(self.mouse.isPressedIn(self.button0, buttons=[0]) and self.button0 in self.drawables):
            [self.output["Decision"].append(-1) for _ in range(len(self.output["Box_Num"]) - 1)]
            self.output["Decision"].append(self.colours[0])
            self.manager.completed_trial()
            return
        elif (self.mouse.isPressedIn(self.button1, buttons=[0]) and self.button0 in self.drawables):
            [self.output["Decision"].append(-1) for _ in range(len(self.output["Box_Num"]) - 1)]
            self.output["Decision"].append(self.colours[1])
            self.manager.completed_trial()
            return 
        elif(len(self.sequence) == 0 and self.mouse.isPressedIn(self.continue_box, buttons=[0])):
            self.output["Box_Num"].append(self.boxes_revealed+1)
            self.output["Reaction_time"].append(-1)
            self.output["Probability_Estimates"].append(-1)
            [self.output["Decision"].append(-1) for _ in self.output["Box_Num"]]
            self.manager.failed_trial()
            return
        if 'escape' in event.getKeys():
                core.quit()
        if self.mouse.isPressedIn(self.continue_box, buttons=[0]):
            self.next_box()
            box_seen = self.clock.getTime()
            self.get_rating()
            rating_given = self.clock.getTime()
            self.output["Reaction_time"].append(rating_given - box_seen)
    
    def next_box(self):
        """
        Opens the next box. Reads the sequence data and gives the appropriate box its colour and writes data to the output.
        Params:
            None
        Returns:
            None
        """
        if(self.boxes_revealed == 0):
            self.drawables += self.choice_stims
        location = self.location_sequence[0]
        box = self.grid[location-1]
        if(self.sequence[0] == '0'):
            box.fillColor = self.colours[0]
        elif(self.sequence[0] == '1'):
            box.fillColor = self.colours[1]
        else:
            raise SyntaxError("The given input does not match program specification for a sequence. Allowed values: 0 and 1")
        self.boxes_revealed += 1
        self.output["Box_Num"].append(self.boxes_revealed)
        self.sequence = self.sequence[1:]
        self.location_sequence = self.location_sequence[1:]

    def get_rating(self):
        """
        Draws the rating scale and waits for input. Once the input is given, it is written to the output and the method returns.
        Params:
            None
        Returns:
            None
        """
        event.clearEvents()
        while(self.rating_scale.noResponse() == True):
            if 'escape' in event.getKeys():
                core.quit()
            self.rating_scale.draw()
            [x.draw() for x in self.rating_stims]
            self.win.flip()
        self.output["Probability_Estimates"].append(self.rating_scale.getRating())
        self.rating_scale.reset()
        event.clearEvents() #Event queue is cleared to prevent keypresses from rating period to be carried forward
        

    def save(self):
        return self.output

    def draw(self):
        """
        Draws the Trial to a window.
        Params:
            None
        Returns:
            None
        """
        for drawable in self.drawables:
            drawable.draw()