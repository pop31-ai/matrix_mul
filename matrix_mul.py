#!/usr/bin/env python3
import sys
import json
import argparse


def parse_matrix(s):
    try:
        m = json.loads(s)
        if not isinstance(m, list) or not all(isinstance(row, list) for row in m):
            raise ValueError
        return m
    except Exception:
        raise ValueError(f"Матрица должна быть JSON-массивом массивов, например: [[1,2],[3,4]]")


def multiply(a, b):
    if len(a[0]) != len(b):
        raise ValueError(
            f"Несовместимые размеры: {len(a)}x{len(a[0])} и {len(b)}x{len(b[0])}"
        )
    rows_a, cols_a = len(a), len(a[0])
    cols_b = len(b[0])
    result = [[0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]
    return result


def print_matrix(m):
    for row in m:
        print("  ".join(f"{v:g}" for v in row))


def main():
    parser = argparse.ArgumentParser(description="CLI для умножения матриц")
    parser.add_argument("matrices", nargs="*", help='Матрицы в формате JSON, например: [[1,2],[3,4]]')
    parser.add_argument("-i", "--interactive", action="store_true", help="Интерактивный режим")
    args = parser.parse_args()

    matrices = []
    if args.matrices:
        for s in args.matrices:
            matrices.append(parse_matrix(s))
    elif args.interactive or not sys.stdin.isatty():
        source = sys.stdin if not sys.stdin.isatty() else sys
        print("Вводите матрицы по одной (JSON-массив). Пустая строка — завершить ввод:")
        for line in source:
            line = line.strip()
            if not line:
                break
            matrices.append(parse_matrix(line))
    else:
        parser.print_help()
        sys.exit(1)

    if len(matrices) < 2:
        print("Ошибка: нужно минимум 2 матрицы для умножения.", file=sys.stderr)
        sys.exit(1)

    result = matrices[0]
    for m in matrices[1:]:
        try:
            result = multiply(result, m)
        except ValueError as e:
            print(f"Ошибка: {e}", file=sys.stderr)
            sys.exit(1)

    print("Результат:")
    print_matrix(result)


if __name__ == "__main__":
    main()
