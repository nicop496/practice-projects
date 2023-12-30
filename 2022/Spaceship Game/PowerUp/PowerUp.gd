extends Area2D

var velocity
onready var screen_size = get_viewport_rect().size
onready var explosion = load("res://Meteor/Explosion/Explosion.tscn")

func _ready():
	position.x = rand_range(0, screen_size.x)
	position.y = -8
	var x
	if position.x < screen_size.x / 2:
		x = rand_range(0, .3)
	else:
		x = rand_range(-.3, 0)
	velocity = Vector2(x, rand_range(.8, 2))
	
	
func _process(_delta):
	if position.y > screen_size.y + 50:
		queue_free()


func _physics_process(delta):
	position += velocity * delta * 100


func on_PowerUp_area_entered(area, type):
	if "Bullet" in area.name:
		area.queue_free()
		var e = explosion.instance()
		e.position = position
		get_parent().call_deferred("add_child", e)
		get_parent().get_parent().get_node("Meteors/ExplosionSound").play()
		queue_free()
		
	if area.name == "Player":
		get_parent().get_node(type).play()
		effect(area)
		queue_free()
	

func effect(_player):
	pass
