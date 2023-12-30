extends Area2D

export var SPEED = 1
var mx = 0 #movement_x
var my = 0 #movement_y
onready var screen_size = get_viewport_rect().size

func _physics_process(_delta):
	# Movimiento
	position.x += mx
	position.y += my
	position.x = clamp(position.x, 0, screen_size.x)
	position.y = clamp(position.y, 0, screen_size.y)
	
	if Input.is_action_pressed("ui_right"): mx = SPEED
	elif Input.is_action_pressed("ui_left"): mx = -SPEED
	else: mx = 0
	
	if Input.is_action_pressed("ui_down"): my = SPEED
	elif Input.is_action_pressed("ui_up"): my = -SPEED
	else: my = 0
	
	# Rotacion al mover
	if mx!=0 and my!=0:
		rotation_degrees += 5
	else: 
		if not int(rotation_degrees) % 90 == 0: 
			rotation_degrees += 5
	
	if rotation_degrees > 360: rotation_degrees = 0
