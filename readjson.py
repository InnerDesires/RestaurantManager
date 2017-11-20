# encoding: utf-8
import json


class JsonReader:
    """Class for reading and writing dishes from/to .json file."""
    def __init__(self, json_path):
        self.json_path = json_path
        self.dishes = {}
        self.dishes_names = []

        self.prepInformation()

    def getDishesDict(self):
        """Return a dishes dictionary"""
        return self.dishes

    def getDishesNames(self):
        """Return a dishes names list"""
        return self.dishes_names

    def writeDish(self, dish_dict):
        """Write a dict {name,type,weight,price} into json """
        with open(self.json_path, 'r', encoding='utf-8') as f:
            json_content = json.load(f)
        json_content.update(dish_dict)
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(json_content, f, ensure_ascii=False, indent=4)

    def prepInformation(self):
        """Generate a dishes dictionary and a list with dishes names"""
        self.prepDishesDict()
        self.prepDishesNames()

    def prepDishesDict(self):
        """Get a dictionary {name:{type,weight,price}, ..., ...} from .json file"""
        with open(self.json_path, 'r+', encoding='utf-8') as f:
            tmp = f.read()
            json_content = json.loads(tmp)
        for dish_dict in json_content:
            self.dishes[dish_dict] = json_content[dish_dict]

    def prepDishesNames(self):
        """"Get a list [name, name2, name3...] from .json file"""
        for name in self.dishes:
            self.dishes_names.append(name)
