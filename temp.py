import os
import yaml
import time
import json
import torch
import warnings
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM

warnings.filterwarnings("ignore")


with open("generation_config.yaml", "r") as file:
    config = yaml.safe_load(file)


def load_sections(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    return data


def generate_questions(qa_dict):
    prompt_template = """<|user|> PromptReplaceMe<|end_of_turn|><|bot|> """
    generated_list = []

    for k in qa_dict.keys():
        section = (
            "Question: " + qa_dict[k]["question"] + "\nAnswer: " + qa_dict[k]["answer"]
        )

        content_prompt = f"""
Give explaination for the following question and answer pair in detail -
{section}
"""

        content_prompt = content_prompt.format(section)

        prompt = prompt_template.replace("PromptReplaceMe", content_prompt)

        inputs = tokenizer(prompt, return_tensors="pt")
        input_ids = inputs.input_ids.to("cuda")

        outputs = model.generate(
            input_ids,
            max_length=4096,
            do_sample=True,
            temperature=config["temperature"],
            top_p=config["top_p"],
            repetition_penalty=config["repetition_penalty"],
            top_k=config["top_k"],
        )

        context = (
            tokenizer.decode(outputs[0], skip_special_tokens=True)
            .split("<|bot|>")[-1]
            .strip()
        )

        content_str = "Context -\n" + section +  "\n\nExplaination -\n" + context + f"""
            
Instruction -
Give me *{config['num_questions']}* unique and interesting variations of the question-answer pair based it's explaination given above. Give the Questions and corresponding Answers and Make the answers long and detailed. Make sure the questions are independent of each other and in the given format.
Format -
1. Question: <Question>
Answer: <Answer> END

2. Question: <Question>
Answer: <Answer> END

"""
        prompt = prompt_template.replace("PromptReplaceMe", content_str)

        print(prompt)

        inputs = tokenizer(prompt, return_tensors="pt")
        input_ids = inputs.input_ids.to("cuda")

        outputs = model.generate(
            input_ids,
            max_length=4096,
            do_sample=True,
            temperature=config["temperature"],
            top_p=config["top_p"],
            repetition_penalty=config["repetition_penalty"],
            top_k=config["top_k"],
        )

        generated = (
            tokenizer.decode(outputs[0], skip_special_tokens=True)
            .split("<|bot|>")[-1]
            .strip()
        )
        generated_list.append(generated)
        break

    # data = {"question": [], "answer": []}

    # for item in generated_list:
    #     q = item.split("Answer:")[0].split("Question:")[-1].strip()
    #     a = item.split("Answer:")[-1].strip()

    #     if len(q) > 0 and len(a) > 0:
    #         data["question"].append(q)
    #         data["answer"].append(a)

    # df = pd.DataFrame(data)

    return generated_list


model = AutoModelForCausalLM.from_pretrained(
    config["model_name"],
    device_map="cuda",
    trust_remote_code=True,
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
)

tokenizer = AutoTokenizer.from_pretrained(
    config["model_name"],
    trust_remote_code=True,
)
print("Model loaded successfully.")

data = {"question": [], "answer": []}


for file_path in os.listdir(config["context_data_dir"]):
    st = time.time()
    sections = load_sections(os.path.join(config["context_data_dir"], file_path))

    qa_list = generate_questions(sections)
    break

for item in qa_list:
    print(item)
    print("----------------\n\n")
# qa_df.to_csv(f"{config['output_dir']}/generated_questions.csv", index=False)
