extends Area2D


export (int) var SPEED = 100
var velocity = Vector2(SPEED, 0)
var was_colliding

func flip():
	scale.x *= -1
	velocity.x *= -1


func _physics_process(delta):
	position += velocity * delta


func _on_Rat_body_entered(body):
	if body is TileMap or body is StaticBody2D:
		flip()


func _on_floor_body_exited(body):
	if body is TileMap:
		flip()
