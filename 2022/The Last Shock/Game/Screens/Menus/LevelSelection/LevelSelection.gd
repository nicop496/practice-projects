extends "res://Game/Screens/ResponsiveControl.gd"


const SETTINGS_SCREEN = preload("res://Game/Screens/Menus/Settings/SettingsScreen.tscn")


func _ready():
	AudioController.play("Lobby.mp3")


func _on_BackButton_pressed():
	AudioController.play_ui_btn_sfx()
	var _err = get_tree().change_scene("res://Game/Screens/Menus/Start/StartScreen.tscn")


func _on_SettingsButton_pressed():
	AudioController.play_ui_btn_sfx()
	add_child(SETTINGS_SCREEN.instance())
