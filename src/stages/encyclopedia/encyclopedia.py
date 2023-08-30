from src.stages.stage import Stage
from src.logic.animal import classFromType, TYPE_TO_CLASS
from src.logic.ui import TextBox, MenuButton
from src.util import graphics as gr
from src.util import colors as col
from pygame import Rect

class Encyclopedia(Stage):

    def __init__(self, app, state):
        super().__init__(app, state)

        # encyclopedia
        self.encyclopediaUnlocked = []
        self.curr_entry_idx = -1
        # create COMPLETE dictionary of animal species (dictionary of dictionaries)
        self.encyclopediaComplete = {}
        for typeID in TYPE_TO_CLASS:
            speciesClass = classFromType(typeID)
            speciesName = speciesClass.getNameCommon()
            speciesEntry = {'Common Name': speciesName,
                            'Scientific Name': speciesClass.getNameScientific(),
                            'Conservation Status': speciesClass.getConservationStatus(),
                            'Habitat': speciesClass.getHabitat(),
                            'Description': speciesClass.getDescription(),
                            'Height range': speciesClass.getHeightRange(),
                            'Weight range': speciesClass.getWeightRange(),
                            'Art filename': speciesClass.getFilename()}
            self.encyclopediaComplete[speciesName] = speciesEntry

            # TODO: DELETE AFTER TESTING
            newEntry = self.encyclopediaComplete[speciesName]
            self.encyclopediaUnlocked.append(newEntry)

        # display state
        self.showUi = True
        self.action = ""
        # ui elements
        self.TextBox = TextBox(self, Rect(6, 6, gr.SCR_WID-12, gr.SCR_HT/2-10))
        self.nextButton = MenuButton(self, Rect(200, 180, 100, 40), "NEXT")
        self.prevButton = MenuButton(self, Rect(20, 180, 100, 40), "PREVIOUS")
        self.exitButton = MenuButton(self, Rect(20, 230, 280, 40), "EXIT")

    """Loading methods"""
    def load(self):
        super().load()

        # load triggers
        self.TextBox.changeText("This is your encyclopedia!")
    def unload(self):
        pass

    """Input methods"""
    def mouseUp(self, position):
        # nav buttons
        if self.nextButton.bounds.collidepoint(position):
            # action trigger
            if self.curr_entry_idx >= len(self.encyclopediaUnlocked)-1:
                pass
            else:
                self.curr_entry_idx += 1
                # self.drawEntry()
                self.draw()
            # self.actionTimer = 0  # what is this for...? copied from run button
        if self.prevButton.bounds.collidepoint(position):
            # action trigger
            if self.curr_entry_idx <= 0:
                pass
            else:
                self.curr_entry_idx -= 1
                # self.drawEntry()
                self.draw()
        if self.exitButton.bounds.collidepoint(position):
            # action trigger
            self.switchStage("world")

    """Update methods"""
    def addEntry(self, animalName):
        newEntry = self.encyclopediaComplete[animalName]
        self.encyclopediaUnlocked.append(newEntry)

    def update(self):
        # update action
        # if self.action == "add-entry":
        #     self.addEntry(self,animalName)
        # if self.action == "feeding-berry":
        #     self.updateFeedingBerry()
        # elif self.action == "run-away":
        #     self.updateRunAway()

        # update ui elements
        self.TextBox.update()

        # update showing ui
        # if self.TextBox.showingAllText() and self.action == "":
        if self.TextBox.showingAllText():
            self.showUi = True

    """Draw methods"""
    def draw(self):
        # def drawEntry(self):
        if self.curr_entry_idx >= 0:
            currSpecies = self.encyclopediaUnlocked[self.curr_entry_idx]

            (heightMin, heightMax) = currSpecies.get('Height range')
            text_height = "Ht.: " + str(heightMin) + "-" + str(heightMax) + " m"
            (weightMin, weightMax) = currSpecies.get('Weight range')
            text_weight = "Wt.: " + str(weightMin) + "-" + str(weightMax) + " kg"

            text_surface_list = [gr.FONT_12.render(currSpecies.get('Common Name'), False, (0, 0, 0)),
                                 gr.FONT_12.render(currSpecies.get('Scientific Name'), False, (0, 0, 0)),
                                 gr.FONT_12.render(currSpecies.get('Conservation Status'), False, (0, 0, 0)),
                                 gr.FONT_12.render(currSpecies.get('Habitat'), False, (0, 0, 0)),
                                 gr.FONT_12.render(text_height, False, (0, 0, 0)),
                                 gr.FONT_12.render(text_weight, False, (0, 0, 0))]

            # Display each text
            for i in range(len(text_surface_list)):
                text_rect = text_surface_list[i].get_rect()
                text_rect.center = (gr.SCR_WID/2, gr.SCR_HT/2 + 18*i)
                self.drawUpImage(text_surface_list[i], text_rect)

            self.TextBox.changeText(currSpecies.get('Description'))

        self.drawUpRect(col.JOURNAL_BGROUND, gr.BOUND_SCR)
        self.drawLowRect(col.JOURNAL_BGROUND, gr.BOUND_SCR)
        self.TextBox.draw()

        #showing the current ui
        if self.showUi:
            # #berries
            # for b in self.berryButtons:
            #     b.draw()
            # #catch and run
            # self.catchButton.draw()
            # self.runButton.draw()

            # nav buttons
            self.nextButton.draw()
            self.prevButton.draw()
            self.exitButton.draw()
