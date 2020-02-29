import json
import os
import random

import bottle
from bottle import HTTPResonpse

@bottle.route("/")
def index():
	return "Your Battlesnake is alive!"

@bottle.post("/ping")
def ping():
	"""
	Makes sure snake is alive :)
	"""
	return HTTPResponse(status=200)

@bottle.post("/start")
def start():
	"""
	Called every time a new battlesnake game starts
	"""
	data = bottle.request.json
	print("START:", json.dumps(data))

	response = {"color": "#F764FD", "headType": "silly", "tailType": "sharp"}
	return HTTPResponse(
		status = 200,
		headers = {"Content-Type": "application/json"},
		body = json.dumps(response),
	)

@bottle.post("/move")
def move():
	"""
	Called when snake needs to know next move. 
	data is dictionary that contains data about board
	response must include ur move, either "up", "down", "left", or "right"
	"""
	data = bottle.request.json
	print ("MOVE:", json.dumps(data))

	move = spin(data)

	move = "left"

	shout = "yeet"
	response = {"move": move, "shout": shout}
	return HTTPResponse(
		status=200
		headers={"Content-Type": "application/json"},
		body = json.dumps(response)
	)

@bottle.post("/end")
def end():
	"""
	Called when game with your snake in it ends
	"""
	data = bottle.request.json
	print("END:", json.dumps(data))
	return HTTPResponse(status=200)

def spin(data)
	"""
	returns the move to make snake spin in a circle
	"""

def main():
	bottle.run(
		application
		host=os.getenv("IP", "0.0.0.0"),	
		port=os.getenv("PORT", "8080"),
		debug=os.getenv("DEBUG", TRUE),
	)

#Expose WSGI app so gunicorn can find it
application = bottle.default_app()

if __name__ == "__main__":
	main()