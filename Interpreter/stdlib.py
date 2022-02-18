import fractions
import math


def std_print(args: list) -> None:
    print(str(args[0]))


def build_frc(args: list) -> fractions.Fraction:
    return fractions.Fraction(args[0], args[1])


def cast_frc(args: list) -> fractions.Fraction:
    return fractions.Fraction(args[0])


def cast_int(args: list) -> int:
    return math.floor(args[0])


def cast_float(args: list) -> float:
    return float(args[0])


def cast_string(args: list) -> str:
    return str(args[0])


functions = {
    'print': std_print,
    'frc': build_frc,
    'int_to_frc': cast_frc,
    'int_to_float': cast_float,
    'frc_to_float': cast_float,
    'float_to_int': cast_int,
    'frc_to_int': cast_int,
    'frc_to_string': cast_string,
    'float_to_string': cast_string,
    'int_to_string': cast_string
}
