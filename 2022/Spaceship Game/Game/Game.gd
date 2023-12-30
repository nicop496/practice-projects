extends Node2D


const HIGHSCORE_FILE = "user://highscore.dat"
onready var difficulty = 1
onready var score = 0.0
onready var is_game_over = false
onready var can_restart = false
onready var highscore = get_highscore()
onready var screen_size = get_viewport_rect().size
onready var explosion = load("res://Meteor/Explosion/Explosion.tscn")
onready var meteors = {
	"small":load("res://Meteor/Small/SmallMeteor.tscn"),
	"medium":load("res://Meteor/Medium/MediumMeteor.tscn"),
	"big":load("res://Meteor/Big/BigMeteor.tscn")
}
onready var POWER_UPS_LIST = [
	load("res://PowerUp/LifePowerUp/LifePowerUp.tscn"),
	load("res://PowerUp/AmmoPowerUp/AmmoPowerUp.tscn"),
]


#### Puntuación ####
func get_highscore():
	var file = File.new()
	file.open(HIGHSCORE_FILE, File.READ)
	var highscore = int(file.get_float())
	file.close()
	return highscore
	
func update_highscore(new_score):
	var file = File.new()
	highscore = new_score
	file.open(HIGHSCORE_FILE, File.WRITE)
	file.store_float(new_score)
	file.close()

func increase_score(value):
	score += value
	$Score/Score/Value/Value.text = str(score)


# Al iniciar
func _ready():
	$AnimationPlayer.play("Start")
	get_tree().paused = false
	$Score/HighScore/Value/Value.text = str(highscore)
	print(can_restart)
	# Crear el archivo de puntuación máxima si es que no existe
	var file = File.new()
	if not file.file_exists(HIGHSCORE_FILE):
		file.open(HIGHSCORE_FILE, File.WRITE)
		file.store_float(0)
		file.close()
		
		
# Aumentar la dificultad
func _on_DifficultyTimer_timeout():
	if is_game_over:
		return
	difficulty += 1

# Crear los meteoritos y los power ups
func _on_CreateTimer_timeout():
	if is_game_over:
		return
	
	# Meteoritos
	var new_meteors = []
	
	for _a in range(difficulty + 3):
		new_meteors.append("small")
	for _b in range(difficulty + 2):
		new_meteors.append("medium")
	for _c in range(difficulty + 1):
		new_meteors.append("big")
	
	for m in new_meteors:
		m = meteors[m].instance()
		m.position = Vector2(rand_range(0, screen_size.x), -100)
		$Meteors.add_child(m)

	# Power ups
	var power_ups = POWER_UPS_LIST.slice(int($Player.lifes == $Player.LIFES), len(POWER_UPS_LIST))
	$PowerUps.add_child(power_ups[rand_range(0, len(power_ups))].instance())


# Aumentar la puntuación
func _on_Score_timeout():
	if is_game_over:
		return
	increase_score(.1)
	if score > highscore:
		update_highscore(score)
		$Score/HighScore/Value/Label.text = "new best!"
		$Score/HighScore/Value/Value.visible = false
		

# Game over
func game_over():
	get_tree().paused = true
	is_game_over = true
	var e = explosion.instance()
	e.position = screen_size / 2
	e.scale = Vector2(10, 10)
	e.speed_scale = 1
	$Meteors.call_deferred("add_child", e)
	$AnimationPlayer.play("GameOver")
	$AnimationPlayer.queue("TapToRestart")
	
	
# Input
func _input(event):
	# Reiniciar
	if is_game_over and can_restart:
		if event.is_action_pressed("ui_accept") or event is InputEventScreenTouch:
			get_tree().change_scene("res://Game/Game.tscn")



func _on_TapToRestart_visibility_changed():
	can_restart = true
