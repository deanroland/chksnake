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
	#print("MOVE:", json.dumps(data))
	# THE BEST MOVE IS CALUCLATED USING A FLOODFILL. HIGHEST AREA WIN. ME SPEEL GOOD
	move = "nothing lol"
	upC = floodFill(getNextPosition("up", data), data, arrayify("up", data))
	downC = floodFill(getNextPosition("down", data), data, arrayify("down", data))
	rightC = floodFill(getNextPosition("right", data), data, arrayify("right", data))
	leftC = floodFill(getNextPosition("left", data),  data, arrayify("left", data))

	moveC = [upC, downC, rightC, leftC]
	print(str(moveC))

	goodMoves = []
	if upC == max(moveC):
		goodMoves.append("up")
	if downC == max(moveC):
		goodMoves.append("down")
	if leftC == max(moveC):
		goodMoves.append("left")
	if rightC == max(moveC):
		goodMoves.append("right")
	move = random.choice(goodMoves)

	print("Turn: " + str(data["turn"]))
	print("Move: " + move)

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
	#print("END:", json.dumps(data))
	return HTTPResponse(status=200)



def getNextPosition(move, data):
	"""
	returns next position depending on which inputted
	"""
	nextPos = {"x": data["you"]["body"][0]['x'],
				"y": data["you"]["body"][0]['y']}

	if move == 'up':
		nextPos["y"] = nextPos["y"] - 1
	elif move == 'down':
		nextPos["y"] = nextPos["y"] + 1
	elif move == 'right':
		nextPos["x"] = nextPos["x"] + 1
	elif move == 'left'	:
		nextPos["x"] = nextPos["x"] - 1
	return nextPos

def floodFill(pos, data, dataArray):
	"""
	checks how much room there is if snake does a move
	used so snake doesn't run into a corner
	returns free space
	"""
	count = 0
	try:
		if dataArray[pos["y"]][pos["x"]] == 1 or pos["x"] not in range (0, data["board"]["width"]) or pos["y"] not in range(0, data["board"]["height"]):
			return count
		else:
			dataArray[pos["y"]][pos["x"]] = 1
	except IndexError:
		return count

	count += 1
	count += floodFill({"x": pos["x"], "y": pos["y"]-1}, data, dataArray)
	count += floodFill({"x": pos["x"], "y": pos["y"]+1}, data, dataArray)
	count += floodFill({"x": pos["x"]-1, "y": pos["y"]}, data, dataArray)
	count += floodFill({"x": pos["x"]+1, "y": pos["y"]}, data, dataArray)

	return count


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
