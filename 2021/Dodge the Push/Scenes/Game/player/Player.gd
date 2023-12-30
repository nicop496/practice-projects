extends KinematicBody2D

export var speed = 600
onready var screen_width_divided_2 = get_viewport_rect().size.x / 2
onready var platform_is_computer = not OS.get_name() == "Android" and not OS.get_name() == "iOS"
const WIDTH = 32
const HEIGHT = 48
var velocity = Vector2()
var vel_y = 0
var is_able_to_move = true

func _physics_process(_delta):
	if is_able_to_move:
		velocity = move_and_slide(velocity, Vector2.UP)

	for i in get_slide_count():
		if is_on_wall(): continue
		
		var collider = get_slide_collision(i).collider
	
		if is_on_floor():
			collider.speed = vel_y + 1
			

		if is_on_ceiling():
			vel_y = collider.speed

	# Input en computadora
	if platform_is_computer:
		if Input.is_action_pressed("ui_right"):
			velocity.x = speed
		elif Input.is_action_pressed("ui_left"):
			velocity.x = -speed
		else:
			velocity.x = 0


func _input(event):
	if event is InputEventMouseButton and not platform_is_computer:
		if event.is_pressed():
			if event.position.x > screen_width_divided_2:
				velocity.x = speed
			else:
				velocity.x = -speed
		else:
			velocity.x = 0
