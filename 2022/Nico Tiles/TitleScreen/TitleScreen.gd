extends Node2D


const HIGHSCORE_FILE = "user://highscore.dat"
const SCORE_FILE = "user://score.dat"
const GAME_SCENE = preload("res://Game/Game.tscn")
var can_start = false


func _ready():
	var score_file = File.new()
	var highscore_file = File.new()
	
	if not score_file.file_exists(SCORE_FILE):
		score_file.open(SCORE_FILE, File.WRITE)
		score_file.store_32(0)
		score_file.close()
	if not highscore_file.file_exists(HIGHSCORE_FILE):
		highscore_file.open(HIGHSCORE_FILE, File.WRITE)
		highscore_file.store_32(0)
		highscore_file.close()
	
	score_file.open(SCORE_FILE, File.READ)
	highscore_file.open(HIGHSCORE_FILE, File.READ)
	var score = score_file.get_32()
	var highscore = highscore_file.get_32()
	
	if score > highscore:
		highscore = score
		highscore_file = File.new()
		highscore_file.open(HIGHSCORE_FILE, File.WRITE)
		highscore_file.store_32(score)
		
	$Control/Center/Highscore/Value.text = str(highscore)
	$Control/Center/Score/Value.text = str(score)
	highscore_file.close()
	score_file.close()


func _input(event):
	if event is InputEventScreenTouch and not event.is_pressed() and can_start:
		get_tree().change_scene_to(GAME_SCENE)


func _on_CanStart_timeout():
	can_start = true
