extends Area2D

func _process(_delta):
	$sprite.rotation_degrees -= 5

func _on_sierra_body_entered(body):
	if body.name == "Jugador":
		body.hit()

