extends Node2D


onready var obstacle_class = load("res://Scenes/Game/Obstacles/obstacle/Obstacle.tscn")
var obstacles_color = 0
var difficulty = 1
const OBSTACLES_COLOR_CHANGE = .01
const DIFFICULTY_LIMIT = .4
const DIFFICULTY_CHANGE = .05


func delete_obstacle(obstacle):
	$AnimationPlayer.stop(true)
	$AnimationPlayer.play("Score")
	obstacle.queue_free()
	$ObstacleDeleted.stop()
	$ObstacleDeleted.play(.20)
	get_parent().update_score()
	



func _create_obstacle():
	var obstacle = obstacle_class.instance()
	var s = get_parent().score
	var h
	if s < 10:
		h = "0.0" + str(s)
	elif s < 100:
		h = "0." + str(s)
	else:
		h = "0." + str(s)[-2] + str(s)[-1]
	obstacle.modulate.h = float(h)
	$Obstacles.add_child(obstacle)
	

func _increase_difficulty():
	if difficulty > DIFFICULTY_LIMIT:
		difficulty -= DIFFICULTY_CHANGE
		$Timers/GenerationShedule.wait_time = difficulty
	else:
		$Timers/DifficultyChange.stop()


func _on_ColorChange_timeout():
	obstacles_color += OBSTACLES_COLOR_CHANGE
