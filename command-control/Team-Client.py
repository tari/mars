#!/bin/python
# Mars Team Client Example written in Python
# Requires the following library to install: sudo pip install websocket-client
# if you encounter errors with a Six import:
# you can try: pip remove six; pip install six
# Windows users: you may need to install the Microsoft Visual C++ Compiler for Python 2.7
# Windows users. please use this link: http://aka.ms/vcpython27
import requests
import websocket
import json


# Global Variables
team_name = 'Encephalon'                        # The Name of the Team
team_auth = ''                                  # The Team Authentication Tocken
server_url = 'http://localhost:8000/api'   # URL of the SERVER API
server_ws = 'ws://localhost:8000/ws'       # URL of the Sensors Websocket


# Server Method Calls ------------------------------------------------

def register_team(team_name):
    """
    Registers the Team in the Server
    :param team_name:The team name
    :return:The Team authentication Token
    """

    url = server_url + "/join/" + team_name
    print('Server API URL: ' + url)
    payload = ''

    # POST with form-encoded data
    response = requests.post(url, data=payload)

    team_auth = response.text
    # print ('Team Authentication Code:' + team_auth )

    if response.status_code == 200:
        print ('Team \'' + team_name + '\' joined the game!')
        print (team_name + ' authentication Code: ' + team_auth)
    else:
        print ('Team \'' + team_name + '\' joining game Failed!')
        print ("HTTP Code: " + str(response.status_code) + " | Response: " + response.text)

    return team_auth


# Shield Method Calls ------------------------------------------------
def team_shield_up(team_name, team_auth):
    """
    Sets the team shield up
    curl -i -H 'X-Auth-Token: 1335aa6af5d0289f' -X POST http://localhost:8080/api/shield/enable
    :param team_name:The team name
    :param team_auth:The team authentication token
    :return: nothing
    """
    url = server_url + '/shield/enable'
    auth_header = {'X-Auth-Token': team_auth}
    shield_up = requests.post(url, headers=auth_header)
    if shield_up.status_code == 200:
        print ('Server: Team: ' + team_name + ' Shield is UP!')
    else:
        print ('Server: Team: ' + team_name + ' Shield UP! request Failed!')
        print ("HTTP Code: " + str(shield_up.status_code) + " | Response: " + shield_up.text)


def team_shield_down(team_name, team_auth):
    """
    Sets the team shield Down
    curl -i -H 'X-Auth-Token: 1335aa6af5d0289f' -X POST http://localhost:8080/api/shield/disable
    :param team_name:The team name
    :param team_auth:The team authentication token
    :return: nothing
    """
    url = server_url + '/shield/disable'
    auth_header = {'X-Auth-Token': team_auth}
    shield_down = requests.post(url, headers=auth_header)
    if shield_down.status_code == 200:
        print ('Server: Team: ' + team_name + ' Shield is DOWN!')
    else:
        print ('Server: Team: ' + team_name + ' Shield DOWN! request Failed!')
        print ("HTTP Code: " + str(shield_down.status_code) + " | Response: " + shield_down.text)


# Client Logic ------------------------------------------------

def data_recording(parsed_json):
    """
    Saves the Mars sensor data in data repository
    :param parsed_json:Readings from Mars Sensors
    :return:Nothing
    """
    print("\nData Recording: Saving Data row for persistence. Time: " + str(parsed_json['startedAt']))


def team_strategy(parsed_json):
    false = False
    d = eval(parsed_json)

##    {
##        "running":false,
##        "startedAt":"2015-08-04T00:44:40.854306651Z",
##        "readings":{
##            "solarFlare":false,
##            "temperature":-3.960996217958863,
##            "radiation":872
##        },
##        "teams":[
##            {
##                "name":"TheBorgs",
##                "energy":100,
##                "life":0,
##                "shield":false
##            },
##            {
##                "name":"QuickFandango",
##                "energy":100,
##                "life":0,
##                "shield":false
##            },
##            {
##                "name":"InTheBigMessos",
##                "energy":32,
##                "life":53,
##                "shield":false
##            },{
##                "name":"MamaMia",
##                "energy":100,
##                "life":100,
##                "shield":false
##            }
##        ]
##    }

    for team in parsed_json['teams']:
        if team['name'] == team_name:
            l=team['life']/100.0; e=team['energy']/100.0; r=parsed_json["readings"]["radiation"]/1000.0; t=(parsed_json["readings"]["temperature"]--142.0)/(35.0--142.0)
            coeffs = [0.013881272498496022, 0.45039997868312986, -0.9514054948793587, 0.0837629045368744, 0.0, -2.087719814806384, 1.8122986400733951, 1.8369811394811546, -0.23702946321884122, 0.2767876048134126]
            if team['shield']:
                val = coeffs[0]*l + coeffs[1]*e + coeffs[2]*r + coeffs[3]*t + coeffs[4]
                if val > 0.0:
                    team_shield_down(team_name, team_auth)
            else:
                val = coeffs[5]*l + coeffs[6]*e + coeffs[7]*r + coeffs[8]*t + coeffs[9]
                if val > 0.0:
                    team_shield_up(team_name, team_auth)
            return val > 0.0


# Register the Team

team_auth = register_team(team_name)


# Create the WebSocket for Listening
ws = websocket.create_connection(server_ws)

while True:

    json_string = ws.recv()  # Receives the the json information

    # Received '{"running":false,"startedAt":"2015-08-04T00:44:40.854306651Z","readings":{"solarFlare":false,"temperature":-3.
    # 960996217958863,"radiation":872},"teams":[{"name":"TheBorgs","energy":100,"life":0,"shield":false},{"name":"QuickFandang
    # o","energy":100,"life":0,"shield":false},{"name":"InTheBigMessos","energy":32,"life":53,"shield":false},{"name":"MamaMia
    # ","energy":100,"life":100,"shield":false}]}'

    parsed_json = json.loads(json_string)

    # Check if the game has started
    print("Game Status: " + str(parsed_json['running']))

    if not parsed_json['running']:
        print('Waiting for the Game Start')
    else:
        data_recording(parsed_json)
        team_strategy(parsed_json)

ws.close()

print("Good bye!")
