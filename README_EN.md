[中文](https://github.com/iii-org/gpt-inside-openai)|ENGLISH

# Introduction

This is an open-source tool that allows businesses to easily import their own data using Excel. This empowers enterprises to seamlessly connect their data to chat GPT models, and future updates will include security verification features to make AI chat services more secure and reliable. For more information, please refer to the [introduction website](https://www.gptinside.openiii.org/) of this tool.

This tool is supported by the [Administration for Digital Industries (ADI), Ministry of Digital Affairs, Republic of China (Taiwan)](https://moda.gov.tw/ADI/).
# Table of Contents

* System Requirements
* Installation
* Training
* Inference

# System Requirements

Regarding hardware, you can opt for either local resources or cloud-based computing resources, as detailed below.
### On-Premises Hardware

|         | Minimum Requirements | Recommended Requirements |
| :-------- | --------------------- | --------------------- |
| CPU     | 4 core             | 8 core             |
| Memory  | 8 GB               | 16 GB                 |
| Storage | 256 GB                | 512 GB                |


# Training Data Format

Using the question-answering content from the [Pregnancy Health Education Handbook](https://www.hpa.gov.tw/Pages/EBook.aspx?nodeid=1454) provided by the Health Promotion Administration, Ministry of Health and Welfare, Republic of China (Taiwan) as an example, the format is illustrated in ```data/raw_data.xlsx```. Each row represents a question-answering pair, and the column definitions are as follows:


| Column Name | Column Definition | Column Example                                                  |
| :-------------- | ------------ | ----------------------------------------------------------- |
| Q      | Question    | At what stage of pregnancy should I have a high-level ultrasound scan?          |
| A      | Answer    | It is recommended to have it between the 20th and 24th week of pregnancy.                                                      |
| REF    | Reference | High-level ultrasound scans provide clear images of the fetus and are recommended between the 20th and 24th weeks of pregnancy. This is a self-funded examination, and pregnant women can decide whether to proceed based on their own circumstances. High-level ultrasound scans cannot be used to determine the gender of the fetus. If the pregnant woman feels unwell or the fetus has special conditions, she can discuss the frequency and number of examinations with a doctor. When fetal abnormalities are found, please consult relevant specialists. |

# Quick Start
At the beginning, you need to confirm whether your OpenAI inference engine and embedding engine are available. Next, on an Ubuntu 20.04 TLS operating system, execute the following command in the terminal:
```
bash run_service.sh -i 127.0.0.1 -d ./data/raw_data.xlsx -b {your openai api base} -t azure -v {your openai api version} -k {your openai api key} -e {your openai api engine} -c {your openai api embedding engine}
```
Where:
- -i: The IP address of the machine, defaulting to localhost. If the web interface needs to be accessed by external machines, an externally accessible IP address should be provided.
- -d: Path to the data storage
- -t: openai type, only support azure or openai
- -v: openai api version
- -k: openai api key
- -e: openai api engine
- -c: openai api embedding engine
- -s: skip train/inference stage (-s skip-train/skip-inference)

This command will automatically install the environment and train the model. After training is complete, you'll see the following message on the screen:
```
Please enter the URL link below into your browser to activate the dialog interface
    URL link: http://127.0.0.1/gpt/qa/
```
Copy and paste the URL link into your browser's address bar to begin the question-answering process.

### Starting Only the Web Service
Execute the following command in the terminal:
```
bash run_service.sh -i 127.0.0.1 -d ./data/raw_data.xlsx -b {your openai api base} -t azure -v {your openai api version} -k {your openai api key} -e {your openai api engine} -c {your openai api embedding engine} -s skip-train
```
This command will skip the training phase and directly start the web service using the existing model.

### Stopping the System Service
Execute the following command in the terminal:
```
bash stop_service.sh
```
