import numpy as np

from src.stages.stage import Stage
from src.logic.animal import classFromType
from src.logic.ui import TextBox, BerryButton, TextButton
from src.util import graphics as gr
from src.util import colors as col
from src.logic.state import BERRY_TYPES, BERRY_NAMES
from pygame import Rect
import pygame


class Catch(Stage):

    def __init__(self, app, state):
        super().__init__(app, state)

        # assets
        self.lowBackground, self.upBackground, self.progressBar = None, None, None
        self.encounterAnimal, self.encounterSprite = None, None

        # display state
        self.showUi = True
        self.action = ""
        self.actionTimer = 0
        self.actionDuration = 0

        # ui elements
        self.textBox = TextBox(self, Rect(6, 6, gr.SCR_WID-12, 48))
        self.berryButtons = []
        for i in range(0, 5):
            self.berryButtons.append(BerryButton(self, Rect(20 + 60 * i, 72, 40, 40),
                                            "src/assets/ui/berries/" + BERRY_TYPES[i] + ".png",
                                            "src/assets/ui/berries/" + BERRY_TYPES[i] + "-gray.png", i))
        self.analyzeButton = TextButton(self, Rect(20, 130, 130, 40), col.ANALYZE_CYAN, "Analyze", gr.FONT_16, col.VERY_LIGHT_GRAY, col.VERY_DARK_GRAY)
        self.runButton = TextButton(self, Rect(170, 130, 130, 40), col.RUNAWAY_ORANGE, "Run Away", gr.FONT_16, col.VERY_LIGHT_GRAY, col.VERY_DARK_GRAY)

        # probability mechanics
        self.catchChance = 0
        self.fleeChance = 0
        self.analyzeIsSuccess = True
        self.animalIsFleeing = False

    """
    Loading methods
    """
    def load(self):
        super().load()

        #load assets
        self.encounterAnimal = classFromType(self.state.encounterTypeId)
        self.upBackground = self.loadImage("src/assets/art/catch-art-" + self.encounterAnimal.getTopCatchArt() + ".png")
        self.lowBackground = self.loadImage("src/assets/art/catch-art-low.png")
        self.progressBar = self.loadImage("src/assets/ui/progress-bar.png")
        self.encounterSprite = pygame.transform.scale(self.loadImage("src/assets/sprites/animals/" + self.encounterAnimal.getFilename() + ".png"), (96*2, 96*2))

        #load triggers
        self.showUi = False
        self.textBox.changeText("A wild " + self.encounterAnimal.getNameCommon() + " appeared!")

        #reset state
        self.action = ""
        self.actionTimer = 0
        self.actionDuration = 0

        #berry counts
        for i in range(0, len(BERRY_TYPES)):
            self.berryButtons[i].setImageOn(self.state.berryCounts[i] > 0)

        #probability
        self.catchChance = self.encounterAnimal.getBaseCatchChance()
        self.fleeChance = self.encounterAnimal.getBaseFleeChance()
        self.analyzeIsSuccess = False
        self.animalIsFleeing = False
    def unload(self):
        self.encounterSprite = None
        self.encounterAnimal = None

    """
    Input methods
    """
    def mouseUp(self, position):
        # text box
        if self.textBox.bounds.collidepoint(position):
            if self.textBox.showingAllText():
                self.textBox.click(position)
                self.textBoxClickEvent()
            else:
                self.textBox.click(position)

        # general ui
        if self.showUi:
            # berry buttons
            for i in range(0, len(self.berryButtons)):
                if self.berryButtons[i].bounds.collidepoint(position) and self.state.berryCounts[i] > 0:
                    self.feedBerry(i)
            # analyze button
            if self.analyzeButton.bounds.collidepoint(position):
                #start action
                self.action = "analyze"
                self.showUi = False
                self.textBox.changeText("Analyzing...")
                self.actionTimer = 0

                #probability
                rand = np.random.uniform()
                if rand <= self.catchChance:
                    self.actionDuration = 2.5*gr.FPS
                    self.analyzeIsSuccess = True
                else:
                    self.actionDuration = (0.4 + 1.8 * (rand-self.catchChance)/(1-self.catchChance)) * gr.FPS
                    self.analyzeIsSuccess = False
            # run button
            elif self.runButton.bounds.collidepoint(position):
                # action trigger
                self.action = "run-away"
                self.showUi = False
                self.textBox.changeText("You ran away.")
                self.actionTimer = 0
    def feedBerry(self, idx):
        # update berry
        self.state.berryCounts[idx] -= 1
        if self.state.berryCounts[idx] == 0:
            self.berryButtons[idx].setImageOn(False)

        # action trigger
        self.action = "feeding-berry"
        self.showUi = False

        giveText  = "You gave it a " + str(BERRY_NAMES[idx]) + ". "
        if BERRY_TYPES[idx] == "berry-sweet":
            self.textBox.changeText(giveText + "It liked the taste and became a little more calm!")
            self.catchChance *= 1.2
        elif BERRY_TYPES[idx] == "berry-sour":
            self.textBox.changeText(giveText + "It liked the taste and became a little more friendly!")
            self.fleeChance *= 0.83
        elif BERRY_TYPES[idx] == "berry-blue" or BERRY_TYPES[idx] == "berry-red":
            #get the amount it likes this berry
            amt = self.encounterAnimal.likesBlueRedBerry()
            if BERRY_TYPES[idx] == "berry-blue":
                amt = amt[0]
            elif BERRY_TYPES[idx] == "berry-red":
                amt = amt[1]

            #modify the values
            self.catchChance *= amt
            self.fleeChance *= 1/amt

            #output text
            if amt > 1.3:
                self.textBox.changeText(giveText + "It loved the taste! It became a lot friendlier and calmer!")
            elif amt > 1.05:
                self.textBox.changeText(giveText + "It liked the taste. It became a little friendlier and calmer.")
            elif amt > 0.95:
                self.textBox.changeText(giveText + "It didn't mind the taste.")
            elif amt > 0.7:
                self.textBox.changeText(giveText + "It did not like the taste. It became less friendly and angrier.")
            else:
                self.textBox.changeText(giveText + "It hated the taste! It became a lot less friendly and a lot angrier!")
        elif BERRY_TYPES[idx] == "berry-star":
            self.textBox.changeText(giveText + "It had never had something so tasty!")
            self.catchChance = 1
            self.fleeChance = 0

        self.textBox.showTriangleForThisText(True)

    """
    Update methods
    """
    def update(self):
        # update action
        if self.action == "analyze":
            self.updateAnalyze()
        elif self.action == "waiting-animal":
            self.updateWaitingAnimal()
        elif self.action == "run-away":
            self.updateRunAway()

        # update ui elements
        self.textBox.update()
        if self.showUi:
            self.analyzeButton.mouseUpdate(self.mousePos)
            self.runButton.mouseUpdate(self.mousePos)

        # update showing ui
        if self.textBox.showingAllText() and self.action == "":
            self.showUi = True
    def updateAnalyze(self):
        if self.textBox.showingAllText():
            self.actionTimer += 1

            if self.actionTimer > self.actionDuration:
                # succeeded
                if self.analyzeIsSuccess:
                    self.action = "analyze-success"
                    self.textBox.changeText("You analyzed the " + self.encounterAnimal.getNameCommon() + "! Its information has been added to the journal.")
                    self.textBox.showTriangleForThisText(True)
                # failed
                else:
                    self.action = "analyze-failure"
                    self.textBox.changeText("It wouldn't hold still so the analysis failed!")
                    self.textBox.showTriangleForThisText(True)
    def updateWaitingAnimal(self):
        if self.textBox.showingAllText() and not self.animalIsFleeing:
            self.action = ""
    def updateRunAway(self):
        if self.textBox.showingAllText():
            self.actionTimer += 1

            if self.actionTimer > 30:
                self.switchStage("world")

    """
    Draw methods
    """
    def draw(self):
        self.drawUpImage(self.upBackground, Rect(0, 0, gr.SCR_WID, gr.SCR_HT))
        self.drawLowImage(self.lowBackground, Rect(0, 0, gr.SCR_WID, gr.SCR_HT))
        self.drawUpImage(self.encounterSprite, Rect(gr.SCR_WID/2-96, 20, 96*2, 96*2))
        self.textBox.draw()

        #showing the current ui
        if self.showUi:
            #berries
            for b in self.berryButtons:
                b.draw()
            #catch and run
            self.analyzeButton.draw()
            self.runButton.draw()

        #progress bar frame
        self.drawUpRect(col.PROGRESS_BAR_GRAY, Rect(35+3, 250+3, 244, 28))
        self.drawUpImage(self.progressBar, Rect(35, 250, 250, 34))

        #actual progress
        if self.action == "analyze":
            self.drawProgressBar(col.PROGRESS_BAR_GREEN, self.actionTimer/(2.5*gr.FPS))
        elif self.action == "analyze-success":
            self.drawProgressBar(col.PROGRESS_BAR_GREEN, 1)
        elif self.action == "analyze-failure":
            self.drawProgressBar(col.PROGRESS_BAR_RED, self.actionTimer/(2.5*gr.FPS))

    """
    Utility Methods
    """
    def decideAnimalFlee(self):
        rand = np.random.uniform()

        #decide on fleeing and text
        if rand <= self.fleeChance:
            self.animalIsFleeing = True
            self.textBox.changeText("The animal fled!")
            self.textBox.showTriangleForThisText(True)
        elif rand <= self.fleeChance*2.5:
            self.textBox.changeText("The animal looks at you warily.")
        elif rand <= self.fleeChance*5:
            self.textBox.changeText("The animal seems content for now.")
        else:
            self.textBox.changeText("The animal seems happy to stay.")
    def textBoxClickEvent(self):
        if self.action == "analyze-failure" or self.action == "feeding-berry":
            self.action = "waiting-animal"
            self.decideAnimalFlee()
        elif self.action == "waiting-animal":
            if self.animalIsFleeing:
                self.switchStage("world")
            else:
                self.action = ""
        elif self.action == "analyze-success":
            self.state.analyzedAnimals.append(self.encounterAnimal)
            self.switchStage("world")
    def drawProgressBar(self, color, percent):
        #back cap
        self.drawUpRect(color, Rect(35+5, 250+6, 1, 22))
        self.drawUpRect(color, Rect(35+6, 250+5, 1, 24))
        #middle bars
        self.drawUpRect(color, Rect(35+7, 250+5, 236*percent, 24))
        #front cap
        self.drawUpRect(color, Rect(35+7+236*percent, 250+5, 1, 24))
        self.drawUpRect(color, Rect(35+7+236*percent+1, 250+6, 1, 22))