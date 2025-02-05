import argparse
import json
import sys
from task_implementation.Task_1_Preprocessing import Preprocessing
from task_implementation.Task_2_Counting_Seq import SequenceCounter
from task_implementation.Task_3_Counting_Person import PersonMentionCounter
from task_implementation.Task_4_Search_Engine import SearchEngine
from task_implementation.Task_5_Contexts import PersonContexts
from task_implementation.Task_6_Direct_Connections import DirectConnections
from task_implementation.Task_7_8_Indirect_Connections import IndirectPaths
from task_implementation.Task_9_Grouping_Sentences import SentenceClustering


def readargs(args=None):
    parser = argparse.ArgumentParser(
        prog='Text Analyzer project',
    )
    # General arguments
    parser.add_argument('-t', '--task',
                        help="task number",
                        type=int,
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
    args = readargs()

    # General check for preprocessed data
    if args.preprocessed and not args.preprocessed.endswith('.json'):
        print("Error: The preprocessed file should be a JSON file.")
        sys.exit(1)

    if args.task == 1:
        processor = Preprocessing(question_num=args.task,
                                  sentences_path=args.sentences,
                                  people_path=args.names,
                                  stopwords_path=args.removewords)
        result = processor.generate_results()

    elif args.task == 2:
        counter = SequenceCounter(question_num=args.task,
                                  sentences_path=args.sentences,
                                  stopwords_path=args.removewords,
                                  preprocess_path=args.preprocessed,
                                  N=args.maxk)
        result = counter.generate_results()

    elif args.task == 3:
        person_counter = PersonMentionCounter(question_num=args.task,
                                              sentences_path=args.sentences,
                                              stopwords_path=args.removewords,
                                              people_path=args.names,
                                              preprocess_path=args.preprocessed)
        result = person_counter.generate_results()

    elif args.task == 4:
        search_engine = SearchEngine(question_num=args.task,
                                     sentences_path=args.sentences,
                                     stopwords_path=args.removewords,
                                     k_seq_path=args.qsek_query_path,
                                     preprocess_path=args.preprocessed)
        result = search_engine.generate_results()

    elif args.task == 5:
        context_finder = PersonContexts(question_num=args.task,
                                        sentences_path=args.sentences,
                                        people_path=args.names,
                                        stopwords_path=args.removewords,
                                        preprocess_path=args.preprocessed,
                                        N=args.maxk)
        result = context_finder.generate_results()

    elif args.task == 6:

        direct_conn = DirectConnections(question_num=args.task,
                                        sentences_path=args.sentences,
                                        people_path=args.names,
                                        stopwords_path=args.removewords,
                                        preprocess_path=args.preprocessed,
                                        window_size=args.windowsize,
                                        threshold=args.threshold)
        result = direct_conn.generate_results()

    elif args.task == 7:
        indirect_conn = IndirectPaths(question_num=args.task,
                                      sentences_path=args.sentences,
                                      people_path=args.names,
                                      stopwords_path=args.removewords,
                                      preprocess_path=args.preprocessed,
                                      window_size=args.windowsize,
                                      threshold=args.threshold,
                                      people_connections_path=args.pairs,
                                      maximal_distance=args.maximal_distance)
        result = indirect_conn.generate_results_task_7()

    elif args.task == 8:
        fixed_length_paths = IndirectPaths(question_num=args.task,
                                           sentences_path=args.sentences,
                                           people_path=args.names,
                                           stopwords_path=args.removewords,
                                           preprocess_path=args.preprocessed,
                                           window_size=args.windowsize,
                                           threshold=args.threshold,
                                           people_connections_path=args.pairs,
                                           K=args.fixed_length)
        result = fixed_length_paths.generate_results_task_8()

    elif args.task == 9:
        sentence_cluster = SentenceClustering(question_num=9,
                                              sentences_path=args.sentences,
                                              stopwords_path=args.removewords,
                                              preprocess_path=args.preprocessed,
                                              threshold=args.threshold,
                                              )
        result = sentence_cluster.generate_results()

    else:
        print("Invalid task number. Please specify a task between 1 and 9.")
        return

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
