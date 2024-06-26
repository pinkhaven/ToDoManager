from plyer import gps


class GPSService:
    def __init__(self):
        self.gps = gps

    def get_location(self):
        # Start the GPS
        self.gps.start()

        # Get the current location
        location = self.gps.get_location()

        # Stop the GPS
        self.gps.stop()

        return location['latitude'], location['longitude']
