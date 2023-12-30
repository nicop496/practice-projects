extends Area2D


export var speed : Vector2
onready var start_pos = position
var velocity : Vector2


func do_action():
	velocity = speed


func reset():
	velocity = Vector2.ZERO
	position = start_pos


func _physics_process(delta):
	position += velocity * delta


func _on_Lightning_body_entered(body):
	if body.name == "Player":
		body.electrocute()
