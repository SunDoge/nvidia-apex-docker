import argparse
import subprocess


def pull_cuda_image(cuda_version: str):
    cmd = f'docker pull nvidia/cuda:${cuda_version}-devel'
    subprocess.run(cmd, shell=True)


def build_apex(cuda_version: str, container_name: str = 'dummy'):
    build_whl_cmd = 'bash -c "cd /apex && $(which python) setup.py bdist_wheel --cpp_ext --cuda_ext"'

    cmds = [
        f'docker create -ti -v $(pwd)/apex:/apex -v $HOME:$HOME --name {container_name} nvidia/cuda:{cuda_version}-devel bash',
        f'docker run --rm --volumes-from {container_name} nvidia/cuda:{cuda_version}-devel {build_whl_cmd}',
        # f'docker cp {container_name}:/apex/dist/ ./',
        f'docker rm -fv {container_name}',
    ]

    for cmd in cmds:
        print('exec:', cmd)
        subprocess.run(cmd, shell=True)


def main(args: argparse.Namespace):
    pull_cuda_image(args.cuda_version)
    build_apex(args.cuda_version, container_name=args.container_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--cuda-version', default='10.0', help='CUDA version')
    parser.add_argument(
        '-n', '--container-name', default='dummy', help='container name, change it if conflict'
    )
    args = parser.parse_args()

    main(args)
