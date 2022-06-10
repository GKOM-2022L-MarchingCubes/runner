import argparse
import os
import pathlib
import shutil
import sys
from envbuilder import EnvBuilder

parser = argparse.ArgumentParser(description='Wrapper script running format converter, marching cube algorithm implementation'\
    + ' and output model visualizer.')
parser.add_argument('input', type=pathlib.Path,
    help='path to a PLY model containing voxel data in the point cloud format')
parser.add_argument('--isomin', type=float, default=0.001,
    help='lower bound for the density of voxels visualized as an isosurface')
parser.add_argument('--isomax', type=float, default=1.0,
    help='upper bound for the density of voxels visualized as an isosurface')

if __name__ == '__main__':
    args = parser.parse_args()
    env_builder = EnvBuilder(with_pip=True)
    env_builder.create('./.venv')
    env_builder.install_requirements('./marching-cubes/requirements.txt')

    visualizer_binary = pathlib.Path('./build/visualizer.exe')
    
    if not visualizer_binary.exists():
        print('Visualizer binary not found!', file=sys.stderr)
        print('Use "build.sh" or place the binary with assets in "build" subdirectory.', file=sys.stderr)
        exit(-1)

    model_path = str(args.input.absolute())
    model_path_noext = os.path.splitext(model_path)[0]

    print('Converting to internal JSON format...')
    env_builder.run_module('marching-cubes.vox2json', [model_path])

    print('Running the marching cubes algorithm...')
    json_path = model_path_noext + '.json'
    env_builder.run_module('marching-cubes.voxel_importer', [json_path, f'{args.isomax:f}', f'{args.isomin:f}'])

    print('Running the visualizer...')
    obj_path = model_path_noext + '.obj'
    shutil.copyfile(obj_path, './build/assets/mesh.obj')
    os.system(str(visualizer_binary.absolute()))
