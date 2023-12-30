extends Area2D


export (int) var speed_x = 0
export (int) var speed_y = 0
var start = false

func _process(delta):
	if start:
		position.x += speed_x * delta
		position.y += speed_y * delta


func _on_Barrier_body_entered(body):
	if "Player" in body.name:
		body.electrocuted()
		$Collider.queue_free()
