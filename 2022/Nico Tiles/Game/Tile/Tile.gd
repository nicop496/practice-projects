extends Node2D


const WIDTH = 112
onready var window_size = get_viewport_rect().size
onready var column = int(rand_range(0, 4)) 
var speed = 0


func _ready():
	position.x = column * WIDTH
	position.y = -130


func _process(delta):
	position.y += speed * delta
	if position.y > window_size.y:
		get_parent().get_parent().game_over()
		queue_free()


func _on_Tile_button_down():
	get_parent().get_parent().tile_destroyed(self)
