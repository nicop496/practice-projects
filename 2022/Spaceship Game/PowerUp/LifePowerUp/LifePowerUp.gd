extends "res://PowerUp/PowerUp.gd"


export var value = 4


func effect(player):
	player.add_lifes(value)
	


func _on_LifePowerUp_area_entered(area):
	on_PowerUp_area_entered(area, "Life")
