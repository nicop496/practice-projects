extends Control


func _ready():
	$PauseScreen.visible = false
	$Left.visible = true
	$Right.visible = true
	var size = get_viewport_rect().size / 2
	margin_bottom = size.y
	margin_top = -size.y
	margin_right = size.x
	margin_left = -size.x

	size = get_viewport_rect().size
	if OS.get_name() == "Android" or OS.get_name() == "iOS":
		$PauseScreen.margin_left = $Left.margin_right
		$PauseScreen.margin_right = size.x - abs($Right.margin_left)
		$PauseScreen.margin_bottom = size.y
	else:
		pass
		$Left/BG.visible = false
		$Right/BG.visible = false
		$Left/HBoxContainer/LeftButton.visible = false
		$Left/HBoxContainer/RightButton.visible = false
		$Right/HBoxContainer/UpButton.visible = false
		$Right/HBoxContainer/DashButton.visible = false
		$PauseScreen.margin_left = 0
		$PauseScreen.margin_right = size.x
		$PauseScreen.margin_bottom = size.y

