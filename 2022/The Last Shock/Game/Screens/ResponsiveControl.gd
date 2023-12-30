extends Control


func _ready():
	add_to_group("ResponsiveControls")
	get_tree().call_group("ResponsiveControls", "resize")


func resize():
	rect_size = get_viewport_rect().size
