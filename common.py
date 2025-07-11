BBOX = "bbox"
FRAME = "frameNum"
TRACK_ID = "carId"
X = "carCenterXft"
Y = "carCenterYft"
LENGTH = "length"
WIDTH = "width"
X_VELOCITY = "vx"
Y_VELOCITY = "vy"
X_ACCELERATION = "ax"
Y_ACCELERATION = "ay"
LON_VELOCITY = "v_lon"
LAT_VELOCITY = "v_lat"
LON_ACCELERATION = "a_lon"
LAT_ACCELERATION = "a_lat"

COURSE = "course"
COURSE_RAD = "course_rad"
SPEED = "speed"

FT_TO_M = 0.3048
MPH_TO_MPS = 0.44704

class State(object):
    def __init__(self, this_id, x, y, lon, lat, width, height, course_rad):
        self.id = this_id
        self.x = x
        self.y = y
        self.lon = lon
        self.lat = lat
        self.width = width
        self.height = height
        self.course_rad = course_rad
