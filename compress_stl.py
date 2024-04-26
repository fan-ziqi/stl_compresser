import os
import trimesh

target_number_of_triangles = 1000

current_directory = os.getcwd()

input_directory = os.path.join(current_directory, 'input')
output_directory = os.path.join(current_directory, 'output')

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for stl_file in os.listdir(input_directory):
    if stl_file.lower().endswith(".stl"):
        mesh = trimesh.load_mesh(os.path.join(input_directory, stl_file))
        simplified_mesh = mesh.simplify_quadric_decimation(target_number_of_triangles)
        output_file_path = os.path.join(output_directory, stl_file)
        simplified_mesh.export(output_file_path)
