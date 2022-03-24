#############################################################################
# Code containing helper functions 
#############################################################################

from rijksdriehoek import rijksdriehoek


def wgs_to_rd(lat, lon):
    '''Converts WGS84 coordinates to Rijksdriehoek'''

    rd = rijksdriehoek.Rijksdriehoek()
    rd.from_wgs(lat, lon)
    x, y = rd.rd_x, rd.rd_y

    return x, y


def rd_to_wgs(x, y):
    '''Converts Rijksdriehoek coordinates to WGS84'''

    rd = rijksdriehoek.Rijksdriehoek()
    rd.rd_x, rd.rd_y = x, y
    lat, lon = rd.to_wgs()

    return lat, lon


