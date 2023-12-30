extends Node2D

var coin_counter = 0
var score = 0
var dificulty = 10

var coin = load("res://escenas/moneda.tscn")

onready var screen_size = get_viewport_rect().size
onready var start_children = get_children()

func _ready():
	if load_file() == "":
		save_file("0")


# Funcion que se llama en cada frame
func _process(_delta):
	# Crear nuevas monedas
	if $cuando_nueva_moneda.time_left < .1:
		coin_counter += 1
		var new_coin = coin.instance()
		new_coin.position = Vector2(rand_range(50, screen_size.x-50), rand_range(50, screen_size.y-50))
		add_child(new_coin)
		$cuando_nueva_moneda.start(3)
	
	# Game over si hay muchas monedas
	if coin_counter > dificulty:
		game_over()
		
	# Textos de puntuacion
	$puntuacion.text = "Puntuación: " + str(score)
	$"mejor punt".text = "Mejor puntuación: " + load_file()
	$"cuantas monedas".text = "Capacidad de monedas: " + str(dificulty)

# Funcion que se llama cuando se recoge una moneda
func collected_coin():
	$"sonido recoger moneda".play()
	coin_counter -= 1
	score += 1
	if int(load_file()) < score:
		save_file(str(score))
		
	if score % 3 == 0 and dificulty > 2: dificulty -= 1

# Funcion que se llama cuando es game over
func game_over():
	get_tree().paused = true
	var game_over_scene = load("res://escenas/game over.tscn").instance()
	add_child(game_over_scene)

# Funcion que se llama cuando le das al boton restart
func restart():
	$cuando_nueva_moneda.start(4)
	coin_counter = 0
	score = 0
	dificulty = 10
	$jugador.position = Vector2(screen_size.x / 2, screen_size.y / 2)
	
	for child in get_children():
		if not child in start_children:
			remove_child(child)
	get_tree().paused = false


func save_file(content):
	var file = File.new()
	file.open("user://highscore.dat", file.WRITE)
	file.store_string(content)
	file.close()

func load_file():
	var file = File.new()
	file.open("user://highscore.dat", file.READ)
	var content = file.get_as_text()
	file.close()
	return content
	
