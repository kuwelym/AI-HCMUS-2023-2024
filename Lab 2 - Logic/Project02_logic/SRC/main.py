from pl_resolution import PLResolution

INPUT_FILE_PATHS = [r'Input/input_1.txt',
                   r'Input/input_2.txt',
                   r'Input/input_3.txt',
                   r'Input/input_4.txt',
                   r'Input/input_5.txt']

OUTPUT_FILE_PATHS = [r'Output/output_1.txt',
                    r'Output/output_2.txt',
                    r'Output/output_3.txt',
                    r'Output/output_4.txt',
                    r'Output/output_5.txt']

def main():
    """
    Executes the PLResolution algorithm for a list of input files and saves the results to corresponding output files.
    """
    for input_file, output_file in zip(INPUT_FILE_PATHS, OUTPUT_FILE_PATHS):
        pl_resolution = PLResolution(input_file, output_file)
        pl_resolution.read_input()
        pl_resolution.pl_resolution()
        pl_resolution.write_output()

if __name__ == "__main__":
    main()
