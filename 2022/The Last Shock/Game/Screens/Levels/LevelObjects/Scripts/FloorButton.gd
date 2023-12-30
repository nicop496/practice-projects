extends StaticBody2D


export var group : String


func _on_ButtonArea_body_entered(body):
	if body is KinematicBody2D or body is RigidBody2D:
		$AnimationPlayer.play("Press")
		get_tree().call_group(group, "do_action")
		$AudioStreamPlayer2D.play()


func _on_ButtonArea_body_exited(body):
	if body is KinematicBody2D or body is RigidBody2D:
		$AnimationPlayer.play_backwards("Press")
