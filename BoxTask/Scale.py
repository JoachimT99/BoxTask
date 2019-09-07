import Constants
from psychopy import visual

class Scale():
    """
    The Scale class exists to adapt the RatingScale class to get the actual rating data in integer values
    instead of the choices given to the RatingScale class. This class uses composition.

    Note:
        To use more of the functions in the RatingScale class, this class must be extended with pass-through methods.
        It was too much work to use inheritance, so this ad hoc approach was used.
    """
    def __init__(self, win, colours):
        """
        This method initializes a new RatingScale object to use as the rating scale.
        Params:
            win: A window object representing the window the object should be drawn to
            colours: A colours tuple containing two colours
        Returns:
            None
        """
        self.scale = visual.RatingScale(win,
                                        pos=[0, -400],
                                        choices=Constants.CONFIDENCE_RATING_LVLS,
                                        textSize=Constants.RATING_TEXT_SCALE,
                                        stretch=2.5,
                                        scale=f"In your opinion, what is the most dominant colour between {colours[2]} and {colours[3]}",
                                        )
    def getRating(self):
        """
        Returns the actual number rating instead of indexing the choice dictionary and returning that value.
        Params:
            None
        Returns:
            int: number value for the chosen rating.
        """
        return self.scale.markerPlacedAt * self.scale.autoRescaleFactor

    def noResponse(self):
        """
        Pass-through method to the RatingScale object
        Params:
            None
        Returns:
            bool: depending on wether a rating has been selected
        """
        return self.scale.noResponse
    
    def reset(self):
        """
        Pass-through method to the RatingScale object
        Params:
            None
        Returns:
            None
        """
        self.scale.reset()

    def draw(self):
        """
        Pass-through method to the RatingScale object
        Params:
            None
        Returns:
            None
        """
        self.scale.draw()