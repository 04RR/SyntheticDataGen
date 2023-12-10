import os
import yaml
import time
import torch
import warnings
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM

warnings.filterwarnings("ignore")


with open("generation_config.yaml", "r") as file:
    config = yaml.safe_load(file)


def load_sections(file_path):
    with open(file_path, "r") as file:
        sections = file.read()

    sections = [x.strip() for x in sections.split("### ")[1:-1]]
    return sections


def generate_questions(section):
    prompt_template = """<|user|> PromptReplaceMe<|end_of_turn|><|bot|> """

    content_str = (
        "Context -\n"
        + section
        + f"""
        
        Instruction -
        Give me *{config['num_questions']}* unique and interesting Questions and corresponding Answers based on the context given above. Make the answers long and detailed. Make sure the questions are independent of each other and in the given format.
        Format -
        1. Question: <Question>
        Answer: <Answer> END
        
        2. Question: <Question>
        Answer: <Answer> END
        
        """
    )
    prompt = prompt_template.replace("PromptReplaceMe", content_str)

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

    return generated


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

    qa_item = generate_questions(sections[0]).split("END")

    for i, item in enumerate(qa_item):
        q = item.split("Answer:")[0].split("Question:")[-1].strip()
        a = item.split("Answer:")[-1].strip()

        if len(q) > 0 and len(a) > 0:
            data["question"].append(q)
            data["answer"].append(a)

    df = pd.DataFrame(data)
    df.to_csv(config["output_file"], index=False)

    print(len(data["answer"]), len(data["question"]))
