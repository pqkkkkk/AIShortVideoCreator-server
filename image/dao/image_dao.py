from abc import ABC, abstractmethod

class image_dao(ABC):
    def get_images(self):
        pass

class mongo_image_dao(image_dao):
    def get_images(self):
        print("Getting images from MongoDB")

class mysql_image_dao(image_dao):
    def get_images(self):
        print("Getting images from MySQL")