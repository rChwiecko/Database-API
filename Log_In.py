#Ryan C
#POST METHOD: URL = BASE + "/Log_in" + form containing the passwword the user entered and the email they entered (ordered).
from flask import Flask, make_response
from flask_restful import Api, Resource, reqparse, abort
from DB import *

app = Flask(__name__)
api = Api(app)

login_Parse = reqparse.RequestParser()
login_Parse.add_argument("Email",type=str,help="Enter Email",required=True)
login_Parse.add_argument("Password",type=str,help="Enter Password",required=True)

class Log_in(Resource):
    def post(self):
        args = login_Parse.parse_args()
        if not(is_Email_Taken(args["Email"])):
            abort(404, message = "404 not found")
        hash_Pass = hash_Input(args["Password"])
        db_Hash = get_Hash(args["Email"])
        if (hash_Pass == db_Hash):
            return {"Status":200}
        return {"Status":403}


api.add_resource(Log_in,"/Log_in")

if __name__ == "__main__":
    app.run(debug = True)
