import warnings
import subprocess
import os

warnings.filterwarnings("ignore")


def execute_nougat(file_path, output_dir, version="0.1.0-base"):
    command = (
        f"nougat {file_path} -o {output_dir} -m {version} --no-skipping --markdown"
    )
    print(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(process.stdout.read())


folder_path = "math_textbooks/solutions/"
output_dir = "output/sol/"

# for folder_name in os.listdir(folder_path):
#     os.makedirs(os.path.join(output_dir, folder_name), exist_ok=True)
#     folder_path = os.path.join(folder_path, folder_name)
#     output_path = os.path.join(output_dir, folder_name)
output_path = output_dir
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    execute_nougat(file_path, output_path)
