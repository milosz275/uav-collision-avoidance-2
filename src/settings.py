class Settings:
    """Settings"""
    resolution = (1000, 800)  # default resolution
    refresh_rate = 60  # default refresh rate

    @classmethod
    def set_resolution(self, width, height):
        """Sets the resolution"""
        self.resolution = (width, height)

    @classmethod
    def set_refresh_rate(self, rate):
        """Sets the refresh rate"""
        self.refresh_rate = rate
