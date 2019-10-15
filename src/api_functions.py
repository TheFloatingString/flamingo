from datetime import datetime

class TimeCounter():

	def __init__(self):
		self.initial_day = datetime(year=1900, month=1, day=1)
		self.start_days_list = []
		self.start_datetime_list = []
		self.end_days_list = []
		self.end_datetime_list = []
		self.stress_levels_list = []
		self.stress_colors_list = []
		self.stress_color_code_dict = {
			0: 'green',
			1: 'green',
			2: 'green',
			3: 'yellow',
			4: 'yellow',
			5: 'yellow',
			6: 'orange',
			7: 'orange',
			8: 'red',
			9: 'red',
			10: 'red'
		}

	def set_initial_day(self, initial_datetime_obj):
		self.initial_day = initial_datetime_obj


	def add_row(self, start, end, stress_level):
		start_delta = start - self.initial_day
		start_day = start_delta.days
		self.start_days_list.append(start_day)
		self.start_datetime_list.append(start)

		end_delta = end - self.initial_day
		end_day = end_delta.days
		self.end_days_list.append(end_day)
		self.end_datetime_list.append(end)

		self.stress_levels_list.append(stress_level)
		self.stress_colors_list.append(self.stress_color_code_dict[stress_level])


	def return_data(self):
		return_data = []
		return_pointBackgroundColor = []
		print(self.start_days_list)
		print(self.start_datetime_list)
		print(self.stress_colors_list)
		for start_day, start_datetime, stress_level_color in zip(self.start_days_list, self.start_datetime_list, self.stress_colors_list):
			data_sample = {
				'x': start_day,
				'y': start_datetime.hour,
			}
			return_data.append(data_sample)
			return_pointBackgroundColor.append(stress_level_color)
		return return_data, return_pointBackgroundColor