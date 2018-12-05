# Real-Estate API

A Real-Estate API created using Flask and SQL-Alchemy

### How to use

  1. Install all packages in requirements.txt
  2. Run main.py
  3. Execute the requests you want
  
Here are the possible requests that can be done using this API and the format of the JSON that needs to be sent:

1. The following request returns all the properties from the city
```
import requests
url = "http://127.0.0.1:5000/api/search"
payload = "{\n\t\"city\": <Name of the city>\n}"
headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
response = requests.request("GET", url, data=payload, headers=headers)
```
Example of answer:
```
{
    "Address": "12 Baker Street",
    "City": "Paris",
    "Description": "Beautiful",
    "ID": 1,
    "Name": "Test",
    "Owner": {
        "Birthdate": null,
        "Firstname": "Test",
        "ID": 1,
        "Name": "Test"
    },
    "Rooms": [
        {
            "Area": 14,
            "Description": "Huge",
            "ID": 1
        },
        {
            "Area": 2,
            "Description": "Small",
            "ID": 2
        }
    ],
    "Type": "Apartment"
}
```

2. The following request creates a new user and returns a JSON with all information except login and password
```
import requests
url = "http://127.0.0.1:5000/api/add_user"
payload = "{\n\t\"login\": <Login of the new user>,\n\t\"password\" : <Password of the new user>,\n\t\"name\": <Name of the user> (Optionnal),\n\t\"firstname\": <Firstname of the user> (Optionnal),\n\t\"birthdate\": <Birthdate of the user as a string with this format 'dd_mm_aaaa'> (Optionnal)\n}"
headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
response = requests.request("POST", url, data=payload, headers=headers)
```
Example of answer:
```
{
    "Birthdate": "04-08-1950",
    "Firstname": "Test",
    "ID": 1,
    "Name": "Test",
    "Properties": []
}
```

3. The following request returns a token to allow the user to authentificate without his login and password
```
import requests
from requests.auth import HTTPBasicAuth
url = "http://127.0.0.1:5000/api/token"
payload = ""
headers = {
    'Authorization': "Basic dGVzdDp0ZXN0",
    'cache-control': "no-cache"
    }
response = requests.request("GET", url, data=payload, headers=headers, auth=HTTPBasicAuth(<login>, <password>))
print(response.text)
```
Example of answer:
```
{
  "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTU0NDAyMDQ4OSwiZXhwIjoxNTQ0MDI0MDg5fQ.eyJpZCI6MX0.-uQo8MbMP-_MI_Hvty5QtBDM593iG2Yo_q3oob_RFhLiY8UDDdkEBg_7yCTc_tdTbuWOHMOyxwfKxUkS8EiLjg"
}
```

4. The following request returns the list of all users
```
import requests
url = "http://127.0.0.1:5000/api/all_users"
payload = ""
headers = {
    'cache-control': "no-cache"
    }
response = requests.request("GET", url, data=payload, headers=headers)
```
Example of answer:
```
[
    {
        "Birthdate": null,
        "Firstname": "Test",
        "ID": 1,
        "Name": "Test",
        "Properties": []
    }
]
```

5. The following request edits an existing user and returns a JSON with all information except login and password
```
import requests
from requests.auth import HTTPBasicAuth
url = "http://127.0.0.1:5000/api/edit_user"
payload = "{\n\t\"password\" : <New password> (Optionnal),\n\t\"name\": <New name> (Optionnal),\n\t\"firstname\": <New firstname> (Optionnal),\n\t\"birthdate\": <New birthdate of the user as a string with this format 'dd_mm_aaaa'> (Optionnal)\n}"
headers = {
    'cache-control': "no-cache",
	'Content-Type': "application/json",
    'Authorization': "Basic VGVzdDpUZXN0Ymlz"
    }
response = requests.request("PUT", url, data=payload, headers=headers, auth=HTTPBasicAuth(<login or token>, <password (no need if token>)
```
Example of answer:
```
{
    "Birthdate": "04-08-1950",
    "Firstname": "Test",
    "ID": 1,
    "Name": "Test",
    "Properties": []
}
```

6. The following request adds a property to the database and returns a JSON with all information about it
```
import requests
from requests.auth import HTTPBasicAuth
url = "http://127.0.0.1:5000/api/add_property"
payload = "{\n\t\"name\": <Name of the property>,\n\t\"city\": <City of the property>,\n\t\"address\": <Location of the property> (Optionnal),\n\t\"description\": <Description of the property> (Optionnal),\n\t\"type\": <Type of property> (Optionnal),\n\t\"rooms\": [\n\t\t{\n\t\t\t\"Area\": <Area of the room> (Optionnal),\n\t\t\t\"Description\": <Description of the room> (Optionnal)\n\t\t},\n\t\t{\n\t\t\t\"Area\": <Area of the room> (Optionnal),\n\t\t\t\"Description\": <Description of the room> (Optionnal)\n\t\t}]\n}"
headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Authorization': "Basic VGVzdDpUZXN0Ymlz"
    }
response = requests.request("GET", url, data=payload, headers=headers, auth=HTTPBasicAuth(<login or token>, <password (no need if token>)
```
Example of answer:
```
{
    "Address": "12 Baker Street",
    "City": "Paris",
    "Description": "Beautiful",
    "ID": 1,
    "Name": "Test",
    "Owner": {
        "Birthdate": null,
        "Firstname": "Test",
        "ID": 1,
        "Name": "Test"
    },
    "Rooms": [
        {
            "Area": 14,
            "Description": "Huge",
            "ID": 1
        },
        {
            "Area": 2,
            "Description": "Small",
            "ID": 2
        }
    ],
    "Type": "Apartment"
}
```

7. The following request edits an existing property and returns a JSON with all information about it
In this request, there are 3 types of action possible concerning the rooms. There is, in this example, one room for each action.
```
import requests
from requests.auth import HTTPBasicAuth
url = "http://127.0.0.1:5000/api/add_property"
payload = "{\n\t\"id\": <ID of the property>,\n\t\"name\": <New name of the property> (Optionnal),\n\t\"city\": <New city of the property> (Optionnal),\n\t\"address\": <New address of the property> (Optionnal),\n\t\"description\": <New description of the property> (Optionnal),\n\t\"type\": <New type of property> (Optionnal),\n\t\"rooms\": [\n\t\t{\n\t\t\t\"action\": \"add\",\n\t\t\t\"area\": <Area of the new room> (Optionnal),\n\t\t\t\"description\": <Description of the new room> (Optionnal)\n\t\t},\n\t\t{\n\t\t\t\"action\": \"delete\",\n\t\t\t\"id\": <ID of the room>\n\t\t},\n\t\t{\n\t\t\t\"action\": \"edit\",\n\t\t\t\"id\": <ID of the room>,\n\t\t\t\"area\": <New area of the room> (Optionnal),\n\t\t\t\"description\": <New description of the new room> (Optionnal)\n\t\t}]\n}"
headers = {
    'Content-Type': "application/json",
    'Authorization': "Basic VGVzdDpUZXN0Ymlz",
    'cache-control': "no-cache"
    }
response = requests.request("POST", url, data=payload, headers=headers, auth=HTTPBasicAuth(<login or token>, <password (no need if token>)
```
Example of answer:
```
{
    "Address": "12 Baker Street",
    "City": "Paris",
    "Description": "Beautiful",
    "ID": 1,
    "Name": "Test",
    "Owner": {
        "Birthdate": null,
        "Firstname": "Test",
        "ID": 1,
        "Name": "Test"
    },
    "Rooms": [
        {
            "Area": 14,
            "Description": "Huge",
            "ID": 1
        },
        {
            "Area": 2,
            "Description": "Small",
            "ID": 2
        }
    ],
    "Type": "Apartment"
}
```

8. The following request returns the list of all properties owned by the user
```
import requests
from requests.auth import HTTPBasicAuth
url = "http://127.0.0.1:5000/api/get_properties"
payload = ""
headers = {
    'Authorization': "Basic VGVzdDpUZXN0Ymlz",
    'cache-control': "no-cache"
    }
response = requests.request("GET", url, data=payload, headers=headers, auth=HTTPBasicAuth(<login or token>, <password (no need if token>)
```
Example of answer:
```
[
    {
        "Address": "14 boulevard",
        "City": "Paris",
        "Description": "Joli",
        "ID": 1,
        "Name": "Test",
        "Owner": {
            "Birthdate": null,
            "Firstname": "Test",
            "ID": 1,
            "Name": "Test"
        },
        "Rooms": [
            {
                "Area": 16,
                "Description": "Grande",
                "ID": 1
            },
            {
                "Area": 17,
                "Description": "Magique",
                "ID": 3
            }
        ],
        "Type": "Maison"
    }
]
```
