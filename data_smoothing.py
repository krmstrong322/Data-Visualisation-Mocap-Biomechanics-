from functions_ import *


def get_input(input_file):
	input_file = pd.read_csv(input_file)
	return input_file


def complex_smoothing(input_file, smoothing_method, window):
	if (int(window) % 2) == 0:
		print("window size must be odd")
		return
	complex_df = input_file
	if smoothing_method == "filter" or smoothing_method == "Filter":
		complex_df = complex_df.apply(lambda x: savgol_filter(x, window, 1))
	elif smoothing_method == "rolling" or smoothing_method == "Rolling":
		for i in complex_df:
			complex_df[i] = complex_df[i].rolling(window=window, center=False, min_periods=1).mean()
	return complex_df


def simple_smoothing(input_file, magnitude):
	simple_df = input_file
	for j in simple_df:
		simple_df[j] = simple_df[j][::magnitude]
	return simple_df


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Read file form Command line.")
	parser.add_argument("-i", "--input", dest="filename", required=True, type=validate_file, help="input file", metavar="FILE")
	parser.add_argument("-s", "--smoothing", required=True, help="simple or complex")
	parser.add_argument("-m", "--method", required=False, default="filter", help="filter or rolling")
	parser.add_argument("-w", "--window", required=False, default=5, help="size of window")
	args = parser.parse_args()
	path = args.filename
	if args.smoothing == "simple" or args.smoothing == "Simple":
		simple_smoothing(get_input(path), 2).to_csv("simple_smoothing.csv")
	elif args.smoothing == "complex" or args.smoothing == "Complex":
		complex_smoothing(get_input(path), args.method, int(args.window)).to_csv("complex_smoothing.csv")
	else:
		print("Smoothing selection not a valid choice")


data = pd.read_csv("sit.pkl.csv")
print(data)



#new_df = complex_smoothing(data, "filter", 5).to_csv("complex_smoothing.csv")
#test1 = pd.Series(data[1])
#print(test1.rolling(5).mean())
#print(savgol_filter(data[1], 5, 2))

for i in data:
	data[i] = data[i].rolling(window=5, center=False, min_periods=1).mean()
print(data)
data.apply(lambda x: savgol_filter(x, 5, 1)).to_csv("out.csv")