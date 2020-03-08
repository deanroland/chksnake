import json
import os
import random
import operator
import sys
import math
import pprint
from pprint import pprint
import bottle
from bottle import HTTPResponse

sys.setrecursionlimit(10**9)

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
	directions = ["up", "down", "left", "right"]
	data = bottle.request.json
	print("MOVE:", json.dumps(data))
	# THE BEST MOVE IS CALUCLATED USING A FLOODFILL. HIGHEST AREA WIN. ME SPEEL GOOD
	move = "nothing lol"
	upC = floodFill(0, getNextPosition("up", data), data, arrayify("up", data), 0)
	downC = floodFill(0, getNextPosition("down", data), data, arrayify("down", data), 0)
	rightC = floodFill(0, getNextPosition("right", data), data, arrayify("right", data), 0)
	leftC = floodFill(0, getNextPosition("left", data),  data, arrayify("left", data), 0)

	moveC = [upC, downC, rightC, leftC]
	print(str(moveC))
	nearestFruit = findNearestFruit(data)


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
	"""
	collide = nextPositionOccupied(move, data)
	collideCounter = 0
	#in case fill messes up, this loop will stop the snake from colliding
	while collide == True:
		print("move forricbly ovverulled")
		move = directions[collideCounter]
		collideCounter = collideCounter + 1
		if collideCounter > 3:
			break
		collide = nextPositionOccupied(move, data)
	"""
	print(move)
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
	return (isOccupied(getNextPosition(move,data), data))

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

def floodFill(count, pos, data, dataArray, level):
	"""
	checks how much room there is if snake does a move
	used so snake doesn't run into a corner
	returns free space
	"""
	try:
		if dataArray[pos["y"]][pos["x"]] == 1 or level > 6 or pos["x"] not in range (0, data["board"]["height"]) or pos["y"] not in range(0, data["board"]["height"]):
			return 0
		else:
			dataArray[pos["y"]][pos["x"]] = 1
	except IndexError:
		return 0
	if pos["y"] >= 0 or pos["x"] >= 0:
		#pprint(dataArray)
		count = count + 1

		count += floodFill(0, {"x": pos["x"], "y": pos["y"]-1}, data, dataArray, level + 1)
		count += floodFill(0, {"x": pos["x"], "y": pos["y"]+1}, data, dataArray, level + 1)
		count += floodFill(0, {"x": pos["x"]-1, "y": pos["y"]}, data, dataArray, level + 1)
		count += floodFill(0, {"x": pos["x"]+1, "y": pos["y"]}, data, dataArray, level + 1)
		return count
	return 0

def arrayify(nextMove, data):
	"""
	returns state of board as a 2d array. used for floodFill
	"""
	n = data["board"]["height"]
	m = data["board"]["width"]
	a = [[0] * m for i in range(n)]

	nextPos = getNextPosition(nextMove,data)

	snakes = data["board"]["snakes"]
	bodys = []
	for snake in snakes:
		for body in snake['body']:
			bodys.append(body)

	for x in bodys:
		a[x['y']][x['x']] = 1

		#i dont need to do anything with this cuz it gets handled in floodfill
	return a

def findNearestFruit(data):
	"""
	finds nearest fruit to you returns poition of fruit
	"""
	foods = data["board"]["food"]
	x = data["you"]["body"][0]["x"]
	y = data["you"]["body"][0]["y"]
	lowestIndex = 0

	for i in range(len(foods)-1):
			if abs(foods[i]["x"]-x)+abs(foods[i]["y"]-y) < abs(foods[lowestIndex]["x"]-x)+abs(foods[lowestIndex]["y"]-y):
				lowestIndex = i

	pos = {"x": foods[lowestIndex]["x"], "y": foods[lowestIndex]["y"]}

	return pos

def findNearestSnake(pos, data):
	"""
	finds closest snake to a position using the position of the snakes head
	returns the ID of the snake as a string
	"""
	snakes = data["board"]["snakes"]

	lowestSnakePos = {"x": data["you"]["body"][0]["x"],
						"y": data["you"]["body"][0]["y"]}
	lowestSnakeID = data["you"]["id"]
	smallestMagnitude = math.sqrt((pos["x"]-lowestSnakePos["x"])**2 + (pos["y"] - (lowestSnakePos["y"])**2 - pos["y"])**2)

	for snake in snakes:
		lowestSnakePosSnake = snake["body"][0]
		magnitude = math.sqrt((pos["x"]-lowestSnakePos["x"])**2 + (pos["y"] - (lowestSnakePos["y"])**2 - pos["y"])**2)
		if magnitude <= smallestMagnitude:
			smallestMagnitude = magnitude
			lowestSnakeID = snake["id"]

	return lowestSnakeID


def amIBiggestSnake(data):
	"""
	returns true if my snake is longer and false if not ( duh )
	used to determine if my snake needs to avoid head on collisions
	if 2 snakes are equal distance from me, largest size will be compared
	"""
	myLength = len(data["you"]["body"])
	snakes = data["board"]["snakes"]
	for snake in snakes:
		if len(data["board"]["snakes"][snake]) >= myLength:
			return False
	return True

def goto(moveC, pos, data):
	"""
	sends snake to a position
	returns move
	"""
	snakeHeadX = data["you"]["body"][0]["x"]
	snakeHeadY = data["you"]["body"][0]["y"]
	posX = pos["x"]
	posY = pos["y"]
	moveX = ""
	moveY = ""
	movePotentialX = 0
	movePotentialY = 0

	if posX > snakeHeadX:
		moveX = "right"
		movePotentialX = moveC[2]
	elif posX < snakeHeadX:
		moveX = "left"
		movePotentialX = moveC[3]

	if posY > snakeHeadX:
		moveY = "down"
		movePotentialX = moveC[1]
	elif posY < snakeHeadY:
		moveY = "up"
		movePotentialX = moveC[0]

	if movePotentialX > movePotentialY:
		return moveX
	return moveY

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
