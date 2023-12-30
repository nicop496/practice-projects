extends "res://Game/Screens/ResponsiveControl.gd"


onready var score_label = $TopRight/Score
onready var score_timer = $TopRight/Score/Timer
var score : float


func do_action():
	score_timer.start()


func reset():
	score = 0.0
	score_label.text = "0.00"
	score_timer.stop()


func _on_ScoreTimer_timeout():
	score += score_timer.wait_time
	var txt = str(score) + "0000"
	txt = txt.substr(0, 4)
	score_label.text = txt
