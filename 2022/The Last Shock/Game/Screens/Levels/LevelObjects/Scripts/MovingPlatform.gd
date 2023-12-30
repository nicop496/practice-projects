extends KinematicBody2D


export (bool) var play_backwards = true

onready var animation_player : AnimationPlayer = get_children()[-1]
onready var anim_name : String = animation_player.get_animation_list()[0]
var playing_backwards : bool


func do_action():
	if not animation_player.is_playing():
		play_anim()


func reset():
	if animation_player.current_animation == "":
		return
	playing_backwards = false
	animation_player.stop()
	animation_player.seek(0, true)


func play_anim():
	if play_backwards and playing_backwards:
		animation_player.play_backwards(anim_name)
	else:
		animation_player.play(anim_name)


func on_AnimationPlayer_animation_finished(_anim_name):
	playing_backwards = not playing_backwards
	play_anim()
