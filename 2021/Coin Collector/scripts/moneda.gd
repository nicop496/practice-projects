extends Area2D

var enemy = load("res://escenas/enemigo.tscn")


func _on_moneda_area_entered(area):
	# Si el jugador toca una moneda:
	if area.name == "jugador":
		# Crear un enemigo
		var new_enemy = enemy.instance()
		new_enemy.position = get_parent().get_node("jugador").position
		get_parent().call_deferred("add_child", new_enemy)
		
		# Recoger la moneda
		get_parent().collected_coin()
		
		queue_free()
		
		
		
		
