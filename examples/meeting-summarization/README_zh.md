# 会议纪要总结 CLI

[English](README.md) | [中文](README_zh.md)


[![Discord](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)](https://discord.com/invite/liquid-ai)

![Meeting summarization CLI](./media/demo.gif)

该示例是一个 100% 本地运行的会议纪要总结工具，依赖以下组件在你的机器上运行：

- [`LiquidAI/LFM2-2.6B-Transcript`](https://huggingface.co/LiquidAI/LFM2-2.6B-Transcript) -> 一个专用于会议转录摘要的小型语言模型。

- [`llama.cpp`](https://github.com/ggerganov/llama.cpp) -> 一个快速推理引擎，配置最小化，在本地与云端各种硬件上都具备一流性能。

该工具可以与音频转写模型串联，实现：

- 将音频文件转为对应的文字转录，
- 再使用本工具把转录内容生成摘要。

这个两步流程可以完全在本机运行，不需要云服务或 API Key。

是不是很棒？

## 快速开始

1. 如果你尚未安装 `uv`，请先安装。安装说明见 [这里](https://docs.astral.sh/uv/getting-started/installation/)。

2. 无需克隆仓库，使用 `uv run` 一行命令即可运行：
  
    ```sh
    uv run https://raw.githubusercontent.com/Liquid4All/cookbook/refs/heads/main/examples/meeting-summarization/summarize.py
    ```

    上述命令默认会使用 [这个转录文件](https://raw.githubusercontent.com/Liquid4All/cookbook/refs/heads/main/examples/meeting-summarization/transcripts/example_1.txt) 来生成摘要。

3. 若要使用其他转录文件，可通过 `--transcript-file` 参数显式传入本地路径或 HTTP/HTTPS URL，工具会自动下载并使用该文件。

    例如，使用 [这个文件](https://raw.githubusercontent.com/Liquid4All/cookbook/refs/heads/main/examples/meeting-summarization/transcripts/example_2.txt) 可运行：

    ```sh
    uv run https://raw.githubusercontent.com/Liquid4All/cookbook/refs/heads/main/examples/meeting-summarization/summarize.py \
      --transcript-file https://raw.githubusercontent.com/Liquid4All/cookbook/refs/heads/main/examples/meeting-summarization/transcripts/example_2.txt
    ```


4. 如果你想深入理解并修改代码，可以克隆仓库：

    ```sh
    git clone https://github.com/Liquid4All/cookbook.git
    cd cookbook/examples/meeting-summarization
    ```

    然后使用以下命令运行总结 CLI：

    ```sh
    uv run summarize.py \
      --model LiquidAI/LFM2-2.6B-Transcript-GGUF \
      --hf-model-file LFM2-2.6B-Transcript-1-GGUF.gguf \
      --transcript-file transcripts/example_1.txt
    ```

## 工作原理

CLI 使用 llama.cpp 的 Python 绑定自动下载并构建适合你平台的 llama.cpp 二进制，因此无需额外配置。构建版本针对平台优化，可直接在本机使用。

随后使用 `LiquidAI/LFM2-2.6B-Transcript` 模型对转录进行摘要。

```python
model = Llama(
    model_path="LiquidAI/LFM2-2.6B-Transcript-GGUF",
    n_ctx=8192,
    n_threads=4,
    verbose=False,
)
```

生成的 token 会实时流式输出到控制台，因此你能看到摘要逐步生成：

```python
stream = model.create_chat_completion(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": transcript}
    ],
    max_tokens=2048,
    temperature=0.0,
    top_p=0.9,
    stream=True,  # Enable streaming
)

for chunk in stream:
    delta = chunk['choices'][0]['delta']
    if 'content' in delta:
        token = delta['content']
        summary_text += token
        console.print(token, end='', highlight=False)

```

## 下一步

- [ ] 将 CLI 接入两步流水线：先把音频转写成文本，再进行摘要总结。
