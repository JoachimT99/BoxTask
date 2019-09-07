from psychopy import visual, event


class Form():
    def __init__(self, win, data_frame, output, clock):
        """
        Initializes a form with questions and a rating scale.
        Params:
            win: A window object the form should be drawn onto
            data_frame: A data frame containing the data for the form. It is a python dict containing lists.
            output: output stream as a defaultdict(list)
            clock: a python clock object
        Returns:
            None
        """
        self.win = win
        self.clock = clock
        self.data = data_frame
        self.current_question = 0
        self.output = output
        self.t0 = self.clock.getTime()
        self.next_question()

    def check_input(self):
        """
        Checks input to the form.
        Params:
            None
        Returns:
            bool: depending on if the form has been completed or not. A True value indicates the form has been completed.
        """
        if 'escape' in event.getKeys():
            core.quit()
        if(self.scale.noResponse == False and self.current_question < len(self.data)):
            self.t1 = self.clock.getTime()
            self.output["Survey_item"].append(self.data["Survey_items"][self.current_question-1])
            self.output["Answer"].append(self.scale.getRating())
            self.output["Response_time"].append(self.t1 - self.t0)
            self.next_question()
            return False
        elif(self.scale.noResponse == False):
            self.t1 = self.clock.getTime()
            self.output["Survey_item"].append(self.data["Survey_items"][self.current_question-1])
            self.output["Answer"].append(self.scale.getRating())
            self.output["Response_time"].append(self.t1 - self.t0)
            return True

    def next_question(self):
        """
        Gets the next form question and creates a RatingScale. Two different RatingScales are created depending on how many labels are needed.
        Note that it does not work setting the number of labels to the number of ticks. The reason for this is unkown.
        Params:
            None
        Returns:
            None
        """
        if(len(self.data["Scale"][self.current_question].split(",")) > 2):
            self.scale = visual.RatingScale(self.win,
                                            choices=self.data["Scale"][self.current_question].split(","),
                                            scale=self.data["Survey_items"][self.current_question],
                                            size=1,
                                            stretch=2
                                            )
        else:
            self.scale = visual.RatingScale(self.win,
                                            low=1,
                                            high=len(self.data["Response_options"][0].split(",")), #Needs format revision
                                            labels=self.data["Scale"][self.current_question].split(","),
                                            scale=self.data["Survey_items"][self.current_question],
                                            size=1,
                                            stretch=2
                                            )
        self.current_question += 1
        self.t0 = self.clock.getTime()

    def draw(self):
        """
        Function to draw the form and all of its components.
        Params:
            None
        Returns:
            None
        """
        self.scale.draw()