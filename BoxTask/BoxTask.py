"""
This script is used to run a box trial task in the PsychoPy application.
"""

from psychopy import core, visual, event, data, clock, gui
import glob
from random import shuffle
import Constants
from Trial import Trial
from Form import Form
import pandas
from collections import defaultdict, namedtuple
import os
from InfoScene import InfoScene

def build_location_sequence(sequence):
    if(sequence is None):
        random_loc = [x for x in range(1, 13)]
        shuffle(random_loc)
        return random_loc
    return [int(x) for x in sequence.split(",")]


class ExperimentManager(object):
    def __init__(self, win, mouse, timer):
        self.win = win
        self.mouse = mouse
        self.timer = timer
        self.block_count = 0
        self.is_running = True
        self.scene = InfoScene(self.win, self, self.mouse, "The next trial presented will be a practice trial. You can open boxes and choose which is the dominant colour. The trial will automatically end if too many boxes are opened.")
        self.practice_run()

    def practice_run(self):
        practice_data = data.importConditions(Constants.PRACTICE_RUN)
        self.handler = data.TrialHandler(practice_data, 1, method="sequential")

    def next_block(self):
        if self.block_count >= len(Constants.BLOCK_FILES):
            self.scene = None
        block_data = data.importConditions(Constants.BLOCK_FILES[self.block_count])
        self.block_count += 1
        self.handler = data.TrialHandler(block_data, 1, method="sequential")


    def failed_trial(self):
        self.scene = InfoScene(self.win, self, self.mouse, "You failed the trial because too many boxes were opened!")

    def completed_trial(self):
        self.scene = InfoScene(self.win, self, self.mouse, "Your decision has been saved. Continue to the next trial")

    def next_trial(self, writer=None):
        try:
            trial_data = self.handler.next()
        except StopIteration:
            self.run_form()
            return
        #Parsing data from the data frame
        colours = (trial_data["Colour0"], trial_data["Colour1"], trial_data["ColourName0"], trial_data["ColourName1"])
        sequence = trial_data["Sequence"][1:-1] #The sequence string is specified with quotes marking beginning and end. The list slice will remove these.
        location_sequence = build_location_sequence(trial_data["Location_Sequence"])
        #Creating and running the trial
        trial_output = defaultdict(list) #The default dict allows for dynamically adding keywords with empty lists as the default value
        self.scene = Trial(self.win, colours, sequence, self.mouse, trial_output, self.timer, location_sequence, self) # The trial object is created with each sequence. It is responsible for outputting necessary data from the trial
        #Save the trial data
        if(writer is not None):
            pandas.DataFrame(trial_output).to_excel(writer, sheet_name=f"block{self.block_count+1}_trial{trial_count+1}") #Creates a new sheet and uses the same output object that the trial object was given a shallow copy of 

    def run_form(self, writer=None):
        if(Constants.FORM_FILES[self.block_count] is None):
            self.next_block()
            return
        #Parsing questionnaire data and creating form
        data_frame = pandas.read_excel(Constants.FORM_FILES[self.block_count])
        form_output = defaultdict(list) #Output stream
        self.scene = Form(self.win, data_frame, form_output, self.timer, self)
        self.next_block()
        if(writer is not None):
            pandas.DataFrame(form_output).to_excel(writer, sheet_name=f"{Constants.FORM_FILES[block_count]}_answered")

    def update(self):
        self.scene.check_input()
        self.scene.draw()
        self.win.flip()

def get_subject_info():
    dlg = gui.Dlg(title="Box Task Experiment")
    dlg.addText("Subject info")
    dlg.addField("ID")
    dlg.addField("Gender", choices=["Male", "Female"])
    dlg.addField("Age")
    data = dlg.show()
    if(dlg.OK):
        return data
    else:
        raise ValueError("Participant did not fill out the dialogue box")

# path = os.path.join(os.getcwd(), 'data', 'individual_data')
# os.chdir(path)
# extension = 'xlsx'
# result = [i for i in glob.glob(os.path.join(path, f'*.{extension}'))]
# print(os.path.join(path, '*.{}'.format(extension)))
# {elm:pandas.ExcelFile(elm) for elm in result}



def main():
    subject_data = get_subject_info()
    print(subject_data)
    win = visual.Window(Constants.WINDOW_SIZE, units="pix"); # NOTE: pixel units are not scalable.
    mouse = event.Mouse()
    timer = clock.Clock()
    manager = ExperimentManager(win, mouse, timer)
    while manager.is_running:
        manager.update()

#Start program
main()

