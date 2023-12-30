extends CanvasLayer


const SETTINGS_SCREEN = preload("res://Game/Screens/Menus/Settings/SettingsScreen.tscn")


func _ready():
	set_visibiliy()


func _input(event):
	if event.is_action_released("pause") and get_child_count() == 1:
		AudioController.play_ui_btn_sfx()
		if get_tree().paused:
			_on_ResumeButton_pressed()
		else:
			get_tree().paused = true
			set_visibiliy()


func _on_ResumeButton_pressed():
	get_tree().paused = false
	if AudioController.is_music_disabled:
		AudioController.stop()
	AudioController.play("Stage1.mp3")
	set_visibiliy()
	

func _on_RestartButton_pressed():
	get_tree().paused = false
	AudioController.restart()
	var _err = get_tree().change_scene("res://Game/Screens/Levels/%s.tscn" % get_parent().name)


func _on_ExitButton_pressed():
	get_tree().paused = false
	var _err = get_tree().change_scene("res://Game/Screens/Menus/LevelSelection/LevelSelection.tscn")


func _on_SettingsButton_pressed():
	add_child(SETTINGS_SCREEN.instance())


func set_visibiliy():
	$Control.visible = get_tree().paused
