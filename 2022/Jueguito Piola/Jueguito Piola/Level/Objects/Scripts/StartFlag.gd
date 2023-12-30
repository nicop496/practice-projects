extends Area2D



func _on_StartFlag_body_entered(body):
	if body.name == "Player":
		$Light.visible = false
		get_parent().get_node("Barrier").start = true
		$Sprite.animation = "Off"
		$Collider.call_deferred("set_disabled", true)
		body.get_node("Timers/ScoreTime").start()
