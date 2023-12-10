## Overview
This GitHub repository contains a collection of Python scripts designed for generating, processing, and manipulating question-answer pairs from various text sources. The scripts are tailored for handling data in the context of natural language processing (NLP) and machine learning, particularly using transformers. The repository includes the following key files:

- `data_gen.py`: Generates questions and answers based on provided context sections.
- `main.py`: Extracts questions and answers from text and processes them with the Nougat tool.
- `pdfocr.py`: Processes PDF files to extract and convert content to a markdown format.
- `temp.py`: Generates variations of question-answer pairs based on explanations.
- `generation_config.yaml`: Configuration file for the generation script.

## Requirements
- Python 3.6 or higher
- PyTorch
- Nougat: follow installation process from [here](https://github.com/facebookresearch/nougat?tab=readme-ov-file#install)
- Transformers library
- Pandas
- YAML

## Usage

### Data Generation (`data_gen.py`)
- Purpose: To generate questions and answers from provided text sections.
- Usage: Run `python data_gen.py`. Ensure that the `generation_config.yaml` is configured correctly.

### Main Processing Script (`main.py`)
- Purpose: To extract questions and answers from provided text and process them.
- Usage: Run `python main.py`. The script will process files located in the specified folder path.

### PDF OCR Script (`pdfocr.py`)
- Purpose: To process PDF files and extract text in markdown format.
- Usage: Run `python pdfocr.py`. Make sure to have your PDF files in the specified folder path.

### Temporary Script (`temp.py`)
- Purpose: To generate variations of question-answer pairs.
- Usage: Run `python temp.py` after configuring `generation_config.yaml` with appropriate settings.

## Configuration (`generation_config.yaml`)
- Modify this YAML file to change the settings for question generation, such as the model name, temperature, and other parameters.
