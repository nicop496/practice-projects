extends Node2D

onready var up = bool(randi() % 2)
onready var down = not up
const RANGE = [.05, .3]
const COLOR_CHANGE = .01


func _ready():
	self.modulate.v = rand_range(RANGE[0], RANGE[1])

func _process(_delta):
	if down:
		if self.modulate.v > RANGE[0]:
			self.modulate.v -= COLOR_CHANGE
		else:
			down = false
			up = true
		
	elif up:
		if self.modulate.v < RANGE[1]:
			self.modulate.v += COLOR_CHANGE
		else:
			down = true
			up = false
