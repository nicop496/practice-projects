extends TextureButton


export (String) var text


func _ready():
	$Label.text = text


func _on_UIButton_pressed():
	AudioController.play_ui_btn_sfx()
