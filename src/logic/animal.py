from abc import ABC, abstractmethod
import random

class Animal(ABC):
    def __init__(self):
        pass

    # metadata methods
    @abstractmethod
    def getFilename(self):
        pass
    @abstractmethod
    def getTypeId(self):
        pass

    # descriptive data methods
    @abstractmethod
    def getNameCommon(self):
        pass
    @abstractmethod
    def getNameScientific(self):
        pass
    @abstractmethod
    def getConservationStatus(self):
        pass
    @abstractmethod
    def getHabitat(self):
        pass
    @abstractmethod
    def getDescription(self):
        pass
    @abstractmethod
    def getHeightRange(self):
        pass
    @abstractmethod
    def getWeightRange(self):
        pass

    # game data methods
    @abstractmethod
    def getBaseCatchChance(self):
        pass
    @abstractmethod
    def getBaseFleeChance(self):
        pass
    def getTopCatchArt(self):
        return "plains"
    @abstractmethod
    def likesBlueRedBerry(self):
        #should return a tuple of (likes blue, likes red), each is a float: =1 neutral, >1 likes, <1 dislikes
        pass
class IndAnimal(Animal, ABC):
    def __init__(self, nickname):
        super().__init__()
        if nickname is None:
            self.name = self.getNameCommon()
        else:
            self.name = nickname    # user input for nickname
        self.weight = round(random.uniform(self.getWeightRange()[0], self.getHeightRange()[1]), 1)  # random value w/in weight bounds for species
        self.height = round(random.uniform(self.getHeightRange()[0], self.getHeightRange()[1]), 1)  # random value w/in height bounds for species

class Elephant(IndAnimal):
    def __init__(self, nickname):
        super().__init__(nickname)

    def getFilename(self):
        return "african-forest-elephant"
    def getTypeId(self):
        return 1

    def getNameCommon(self):
        return "African forest elephant"
    def getNameScientific(self):
        return "Loxodonta cyclotis"
    def getConservationStatus(self):
        return "CR"
    def getHabitat(self):
        return "Dense Tropical Forests of Central and West Africa"
    def getDescription(self):
        return "The key reason that the number of African Forest Elephants is declining is due to poaching, which is " \
               "frequent and widespread in Central Africa."
    def getHeightRange(self):
        return 2.4, 3
    def getWeightRange(self):
        return 1814, 4536

    def getBaseCatchChance(self):
        return 0.5
    def getBaseFleeChance(self):
        return 0.05
    def likesBlueRedBerry(self):
        return 1.2,1.2
class Turtle(IndAnimal):
    def __init__(self, nickname):
        super().__init__(nickname)

    def getFilename(self):
        return "hawksbill-turtle"
    def getTypeId(self):
        return 2

    def getNameCommon(self):
        return "Hawksbill sea turtle"
    def getNameScientific(self):
        return "Eretmochelys imbricata"
    def getConservationStatus(self):
        return "CR"
    def getHabitat(self):
        return "Tropical and subtropical oceans"
    def getDescription(self):
        return "The worldwide population of Hawksbill Turtles has reduced by at least 80% in the last 30 years as a " \
               "consequence of accidental capture in fishing gear, nesting habitat degradation, coral reef damage, " \
               "and the illegal trade of hawksbill shells and products. "
    def getHeightRange(self):
        return 0.76, 0.89
    def getWeightRange(self):
        return 40.8, 68

    def getBaseCatchChance(self):
        return 0.15
    def getBaseFleeChance(self):
        return 0.3
    def getTopCatchArt(self):
        return "ocean"
    def likesBlueRedBerry(self):
        return 1.6,0.4
class Gorilla(IndAnimal):
    def __init__(self, nickname):
        super().__init__(nickname)

    def getFilename(self):
        return "mountain-gorilla"
    def getTypeId(self):
        return 3

    def getNameCommon(self):
        return "Mountain Gorilla"
    def getNameScientific(self):
        return "Gorilla beringei beringei"
    def getConservationStatus(self):
        return "EN"
    def getHabitat(self):
        return "Mountainous regions of Central Africa"
    def getDescription(self):
        return "Due to political instability and high levels of poverty in the Virunga Landscape region, a " \
               "substantial threat has been posed to Mountain Gorillas as people move to areas closer to these " \
               "great apes for food, shelter, and space."
    def getHeightRange(self):
        return 1.6, 1.7
    def getWeightRange(self):
        return 70, 191

    def getBaseCatchChance(self):
        return 0.35
    def getBaseFleeChance(self):
        return 0.2
    def getTopCatchArt(self):
        return "cave"
    def likesBlueRedBerry(self):
        return 0.9, 1.3
class Porpoise(IndAnimal):
    def __init__(self, nickname):
        super().__init__(nickname)

    def getFilename(self):
        return "finless-porpoise-outofwater"
    def getTypeId(self):
        return 4

    def getNameCommon(self):
        return "Finless Porpoise"
    def getNameScientific(self):
        return "Neophocaena asiaeorientalis"
    def getConservationStatus(self):
        return "CR"
    def getHabitat(self):
        return "Yangtze River of China"
    def getDescription(self):
        return "Due to years of environmental degradation, overfishing, and water pollution in the Yangtze " \
               "River, many animals living here have encountered detrimental impacts. "
    def getHeightRange(self):
        return 1.5, 2.2
    def getWeightRange(self):
        return 45, 71.8

    def getBaseCatchChance(self):
        return 0.6
    def getBaseFleeChance(self):
        return 0.05
    def getTopCatchArt(self):
        return "ocean"
    def likesBlueRedBerry(self):
        return 1.3,0.7
class Orangutan(IndAnimal):
    def __init__(self, nickname):
        super().__init__(nickname)

    def getFilename(self):
        return "sumatran-orangutan"
    def getTypeId(self):
        return 5

    def getNameCommon(self):
        return "Sumatran Orangutan"
    def getNameScientific(self):
        return "Pongo abelii"
    def getConservationStatus(self):
        return "CR"
    def getHabitat(self):
        return "Forests of Sumatra, Indonesia"

    def getDescription(self):
        return "Sumatran Orangutans need vast tracts of connecting forests to live, but between 1985 and 2007, " \
               "these great apes lost 60% of their forest habitat. "
    def getHeightRange(self):
        return 1.2, 1.5
    def getWeightRange(self):
        return 30, 90

    def getBaseCatchChance(self):
        return 0.3
    def getBaseFleeChance(self):
        return 0.05
    def getTopCatchArt(self):
        return "cave"
    def likesBlueRedBerry(self):
        return 0.7,1.4
class Leopards(IndAnimal):
    def __init__(self, nickname):
        super().__init__(nickname)

    def getFilename(self):
        return "amur-leopard"
    def getTypeId(self):
        return 6

    def getNameCommon(self):
        return "Amur Leopard"
    def getNameScientific(self):
        return "Panthera pardus orientalis"
    def getConservationStatus(self):
        return "CR"
    def getHabitat(self):
        return "East Russia and North- Eastern China"

    def getDescription(self):
        return "Threats to Amur Leopard survival include habitat loss and fragmentation, prey scarcity, and " \
               "transportation infrastructure. "
    def getHeightRange(self):
        return 0.45, 1.36
    def getWeightRange(self):
        return 32, 48

    def getBaseCatchChance(self):
        return 0.35
    def getBaseFleeChance(self):
        return 0.1
    def getTopCatchArt(self):
        return "plains"
    def likesBlueRedBerry(self):
        return 0.4, 1.35
class Rhinos(IndAnimal):
    def __init__(self, nickname):
        super().__init__(nickname)

    def getFilename(self):
        return "javan-rhino"
    def getTypeId(self):
        return 7

    def getNameCommon(self):
        return "Javan Rhino"
    def getNameScientific(self):
        return "Rhinoceros sondaicus"
    def getConservationStatus(self):
        return "CR"
    def getHabitat(self):
        return "Java, Indonesia"

    def getDescription(self):
        return "Ever since they were discovered, Javan Rhinos suffered a staggering decline in numbers due to illegal " \
               "hunting and habitat loss. "
    def getHeightRange(self):
        return 1.4, 1.76
    def getWeightRange(self):
        return 1984, 5071

    def getBaseCatchChance(self):
        return 0.2
    def getBaseFleeChance(self):
        return 0.15
    def getTopCatchArt(self):
        return "plains"
    def likesBlueRedBerry(self):
        return 0.8, 1.6
class Gazelle(IndAnimal):
    def __init__(self, nickname):
        super().__init__(nickname)

    def getFilename(self):
        return "dama-gazelle"
    def getTypeId(self):
        return 8

    def getNameCommon(self):
        return "Dama Gazelle"
    def getNameScientific(self):
        return "Nanger dama"
    def getConservationStatus(self):
        return "CR"
    def getHabitat(self):
        return "Sahara Desert and area of African Sahel"

    def getDescription(self):
        return "Due to unmanaged large-scale hunting and habitat loss, the population of Dama Gazelles has declined " \
               "by over 80% in the past 10 years. "
    def getHeightRange(self):
        return 0.90, 0.95
    def getWeightRange(self):
        return 35, 75

    def getBaseCatchChance(self):
        return 0.75
    def getBaseFleeChance(self):
        return 0.3
    def getTopCatchArt(self):
        return "mesa"
    def likesBlueRedBerry(self):
        return 1.15, 1.35
class Owl(IndAnimal):
    def __init__(self, nickname):
        super().__init__(nickname)

    def getFilename(self):
        return "snowy-owl"
    def getTypeId(self):
        return 9

    def getNameCommon(self):
        return "Snowy Owl"
    def getNameScientific(self):
        return "Bubo scandiacus"
    def getConservationStatus(self):
        return "VU"
    def getHabitat(self):
        return "North of the 60 degree lat line of the Arctic region"

    def getDescription(self):
        return "The Snowy Owl population has decreased tremendously due to melting polar ice caps. The food Snowy " \
               "Owls depend on, such as mice, are also thinning in population. "
    def getHeightRange(self):
        return 0.53, 0.64
    def getWeightRange(self):
        return 1.7, 1.8

    def getBaseCatchChance(self):
        return 0.25
    def getBaseFleeChance(self):
        return 0.15
    def getTopCatchArt(self):
        return "cave"
    def likesBlueRedBerry(self):
        return 1.35, 0.6
class Dove(IndAnimal):
    def __init__(self, nickname):
        super().__init__(nickname)

    def getFilename(self):
        return "makatea-fruit-dove"
    def getTypeId(self):
        return 10

    def getNameCommon(self):
        return "Makatea Fruit Dove"
    def getNameScientific(self):
        return "Ptilinopus chalcurus"
    def getConservationStatus(self):
        return "VU"
    def getHabitat(self):
        return "Guam and Northern Marianas Islands "

    def getDescription(self):
        return "Two of the core threats that caused a rapid decline in Fruit Doves include invasive species (tree " \
               "snakes) and habitat loss. "
    def getHeightRange(self):
        return 0.18, 0.22
    def getWeightRange(self):
        return 0.095, 0.125

    def getBaseCatchChance(self):
        return 0.35
    def getBaseFleeChance(self):
        return 0.15
    def getTopCatchArt(self):
        return "plains"
    def likesBlueRedBerry(self):
        return 0.85, 1.2

TYPE_TO_CLASS = {           # parr / arbo / wood
    1: Elephant(None),      # 0.3           0.25
    2: Turtle(None),        # 0.05  0.05    0.1
    3: Gorilla(None),       #       0.3
    4: Porpoise(None),      #       0.15    0.1
    5: Orangutan(None),     # 0.2
    6: Leopards(None),      # 0.3           0.2
    7: Rhinos(None),        #       0.2     0.1
    8: Gazelle(None),       # 0.05  0.05
    9: Owl(None),           # 0.1   0.05    0.2
    10: Dove(None)          #       0.2     0.05
}
def classFromType(typeId):
    return TYPE_TO_CLASS[typeId]