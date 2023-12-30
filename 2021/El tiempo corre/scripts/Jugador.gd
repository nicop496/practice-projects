extends KinematicBody2D

export var SPEED = 0
export var JUMP = 0
export var GRAVITY = 0
export var IMPULSE = 0
var velocity = Vector2.ZERO
var still = false
var up = Vector2.UP

onready var nodes = {
	"sprite":		get_node("sprite"),
	"anims":		get_node("animaciones"),
	"sounds":		get_node("sonidos"),
	"camera":		get_node("camara"),
	"time left":	get_node("temporizadores/tiempo restante"),
	"blood":		get_node("particulas/sangre"),
	"shake":		get_node("temporizadores/vibracion duracion"),
	"dash":{"right":get_node("particulas/dash derecha"),
			"left":	get_node("particulas/dash izquierda"),
			"duration":get_node("temporizadores/dash duracion")},
	"time anims":{	"plus1":get_parent().get_node("animaciones/tiempo +1"),
					"less1":get_parent().get_node("animaciones/tiempo -1")}
}

const shake_amount = 4
func _process(_delta):
	# Temblor de la cámara
	if nodes["anims"].is_playing() or nodes["dash"]["duration"].time_left:
		$camara.set_offset(Vector2( \
			rand_range(-1.0, 1.0) * shake_amount, \
			rand_range(-1.0, 1.0) * shake_amount \
		))

	# Sangre
	if not nodes["anims"].is_playing():
		nodes["blood"].visible = false
	
	# Morir al caer al vacio
	if position.y > 1024:
		nodes["time left"].stop()

func h_movement():
	# Derecha
	if Input.is_action_pressed("ui_right"):
		velocity.x = SPEED
		nodes["sprite"].animation = "run"
		nodes["sprite"].flip_h = false
		
	# Izquierda
	elif Input.is_action_pressed("ui_left"):
		velocity.x = -SPEED
		nodes["sprite"].animation = "run"
		nodes["sprite"].flip_h = true
	
	# Quieto
	else:
		velocity.x = 0
		nodes["sprite"].animation = "idle"
		
	# Impulso (dash)
	if Input.is_action_just_pressed("ui_down"):
		nodes["sounds"].get_node("dash").play()
		nodes["dash"]["duration"].start(.3)
	
	if nodes["dash"]["duration"].time_left:
		nodes["sprite"].animation = "dash"
		
		if not nodes["sprite"].flip_h: #derecha
			velocity.x = IMPULSE
			nodes["dash"]["right"].emitting = true
		else: #izquierda
			velocity.x = -IMPULSE
			nodes["dash"]["left"].emitting = true
			
	else:
		nodes["dash"]["right"].emitting = false
		nodes["dash"]["left"].emitting = false

		if is_on_wall():
			nodes["sprite"].animation = "idle"

func v_movement():
	# Animaciones de salto y de caida
	if not nodes["dash"]["duration"].time_left and not velocity.x:
		if velocity.y > 30:
			nodes["sprite"].animation = "fall"
		if velocity.y < 0:
			nodes["sprite"].animation = "jump"
	
	# Salto
	if is_on_floor():
		velocity.y = 0

		if Input.is_action_pressed("ui_up"):
			jump()
			
	# Gravedad
	if velocity.y == 0:
		velocity.y = 1
	else:
		velocity.y += GRAVITY
		
	if is_on_ceiling():
		velocity.y = 0

func _physics_process(_delta):
	# Si no está quito se mueve
	if not still:
		h_movement()
		move_and_slide(velocity, up)
		v_movement()
	
	# Sino, no se mueve
	else:
		velocity = Vector2.ZERO
		nodes["sprite"].animation = "idle"

func hit(impulse=JUMP-JUMP/3):
	jump(impulse)
	nodes["anims"].play("daño")
	nodes["time anims"]["less1"].stop()
	nodes["time anims"]["less1"].play("tiempo -1")
	nodes["blood"].visible = true
	nodes["sounds"].get_node("daño").play()
	
	if nodes["time left"].time_left > 1:
		nodes["time left"].start(nodes["time left"].time_left-1)
	else:
		nodes["time left"].stop()
		
func jump(impulse=JUMP):
	velocity.y = -impulse
	nodes["sounds"].get_node("salto").play()
		
func collect_coin():
	nodes["sounds"].get_node("moneda").play()
	nodes["time left"].start(nodes["time left"].time_left+1)
	nodes["time anims"]["plus1"].stop()
	nodes["time anims"]["plus1"].play("tiempo +1")
	
