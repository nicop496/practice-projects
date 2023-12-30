extends Node2D


var last_music_pos = 0.0
var level = "Lobby"
var score_time = 0
var skin = "Original"
const CASH_PATH = "user://0.6 - cash.dat"
const MUSIC_BTN_PATH = "Player/MarginButtons/Control/Left/MusicButton"
const SKINS_PATH = "user://skins.dat"
const SKINS = ["Original", "White", "Cave", "Rat"]



func _ready():
	current_level("Music").play()
	
	var f = File.new()
	if not f.file_exists(CASH_PATH):
		f.open(CASH_PATH, File.WRITE)
		f.store_float(0.0)
	f.close()


#### Level
func load_level(lvl_name):
	# Check if level exists
	var path = "res://Level/%s.tscn" % lvl_name
	if not File.new().file_exists(path):
		return
	# Remove the level
	current_level().queue_free()
	
	get_tree().paused = false
	current_level("CanvasModulate").visible = false
	
	# Load level
	var new_lvl = load(path).instance()
	
	# Restart music or not
	if lvl_name == level or new_lvl.get_node("Music").stream != current_level("Music").stream:
		last_music_pos = 0
	else:
		save_music_pos()
	level = lvl_name
	var music_was_disabled = current_level(MUSIC_BTN_PATH).disabled
	if music_was_disabled:
		new_lvl.get_node(MUSIC_BTN_PATH).set_disabled()
	else:
		new_lvl.get_node(MUSIC_BTN_PATH).set_active()
		new_lvl.get_node("Music").play(last_music_pos)
	
	# Add the level to the scene
	$CurrentLevel.call_deferred("add_child", new_lvl)
	
	
func restart_level():
	load_level(level)
	
func current_level(sub_node:String = "."):
	"""Get a node from the current level"""
	return $CurrentLevel.get_child(0).get_node(sub_node)

#### Music
func music_btn_released(btn):
	if current_level("Player").get_node("Timers/GameOver").time_left:
		return
	
	if current_level("Music").playing:
		save_music_pos()
		current_level("Music").stop()
		btn.set_disabled()
	else:
		current_level("Music").play(last_music_pos)
		btn.set_active()

func save_music_pos():
	last_music_pos = current_level("Music").get_playback_position()

#### Pause mode
func toggle_pause_mode():
	if current_level("Player/AnimationPlayer").is_playing():
		return
	get_tree().paused = not get_tree().paused
	current_level("Player/MarginButtons/Control/PauseScreen").visible = get_tree().paused


#### Cash
func save_cash(new_cash):
	var f = File.new()
	f.open(CASH_PATH, File.WRITE)
	f.store_float(new_cash)
	f.close()

func get_cash():
	var f = File.new()
	f.open(CASH_PATH, File.READ)
	var cash = f.get_float()
	f.close()
	return cash


#### Skins
func save_new_skin(skin_name):
	var f = File.new()
	f.open(SKINS_PATH, File.WRITE)
	f.store_string(get_skins() + "-" + skin_name)
	f.close()


func get_skins():
	"""
	Format:
	<skin_name>-<skin_name>-...
	
	Example:
	White-Original-Cave
	"""
	var f = File.new()
	f.open(SKINS_PATH, File.READ)
	var skins = f.get_as_text()
	f.close()
	return skins
