extends "res://Meteor/Meteor.gd"

func set_ready():
	$Sprite.frame = rand_range(0, 2)

func _on_SmallMeteor_area_entered(area):
	on_Meteor_area_entered(area)
