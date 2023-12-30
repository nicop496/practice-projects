extends AudioStreamPlayer2D


onready var volume = volume_db


func _ready():
	add_to_group("SoundEffects")
	AudioController.set_sfx_disabled(AudioController.are_sfx_disabled)


func set_disabled(value : bool):
	if value:
		volume_db = -80
	else:
		volume_db = volume

