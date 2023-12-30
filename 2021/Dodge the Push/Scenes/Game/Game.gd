extends Node2D

const HIGHSCORE_FILE = "user://highscore.dat"
onready var screen_size = get_viewport_rect().size
var GameOverScene = preload("res://Scenes/GameOver/GameOver.tscn")
var score = 0
var game_over = false


#### Puntuación ####
func load_highscore():
	var file = File.new()
	file.open(HIGHSCORE_FILE, File.READ)
	var highscore = int(file.get_32())
	file.close()
	return highscore
	
func update_score():
	score += 1
	$Score.text = "Score: " + str(score)
	if score > load_highscore():
		var file = File.new()
		file.open(HIGHSCORE_FILE, File.WRITE)
		file.store_32(score)
		file.close()
		
		
#### Game Over ####
func _on_GameOver_body_entered(_body):
	$Music.stop()
	game_over = true
	get_tree().paused = true
	add_child(GameOverScene.instance())
	$GameOver.visible = true
	$GameOver.ready(score, load_highscore())


#### Pausa ####
func change_pause_mode():
	if not game_over:
		$Pause/Button/SoundEffect.play(.20)
		get_tree().paused = not get_tree().paused
		$Music.playing = not get_tree().paused
		$Pause/PauseScreen.visible = not $Pause/PauseScreen.visible

func _input(event):
	if event.is_action_pressed("Pause"):
		change_pause_mode()
		
func _pause_button_released():
	change_pause_mode()
	$Player.is_able_to_move = true
	
	
func _pause_button_pressed():
	$Player.is_able_to_move = false
