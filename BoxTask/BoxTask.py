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

    def practice_run(self):
        practice_data = data.importConditions(Constants.PRACTICE_RUN)
        handler = data.TrialHandler(practice_data, 1, method="sequential")
        self.run_trial(-1, handler)

    def next_block(self):
        if self.block_count >= len(Constants.FORM_FILES):
            self.scene = None
        block_data = data.importConditions(Constants.FORM_FILES[self.block_count])
        handler = data.TrialHandler(block_data, 1, method="sequential")
        self.manager.run_trial(self.block_count, handler, writer=writer)

    def run_trial(self, block_count, handler, writer=None):
        for trial_count, trial_data in enumerate(handler): #The number of trials to be run according to length of the trial column
            #Parsing data from the data frame
            colours = (trial_data["Colour0"], trial_data["Colour1"], trial_data["ColourName0"], trial_data["ColourName1"])
            sequence = trial_data["Sequence"][1:-1] #The sequence string is specified with quotes marking beginning and end. The list slice will remove these.
            location_sequence = build_location_sequence(trial_data["Location_Sequence"])
            #banner_text = trial_data["Banner"]
            #Creating and running the trial
            trial_output = defaultdict(list) #The default dict allows for dynamically adding keywords with empty lists as the default value
            trial = Trial(self.win, colours, sequence, self.mouse, trial_output, self.timer, location_sequence, "This is a very long test banner, which is meant to check the length of the banner. It should wrap around and go onto a second line.") # The trial object is created with each sequence. It is responsible for outputting necessary data from the trial
            while not trial.check_input():
                trial.draw()
                self.win.flip()
            #Save the trial data
            if(writer is not None):
                pandas.DataFrame(trial_output).to_excel(writer, sheet_name=f"block{block_count+1}_trial{trial_count+1}") #Creates a new sheet and uses the same output object that the trial object was given a shallow copy of 

    def run_form(self, block_count, writer=None):
        #Parsing questionnaire data and creating form
        data_frame = pandas.read_excel(Constants.FORM_FILES[block_count])
        form_output = defaultdict(list) #Output stream
        form = Form(self.win, data_frame, form_output, self.timer)
        self.win.flip() #Clearing screen
        # Run through form
        while not form.check_input():
            form.draw()
            self.win.flip()
        if(writer is not None):
            pandas.DataFrame(form_output).to_excel(writer, sheet_name=f"{Constants.FORM_FILES[block_count]}_answered")

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

def main():
    """
    This is the main program. Executing this function will start the experiment.
    Params:
        None
    Returns:
        None
    """
    subject_data = get_subject_info()
    print(subject_data)
    win = visual.Window(Constants.WINDOW_SIZE, units="pix"); # NOTE: pixel units are not scalable.
    mouse = event.Mouse()
    timer = clock.Clock()
    manager = ExperimentManager(win, mouse, timer)
    manager.practice_run()
    with pandas.ExcelWriter(f"ID_{subject_data[0]}.xlsx", engine='xlsxwriter') as writer, pandas.ExcelWriter("Summary.xlsx") as summary: #Context manager managing the output file
        for block_count, block in enumerate(Constants.BLOCK_FILES): #Cycles through all the blocks of sequences. Between each block an optional form(questionnaire) can be specified
            block_data = data.importConditions(block)
            handler = data.TrialHandler(block_data, 1, method="sequential")
            manager.run_trial(block_count, handler, writer=writer)
            #If there is no form to be filled, skip to the next block
            if(Constants.FORM_FILES[block_count] is None): 
                continue
            manager.run_form(block_count, writer=writer)
        #Output data to file
        print(writer)
        writer.save()
    path = os.path.join(os.getcwd(), 'data', 'individual_data')
    os.chdir(path)
    extension = 'xlsx'
    result = [i for i in glob.glob(os.path.join(path, f'*.{extension}'))]
    print(os.path.join(path, '*.{}'.format(extension)))
    {elm:pandas.ExcelFile(elm) for elm in result}

#Start program
main()

