extends "res://Game/Screens/ResponsiveControl.gd"


onready var fullscreen_btn = $VBoxContainer/Fullscreen/TextureButton
onready var fullscreen_label = $VBoxContainer/Fullscreen/Label
onready var fullscreen_timer = $VBoxContainer/Fullscreen/Timer
onready var sfx_btn = $VBoxContainer/SFX/TextureButton
onready var music_btn = $VBoxContainer/Music/TextureButton


func _ready():
	fullscreen_btn.pressed = not OS.window_fullscreen
	music_btn.pressed = AudioController.is_music_disabled
	sfx_btn.pressed = AudioController.are_sfx_disabled
	
	var os_name : String = OS.get_name()
	if os_name == "Android" or os_name == "iOS" or os_name == "HTML5":
		fullscreen_btn.disabled = true
		fullscreen_label.add_color_override("font_color", Color("#888"))


func _input(event):
	if event.is_action_released("pause"):
		_on_DoneButton_pressed()


func _on_MusicButton_toggled(is_off : bool):
	AudioController.set_music_disabled(is_off)
	AudioController.play_ui_btn_sfx()


func _on_SFXButton_toggled(is_off : bool):
	AudioController.set_sfx_disabled(is_off)
	AudioController.play_ui_btn_sfx()


func _on_FullscreenButton_toggled(is_off : bool):
	OS.window_fullscreen = not is_off
	fullscreen_timer.start()
	AudioController.play_ui_btn_sfx()

func _on_FullScreenTimer_timeout():
	get_tree().call_group("ResponsiveControls", "resize")


func _on_DoneButton_pressed():
	queue_free()
