extends KinematicBody2D


const SPEED : int = 16*7
const GRAVITY_FORCE : int = 10
const JUMP_FORCE : int = 193
const PORTAL_ANIM : String = "EnterPortal"
const DASH_IMPULSE : int = 400
const SNAP : Vector2 = Vector2(0, 8)
const DASH_ZOOM : Vector2 = Vector2(.02, .02)
const DASH_TEXTURE_LEFT = preload("res://Assets/Images/Character/DashLeft.png")
const DASH_TEXTURE_RIGHT = preload("res://Assets/Images/Character/DashRight.png")

export (String, FILE, "*.tscn") var next_level_path

var velocity : Vector2
var must_snap_to_floor : bool = true
var moving_right : bool
var moving_left : bool
var was_on_floor : bool
var electrocuted : bool
var entered_portal : bool
var on_dash : bool
var on_portal_anim : bool = true

onready var sprite = $Sprite
onready var camera = $Camera
onready var collider = $Collider
onready var jump_delay_timer = $Timers/JumpPressedDelay
onready var dash_timer = $Timers/DashDuration
onready var dash_particles = $DashParticles
onready var coyote_jump_timer = $Timers/CoyoteTime
onready var anim_player = $AnimationPlayer
onready var curtain_rect = $Curtain/ColorRect
onready var hud_control = $HUD/Control
onready var CAMERA_ZOOM = camera.zoom
onready var start_pos : Vector2 = position
onready var level_name = get_parent().name


func _ready():
	anim_player.play_backwards(PORTAL_ANIM)
	AudioController.play("Stage1.mp3")
	curtain_rect.rect_size =  get_viewport_rect().size


func _physics_process(_delta):
	if electrocuted:
		shake_camera(0.2)
	else:
		if not (velocity.y < 0 and must_snap_to_floor == false):
			must_snap_to_floor = true
		_animate()
		_horizontal_movement()
		_process_jumps()
		_tile_collisions()
	
	var snap = Vector2.ZERO
	if must_snap_to_floor:
		snap = SNAP

	velocity = move_and_slide_with_snap(velocity, snap, Vector2.UP)
	_calculate_gravity()


func _input(event):
	if electrocuted:
		return
	if event.is_action_pressed("right"):
		moving_right = true
		moving_left = false
		sprite.scale.x = 1
	if event.is_action_released("right"):
		moving_right = false
		
	if event.is_action_pressed("left"):
		moving_right = false
		moving_left = true
		sprite.scale.x = -1
	if event.is_action_released("left"):
		moving_left = false
	
	if event.is_action_pressed("jump"):
		jump_delay_timer.start()

	if event.is_action_pressed("dash"):
		dash()


func _animate():
	if on_dash:
		sprite.animation = "Dash"
		if sprite.scale.x > 0:
			dash_particles.texture = DASH_TEXTURE_RIGHT
		elif sprite.scale.x < 0:
			dash_particles.texture = DASH_TEXTURE_LEFT
		dash_particles.emitting = true
		return
	if is_on_floor():
		if moving_left or moving_right and not is_on_wall():
			sprite.animation = "Running"
		else:
			sprite.animation = "Idle"
	else:
		if velocity.y < 0:
			sprite.animation = "GoingUp"
		if velocity.y > 0:
			sprite.animation = "GoingDown"


func _horizontal_movement():
	if moving_right:
		velocity.x = SPEED
	elif moving_left:
		velocity.x = -SPEED
	else:
		velocity.x = 0
	
	if on_dash:
		shake_camera(0.009)
		velocity.x = DASH_IMPULSE * sprite.scale.x


func _calculate_gravity():
	if is_on_floor() or is_on_ceiling():
		velocity.y = 0
	if velocity.y == 0:
		velocity.y = 1
	else:
		velocity.y += GRAVITY_FORCE

func _process_jumps():
	if not is_on_floor() and was_on_floor and velocity.y > 0:
		coyote_jump_timer.start()
		
	if jump_delay_timer.time_left:
		if is_on_floor() or coyote_jump_timer.time_left:
			jump(JUMP_FORCE)
			jump_delay_timer.stop()
			coyote_jump_timer.stop()
			$Audio/Jump.play()
	
	was_on_floor = is_on_floor()


func _tile_collisions():
	for collision_idx in get_slide_count():
		var tile = get_slide_collision(collision_idx).collider
		if tile.name == "BareWires":
			electrocute()


func electrocute():
	if on_portal_anim:
		return
	AudioController.stop()
	hud_control.score_timer.stop()
	$Audio/Electrocuted.play(5)
	electrocuted = true
	collider.set_deferred("disabled", true)
	sprite.animation = "Electrocuted"
	sprite.rotation_degrees = -18
	velocity = Vector2(0, -JUMP_FORCE * 1.25)


func pick_coin():
	$Audio/PickCoin.play()


func dash():
	dash_timer.start()
	$Audio/Dash.play()
	camera.zoom = CAMERA_ZOOM - DASH_ZOOM
	on_dash = true


func jump(jump_force : float):
	must_snap_to_floor = false
	velocity.y = -jump_force


func restart_level():
	electrocuted = false
	moving_left = false
	moving_right = false
	get_tree().call_group("Resetable", "reset")
	collider.set_deferred("disabled", false)
	sprite.rotation_degrees = 0
	sprite.animation = "Idle"
	sprite.scale.x = 1
	$Audio/Electrocuted.stop()
	AudioController.restart()
	position = start_pos


func on_entered_portal():
	hud_control.score_timer.stop()
	Scores.set_highscore(level_name, hud_control.score)
	entered_portal = true
	on_portal_anim = true
	AudioController.play_portal_sfx()
	collider.set_deferred("disabled", false)
	anim_player.play(PORTAL_ANIM)


func shake_camera(shake_amount : float):
	camera.offset_h = rand_range(-1.0, 1.0) * shake_amount
	camera.offset_v = rand_range(-1.0, 1.0) * shake_amount


func _on_DashDuration_timeout():
	on_dash = false
	camera.zoom = CAMERA_ZOOM


func _on_VisibilityNotifier2D_screen_exited():
	if electrocuted:
		restart_level()


func _on_AnimationPlayer_animation_finished(anim_name):
	if anim_name == PORTAL_ANIM:
		on_portal_anim = false
		if entered_portal:
			var _err = get_tree().change_scene(next_level_path)
