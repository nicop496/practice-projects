extends Area2D


var velocity = Vector2()
export var LIFES = 30
export var AMMO_LIMIT = 200
export var ammo = 100
onready var bullet_class = load("res://Player/Bullet/Bullet.tscn")
onready var lifes = LIFES
const SPEED = 100
const SLIDE = 10
const MAX_ROTATION = 20
const ROTATION_SLIDE = 2


func _ready():
	get_parent().get_node("Bars/LifeBar").max_value = LIFES
	get_parent().get_node("Bars/LifeBar").value = lifes
	get_parent().get_node("Bars/AmmoBar").max_value = AMMO_LIMIT
	get_parent().get_node("Bars/AmmoBar").value = ammo


# Movimiento
func _physics_process(delta):
	position += velocity * delta


func _process(_delta):
	rotation_degrees -= int(rotation_degrees) % ROTATION_SLIDE
	
	if Input.is_action_pressed("right"):
		if velocity.x < SPEED:
			velocity.x += SLIDE
		if rotation_degrees < MAX_ROTATION:
			rotation_degrees += ROTATION_SLIDE
	elif Input.is_action_pressed("left"):
		if velocity.x > -SPEED:
			velocity.x -= SLIDE
		if rotation_degrees > -MAX_ROTATION:
			rotation_degrees -= ROTATION_SLIDE
			
	elif velocity.x > 0: # right
		velocity.x -= SLIDE
		rotation_degrees -= ROTATION_SLIDE
	elif velocity.x < 0: #left
		rotation_degrees += ROTATION_SLIDE
		velocity.x += SLIDE
	
	if Input.is_action_just_pressed("shoot"):
		$ShotCooldown.start()
		shoot()
	if Input.is_action_just_released("shoot"):
		$ShotCooldown.stop()


# Disparar
func shoot():
	if ammo > 0:
		$Audio/Laser.play(.1)
		var left_bullet = bullet_class.instance()
		var right_bullet = bullet_class.instance()
		left_bullet.position = $LeftCannon.global_position
		right_bullet.position = $RightCannon.global_position
		get_parent().get_node("Bullets").add_child(left_bullet)
		get_parent().get_node("Bullets").add_child(right_bullet)
		add_ammo(-2)
	else:
		$Audio/NoAmmo.play()

func _on_ShotCooldown_timeout():
	shoot()


# Chocar con los meteoritos y las paredes
func _on_Player_area_entered(area):
	if "Meteor" in area.name:
		$Audio/Hit.play()
		if "Small" in area.name:
			lifes -= 1
		if "Medium" in area.name:
			lifes -= 2
		if "Big" in area.name:
			lifes -= 3
		get_parent().get_node("AnimationPlayer").stop()
		get_parent().get_node("AnimationPlayer").play("Hit")
		if lifes <= 0:
			lifes = 0
			get_parent().game_over()
			queue_free()
		get_parent().get_node("Bars/LifeBar").value = lifes
	
	if area.name == "LeftWall":
		velocity.x = SPEED
		rotation_degrees *= -1
	if area.name == "RightWall":
		velocity.x = -SPEED
		rotation_degrees *= -1


func add_lifes(value):
	lifes += value
	if lifes > LIFES:
		lifes = LIFES
	get_parent().get_node("Bars/LifeBar").value = lifes


func add_ammo(value):
	ammo += value
	if ammo > AMMO_LIMIT:
		ammo = AMMO_LIMIT
	get_parent().get_node("Bars/AmmoBar").value = ammo
