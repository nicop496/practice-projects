extends Area2D

func _on_moneda_body_entered(body):
	if body.name == "Jugador":
		body.collect_coin()
		queue_free()
		
