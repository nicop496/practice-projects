extends Area2D



export (String) var new_level
onready var game = get_node('/root/Game')


func _process(_delta):
	rotation_degrees += 1


func _on_Portal_body_entered(body):
	if body.name == "Player":
		body.enter_portal(new_level)


