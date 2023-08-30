import math, pygame
import numpy as np
from pygame import Rect
from src.logic.state import BERRY_TYPES
from src.stages.stage import Stage
from src.util import graphics as gr, colors as col
from src.stages.world.loader import loadArea
from src.util.tiles import tilePathFromColor, entityPathFromName, getEntityWidth, getEntityHeight, isTileWall
from src.logic.ui import MenuButton
import time, json

#number of frames to display on each half of the connection
CONN_FRMS = 20
#number of frames to display when loading an encounter
ENC_FRAMES = 36
#base encounter chance for each tile of tall grass
ENCOUNTER_CHANCE = 0.2
#animation order for encounter transition
ENCOUNTER_ANIM = [
    (0,3), (1,3), (2,3), (3,3), (3,2), (3,1), (3,0), #bottom and right
    (2,0), (1,0), (0,0), (0,1), (0,2), #top and left
    (1,2), (2,2), (2,1), (1,1) #center
]

class World(Stage):

    # a dictionary that, when loaded, maps tile codes -> tile images
    tileImages = {}
    # a dictionary that, when loaded, maps entity names -> entity images
    entityImages = {}
    # a dictionary that, when loaded, maps bush name-state -> bush images
    bushImages = {}

    def __init__(self, app, state):
        super().__init__(app, state)

        #load the player and camera
        self.player = Player([20,25])
        self.cam = [self.player.pos[0], self.player.pos[1]]

        #load the area data
        self.tiles, self.connections, self.entities, self.camLim, self.encounters, self.bushes =\
            None, None, None, None, None, None
        self.walls = []
        self.bushFullness = {} #elements are 'area-x-y' -> True/False for full, tracks for all bushes (not just in area)
        self.loadAreaData()

        #world menu
        self.showUI = True
        # create button objects
        self.journalButton = MenuButton(self, Rect(20, 40, 100, 40), "JOURNAL")
        self.mapButton = MenuButton(self, Rect(201, 40, 100, 40), "MAP")
        self.bagButton = MenuButton(self, Rect(20, 112, 100, 40), "BAG")
        self.profileButton = MenuButton(self, Rect(201, 112, 100, 40), "PROFILE")
        self.saveButton = MenuButton(self, Rect(20, 184, 100, 40), "SAVE")
        self.exitButton = MenuButton(self, Rect(201, 184, 100, 40), "EXIT")
        self.menuButtons = (self.journalButton, self.mapButton, self.bagButton, self.profileButton, self.saveButton, self.exitButton)

        #connection state
        self.connecting = 0 #0: not connecting, negative: leaving, positive: arriving
        self.connectingDest = None #format: (dstDir, dstArea, dstPos)
        self.connectingFrame = 0

        #encountering state
        self.encountering = 0 #0: not connecting, negative: leaving
        self.encounteringFrame = 0

    """ Loading Methods """
    def load(self):
        super().load()

        #load objects
        self.player.load()
        self.prepareGraphics()
        #reset values
        self.encountering = 0
    def unload(self):
        #unload objects
        self.player.unload()
        #unload tiles and entities
        self.tileImages.clear()
        self.entityImages.clear()
        self.bushImages.clear()

    def loadAreaData(self):
        data = loadArea(self.state.area)
        self.tiles = data[0]
        self.connections = data[1]
        self.entities = data[2]
        self.camLim = data[3]
        self.encounters = data[4]
        self.bushes = data[5]

        #generate the walls
        self.walls.clear()
        self.generateWalls()

        #bushes
        self.loadBushState()
    def generateWalls(self):
        x, y = 0, 0
        for row in self.tiles:
            for t in row:
                if isTileWall(t):
                    self.walls.append(Rect(32*x, 32*y, 32, 32))
                x += 1
            y += 1
            x = 0

        for e in self.entities:
            self.walls.append(Rect(32*e[1], 32*e[2], getEntityWidth(e[0]), getEntityHeight(e[0])))
        for b in self.bushes:
            self.walls.append(Rect(32*b[1], 32*b[2], 32, 32))
    def loadBushState(self):
        for i in range(0, len(self.bushes)):
            #add it to the dictionary if it isn't there
            string = self.state.area + '-' + str(self.bushes[i][1]) + '-' + str(self.bushes[i][2])
            if string not in self.bushFullness:
                self.bushFullness[string] = False

            #randomly set to full
            rand = np.random.uniform()
            if rand < 0.4:
                self.bushFullness[string] = True

            #copy value from fullness dict to bush value
            self.bushes[i][3] = self.bushFullness[string]

    def prepareGraphics(self):
        #load tiles
        self.tileImages.clear()
        for arr in self.tiles:
            for t in arr:
                if not t in self.tileImages:
                    self.tileImages[t] = self.loadImage(tilePathFromColor(t))

        #load entities
        self.entityImages.clear()
        for e in self.entities:
            if not e[0] in self.entityImages:
                self.entityImages[e[0]] = self.loadImage(entityPathFromName(e[0]))

        #load bushes
        for berry in BERRY_TYPES[:4]:
            type = berry.split('-')[1]
            self.bushImages[type + '-empty'] = self.loadImage("src/assets/entities/bushes/bush-" + type + "-empty.png")
            self.bushImages[type + '-full'] = self.loadImage("src/assets/entities/bushes/bush-" + type + "-full.png")

    """ Updating Methods """
    def update(self):
        # check if player should be connecting
        if self.connecting == 0 and self.encountering == 0:
            self.checkConnect()

        # normal actions
        if self.connecting == 0 and self.encountering == 0:
            keys = pygame.key.get_pressed()
            self.player.move(keys, self)
            self.player.checkForEncounter(self)
            if keys[pygame.K_SPACE]:
                self.harvestCheck()
        # connecting
        elif self.connecting != 0:
            self.evolveConnect()
        # encountering
        elif self.encountering != 0:
            self.evolveEncounter()

        # update camera
        self.updateCamera(self.player)

        # load state
        if self.state.load:
            self.loadAreaData()
            self.prepareGraphics()

            self.player.pos = [int(pos*32) for pos in self.state.player_pos]
            self.player.facing = self.state.player_facing

            self.state.load = False

    def checkConnect(self):
        for c in self.connections:
            if self.player.pos[0] / 32 == c[0][0] and self.player.pos[1] / 32 == c[0][1] and self.player.facing == c[1]:
                self.connecting = -1
                self.connectingDest = (c[1], c[2], c[3])
                self.connectingFrame = 0

                self.player.action = "stand"
                break
    def evolveConnect(self):
        self.connectingFrame += 1

        # load the new area
        if self.connectingFrame == CONN_FRMS and self.connecting == -1:
            self.connecting = 2
            self.connectingFrame = 0

            # self.area = self.connectingDest[1]
            self.state.area = self.connectingDest[1]
            self.player.pos[0] = self.connectingDest[2][0] * 32
            self.player.pos[1] = self.connectingDest[2][1] * 32

            self.loadAreaData()
            self.prepareGraphics()
        # end the connection
        elif self.connectingFrame == CONN_FRMS and self.connecting == 1:
            self.connecting = 0
            self.connectingFrame = 0
        # pause in black screen for a bit
        elif self.connectingFrame == CONN_FRMS / 2 and self.connecting == 2:
            self.connecting = 1
            self.connectingFrame = 0
    def evolveEncounter(self):
        self.encounteringFrame += 1

        if self.encounteringFrame > ENC_FRAMES:
            #set state values
            self.state.encounterTypeId = self.encountering

            #reset values
            self.encounteringFrame = 0
            self.encountering = 0

            #switch stage
            self.switchStage("catch")
    def updateCamera(self, player):
        self.cam = player.pos.copy()

        #camera clamp
        if not self.camLim is None:
            # x clamp
            if self.cam[0] < 32*self.camLim[0]:
                self.cam[0] = 32*self.camLim[0]
            elif self.cam[0] > 32*self.camLim[2]:
                self.cam[0] = 32*self.camLim[2]
            # y clamp
            if self.cam[1] < 32*self.camLim[1]:
                self.cam[1] = 32*self.camLim[1]
            elif self.cam[1] > 32*self.camLim[3]:
                self.cam[1] = 32*self.camLim[3]

        self.cam[0] -= gr.SCR_WID/2 - 16
        self.cam[1] -= gr.SCR_HT/2 - 16
    def harvestCheck(self):
        x, y = self.player.pos[0]/32, self.player.pos[1]/32
        if self.player.facing == "left":
            x -= 1
        elif self.player.facing == "right":
            x += 1
        elif self.player.facing == "up":
            y -= 1
        elif self.player.facing == "down":
            y += 1

        #find if there is a bush
        for i in range(0, len(self.bushes)):
            bush = self.bushes[i]
            if bush[1] == x and bush[2] == y:
                #check if the bush is full
                if bush[3]:
                    self.bushes[i][3] = False
                    self.bushFullness[self.state.area + "-" + str(bush[1]) + "-" + str(bush[2])] = False
                    if bush[0] == "sweet":
                        self.state.berryCounts[0] += 1
                    elif bush[0] == "sour":
                        self.state.berryCounts[1] += 1
                    elif bush[0] == "blue":
                        self.state.berryCounts[2] += 1
                    elif bush[0] == "red":
                        self.state.berryCounts[3] += 1

                break

    """ Drawing Methods """
    def draw(self):
        self.drawUpRect(col.BLACK, Rect(0, 0, gr.SCR_WID, gr.SCR_HT))

        #draw main stuff
        self.drawGrid(self.cam)
        self.drawTiles(self.cam)
        self.drawEntities(self.cam)
        self.drawBushes(self.cam)
        self.player.draw(self, self.cam)
        self.drawWorldMenu()

        #draw connecting stuff
        if self.connecting != 0:
            self.drawConnect(self.connectingFrame)
        elif self.encountering != 0:
            self.drawEncounter(self.encounteringFrame)
    def drawConnect(self, frame):
        w = gr.SCR_WID/2
        h = gr.SCR_HT/2

        #leaving area
        if self.connecting == -1:
            self.drawUpRect(col.BLACK, Rect(0, 0, w*frame/CONN_FRMS, 2*h))
            self.drawUpRect(col.BLACK, Rect(w+w*(1-frame/CONN_FRMS), 0, w*frame/CONN_FRMS+3, 2*h))
            self.drawUpRect(col.BLACK, Rect(0, 0, 2*w, h*frame/CONN_FRMS))
            self.drawUpRect(col.BLACK, Rect(0, h+h*(1-frame/CONN_FRMS), 2*w, h*frame/CONN_FRMS+3))
        #entering area
        elif self.connecting == 1:
            self.drawUpRect(col.BLACK, Rect(0, 0, w*(1-frame/CONN_FRMS), 2*h))
            self.drawUpRect(col.BLACK, Rect(w+w*frame/CONN_FRMS, 0, w*(1-frame/CONN_FRMS)+3, 2*h))
            self.drawUpRect(col.BLACK, Rect(0, 0, 2*w, h*(1-frame/CONN_FRMS)))
            self.drawUpRect(col.BLACK, Rect(0, h+h*frame/CONN_FRMS, 2*w, h*(1-frame/CONN_FRMS)+3))
        #black screen pause
        elif self.connecting == 2:
            self.drawUpRect(col.BLACK, Rect(0, 0, 2*w, 2*h))
    def drawEncounter(self, frame):
        for i in range(0, min(int(frame/2), 16)):
            pos = ENCOUNTER_ANIM[i]
            self.drawUpRect(col.BLACK, Rect(pos[0]*gr.SCR_WID/4, pos[1]*gr.SCR_HT/4, gr.SCR_WID/4, gr.SCR_HT/4))
    def drawGrid(self, cam):
        # draw horizontal
        yStart = math.floor(cam[1] / 32)
        for i in range(yStart, yStart + 11):
            self.drawUpRect(col.VERY_DARK_GRAY, Rect(0, 32 * i - 1 - cam[1], gr.SCR_WID, 2))

        # draw vertical
        xStart = math.floor(cam[0] / 32)
        for i in range(xStart, xStart + 11):
            self.drawUpRect(col.VERY_DARK_GRAY, Rect(32 * i - 1 - cam[0], 0, 2, gr.SCR_HT))
    def drawTiles(self, cam):
        x, y = 0, 0
        # loop through the tile map
        for row in self.tiles:
            for t in row:
                # create the rectangle
                rect = pygame.Rect(32*x - cam[0], 32*y - cam[1], 32, 32)

                # check if the rectangle is on the screen
                if rect.colliderect(gr.BOUND_SCR):
                    # draw the tile
                    if t != 0:
                        self.drawUpImage(self.tileImages[t], rect)
                # transition to next tile
                x += 1
            y += 1
            x = 0
    def drawEntities(self, cam):
        for ent in self.entities:
            rect = pygame.Rect(32*ent[1]-cam[0], 32*ent[2]-cam[1], getEntityWidth(ent[0]), getEntityHeight(ent[0]))

            if rect.colliderect(gr.BOUND_SCR):
                # draw the entity
                self.drawUpImage(self.entityImages[ent[0]], rect)
    def drawBushes(self, cam):
        for b in self.bushes:
            rect = pygame.Rect(32*b[1]-cam[0], 32*b[2]-cam[1], 32, 32)

            if rect.colliderect(gr.BOUND_SCR):
                if self.bushFullness[self.state.area + '-' + str(b[1]) + '-' + str(b[2])]:
                    self.drawUpImage(self.bushImages[b[0] + "-full"], rect)
                else:
                    self.drawUpImage(self.bushImages[b[0] + "-empty"], rect)
    def drawWorldMenu(self):
        #
        self.drawLowRect(col.JOURNAL_SHADED_DARK, gr.BOUND_SCR)

        # create and draw the rectangle
        x, y = 0, 0  # placeholder x and y values for initialize the rectangle
        width = .85 * gr.SCR_WID
        height = .80 * gr.SCR_HT
        rect = Rect(x, y, width, height)
        rect.center = (gr.SCR_WID / 2, gr.SCR_HT / 2 - 10)  # center the rectangle
        self.drawLowRect(col.JOURNAL_BGROUND, rect)

        # create and draw the rectangle's border
        border = pygame.Rect(x, y, width + 0.01 * gr.SCR_WID, height + 0.01 * gr.SCR_HT)
        border.center = (gr.SCR_WID / 2, gr.SCR_HT / 2 - 10)  # center the border
        self.drawLowRectRoundedBorders("black", border)

        # display menu buttons
        for button in self.menuButtons:
            if button.bounds.collidepoint(self.mousePos):
                button.draw(col.VERY_LIGHT_GRAY)
            else:
                button.draw()

    def saveState(self):
        saveData = {
            'area': self.state.area,
            'pos_x': int(self.player.pos[0]/32),
            'pos_y': int(self.player.pos[1]/32),
            'facing': self.player.facing,
            'analyzedAnimalsTypeIDs': [x.getTypeId() for x in self.state.analyzedAnimals],
            'berryCounts': self.state.berryCounts,
            'playerID': self.state.playerID,
            'licenseDateStr': self.state.licenseDateStr
        }

        with open('saveFile.txt', 'w') as store_data:
            json.dump(saveData, store_data, indent=6)

        messageSurf = gr.FONT_12.render('GAME SAVED.', False, col.BLACK)
        messageRect = messageSurf.get_rect()
        messageRect.center = (int(gr.SCR_WID / 2), int(0.93 * gr.SCR_HT))
        self.drawLowImage(messageSurf, messageRect)
        pygame.display.update()
        time.sleep(1)

    def mouseUp(self, position):
        if self.mapButton.bounds.collidepoint(position):
            # self.switchStage("map")
            pass
        elif self.journalButton.bounds.collidepoint(position):
            self.switchStage("journal")
        elif self.exitButton.bounds.collidepoint(position):
            self.switchStage("splash")
        elif self.bagButton.bounds.collidepoint(position):
            self.switchStage("bag")
        elif self.saveButton.bounds.collidepoint(position):
            self.saveState()
        elif self.profileButton.bounds.collidepoint(position):
            self.switchStage("profile")


class Player:

    sprites = {
        "stand-up": None,
        "stand-down": None,
        "stand-left": None,
        "stand-right": None,

        "walk-left": None,
        "walk-right": None,
        "walk-down-l": None,
        "walk-down-r": None,
        "walk-up-l": None,
        "walk-up-r": None,
    }
    dirs = ["left", "right", "up", "down"]

    def __init__(self, pos):
        self.pos = [32*pos[0], 32*pos[1]]
        self.action = "stand"
        self.facing = "down"
        self.walkFrame = 0

        #whether this tile has been checked for encounters
        self.encounterCheck = False

        # player detection rect in order L, R, U, D
        self.relDetect = [
            pygame.Rect(-4, 12, 8, 8),
            pygame.Rect(28, 12, 8, 8),
            pygame.Rect(12, -4, 8, 8),
            pygame.Rect(12, 28, 8, 8)
        ]

    """ Loading Methods """
    def load(self):
        for s in self.sprites:
            self.sprites[s] = Stage.loadImage("src/assets/sprites/chars/player-" + s + ".png")
    def unload(self):
        for s in self.sprites:
            self.sprites[s] = None

    """ Moving Methods """
    def getDetect(self):
        arr = []
        for i in range(0, len(self.relDetect)):
            arr.append(self.relDetect[i].copy().move(self.pos[0], self.pos[1]))
        return arr
    def move(self, keys, world):
        collision = list(map(lambda rec: rec.collidelist(world.walls), self.getDetect()))

        # if in the center of a tile
        if abs(self.pos[0])%32 == 0 and abs(self.pos[1])%32 == 0:
            self.action = "stand"

            if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                self.facing = "left"
                if collision[0] == -1:
                    self.action = "walk"
                    self.pos[0] -= 4
            elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                self.facing = "right"
                if collision[1] == -1:
                    self.action = "walk"
                    self.pos[0] += 4
            elif keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                self.facing = "up"
                if collision[2] == -1:
                    self.action = "walk"
                    self.pos[1] -= 4
            elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
                self.facing = "down"
                if collision[3] == -1:
                    self.action = "walk"
                    self.pos[1] += 4
        # if moving between tiles
        else:
            if self.facing == "left":
                if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                    self.facing = "right"
                    self.pos[0] += 4
                else:
                    self.pos[0] -= 4
            elif self.facing == "right":
                if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                    self.facing = "left"
                    self.pos[0] -= 4
                else:
                    self.pos[0] += 4
            elif self.facing == "up":
                if keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
                    self.facing = "down"
                    self.pos[1] += 4
                else:
                    self.pos[1] -= 4
            elif self.facing == "down":
                if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                    self.facing = "up"
                    self.pos[1] -= 4
                else:
                    self.pos[1] += 4

        #clamp position to be inside the tile map
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.action = "stand"
        elif self.pos[0] > 32*len(world.tiles[0])-32:
            self.pos[0] = 32*len(world.tiles[0])-32
            self.action = "stand"
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.action = "stand"
        elif self.pos[1] > 32*len(world.tiles)-32:
            self.pos[1] = 32*len(world.tiles)-32
            self.action = "stand"
    def checkForEncounter(self, world):
        # not in the middle of a tile
        if self.pos[0]%32 != 0 or self.pos[1]%32 != 0:
            self.encounterCheck = False
        # in the middle of a tile and haven't checked it yet
        elif not self.encounterCheck:
            self.encounterCheck = True
            # check the tile type
            if world.tiles[int(self.pos[1]/32)][int(self.pos[0]/32)] == 3:
                # rng for an encounter
                if np.random.uniform() < ENCOUNTER_CHANCE:
                    seed = np.random.uniform()
                    base = 0
                    # figure out which encounter to give
                    for key in world.encounters:
                        if base <= seed <= base+world.encounters[key]:
                            # trigger encounter
                            self.action = "stand"
                            world.encountering = key
                            break
                        base += world.encounters[key]

    """ Drawing """
    def draw(self, world, cam):
        drawable = Rect(self.pos[0]-cam[0], self.pos[1]-cam[1], 0, 0)

        #draw walking
        if self.action == "walk":
            self.walkFrame += 1

            if self.facing == "left" or self.facing == "right":
                #draw the walking frame
                if self.walkFrame % 8 >= 4:
                    world.drawUpImage(self.sprites["walk-" + self.facing], drawable)
                #draw the standing frame
                else:
                    world.drawUpImage(self.sprites["stand-" + self.facing], drawable)
            elif self.facing == "up" or self.facing == "down":
                #draw the walking frame
                if self.walkFrame % 8 >= 4:
                    if self.walkFrame % 16 < 8:
                        world.drawUpImage(self.sprites["walk-" + self.facing + "-l"], drawable)
                    else:
                        world.drawUpImage(self.sprites["walk-" + self.facing + "-r"], drawable)
                #draw the standing frame
                else:
                    world.drawUpImage(self.sprites["stand-" + self.facing], drawable)
        #draw standing
        elif self.action == "stand":
            world.drawUpImage(self.sprites[self.action + "-" + self.facing], drawable)
