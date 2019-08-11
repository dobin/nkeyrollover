import logging

from texture.character.characteranimationtype import CharacterAnimationType
from texture.character.charactertype import CharacterType

logger = logging.getLogger(__name__)


class FileTextureLoader(object): 
    def __init__(self): 
        pass


    def readAnimation(
        self, characterType :CharacterType, 
        characterAnimationType :CharacterAnimationType
    ):
        ct = characterType.name
        cat = characterAnimationType.name

        filename = "texture/textures/{}/{}_{}.ascii".format(ct, ct, cat)
        return self.readAnimationFile(filename)


    def readAnimationFile(self, filename :str) -> {}:
        lineList = [line.rstrip('\n') for line in open(filename)]
        res = []

        # find longest line to make animation
        maxWidth = 0
        for line in lineList: 
            if len(line) > maxWidth: 
                maxWidth = len(line)

        maxHeight = 0
        tmp = []
        for line in lineList: 
            if line == '': 
                res.append(tmp)
                if len(tmp) > maxHeight: 
                    maxHeight = len(tmp)
                tmp = []
            else: 
                line += '' * (maxWidth - len(line))
                tmp.append(list(line))
        res.append(tmp)
            
        d = {
            'arr': res,
            'width': maxWidth, 
            'height': maxHeight,
        }

        logger.info("Loaded {}: width={} height={} animations={}".format(filename, maxWidth, maxHeight, len(res)))
        return d
