extends Area2D


var velocity
onready var screen_size = get_viewport_rect().size

onready var explosion = load("res://Meteor/Explosion/Explosion.tscn")
onready var break_meteor = load("res://Meteor/BreakMetorAnimation.tscn")
onready var meteors = {
	"small":load("res://Meteor/Small/SmallMeteor.tscn"),
	"medium":load("res://Meteor/Medium/MediumMeteor.tscn"),
	"big":load("res://Meteor/Big/BigMeteor.tscn")
}


func _ready():
	set_ready()
	var x
	if position.x < screen_size.x / 2:
		x = rand_range(0, 4)
	else:
		x = rand_range(-4, 0)
	velocity = Vector2(x, rand_range(.5, 4))
	
	
func _process(_delta):
	if position.y > screen_size.y + 200:
		queue_free()

func _physics_process(delta):
	position += velocity * delta * 100


func on_Meteor_area_entered(area, new_meteor_size=null):
	if area.name == "Player" or "Bullet" in area.name:
		if "Bullet" in area.name:
			area.queue_free()
			
		if new_meteor_size:
			var break_animation = break_meteor.instance()
			break_animation.position = position
			break_animation.emitting = true
			get_parent().call_deferred("add_child", break_animation)
			get_parent().get_node("BreakSound").play()
			for _i in range(2):
				var new_meteor = meteors[new_meteor_size].instance()
				new_meteor.position = position
				get_parent().call_deferred("add_child", new_meteor)
		else:
			var e = explosion.instance()
			e.position = position
			get_parent().call_deferred("add_child", e)
			get_parent().get_node("ExplosionSound").play()
			
		queue_free()


func set_ready():
	pass
