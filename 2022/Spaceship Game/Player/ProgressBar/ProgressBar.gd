extends TextureProgress


export (Color) var low_color
export (Color) var medium_color
export (Color) var high_color


func _ready():
	_on_LifeBar_value_changed(value)

func _on_LifeBar_value_changed(value):
	if value <= int(max_value / 3):
		tint_progress = low_color
	elif value <= int(max_value / 3 * 2):
		tint_progress = medium_color
	elif value <= max_value:
		tint_progress = high_color
