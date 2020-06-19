from .Highscores.read_write import read_data, dump_data

class Upgrades:
	@staticmethod
	def update_upgrades(file):
		data = read_data(file)

		for upgrade in data["upgrades"]:
			if data[upgrade]["active"]:
				if data[upgrade]["time"] >= data[upgrade]["duration"]: # If passed duration, revert upgrade
					data[upgrade]["time"] = 0
					data[upgrade]["active"] = False
					data[data[upgrade]["revert_variable"]] = data[upgrade]["revert_val"]
				else:
					data[upgrade]["time"] += 1 # Increase timer (once per game)
		
		dump_data(file, data)