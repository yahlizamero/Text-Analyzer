#!/usr/bin/env python3

import argparse
from task_implementation.Task_1_Preprocessing import *
from task_implementation.Task_2_Counting_Seq import *
from task_implementation.Task_3_Counting_Person import *
from utils.helper_Task1 import *
from utils.helper_Task2 import *


def readargs(args=None):
    parser = argparse.ArgumentParser(
        prog='Text Analyzer project',
    )
    # General arguments
    parser.add_argument('-t', '--task',
                        help="task number",
                        required=True
                        )
    parser.add_argument('-s', '--sentences',
                        help="Sentence file path",
                        )
    parser.add_argument('-n', '--names',
                        help="Names file path",
                        )
    parser.add_argument('-r', '--removewords',
                        help="Words to remove file path",
                        )
    parser.add_argument('-p', '--preprocessed',
                        action='append',
                        help="json with preprocessed data",
                        )
    # Task specific arguments
    parser.add_argument('--maxk',
                        type=int,
                        help="Max k",
                        )
    parser.add_argument('--fixed_length',
                        type=int,
                        help="fixed length to find",
                        )
    parser.add_argument('--windowsize',
                        type=int,
                        help="Window size",
                        )
    parser.add_argument('--pairs',
                        help="json file with list of pairs",
                        )
    parser.add_argument('--threshold',
                        type=int,
                        help="graph connection threshold",
                        )
    parser.add_argument('--maximal_distance',
                        type=int,
                        help="maximal distance between nodes in graph",
                        )

    parser.add_argument('--qsek_query_path',
                        help="json file with query path",
                        )
    return parser.parse_args(args)

def main():

    args=readargs()
    
    # Start with implementing according to the task number
    # if statment with the tasks and different classes for each task

    # Task 1 Implementation
    if int(args.task) == 1:
        if not args.sentences or not args.names or not args.removewords:
            print("Invalid input: Missing required arguments for task 1.")
            return

        preprocessor = Preprocessing(
            question_num=1,
            sentences_path=args.sentences,
            people_path=args.names,
            stopwords_path=args.removewords,
        )

        results = preprocessor.preprocess()

        # Save to output file if specified
        if args.output_file:
            with open(args.output_file, "w") as file:
                json.dump(results, file, indent=4)
            print(f"Results saved to {args.output_file}")

        # Print to terminal
        print(json.dumps(results, indent=4, sort_keys=True))


if __name__=="__main__":
    main()
