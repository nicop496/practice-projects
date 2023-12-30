extends TextureButton


export (String, FILE, "*.tscn") var level_path


func _ready():
	if not disabled:
		$Label.text = level_path.get_file().split('.')[0]


func _on_LevelButton_pressed():
	AudioController.play_ui_btn_sfx()
	var _err = get_tree().change_scene(level_path)
