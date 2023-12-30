extends AnimatedSprite


func _ready():
	rotation_degrees = rand_range(-360, 360)
	play()


func _on_Explosion_animation_finished():
	queue_free()
