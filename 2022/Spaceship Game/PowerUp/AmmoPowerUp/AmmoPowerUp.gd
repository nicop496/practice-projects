extends "res://PowerUp/PowerUp.gd"


export var value = 20


func effect(player):
	player.add_ammo(value)
	

func _on_AmmoPowerUp_area_entered(area):
	on_PowerUp_area_entered(area, "Ammo")
