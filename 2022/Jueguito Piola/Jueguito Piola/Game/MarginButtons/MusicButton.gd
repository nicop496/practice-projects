extends TouchScreenButton

const ACTIVATED_IMAGES = [
	preload("res://Game/MarginButtons/Images/Music - Normal.png"),
	preload("res://Game/MarginButtons/Images/Music - Pressed.png")
]
const DISABLED_IMAGES = [
	preload("res://Game/MarginButtons/Images/No music - Normal.png"),
	preload("res://Game/MarginButtons/Images/No music - Pressed.png"),
]
var disabled = false

	
func set_disabled():
	disabled = true
	normal = DISABLED_IMAGES[0]
	pressed = DISABLED_IMAGES[1]

func set_active():
	disabled = false
	normal = ACTIVATED_IMAGES[0]
	pressed = ACTIVATED_IMAGES[1]


func _on_Music_released():
	get_node("/root/Game").music_btn_released(self)
