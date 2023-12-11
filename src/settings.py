class Settings:
    """A"""
    resolution = (1000, 800)  # default resolution
    refresh_rate = 60  # default refresh rate

    @classmethod
    def set_resolution(cls, width, height):
        """A"""
        cls.resolution = (width, height)

    @classmethod
    def set_refresh_rate(cls, rate):
        """A"""
        cls.refresh_rate = rate
