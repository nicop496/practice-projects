extends Control


onready var game = get_node("/root/Game")
var skin


func button_pressed():
	game.get_node("Audio/MenuButton").play()


func _on_ResumeButton_button_up():
	game.toggle_pause_mode()


func _on_LobbyButton_button_up():
	game.load_level("Lobby")
	game.toggle_pause_mode()


func _on_QuitButton_button_up():
	$VBoxContainer/Buttons.visible = false
	$VBoxContainer/ConfirmQuit.visible = true

func _on_Restart_button_up():
	if skin and skin in game.SKINS:
		game.skin = skin
	game.restart_level()


func _on_Yes_button_up():
	get_tree().quit()

func _on_No_button_up():
	skin = $VBoxContainer/ConfirmQuit/LineEdit.text
	$VBoxContainer/ConfirmQuit.visible = false
	$VBoxContainer/Buttons.visible = true


func _input(event):
	if event is InputEventAction or InputEvent:
		if event.is_action_released("pause"):
			_on_No_button_up()
			game.toggle_pause_mode()



