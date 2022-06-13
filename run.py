import argparse
import os
import pathlib
import shutil
import sys
from envbuilder import EnvBuilder
from pscheck import process_exists

parser = argparse.ArgumentParser(description='Wrapper script running format converter, marching cube algorithm implementation'\
    + ' and output model visualizer.')
parser.add_argument('input', type=pathlib.Path,
    help='path to a PLY model containing voxel data in the point cloud format -OR- to a JSON file containing voxel data -OR- to an OBJ model file')
parser.add_argument('--isomin', type=float, default=0.001,
    help='lower bound for the density of voxels visualized as an isosurface (default: %(default)s)')
parser.add_argument('--isomax', type=float, default=1.0,
    help='upper bound for the density of voxels visualized as an isosurface (default: %(default)s)')

if __name__ == '__main__':
    args = parser.parse_args()
    env_builder = EnvBuilder(with_pip=True)
    env_builder.create('./.venv')
    requirements_path = pathlib.Path('./marching-cubes/requirements.txt')
    if requirements_path.exists():
        env_builder.install_requirements(str(requirements_path.absolute()))
        requirements_path.unlink()

    visualizer_pname = 'visualizer.exe'
    visualizer_binary = pathlib.Path(f'./build/{visualizer_pname}')
    
    if not visualizer_binary.exists():
        print('Building the visualizer...')
        if os.system('cargo --help') != 0:
            print('Missing build toolchain!', file=sys.stderr)
            print('Place the binary with assets in "build" subdirectory manually.', file=sys.stderr)
            exit(-1)
        os.system('build.bat')

    model_path = str(args.input.absolute())
    model_path_noext, model_path_ext = os.path.splitext(model_path)
    model_path_ext = model_path_ext[1:].lower()

    if model_path_ext not in ['ply', 'json', 'obj']:
        print(f'Unknown input file extension: {model_path_ext}', file=sys.stderr)
        exit(-1)

    if model_path_ext in ['ply']:
        print('Converting to internal JSON format...')
        json_path = model_path_noext + '.json'
        env_builder.run_module('marching-cubes.vox2json', [model_path, json_path])
    else:
        json_path = model_path

    obj_path = str(pathlib.Path('./build/assets/mesh.obj').absolute())
    if model_path_ext in ['ply', 'json']:
        print('Running the marching cubes algorithm...')
        env_builder.run_module('marching-cubes.voxel_importer',
            [json_path, obj_path, '--isomax', f'{args.isomax:f}', '--isomin', f'{args.isomin:f}'])
    else:
        print('Ignoring --isomin and --isomax arguments...')
        shutil.copyfile(model_path, obj_path)

    if not process_exists(visualizer_pname):
        print('Running the visualizer...')
        os.system(f'start "" {str(visualizer_binary.absolute())}')
