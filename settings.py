class Settings:

    def __init__(self, screen_width, screen_height):
        self.__screen_width = screen_width
        self.__screen_height = screen_height
        self.__full_screen = False
        self.__fps = 30

    def get_screen_width(self):
        return self.__screen_width

    def get_screen_height(self):
        return self.__screen_height

    def get_fps(self):
        return self.__fps

    def get_full_screen(self):
        return self.__full_screen

    def set_full_screen(self, value):
        self.__full_screen = value

