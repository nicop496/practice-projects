extends StaticBody2D

onready var screen_height = get_viewport_rect().size.y
onready var speed = rand_range(50, 220)
onready var velocity = Vector2(0, speed)
const HEIGHT = 32


func _ready():
	position.y = -48
	var screen_size_x = get_viewport_rect().size.x
	position.x = rand_range(0, screen_size_x) 
	position.x -= int(position.x) % int(screen_size_x / 5)
	
	
func _physics_process(delta):
	velocity.y = speed
	position += velocity * delta
	
	
func _process(_delta):
	if position.y > screen_height + HEIGHT:
		get_parent().get_parent().delete_obstacle(self)
	
