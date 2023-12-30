extends Node

const VERSION : int = 2
const NULL_SCORE : float = -1.0


# If highscore doesn't exist, it returns NULL_SCORE
# Otherwise returns the highscore
func get_highscore(lvl_name : String) -> float:
	return _get_file(lvl_name, File.READ).get_float()

# It sets the new highscore if the new score 
# is lower (i. e. faster) than the old highscore
func set_highscore(lvl_name : String, new_score):
	var old_highscore = get_highscore(lvl_name)
	
	if old_highscore == NULL_SCORE or new_score < old_highscore:
		var f = _get_file(lvl_name, File.WRITE)
		f.store_float(new_score)
		f.close()

# It opens a file in open_mode_flag and if it
# doesn't exist it creates it with NULL_SCORE value
func _get_file(lvl_name, open_mode_flag) -> File:
	var path = "user://level %s highscore - version %s.save" % [lvl_name, VERSION]
	var f = File.new()
	if not f.file_exists(path):
		f.open(path, File.WRITE)
		f.store_float(NULL_SCORE)
		f.close()
		return _get_file(lvl_name, open_mode_flag)
	f.open(path, open_mode_flag)
	return f
