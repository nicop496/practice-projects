extends Node


onready var music_player = $AudioStreamPlayer
var is_music_disabled : bool
var are_sfx_disabled : bool

#### Music
func play(music_name : String):
	if is_music_disabled: return
	
	var stream = load("res://Assets/Audio/Music/" + music_name)
	
	if not music_player.playing or stream != music_player.stream:
		music_player.stream = stream
		music_player.play()


func stop():
	music_player.stop()


func restart():
	if is_music_disabled: return
	music_player.play()


func set_music_disabled(value : bool):
	is_music_disabled = value
	if not get_tree().paused:
		if value:
			music_player.stop()
		else:
			music_player.play()

#### SFX
func set_sfx_disabled(value : bool):
	are_sfx_disabled = value
	get_tree().call_group("SoundEffects", "set_disabled", value)

func play_ui_btn_sfx():
	$UIButton.play()

func play_portal_sfx():
	$PortalSFX.play(.6)
