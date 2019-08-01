

class Config:
    fps = 100
    fpsf = 100.0
    rows = 25
    columns = 80

    @staticmethod
    def secToFrames(sec): 
        return sec * Config.fpsf

    