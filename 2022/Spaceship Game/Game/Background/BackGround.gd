extends Sprite

onready var size_y = get_viewport_rect().size.y
export var MOVEMENT_SPEED = 4
var moving = true


func _process(_delta):
	if not moving:
		return
	if position.y > size_y + size_y / 2:
		position.y = -(size_y / 2)
		
	position.y += MOVEMENT_SPEED
