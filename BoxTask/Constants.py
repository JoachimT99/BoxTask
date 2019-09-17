import os
#Grid Constants
BORDER = 50 #Defines the general border inside the window that should be padded in
CENTER_OFFSET = (0, 100)
SQUARE_SIZE = 150 #Length of the sides of a box
MATRIX = (4, 3) #The grid size

#Application constants
WINDOW_SIZE = [1920, 1080] #The window resolution
# Setting up stimuli
CONFIDENCE_RATING_LVLS = [f"{x}%" for x in range(100, 50, -10)] + [f"{x}%" for x in range(50, 101, 10)]
RATING_TEXT_SCALE = 0.75


#INPUT FILE SPECIFICATION:
PRACTICE_RUN = "data/input/practice.xlsx"
BLOCK_FILES = ["colour_sequences_12.xlsx", "colour_sequences_6or9_a.xlsx", "colour_sequences_6or9_b.xlsx"] #The blocks of sequences. Must be xlsx file and follow a specified format
BLOCK_FILES = ["data/input/" + file for file in BLOCK_FILES]

#The form files. Must be xlsx file and follow a specified format. The list must also have the same number of elements as the block files.
#If a you wish not to display any questionnaires, specify only None values. If you want to remove a questionnaire between blocks, replace the questionnaire path with a None value
FORM_FILES = [None, "data/input/CAPE.xlsx", "data/input/5D_Curiosity.xlsx", "data/input/NfCS_full.xlsx"] # e.g. ["CAPE.xlsx", None, "NfCS_full.xlsx"] or [None, None, None]

#Message strings:
FAILED_TRIAL = ""
TRIAL_INFO = ""


if (len(FORM_FILES) != len(BLOCK_FILES) + 1):
    raise ValueError("There must be as many FORM_FILES as there are BLOCK_FILES")
    
    
    
    
    
"""
Practice run: 3 boxes before finishing. Locations: random. Practice_trial excel file X
Info banner: Top of the screen on the trial scene.
Info screen between each trial
Data output: summary for all. And decision should be recorded
Dialog box: ID age sex 
No decision circles on entering each trial X
No rating on premature end X
Decision allowed on last box X
"""