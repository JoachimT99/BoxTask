"""
Serves as a singleton to keep an ordered view of program constants
"""

import os
#Grid Constants
BORDER = 50 #Defines the general border inside the window that should be padded in
CENTER_OFFSET = (0, 100)
SQUARE_SIZE = 150 #Length of the sides of a box
MATRIX = (4, 3) #The grid size

#Application constants
WINDOW_SIZE = [1920, 1080] #The window resolution
FULLSCREEN = True
BACKGROUND_COLOR = (-0.5, -0.5, -0.5) # A normalized rgb value with each channel taking a value between -1 and 1
# Setting up stimuli
CONFIDENCE_RATING_LVLS = [f"{x}%" for x in range(100, 50, -10)] + [f"{x}%" for x in range(50, 101, 10)]
RATING_TEXT_SCALE = 0.75


#INPUT FILE SPECIFICATION:
PRACTICE_RUN = "practice.xlsx"
BLOCK_FILES = ["colour_sequences_12.xlsx", "colour_sequences_6or9_a.xlsx", "colour_sequences_6or9_b.xlsx"] #The blocks of sequences. Must be xlsx file and follow a specified format

#The form files. Must be xlsx file and follow a specified format. The list must also have the same number of elements as the block files.
#If a you wish not to display any questionnaires, specify only None values. If you want to remove a questionnaire between blocks, replace the questionnaire path with a None value
FORM_FILES = [None, "NfCS_full.xlsx", "5D_Curiosity.xlsx", "CAPE.xlsx"] # e.g. ["CAPE.xlsx", None, "NfCS_full.xlsx"] or [None, None, None]

#Message strings:
TRIAL_BASE_INFO = "This NOT a practice trial. "
FAILED_TRIAL = "You failed the trial because too many boxes were opened! "
COMPLETED_TRIAL = "You completed the trial! "

TIMED_TRIAL_INFO = "The next trial is a timed trial. "
NOT_TIMED_INFO = "The next trial is NOT a timed trial. "

BANNER_TIMED = "This is a timed trial "
BANNER_NOT_TIMED = "This is not a timed trial "

PRACTICE_TRIAL_INFO = "The next trial is a practice trial! "
FAILED_PRACTICE_TRIAL = "You failed the practice trial. The real trial starts now "
COMPLETED_PRACTICE_TRIAL = "You completed the practice trial. The real trial starts now "

QUESTIONNAIRE_INFO = "The next segment is a questionnaire. Please answer the coming questions!"


if (len(FORM_FILES) != len(BLOCK_FILES) + 1):
    raise ValueError("There must be as many FORM_FILES as there are BLOCK_FILES")
    