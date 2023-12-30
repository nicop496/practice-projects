extends Area2D

var player_in = false
var player


func _on_Box_body_entered(body):
	if body.name == "Player":
		player_in = true
		player = body

func _process(_delta):
	if not player:
		return
	if player.get_node("Timers/Dash").time_left and player_in:
		$Collider.queue_free()
		get_parent().texture = null
		$StaticBody2D.queue_free()
		$Particles.emitting = true


func _on_Box_body_exited(body):
	if body.name == "Player":
		player_in = false
