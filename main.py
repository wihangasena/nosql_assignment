from fastapi import FastAPI
from reactpy.backend.fastapi import configure
from reactpy import component, event, html, use_state
import reactpy as rp
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient


@component
def MyCrud():
    ## Creating state
    alltodo = use_state([])
    name, set_name = use_state("")
    password, set_password = use_state(0)
    email, set_email = use_state("")
    age, set_age = use_state(0)
    mobile, set_mobile = use_state("")
    gender, set_gender = use_state("male")  
    hobbies, set_hobbies = use_state([])  
    address, set_address = use_state("")


    def mysubmit(event):
        newtodo = {"name": name, "password": password, "email": email, "age": age,"mobile": mobile,"gender": gender,"hobbies": hobbies,"address": address,}

        # push this to alltodo
        alltodo.set_value(alltodo.value + [newtodo])
        login(newtodo)  # function call to login function using the submitted data

    # looping data from alltodo to show on web

    list = [
        html.li(
            {
              
            },
            f"{b} => Name: {i['name']}, Password: {i['password']}, Email: {i['email']}, Age: {i['age']}, Mobile: {i['mobile']}, Gender: {i['gender']}, Hobbies: {', '.join(i['hobbies'])}, Address: {i['address']}",
        )
        for b, i in enumerate(alltodo.value)
    ]

    def handle_event(event):
        print(event)

    return html.div(
        {"style":
        
        
        
        
         {"padding": "20px","background-color": "#f0f0f0"}},
        ## creating form for submission\
        html.form(
            {"on submit": mysubmit},
            html.img(
                {"src": "https://static.vecteezy.com/system/resources/previews/007/686/736/non_2x/man-in-front-of-computer-monitor-flat-illustraiton-work-from-home-concept-free-vector.jpg", 
                 "alt": "Image Description", 
                 "width": "200px", 
                 "height": "150px",
                 "style":{"float":"right"}
                }
            ), 
            html.h1("Student Registration"),
            html.input(
                {
                    "type": "test",
                    "placeholder": "Name",
                    "on_change": lambda event: set_name(event["target"]["value"]),
                }
            ),
            html.div(),
            html.input(
                {
                    "type": "test",
                    "placeholder": "Password",
                    "on_change": lambda event: set_password(event["target"]["value"]),
                }
            ),
            html.div(),
            html.input(
                {
                    "type": "text",
                    "placeholder": "Email",
                    "on_change": lambda event: set_email(event["target"]["value"]),
                }
            ),
           html.div(),
            html.input(
                {
                    "type": "number",
                    "placeholder": "Age",
                    "on_change": lambda event: set_age(int(event["target"]["value"])),
                }
            ),
            html.div(),
            html.input(
                {
                    "type": "text",
                    "placeholder": "Mobile Number",
                    "on_change": lambda event: set_mobile(event["target"]["value"]),
                }
            ),
           html.div(),
            html.div(
                {"style": {"display": "flex", "flexDirection": "column"}},
                html.label("Gender:"),
                html.div(
                    {"style": {"display": "flex", "flexDirection": "row"}},
                    html.input(
                        {
                            "type": "radio",
                            "name": "gender",
                            "value": "male",
                            "checked": True,  #default to "male"
                            "on_change": lambda event: set_gender(event["target"]["value"]),
                        }
                    ),
                    html.label("Male"),
                    html.input(
                        {
                            "type": "radio",
                            "name": "gender",
                            "value": "female",
                            "on_change": lambda event: set_gender(event["target"]["value"]),
                        }
                    ),
                    html.label("Female"),
                ),
            ),
            html.br(), 
            html.div(),
            html.div(
                {"style": {"display": "flex", "flexDirection": "column"}},
                html.label("Hobbies:"),
                html.div(
                    {"style": {"display": "flex", "flexDirection": "column"}},
                    html.input(
                        {
                            "type": "checkbox",
                            "value": "reading",
                            "on_change": lambda event: update_hobbies("reading", event),
                        }
                    ),
                    html.label("Reading"),
                    html.input(
                        {
                            "type": "checkbox",
                            "value": "cooking",
                            "on_change": lambda event: update_hobbies("cooking", event),
                        }
                    ),
                    html.label("Cooking"),
                    html.input(
                        {
                            "type": "checkbox",
                            "value": "gardening",
                            "on_change": lambda event: update_hobbies("gardening", event),
                        }
                    ),
                    html.label("Gardening"),
                ),
            ),
           html.div(),
            html.textarea(
                {
                    "placeholder": "Address",
                    "on_change": lambda event: set_address(event["target"]["value"]),
                }
            ),
            html.div(),
            # creating submit button on form
            html.button(
                {
                    "type": "submit",
                    "on_click": event(
                        lambda event: mysubmit(event), prevent_default=True
                    ),
                    "style": {
                        "background": "blue",
                        "color": "white",
                        "border": "none",
                        "padding": "10px 20px",
                        "cursor": "pointer",
                    }
                },
                "Submit",
            ),
        ),
        html.ul(list),
    )


app = FastAPI()

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin123@cluster1.jvlmuka.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["SignUp"]
collection = db["users"]
# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



def login(
    login_data: dict,
):  # removed async, since await makes code execution pause for the promise to resolve anyway. doesnt matter.
    username = login_data["name"]
    password = login_data["password"]
    email=login_data["email"]
    age=login_data["age"]
    mobile = login_data["mobile"]
    gender = login_data["gender"]
    hobbies = login_data["hobbies"]
    address = login_data["address"]
    # Create a document to insert into the collection
    document =  {"name": username, "password": password,"email":email,"age":age,"mobile": mobile,
        "gender": gender,
        "hobbies": hobbies,
        "address": address}
    # logger.info('sample log message')
    print(document)

    # Insert the document into the collection
    post_id = collection.insert_one(document).inserted_id  # insert document
    print(post_id)

    return {"message": "Login successful"}


configure(app, MyCrud)