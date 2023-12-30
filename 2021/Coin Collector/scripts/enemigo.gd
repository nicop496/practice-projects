extends Area2D

var valid = [false, false]
var rebounds_counter = 0
onready var screen_size = get_viewport_rect().size
const POSIBLE_VELOCITIES = [1, 1.5, -1, -1.5, 2, -2, 3, -3]

var velocity = Vector2(random_choice(POSIBLE_VELOCITIES), random_choice(POSIBLE_VELOCITIES))

func random_choice(posible_velocities : Array):
	return posible_velocities[rand_range(0, len(posible_velocities))]

func _process(_delta):
	# Girar el hexagono
	$Sprite.rotation += .1
	
	# Mover el hexagono
	position += velocity
	
	# Eliminar el hexagono si reboto 4 (o más) veces
	if rebounds_counter >= 4:
		queue_free()
	
	# Rebote
	if position.x >= screen_size.x or position.x <= 0:
		velocity.x *= -1
		rebounds_counter += 1
	if position.y >= screen_size.y or position.y <= 0:
		velocity.y *= -1
		rebounds_counter += 1

	# Valido para producir un game over o no
	if not $disponible.time_left:
		valid[1] = true
	
	# Cambiar visibilidad dependiendo si es valido o no
	if not valid[0] or not valid[1]:
		 visible = false
	else: 
		visible = true
	

func _on_enemigo_area_entered(area):
	if area.name == "jugador" and valid[0] and valid[1]:
		get_parent().game_over()

func _on_enemigo_area_exited(area):
	if area.name == "jugador":
		valid[0] = true
		
			
