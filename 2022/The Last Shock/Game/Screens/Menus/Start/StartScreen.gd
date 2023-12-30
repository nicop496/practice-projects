extends "res://Game/Screens/ResponsiveControl.gd"


func _ready():
	AudioController.play("Lobby.mp3")


func _input(event):
	if event.is_action_released("click") \
	or event.is_action_released("ui_accept")\
	or event is InputEventScreenTouch:
		var _err = get_tree().change_scene("res://Game/Screens/Menus/LevelSelection/LevelSelection.tscn")
		AudioController.play_ui_btn_sfx()
