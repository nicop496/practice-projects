extends Node

onready var girador = $fondo.get_node("girador de monedas")
const change_scale = Vector2(.001, .001)
const start_scale = Vector2(0.208, 0.208)

# Funciones de los botones
func _on_boton_jugar_button_up():
	get_tree().change_scene("res://escenas/Juego.tscn")
	
func _on_ayuda_button_up():
	get_tree().change_scene("res://escenas/ayuda.tscn")
	
func _on_salir_button_up():
	get_tree().quit()

	
func _process(_delta):
	# Efecto de las monedas
	girador.rotation_degrees += 1

	for coin in girador.get_children():
		if coin.scale > -start_scale:
			coin.scale -= change_scale
			
		elif coin.scale <= start_scale:
			coin.scale *= -1
			
