import os
import subprocess
import difflib
import time

PROGRAM_PATH = "C:\\Users\\Ptryb\\source\\repos\\AiSD2\\x64\\Debug\\AiSD2.exe"
SKIP = []


def search_for_tests():
    for root, dirs, files in os.walk('tests'):
        for file in sorted(files, key=lambda x: int(x.split('.')[0])):
            if file.endswith('.in') and file.split('.')[0] not in SKIP:
                yield os.path.join(root, file).rstrip(".in")


def run_test(input_file, output_file):
    with open(input_file, 'r') as in_file:
        with open(output_file, 'w') as out_file:
            proc = subprocess.Popen(PROGRAM_PATH, stdin=in_file, stdout=out_file)
            return_code = proc.wait(60)
    return return_code


def compare_files(file2, file1):
    with open(file1, 'r') as f1:
        with open(file2, 'r') as f2:
            diffs = difflib.unified_diff(f1.readlines(), f2.readlines())
            return ''.join(diffs)


if __name__ == '__main__':
    passed = 0
    failed = 0
    for test in search_for_tests():
        print(f'Running test {test}...')
        start_time = time.time()
        if run_test(f'{test}.in', f'program_out/{os.path.basename(test)}.txt') == 0:
            diff = compare_files(f'program_out/{os.path.basename(test)}.txt',
                                 f'tests/{os.path.basename(test)}.out')
            if diff:
                print('Test failed!')
                failed += 1
                print(diff)
            else:
                print('Test passed! Time: {:.2f} s'.format(time.time() - start_time))
                passed += 1
        else:
            print('Runtime error!')
            failed += 1
            if input('Continue? [y/n] ') != 'y':
                break
    print('Passed: {}, failed: {}'.format(passed, failed))
