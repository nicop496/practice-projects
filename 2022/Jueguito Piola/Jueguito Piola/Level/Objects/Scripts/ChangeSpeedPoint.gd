extends Area2D


export (int) var new_speed_x
export (int) var new_speed_y


func _on_ChangeSpeedPoint_area_entered(area):
	if area.name == "Barrier":
		area.speed_x = new_speed_x
		area.speed_y = new_speed_y
