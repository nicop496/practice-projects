extends Area2D


func _ready():
	rotation_degrees = -get_parent().rotation_degrees


func _on_Coin_body_entered(body):
	if body.name == "Player":
		body.pick_coin()
		queue_free()
