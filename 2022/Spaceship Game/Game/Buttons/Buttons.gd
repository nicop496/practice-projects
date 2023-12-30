extends Node2D

var moving_left = false
var moving_right = false

func _process(_delta):
	position.y = get_viewport_rect().size.y - 64

func _on_Shoot_pressed():
	get_parent().get_node("Player").shoot()
	get_parent().get_node("Player/ShotCooldown").start()


func _on_Shoot_released():
	get_parent().get_node("Player/ShotCooldown").stop()
