from PIL import Image
import numpy as np
from src.util.tiles import tileCodeFromColor

def loadArea(filename):
    # load the image in
    path = "src/assets/tilemaps/" + filename + ".png"
    image = Image.open(path).convert('RGB')
    image = np.asarray(image)

    #loop through the image
    tiles = []
    for row in image:
        tiles.append([])
        for pix in row:
            tiles[len(tiles)-1].append(tileCodeFromColor(pix))

    #get the metadata
    inp = open("src/assets/tilemaps/" + filename + ".meta", "r")
    lines = inp.readlines()

    #meta data storage
    connections = []  # elements are ((srcX, srcY), dir, destArea, (destX, destY))
    entities = []  # elements are (name, x, y)
    camLim = None  # elements are (minX, minY, maxX, maxY)
    encounters = {}
    bushes = [] # elements are [type, x, y, full]

    for line in lines:
        spl = line.split("#")[0].rstrip().split(" ")

        if spl[0] == "connect":
            srcArr = spl[1].split(",")
            dstArr = spl[4].split(",")

            connections.append(( (int(srcArr[0]), int(srcArr[1])), spl[2], spl[3], (int(dstArr[0]), int(dstArr[1])) ))
        elif spl[0] == "entity":
            entType = spl[1]
            for arr in spl[2:]:
                posArr = arr.split(",")
                entities.append((entType, int(posArr[0]), int(posArr[1])))
        elif spl[0] =="camera":
            camLim = (float(spl[1]), float(spl[2]), float(spl[3]), float(spl[4]))
        elif spl[0] == "encounters":
            for pair in spl[1:]:
                duo = pair.split(",")
                encounters[int(duo[0])] = float(duo[1])
        elif spl[0] == "bush":
            bushType = spl[1]
            for arr in spl[2:]:
                posArr = arr.split(",")
                bushes.append([bushType, int(posArr[0]), int(posArr[1]), False])

    return tiles, connections, entities, camLim, encounters, bushes

