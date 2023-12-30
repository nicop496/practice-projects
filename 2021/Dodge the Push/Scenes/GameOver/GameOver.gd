extends Node2D

onready var restart_label = $UI/HContainer/RestartLabel
onready var game_scene = load("res://Scenes/Game/Game.tscn")
onready var is_able_to_restart = false

func ready(score, highscore):
	$AudioStreamPlayer2D.play()
	$UI/HContainer/Score.text += str(score)
	$UI/HContainer/HighScore.text += str(highscore)
	$UI/HContainer/Title/AnimationPlayer.play("GameOver")
	

func _on_RestartTimer_timeout():
	# Etiqueta que dice "Tap to restart"
	if restart_label.visible:
		restart_label.visible = false
	else:
		restart_label.visible = true


func _input(event):
	if event is InputEventMouseButton or event is InputEventKey:
		if event.pressed and is_able_to_restart:
			# Reiniciar
			var _error = get_tree().change_scene_to(game_scene)
			get_tree().paused = false


func _on_animation_finished(_anim_name):
	$UI/HContainer/RestartTimer.start()
	is_able_to_restart = true
