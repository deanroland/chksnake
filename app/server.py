import json
import os
import random
import operator

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
	("START:", json.dumps(data))

	response = {"color": "#4F1851", "headType": "evil", "tailType": "hook"}
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
	# THE BEST MOVE IS CALUCLATED USING A FLOODFILL. HIGHEST AREA WIN
	move = "nothing lol"
	upC = floodFill(0, getNextPosition("up", data), data, arrayify(data))
	downC = floodFill(0, getNextPosition("down", data), data, arrayify(data))
	rightC = floodFill(0, getNextPosition("right", data), data, arrayify(data))
	leftC = floodFill(0, getNextPosition("left", data),  data, arrayify(data))

	moveC = [upC, downC, rightC, leftC]

	maxValue = max(moveC)
	index = moveC.index(maxValue)

	if index == 0:
		move = "up"
	elif index == 1:
		move = "down"
	elif index == 2:
		move = "right"
	else:
		move = "left"


	response = {"move": move, "shout": "yeet"}
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

def nextPositionOccupied(move, data):
	"""
	checks if next position snake will move is occupied
	returns true if next position is occupied
	"""
	return isOccupied(getNextPosition(move,data), data),

def getNextPosition(move, data):
	"""
	returns next position depending on which inputted
	"""
	myHead = {"x": data["you"]["body"][0]['x'],
				"y": data["you"]["body"][0]['y']}
	nextPos = myHead

	if move == 'up':
		nextPos["y"] = nextPos["y"] - 1
	elif move == 'down':
		nextPos["y"] = nextPos["y"] + 1
	elif move == 'right':
		nextPos["x"] = nextPos["x"] + 1
	elif move == 'left'	:
		nextPos["x"] = nextPos["x"] - 1
	return nextPos


def isOccupied(nextPos, data):
	"""
	checks to see if certain tile is occupied
	returns true if tile is is occupied
	"""
	snakes = data["board"]["snakes"]
	bodys = []
	for snake in snakes:
		for body in snake['body']:
			bodys.append(body)
	for x in bodys:
		if nextPos['x'] == x['x'] and nextPos['y'] == x['y']:
			return True
		if nextPos["x"] == -1 or nextPos["x"] == data["board"]["width"]:
			return True
		if nextPos["y"] == -1 or nextPos["y"] == data["board"]["height"]:
			return True
	return False

def floodFill(count, nextPos, data, dataArray):
	"""
	checks how much room there is if snake does a move
	used so snake doesn't run into a corner
	returns free space
	"""
	if dataArray[nextPos["x"]][nextPos["y"]] == True or nextPos["x"] == -1 or nextPos["x"] == data["board"]["width"] - 1 or nextPos["y"] == -1 or nextPos["y"] == data["board"]["height"]:
		return count
	else:
		dataArray[nextPos['x']][nextPos['y']] = True

	count = count + 1
	count += floodFill(count, getNextPosition("up", data), data, dataArray)
	count += floodFill(count, getNextPosition("down", data), data, dataArray)
	count += floodFill(count, getNextPosition("right", data), data, dataArray)
	count += floodFill(count, getNextPosition("left", data), data, dataArray)

	return count

def arrayify(data):
	"""
	returns state of board as a 2d array. used for floodFill
	"""
	n = data["board"]["height"]
	m = data["board"]["width"]
	a = [[False] * m for i in range(n)]

	snakes = data["board"]["snakes"]
	bodys = []
	for snake in snakes:
		for body in snake['body']:
			bodys.append(body)
	for x in bodys:
		a[x['x']][x['y']] = True
	return a

def main():
	bottle.run(
		application,
		host=os.getenv("IP", "0.0.0.0"),
		port=os.getenv("PORT", "8080"),			debug=os.getenv("DEBUG", True),
	)

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
	main()
