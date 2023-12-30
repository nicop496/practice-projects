extends Node2D


var is_opened : bool
export var timer : float


func do_action():
	if not is_opened:
		_open()


func reset():
	_close()


func _open():
	is_opened = true
	$AnimationPlayer.play("Open")
	if timer > 0:
		$Timer.start(timer)
	
func _close():
	is_opened = false
	$AnimationPlayer.play_backwards("Open")


func _on_Timer_timeout():
	_close()
