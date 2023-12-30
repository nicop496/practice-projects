extends "res://Meteor/Meteor.gd"

onready var small_meteor = load("res://Meteor/Small/SmallMeteor.tscn")


func set_ready():
	$Sprite.frame = rand_range(0, 2)



func _on_MediumMeteor_area_entered(area):
	on_Meteor_area_entered(area, "small")
