import warnings
import subprocess
import json
import os
import re

warnings.filterwarnings("ignore")


def extract_questions_and_answers(text):
    pattern = r"(Q\d+ :)(.*?)(?=(Q\d+ :)|$)"

    matches = re.findall(pattern, text, re.DOTALL)
    questions_dict = {}

    for match in matches:
        question_number = match[0].replace(":", "").strip()
        question_answer_text = match[1].strip()

        split_text = question_answer_text.split("Answer :")
        question_text = split_text[0].strip()
        answer_text = split_text[1].strip() if len(split_text) > 1 else ""

        questions_dict[question_number] = {
            "question": question_text,
            "answer": answer_text,
        }

    return questions_dict


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

for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    execute_nougat(file_path, output_dir)

for file_name in os.listdir(output_dir):
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, "r") as f:
        text = f.read()

    questions_dict = extract_questions_and_answers(text)
    
    print(file_path.replace(".mmd", ".json"))
    with open(file_path.replace(".mmd", ".json"), "w") as f:
        json.dump(questions_dict, f, indent=4)
