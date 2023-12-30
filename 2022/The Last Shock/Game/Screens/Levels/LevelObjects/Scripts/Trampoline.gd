extends StaticBody2D


export (int) var jump_force = 300
onready var animation_player = $AnimationPlayer


func _on_JumpArea_body_entered(body):
	if body is KinematicBody2D or body is RigidBody2D:
		body.jump(jump_force)
		animation_player.play("TrampolineAnimation")
		$SoundEffect.play()
