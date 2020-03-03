import json
import os
import random

import bottle
from bottle import HTTPResponse


@bottle.route("/")
def index():
	return "Your Battlesnake is alive!"


@bottle.post("/ping")
def ping():
	"""
	Used by the Battlesnake Engine to make sure your snake is still working.
	"""
	return HTTPResponse(status=200)


@bottle.post("/start")
def start():
	"""
	Called every time a new Battlesnake game starts and your snake is in it.
	Your response will control how your snake is displayed on the board.
	"""
	data = bottle.request.json
	print("START:", json.dumps(data))
	
	response = {"color": "#00FF00", "headType": "regular", "tailType": "regular"}
	return HTTPResponse(
		status=200,
		headers={"Content-Type": "application/json"},
		body=json.dumps(response),
	)


@bottle.post("/move")
def move():
	"""
	Called when the Battlesnake Engine needs to know your next move.
	The data parameter will contain information about the board.
	Your response must include your move of up, down, left, or right.
	"""
	data = bottle.request.json
	print("MOVE:", json.dumps(data))
	
	# Choose a random direction to move in
	directions = ["up", "down", "left", "right"]
	move = random.choice(directions)
	
	collide = true
	while(collide = true)
		move = random.choice(directions)
		collide = willCollide(move, data)
	
	response = {"move": move, "shout": shout}
	return HTTPResponse(
		status=200,
		headers={"Content-Type": "application/json"},
		body=json.dumps(response),
	)


@bottle.post("/end")
def end():
	"""
	Called every time a game with your snake in it ends.
	"""
	data = bottle.request.json
	print("END:", json.dumps(data))
	return HTTPResponse(status=200)


def main():
	bottle.run(
		application,
		host=os.getenv("IP", "0.0.0.0"),
		port=os.getenv("PORT", "8080"),			debug=os.getenv("DEBUG", True),
	)

def nextPositionOccupied(move, data):
	"""
	checks if next position snake will move is occupied
	"""
	myHead = {"x": data["you"]["body"][0]['x'],
				"y": data["you"]["body"][0]['y']}
	nextPos = myHead
	if move = up
		nextPos["y"] += 1
	elif move = down
		nextPos["y"] -= 1
	elif move = right
		nextPos = ["x"] += 1
	elif move = left
		nextPos = ["x"] -= 1
	return isOccupied(nextPos, data)
	
def isOccupied(nextPos, data):
	"""
	checks to see if target space tile
	first checks walls
	then checks player 
	"""
	
	
	

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
	main()
