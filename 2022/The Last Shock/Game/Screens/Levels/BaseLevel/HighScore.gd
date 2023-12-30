extends Label


onready var level_name = get_parent().name


func _ready():
	var highscore = Scores.get_highscore(level_name)
	if not highscore == Scores.NULL_SCORE:
		text = str(highscore)
