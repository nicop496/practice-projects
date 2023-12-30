extends Node2D

onready var start_label = $UI/StartLabel
onready var is_able_to_start = false
const HIGHSCORE_FILE = "user://highscore.dat"

func _ready():
	
	# Crear el archivo de puntuación máxima si no existe
	var file = File.new()
	if not file.file_exists(HIGHSCORE_FILE):
		file.open(HIGHSCORE_FILE, File.WRITE)
		file.store_32(0)
		file.close()

func _on_animation_finished(_anim_name):
	$UI/StartTimer.start()
	is_able_to_start = true
	
	
func _on_StartTimer_timeout():
	if start_label.visible:
		start_label.visible = false
	else:
		start_label.visible = true


func _input(event):
	if is_able_to_start:
		if event is InputEventMouseButton or event is InputEventKey:
			var _error = get_tree().change_scene("res://Scenes/Game/Game.tscn")
