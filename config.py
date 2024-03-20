import pygame
import yaml


class ConfigNode:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)


class Config:
    def __init__(self):
        with open("config.yaml", "r") as yaml_file:
            self.config = yaml.safe_load(yaml_file)

        self.screen = ConfigNode(**self.config["screen"])
        self.pad = ConfigNode(**self.config["pad"])
        self.physics = ConfigNode(**self.config["physics"])

        self.fruit_names = ["cherry", "strawberry", "grapes", "orange", "persimmon", "apple", "pear", "peach",
                            "pineapple", "melon", "watermelon"]
        # self.radius = 
        self.background_blit = pygame.image.load("blits/background.png")
        self.cloud_blit = pygame.image.load("blits/cloud.png")

        for name in self.fruit_names:
            self.config[name]["blit"] = pygame.transform.scale(
                pygame.image.load(f"blits/{name}.png"),
                size=self.config[name]["size"],
            )

    def __getitem__(self, key):
        index, field = key
        fruit = self.fruit_names[index]
        return self.config[fruit][field]

    @property
    def top_left(self):
        return self.pad.left, self.pad.top

    @property
    def bot_left(self):
        return self.pad.left, self.pad.bot

    @property
    def top_right(self):
        return self.pad.right, self.pad.top

    @property
    def bot_right(self):
        return self.pad.right, self.pad.bot
    
    @property
    def playground_right(self):
        return self.pad.right
    
    @property
    def playground_left(self):
        return self.pad.left

    @property
    def playground_top(self):
        return self.pad.top
    
    @property
    def playground_bot(self):
        return self.pad.bot