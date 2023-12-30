extends Node2D

export var moving = true


func _process(_delta):
	for i in get_children():
		i.moving = moving
