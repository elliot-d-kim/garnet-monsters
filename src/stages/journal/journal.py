from src.stages.stage import Stage
from src.util import graphics as gr
from src.util import colors as col
from src.logic.animal import TYPE_TO_CLASS, classFromType
from src.logic.ui import Label, MultiLabel, TextButton
from pygame import Rect

class Journal(Stage):

    def __init__(self, app, state):
        super().__init__(app, state)

        #animals that have been seen
        self.animalsSeen = {}
        for idx in TYPE_TO_CLASS:
            self.animalsSeen[idx] = False

        #create the id labels
        self.animalIdLabels = {}
        y = 28
        for idx in TYPE_TO_CLASS:
            self.animalIdLabels[idx] = Label(self, Rect(8, y, gr.SCR_WID-16, 20),
                                             str(classFromType(idx).getTypeId()).zfill(3) + " -", gr.FONT_12,
                                             col.VERY_DARK_GRAY, col.GRAY)
            y += 20

        #back button
        self.backButton = TextButton(self, Rect(4, gr.SCR_HT-28-4, 52, 28), col.JOURNAL_SHADED, "Back", gr.FONT_12, col.BLACK, col.GRAY, yOffset=-2)

        #top display state
        self.topImageFrame, self.topImageAnimal = None, None
        self.topCommonLabel = MultiLabel(self, Rect(112, 8, 0, 0), "", gr.FONT_16, col.BLACK, 14, 18)
        self.conserveStatus = MultiLabel(self, Rect(240, 52, 0, 0), "", gr.FONT_12, col.BLACK, 6, 14)
        self.scientificNameLabel = MultiLabel(self, Rect(112, 70, 0, 0), "", gr.FONT_10, col.DARK_GRAY, 24, 12)
        self.habitatLabel = MultiLabel(self, Rect(8, 128, 0, 0), "", gr.FONT_10, col.DARK_GRAY, 12, 12)
        self.minWeightLabel = Label(self, Rect(40, 202, 0, 0), "", gr.FONT_10, col.DARK_GRAY, col.DARK_GRAY, drawLow=False)
        self.maxWeightLabel = Label(self, Rect(40, 214, 0, 0), "", gr.FONT_10, col.DARK_GRAY, col.DARK_GRAY, drawLow=False)
        self.minHeightLabel = Label(self, Rect(40, 228, 0, 0), "", gr.FONT_10, col.DARK_GRAY, col.DARK_GRAY, drawLow=False)
        self.maxHeightLabel = Label(self, Rect(40, 240, 0, 0), "", gr.FONT_10, col.DARK_GRAY, col.DARK_GRAY, drawLow=False)
        self.descriptLabel = MultiLabel(self, Rect(110, 110, 0, 0), "", gr.FONT_10, col.DARK_GRAY, 25, 12)

    """ Loading Methods """
    def load(self):
        super().load()

        #set which animals have been seen
        for a in self.state.analyzedAnimals:
            self.animalsSeen[a.getTypeId()] = True

        #update the id labels
        for idx in TYPE_TO_CLASS:
            first = self.animalIdLabels[idx].text.split('-')[0]
            self.animalIdLabels[idx].changeText(first + "- ??")

            for a in self.state.analyzedAnimals:
                if a.getTypeId() == idx:
                    self.animalIdLabels[idx].changeText(self.animalIdLabels[idx].text[:6] + a.getNameCommon())
                    break

        #top state
        self.loadTopDisplayState()
    def loadTopDisplayState(self):
        self.topImageFrame = self.loadImage("src/assets/art/journal-image-frame.png")
        self.topImageAnimal = None

        self.topCommonLabel.changeText("")
        self.conserveStatus.changeText("")
        self.scientificNameLabel.changeText("")
        self.descriptLabel.changeText("")
        self.habitatLabel.changeText("")
        self.maxWeightLabel.changeText("")
        self.minWeightLabel.changeText("")
        self.maxHeightLabel.changeText("")
        self.minHeightLabel.changeText("")
    def loadTopDisplayAnimal(self, animal):
        self.topImageAnimal = self.loadImage("src/assets/sprites/animals/" + animal.getFilename() + ".png")

        self.topCommonLabel.changeText(animal.getNameCommon())

        status = animal.getConservationStatus()
        self.conserveStatus.changeText(status)
        if status == "LC":
            self.conserveStatus.changeTextColor(col.CONSERVE_GREEN)
        elif status == "NT":
            self.conserveStatus.changeTextColor(col.CONSERVE_YELLOW)
        elif status == "VU" or status == "EN" or status == "CR":
            self.conserveStatus.changeTextColor(col.CONSERVE_ORANGE)
        elif status == "EW" or status == "EX":
            self.conserveStatus.changeTextColor(col.CONSERVE_RED)

        self.scientificNameLabel.changeText(animal.getNameScientific())
        self.descriptLabel.changeText(animal.getDescription())

        self.habitatLabel.changeText(animal.getHabitat())
        wtRng = animal.getWeightRange()
        self.minWeightLabel.changeText(str(wtRng[0]) + "kg-")
        self.maxWeightLabel.changeText(str(wtRng[1]))
        htRng = animal.getHeightRange()
        self.minHeightLabel.changeText(str(htRng[0]) + "m-")
        self.maxHeightLabel.changeText(str(htRng[1]) + "m")

    def unload(self):
        pass

    """ Update Methods """
    def update(self):
        self.backButton.mouseUpdate(self.mousePos)

        for idx in TYPE_TO_CLASS:
            self.animalIdLabels[idx].update()
            if self.animalsSeen[idx]:
                self.animalIdLabels[idx].mouseUpdate(self.mousePos)

    """ Input Methods """
    def mouseUp(self, position):
        if self.backButton.bounds.collidepoint(position):
            self.switchStage("world")

        for idx in TYPE_TO_CLASS:
            if self.animalsSeen[idx] and self.animalIdLabels[idx].bounds.collidepoint(position):
                for a in self.state.analyzedAnimals:
                    if a.getTypeId() == idx:
                        self.loadTopDisplayAnimal(a)
                        break
                break

    """ Drawing Methods """
    def draw(self):
        #draw the backgrounds
        self.drawUpRect(col.JOURNAL_BGROUND, gr.BOUND_SCR)
        self.drawLowRect(col.JOURNAL_BGROUND, gr.BOUND_SCR)

        #draw lower title
        speciesTitleSurface = gr.FONT_20.render("Species", False, col.VERY_DARK_GRAY)
        speciesTitleRect = speciesTitleSurface.get_rect()
        self.drawLowImage(speciesTitleSurface, Rect(gr.SCR_WID/2-speciesTitleRect.w/2, 4, 0, 0))
        self.backButton.draw()

        #draw the labels
        for idx in TYPE_TO_CLASS:
            self.animalIdLabels[idx].draw()

        #draw top stuff
        self.drawTopDetails()
    def drawTopDetails(self):
        #frame and image
        self.drawUpImage(self.topImageFrame, Rect(4, 4, 100, 100))
        if self.topImageAnimal is not None:
            self.drawUpImage(self.topImageAnimal, Rect(6, 6, 96, 96))

        #name
        self.topCommonLabel.draw()
        #divider
        self.drawUpRect(col.BLACK, Rect(112, 46, gr.SCR_WID-112-12, 2))
        #conservation
        surface = gr.FONT_12.render("Conservation: ", False, col.VERY_DARK_GRAY)
        self.drawUpImage(surface, Rect(112, 52, 0, 0))
        self.conserveStatus.draw()
        #scientific name
        self.scientificNameLabel.draw()

        #habitat
        surface = gr.FONT_12.render("Habitat", False, col.VERY_DARK_GRAY)
        self.drawUpImage(surface, Rect(16, 112, 0, 0))
        self.drawUpRect(col.VERY_DARK_GRAY, Rect(16, 126, 68, 1))
        self.habitatLabel.draw()

        #details
        surface = gr.FONT_12.render("Details", False, col.VERY_DARK_GRAY)
        self.drawUpImage(surface, Rect(16, 190, 0, 0))
        self.drawUpRect(col.VERY_DARK_GRAY, Rect(16, 204, 68, 1))
        surface = gr.FONT_12.render("Wt:", False, col.VERY_DARK_GRAY)
        self.drawUpImage(surface, Rect(8, 208, 0, 0))
        self.minWeightLabel.draw()
        self.maxWeightLabel.draw()
        surface = gr.FONT_12.render("Ht:", False, col.VERY_DARK_GRAY)
        self.drawUpImage(surface, Rect(8, 234, 0, 0))
        self.minHeightLabel.draw()
        self.maxHeightLabel.draw()

        #description
        self.drawUpRect(col.JOURNAL_SHADED, Rect(108, 108, gr.SCR_WID-108-6, gr.SCR_HT-108-6))
        self.descriptLabel.draw()
