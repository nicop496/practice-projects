extends Node2D

export (float) var price
export (String) var skin_name
export var unlocked = false


func _ready():
	$AnimatedSprite.frames = load("res://Player/Images/%s/SpriteFrames.tres" % skin_name)
	
	if not unlocked:
		return
	$Label.text = "$" + str(price)
	if price == 0:
		$Label.text = "FREE"
		
	if unlocked:
		$AnimatedSprite.modulate = Color.white
		$padlock.visible = false
		$SkinPortal.visible = true 
		$SkinPortal/Collider.disabled = false


func _on_SkinPortal_body_entered(body):
	if body.name != "Player":
		return
	if body.game.get_cash() < price:
		return
	body.add_cash(-price)
	body.game.save_cash(body.cash)
	body.set_skin(skin_name)
	body.enter_portal("Lobby")
	
