extends Node

func _ready():
	$"sonido perder".play()

func _on_reiniciar_button_down():
	get_parent().restart()

func _on_boton_menu_principal_button_up():
	get_tree().change_scene("res://escenas/pantalla_principal.tscn")
	get_tree().paused = false
	
