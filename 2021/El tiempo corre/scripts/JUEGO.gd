extends Node2D

export var current_level = 0
export var TIME_PER_LEVEL = 15
const LEVELS = 4
var game_over = false

onready var PLAYER = $Jugador
onready var TIME_LEFT = PLAYER.nodes["time left"]
onready var CURTAIN_ANIM = PLAYER.get_node("animacion telon")
onready var PLAYER_ANIMS = PLAYER.nodes["anims"]
onready var SOUNDS = $sonidos
onready var PLUS1_SPRITE = $"CanvasLayer/Control/sprite +1"
onready var TIME_LEFT_LABEL = $"CanvasLayer/Control/texto tiempo"
onready var TIME_BETWEEN_LVLS = $"tiempo entre niveles"
onready var COUNTDOWN = $"CanvasLayer/Control/cuenta atras/numero"

func _ready():
	start_level(false, true, false)
	
func _process(_delta):
	TIME_LEFT_LABEL.text = str(round(TIME_LEFT.time_left))
	TIME_LEFT_LABEL.visible = true if TIME_BETWEEN_LVLS.is_stopped() else false
	PLAYER.still = true if game_over else not TIME_BETWEEN_LVLS.is_stopped()
	
	
	# Cuenta atras
	if TIME_LEFT.time_left <= 3 and not PLAYER.still:
		COUNTDOWN.visible = true
		COUNTDOWN.text = TIME_LEFT_LABEL.text
	else:
		COUNTDOWN.visible = false
	
	# Game over
	if TIME_LEFT.is_stopped() and not game_over:
		game_over = true
		SOUNDS.get_node("musica").stop()
		CURTAIN_ANIM.play("telon")
	
	# Reiniciar el nivel
	if game_over and not CURTAIN_ANIM.is_playing():
		start_level(true, false, false)

func _input(event):
	if event.is_action_released("ui_cancel"):
		get_tree().quit()
	
	if event.is_action_released("ui_select"):
		if get_tree().paused:
			get_tree().paused = false
		else:
			get_tree().paused = true
		
func touch_portal():
	TIME_LEFT.start(100)
	PLAYER_ANIMS.play("portal")
	TIME_BETWEEN_LVLS.start(2.8)
	SOUNDS.get_node("portal").play()
	CURTAIN_ANIM.play("telon")
	
func next_level():
	if current_level+1 < LEVELS:
		start_level()
		
	else:
		get_tree().quit()
		pass # no más niveles

func start_level(restart = false, first = false, win = true):
	# ¿Reiniciar? game_over = false
	if restart:
		game_over = false
		SOUNDS.get_node("musica").play()
	
	# ¿No es la primera vez que hay un nivel? Quitar el nivel viejo.
	if not first:
		var current_level_node = get_child(len(get_children())-1)
		current_level_node.queue_free()
	
	# ¿Ganar? Subir de nivel.
	if win and current_level+1 < LEVELS:
		current_level += 1
		PLAYER_ANIMS.play_backwards("portal")

	# Agregar el nivel actual
	var current_level_scene = load("res://escenas/niveles/nivel " + str(current_level) + ".tscn")
	add_child(current_level_scene.instance())
	
	CURTAIN_ANIM.play_backwards("telon")
	PLAYER.position = get_node("nivel "+ str(current_level) +"/posicion jugador").position
	TIME_LEFT.start(TIME_PER_LEVEL+1)
