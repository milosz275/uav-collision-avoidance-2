class Settings:
    """Settings"""
    resolution = (1100, 900)  # default resolution
    refresh_rate = 60  # default refresh rate

    @classmethod
    def set_resolution(cls, width, height):
        """Sets the resolution"""
        cls.resolution = (width - 10, height - 10)

    @classmethod
    def set_refresh_rate(cls, rate):
        """Sets the refresh rate"""
        cls.refresh_rate = rate
