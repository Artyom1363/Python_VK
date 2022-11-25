import threading
import argparse


def fact(value, result):
    if value == 1:
        return 1

    result[value] = value * fact(value - 1, result)
    return result[value]

# def fact_wrapper(num, result):
#     value = fact(num)
#     result[num] = value


def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', dest='value', metavar='value',
                        type=int, required=True)
    return parser


if __name__ == "__main__":
    arg_parser = create_argparser()
    arg_namespace = arg_parser.parse_args()
    value_to_calc = arg_namespace.value
    print(f"{value_to_calc=}")
    result_fact = {}
    thread = threading.Thread(target=fact,
                              name="fact_1",
                              args=(value_to_calc, result_fact))

    thread.start()
    thread.join()
    print(f"result_fact: {result_fact[value_to_calc]}")
