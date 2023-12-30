extends Area2D

	
func _process(_delta):
	position.y -= 5
	if position.y < -20:
		queue_free()
