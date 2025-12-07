#import pymongo
from pymongo import MongoClient

# Connect to MongoDB
#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#myclient = MongoClient(host='mongodb', port=27017, username='root', password='pass', authSource='admin')
myclient = MongoClient(host='test_mongodb',port=27017, username='root', password='pass',authSource="admin")
mydb = myclient["mydatabase"]
mycol = mydb["recipes"]

def insertRecipe(car_title, model, engine, color): #orderID, chassisID, engineID, interiorID, paintID
    # we let mongoDB set the _id primary key, and we use that as orderID
    recipe = {
        "car_title": car_title,
        "model": model,
        "engine": engine,
        "color": color,
        "Steps": [
            {"step": 1, "task": f"Assemble chassis for model {model}"},
            {"step": 2, "task": f"Install engine {engine}"},
            {"step": 3, "task": f"Apply paint {color}"}
        ],
    }
    
    """recipe = {
        "_id": orderID, # OrderID is Primary key
        "ChassisID": chassisID,
        "EngineID": engineID,
        "InteriorID": interiorID,
        "PaintID": paintID,
        "Steps": [
            {"step": 1, "task": f"Assemble chassis {chassisID}"},
            {"step": 2, "task": f"Install engine {engineID}"},
            {"step": 3, "task": f"Install interior {interiorID}"},
            {"step": 4, "task": f"Apply paint {paintID}"}
        ],
    }"""

    result = mycol.insert_one(recipe)
    print(f"Recipe inserted successfully for order {result.inserted_id}")
    return result.inserted_id


def fetchRecipe(orderID):
    recipe = mycol.find_one({"_id": orderID})
    if recipe:
        print("Recipe found:")
        print(recipe)
    else:
        print("No recipe found for OrderID:", orderID)
    return recipe
