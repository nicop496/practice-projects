extends Label


func _ready():
	var file = File.new()
	file.open("user://highscore.dat", file.READ)
	text = "Mejor puntuación: " + file.get_as_text()
	file.close()
