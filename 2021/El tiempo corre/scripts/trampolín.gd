extends Area2D

func _on_trampolin_body_entered(body):
	$sprite.frame = 1
	body.jump(1200)


func _on_trampolin_body_exited(_body):
	$sprite.frame = 0
