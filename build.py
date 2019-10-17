import argparse
from typing import List
from subprocess import Popen
import subprocess


def retrieve_whl():
    build_whl_cmd = 'cd /root/apex && python setup.py bdist_wheel --cpp_ext --cuda_ext'

    cmds = [
        'docker create -ti --name dummy huangdeng/apex ' + build_whl_cmd,
        'docker cp dummy:/root/apex/dist/ ./',
        'docker rm -fv dummy',
    ]

    for cmd in cmds:
        try:
            ret = subprocess.run(cmd, shell=True)
            return ret, None
        except subprocess.CalledProcessError as e:
            return None, e


def build_docker_image(python_version: str, cuda_version: str, pytorch_version: str = '') -> (subprocess.CompletedProcess, subprocess.CalledProcessError):
    """
    pytorch_version = '' download the latest version
    """
    cmd = [
        'docker', 'build', '.',
        '-t', f'sundoge/apex:cuda{cuda_version}-py{python_version}',
        '--build-arg', f'CUDA_VERSION={cuda_version}',
        '--build-arg', f'PYTHON_VERSION={python_version}',
        '--build-arg', f'PYTORCH_VERSION={pytorch_version}',
    ]
    try:
        ret = subprocess.run(cmd)
        return ret, None
    except subprocess.CalledProcessError as e:
        return None, e


def main(cuda_versions: List[str], python_versions: List[str], torch_versions: List[str], retrieve: bool):

    for cuda_version in cuda_versions:
        for python_version in python_versions:
            for torch_version in torch_versions:
                build_docker_image(
                    python_version, cuda_version, torch_version)
                if retrieve:
                    retrieve_whl()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cuda-version', nargs='*',
                        default=['10.0'], help='--build-arg CUDA_VERSION')
    parser.add_argument('-p', '--python-version', nargs='*',
                        default=['3.7'], help='--build-arg PYTHON_VERSION')
    parser.add_argument('-t', '--torch-version', nargs='*',
                        default=['1.1.0'], help='--build-arg TORCH_VERSION')
    parser.add_argument('-r', '--retreve', action='store_true')

    args = parser.parse_args()

    # print(args)

    main(
        args.cuda_version,
        args.python_version,
        args.torch_version,
        args.retrieve
    )
