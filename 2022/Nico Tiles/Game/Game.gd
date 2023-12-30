extends TextureButton



const SPEED_LIMIT = 1100
const SCORE_FILE = "user://score.dat"
var TILE_SCENE = preload("res://Game/Tile/Tile.tscn")
var TILE_SOUNDS = [
	preload("res://Game/Tile/1.mp3"),
	preload("res://Game/Tile/2.mp3"),
	preload("res://Game/Tile/3.mp3"),
	preload("res://Game/Tile/4.mp3")]
var last_tile
var speed = 550
var score = 0
var tile_is_being_destroyed = false


func _ready():
	create_tile()


func _process(_delta):
	if last_tile.position.y >= 0:
		create_tile()
		if speed < SPEED_LIMIT:
			speed += 5


func create_tile():
	var new_tile = TILE_SCENE.instance()
	new_tile.speed = speed
	$Tiles.add_child(new_tile)
	last_tile = new_tile
	

func game_over():
	var file = File.new()
	file.open(SCORE_FILE, File.WRITE)
	file.store_32(score)
	file.close()
	
	get_tree().change_scene_to(load("res://TitleScreen/TitleScreen.tscn"))

func tile_destroyed(tile):
	tile.queue_free()
	score += 1
	$TileSound.stream = TILE_SOUNDS[tile.column]
	$TileSound.play()
	$Score.text = str(score)


func _on_Game_button_down():
	game_over()
