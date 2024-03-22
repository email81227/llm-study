# LLM讀書會 - 財報機器人專案


### 主辧單位: 台灣人工智慧協會進修交流委員會、H.I.T. 生醫創新實作社群


This is a side project from one of the TAIA study groups. 
The purpose is to build a chatbot and interact with users to analyse and build a profitable investment for seeking alpha.

# Important dependency docs/repo
Langchain: [Doc](https://api.python.langchain.com/en/latest/langchain_api_reference.html#) | [Repo](https://github.com/langchain-ai/langchain)
Chainlit: [Doc](https://docs.chainlit.io/get-started/overview) | [Repo](https://github.com/Chainlit/chainlit)


Preparation / Installation environment
---
* **English**

1. Install [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/).
2. Install [Git](https://git-scm.com/downloads)
3. Change dir to the path you will place the project. Dowland or clone this repo

        git clone https://github.com/email81227/llm-study.git

4. Build the project enviroment

        conda create -n llm-study python=3.10 poetry
        
5. Activate the env. (To deactivate, using `conda deactivate`)

        conda activate llm-study 
        
6. Switch to the project dir

        cd {path to the repo cloned}/llm-study
        
7. Install packages by poetry

        poetry install
        
8. Create `.env` file under the project dir
9. Open `.env` and append the following line

        OPENAI_API_KEY="{your openai key}"
        USER_EMAIL="{your email address}"
        USER_NAME="{your nickname}"
        LANGFUSE_PUBLIC_KEY="{apply here: https://cloud.langfuse.com/}"
        LANGFUSE_SECRET_KEY="{apply here: https://cloud.langfuse.com/}"
        
* **中文說明**

1. 安裝 [Anaconda](https://www.anaconda.com/download) 或 [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/)
2. 安裝 [Git](https://git-scm.com/downloads)
3. 移動到預計放置專案的目錄下，下載或複製專案

        git clone https://github.com/email81227/llm-study.git

4. 建立Python專案環境

        conda create -n llm-study python=3.10 poetry
        
5. 切換到該環境（用`conda deactivate`反過來切換回base env）

        conda activate llm-study 
        
6. 切換到專案目錄下
        
        cd {path to the repo cloned}
        
7. 安裝專案內套件

        poetry install 
        
8. 新增名為`.env`的空白檔案
9. 打開或新增以下內容至`.env`中


        OPENAI_API_KEY="{your openai key}"
        USER_EMAIL="{your email address}"
        USER_NAME="{your nickname}"
        LANGFUSE_PUBLIC_KEY="{apply here: https://cloud.langfuse.com/}"
        LANGFUSE_SECRET_KEY="{apply here: https://cloud.langfuse.com/}"


Execution
---

Run the command on project dir:

```
chainlit run chat.py -w
```

