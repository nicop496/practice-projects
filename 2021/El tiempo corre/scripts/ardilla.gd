extends Area2D

export var speed = -200

func _physics_process(delta):
	position += Vector2(speed, 0) * delta

func _on_ardilla_body_entered(_body):
	speed *= -1
	
	if speed < 0: $sprite.flip_h = false
	elif speed > 0: $sprite.flip_h = true
