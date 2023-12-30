extends KinematicBody2D


var velocity = Vector2()
var right = false
var left = false
var on_game_over_anim = false
var entered_portal = false
var was_on_floor = false
var score_time = 0
var next_level
var dash_textures
export (int) var MOVEMENT_SPEED = 60
export (int) var JUMP_FORCE = 100
export (int) var DASH_IMPULSE = 150
export (int) var GRAVITY_FORCE = 5
const SHAKE_AMOUNT = 0.5
onready var game = get_node("/root/Game")
onready var cash = game.get_cash()
onready var highscore_path = "user://0.6 - %s.dat" % game.level


func _ready():
	$MarginButtons.visible = true
	$Camera.current = true
	$Sprite.frames = load("res://Player/Images/%s/SpriteFrames.tres" % game.skin)
	dash_textures = [
		load("res://Player/Images/%s/dash left.png" % game.skin),
		load("res://Player/Images/%s/dash right.png" % game.skin)]

	add_cash(0)
	
	if game.level == "Lobby" or "Zone" in game.level:
		$MarginButtons/Control/Right/VBoxContainer/TimeLabel.visible = false
	else:
		var f = File.new()
		if f.file_exists(highscore_path):
			f.open(highscore_path, File.READ)
			get_parent().get_node("LevelObjects/TimeLabel").text = str(stepify(f.get_float(), 0.01))
		
	$AnimationPlayer.play_backwards("Portal")


func _process(_delta):
	if on_game_over_anim:
		shake_camera(.025)


func _physics_process(_delta):
	move_and_slide(velocity, Vector2.UP)
	animate_character()
	horizontal_movement()
	if $Timers/Dash.time_left:
		on_dash()
		
	calculate_gravity()
	
	if is_on_floor() != was_on_floor:
		$Timers/JumpOnEdge.start($Timers/JumpOnEdge.wait_time)
		
	if is_on_floor() and $Timers/JumpDelay.time_left:
		jump(JUMP_FORCE)
		
	was_on_floor = is_on_floor()
	



func _input(event):
	if event is InputEventAction or InputEvent:
		
		if not on_game_over_anim:
			if event.is_action_pressed("right"): right = true
			if event.is_action_released("right"): right = false
			
			if event.is_action_pressed("left"): left = true
			if event.is_action_released("left"): left = false
			
			if event.is_action_pressed("jump"):
				$Timers/JumpDelay.start($Timers/JumpDelay.wait_time)
				
				if $Timers/JumpOnEdge.time_left and velocity.y > 0:
					jump(JUMP_FORCE)

			if event.is_action_pressed("dash"):
				$Timers/Dash.start()
				$SoundEffects/Dash.play()
				if $Sprite.scale.x == -1: 
					$Dash.texture = dash_textures[0]
				if $Sprite.scale.x == 1:
					$Dash.texture = dash_textures[1]
		
		if event.is_action_pressed("pause"):
			right = false
			left = false


func _on_GameOver_timeout():
	game.restart_level()
	$SoundEffects/Electrocuted.stop()
	on_game_over_anim = false
	$Sprite.rotation_degrees = 0


func _on_ScoreTime_timeout():
	score_time += $Timers/ScoreTime.wait_time
	$MarginButtons/Control/Right/VBoxContainer/TimeLabel.text = truncate_decimal(
		score_time, len(str($Timers/ScoreTime.wait_time))-2)


func _on_AnimationPlayer_animation_finished(anim_name):
	if anim_name == "Portal" and entered_portal:
		game.load_level(next_level)


func enter_portal(next_lvl):
	if on_game_over_anim:
		return
	$Timers/ScoreTime.stop()
	$Collider.call_deferred("set_disabled", true)
	next_level = next_lvl
	entered_portal = true
	$AnimationPlayer.play("Portal")
	game.get_node("Audio/Portal").play(.6)
	
	if game.level == "Lobby" or "Zone" in game.level:
		return
		
	# Save highscore
	var f = File.new()
	if f.file_exists(highscore_path) \
	   and score_time < get_highscore()\
	   or not f.file_exists(highscore_path):
		set_highscore(score_time)
		
	# Save cash
	game.save_cash(cash)


func get_highscore():
	"""
	The function assumes that the highscore file already exists
	"""
	var f = File.new()
	f.open(highscore_path, File.READ)
	var hs = f.get_float()
	f.close()
	return hs


func set_highscore(new_score):
	var f = File.new()
	f.open(highscore_path, File.WRITE)
	f.store_float(new_score)
	f.close()


func set_skin(skin_name):
	if skin_name in game.SKINS:
		game.skin = skin_name


func electrocuted():
	if on_game_over_anim:
		return
	on_game_over_anim = true
	game.current_level("Music").stop()
	$SoundEffects/Electrocuted.play(5)
	$Timers/Dash.stop()
	$Timers/GameOver.start()
	$Timers/ScoreTime.stop()
	$Sprite.rotation_degrees = -7
	$Sprite.animation = "electrocuted"
	velocity.y = -JUMP_FORCE


func jump(jump_force):
	velocity.y = -jump_force
	$SoundEffects/Jump.play()


func add_cash(value):
	cash += value
	$MarginButtons/Control/Right/VBoxContainer/Cash/CashLabel.text = truncate_decimal(cash, 2)


func truncate_decimal(num, decimal_digits):
	var splitted = str(num).split(".")
	if len(splitted) == 1:
		return str(num)
	return splitted[0] + "." + splitted[1].substr(0, decimal_digits)


func shake_camera(shake_amount):
	$Camera.offset_h = rand_range(-1.0, 1.0) * shake_amount
	$Camera.offset_v = rand_range(-1.0, 1.0) * shake_amount



func calculate_gravity():
	if is_on_floor():
		velocity.y = 0
		
	if velocity.y == 0:
		velocity.y = 1
	else:
		velocity.y += GRAVITY_FORCE


func on_dash():
	shake_camera(.007)
	$Sprite.animation = "dash"
	if $Sprite.scale.x == 1: # to the right
		velocity.x = DASH_IMPULSE
		$Sprite.frame = 2
	if $Sprite.scale.x == -1: # to the left
		velocity.x = -DASH_IMPULSE
		$Sprite.frame = 1
	$Dash.emitting = true


func animate_character():
	if on_game_over_anim:
		return
		
	if velocity.x and left or right: 
		$Sprite.animation = "running"
		
	if not velocity.x or is_on_wall():
		$Sprite.animation = "idle"

	if not is_on_floor():
		$Sprite.animation = "jump"
		if velocity.y < 0: # if it's going up
			$Sprite.frame = 0
		else: # if it's going down
			$Sprite.frame = 1


func horizontal_movement():
	if right:
		velocity.x = MOVEMENT_SPEED
		$Sprite.scale.x = 1
	elif left:
		velocity.x = -MOVEMENT_SPEED
		$Sprite.scale.x = -1
	else:
		velocity.x = 0
