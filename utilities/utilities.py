
class Utility(object):
    @staticmethod
    def distance(coord1, coord2):
        res = {
            'x': 0,
            'y': 0,
            'sum': 0,
        }

        res['x'] = abs(coord1['x'] - coord2['x'])
        res['y'] = abs(coord1['y'] - coord2['y'])
        res['sum'] = res['x'] +res['y']

        return res

    @staticmethod
    def pointInSprite(coord1, sprite2):
        coord2 = sprite2.getLocation()
        if coord1['x'] >= coord2['x'] and coord1['x'] < coord2['x'] + sprite2.width and coord1['y'] >= coord2['y'] and coord1['y'] < coord2['y'] + sprite2.height:
            return True
        else: 
            return False