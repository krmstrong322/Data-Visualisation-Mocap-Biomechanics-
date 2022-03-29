from functions_ import *


def get_input(input_file):
	input_file = pd.read_csv(input_file)
	return input_file


def complex_smoothing(input_file):
	df = input_file
	complex_df = df
	return complex_df


def simple_smoothing(input_file):
	df = input_file
	simple_df = df
	return simple_df


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Read file form Command line.")
	parser.add_argument("-i", "--input", dest="filename", required=True, type=validate_file, help="input file", metavar="FILE")
	parser.add_argument("-s", "--smoothing", required=True, help="simple or complex")
	args = parser.parse_args()
	path = args.filename
	if args.smoothing == "simple" or args.smoothing == "Simple":
		simple_smoothing(get_input(path)).to_csv("simple_smoothing.csv")
	elif args.smoothing == "complex" or args.smoothing == "Complex":
		complex_smoothing(get_input(path)).to_csv("complex_smoothing.csv")
	else:
		print("Smoothing selection not a valid choice")
