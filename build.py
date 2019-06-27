import argparse
from typing import List
from subprocess import Popen


def retrieve_whl():
    pass


def build_docker_image():
    pass


def main(cuda_versions: List[str], python_versions: List[str], torch_versions: List[str]):

    for cuda_version in cuda_versions:
        for python_version in python_versions:
            for torch_version in torch_versions:
                print(
                    f'cuda{cuda_version}-py{python_version}-torch{torch_version}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cuda-version', nargs='*',
                        default=['10.0'], help='--build-arg CUDA_VERSION')
    parser.add_argument('-p', '--python-version', nargs='*',
                        default=['3.7'], help='--build-arg PYTHON_VERSION')
    parser.add_argument('-t', '--torch-version', nargs='*',
                        default=['1.1.0'], help='--build-arg TORCH_VERSION')

    args = parser.parse_args()

    # print(args)

    main(args.cuda_version, args.python_version, args.torch_version)
