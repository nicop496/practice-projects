extends Area2D

var anim_ended = false
var anim_started = false

func _on_portal_body_entered(body):
	if body.name == "Jugador":
		get_parent().get_parent().touch_portal()
		$animaciones.play("desaparecer")
	
func _process(_delta):
	if $animaciones.is_playing():
		anim_started = true
		
	else:
		if anim_started:
			anim_ended = true
			
	if anim_ended:
		visible = true
		scale = Vector2(1,1)
		$sprite.animation = "explocion"
		
		if $sprite.frame == 5:
			get_parent().get_parent().next_level()
			queue_free()
		
