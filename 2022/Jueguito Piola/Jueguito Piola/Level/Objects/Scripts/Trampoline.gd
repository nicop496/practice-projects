extends Area2D



func _on_Trampoline_body_entered(body):
	body.velocity.y = - body.JUMP_FORCE * 1.75
	$AudioStreamPlayer.play()
	$AnimatedSprite.play()


func _on_AnimatedSprite_animation_finished():
	$AnimatedSprite.stop()
