from plyer import gps

class GPSService:
    def __init__(self):
        self.gps = gps

    def get_location(self):
        location = self.gps.get_location()
        return location['latitude'], location['longitude']