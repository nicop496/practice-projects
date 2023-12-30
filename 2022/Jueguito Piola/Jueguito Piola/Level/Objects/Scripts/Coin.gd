extends Area2D

export (float) var VALUE
onready var TYPE = get_node("AnimatedSprite").animation


func on_body_entered(body):
	if body.name == "Player":
		if body.on_game_over_anim:
			return
		get_node("/root/Game/Audio/%sCoin" % TYPE).play()
		body.add_cash(VALUE)
		queue_free()
