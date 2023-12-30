extends "res://Meteor/Meteor.gd"

var medium_meteor = load("res://Meteor/Medium/MediumMeteor.tscn")


func set_ready():
	$Sprite.frame = rand_range(0, 4)


func _on_BigMeteor_area_entered(area):
	on_Meteor_area_entered(area, "medium")
