# import packages
from flask import Flask, Response,request
import pymongo
import json
from bson.objectid import ObjectId

# create the application object
app = Flask(__name__)


# Connect to database
try:
    mongo = pymongo.MongoClient(
        host='localhost',
        port=27017,
        serverSelectionTimeoutMS=1000
    )
    mongo.server_info() # trigger an exception if connection failed
    print('Connected to MongoDB')
    db = mongo.company #company is the name of the database
except:
    print("Failed to connect to MongoDB")
    exit()

##############################################################################################

# create the application routes

@app.route('/users', methods=['GET'])
def get_users():
    try:
        data = list(db.users.find())
        for user in data:
            user['_id'] = str(user['_id'])
        return Response(
            response=json.dumps(data), 
            status=200 ,
            mimetype="application/json"
            )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Cannot read users"}), 
            status=500,
            mimetype="application/json"
            )


################################################################

@app.route('/users', methods=['POST'])
def create_user():
    try:
        user = {
            "name": request.form["name"],
            "lastName": request.form["lastName"],
            }
        dbResponse = db.users.insert_one(user) #users is the collection in the company database
        return Response(
            response=json.dumps(
                {"message": "User created successfully",
                 "id":f"{dbResponse.inserted_id}"
                 }), 
            status=201,
            mimetype="application/json"
            )

    except Exception as ex:
        print("************")
        print(ex)
        print("************")


################################################################

@app.route('/users/<id>', methods=['PATCH'])
def update_user(id):
    try:
        user = {
            "name": request.form["name"],
            "lastName": request.form["lastName"],
            }
        dbResponse = db.users.update_one({"_id": ObjectId(id)}, {"$set": user})
        # for attr in dir(dbResponse):
        #     print(f"*******{attr}*********")
        if dbResponse.modified_count == 1:
            return Response(
                response=json.dumps({"message": "User updated successfully"}), 
                status=200,
                mimetype="application/json"
                )
        return Response(
            response=json.dumps({"message": "Nothing to update"}), 
            status=200,
            mimetype="application/json"
            )

    except Exception as ex:
        print("****************************************************************")
        print(ex)
        print("**************************************************************** ")
        return Response(
            response=json.dumps({"message": "Cannot update user"}), 
            status=500,
            mimetype="application/json"
            )


################################################################
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(
                response=json.dumps({"message": "User deleted successfully", "id":f"{id}"}), 
                status=200,
                mimetype="application/json"
                )
        return Response(
            response=json.dumps({"message": "Nothing to delete"}), 
            status=200,
            mimetype="application/json"
            )

    except Exception as ex:
        print("****************************************************************")
        print(ex)
        print("**************************************************************** ")
        return Response(
            response=json.dumps({"message": "Cannot delete user"}), 
            status=500,
            mimetype="application/json"
            )

#  Listen to server
if __name__ == '__main__':
    app.run(port=81, debug=True)