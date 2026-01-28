# 使用 LFM2-Audio-1.5B 实时语音转文字

[English](README.md) | [中文](README_zh.md)


[![Discord](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)](https://discord.com/invite/liquid-ai)

## 里面有什么？

该示例演示如何结合 llama.cpp 使用 LFM2-Audio-1.5B 模型，在本地实时转写音频文件。

当你把 llama.cpp 的高效与小型音频模型 [LFM2-Audio-1.5B](https://huggingface.co/LiquidAI/LFM2-Audio-1.5B) 的能力结合起来，你可以构建可在以下设备上运行的实时应用：

- 智能手机
- 自动驾驶汽车
- 智能家居设备
- 等等

且无需互联网连接或任何云服务依赖。

端侧智能语音助手是可行的，本仓库只是其中一个构建示例。


## 快速开始

1. 克隆仓库
    ```sh
    git clone https://github.com/Liquid4All/cookbook.git
    cd cookbook/examples/audio-transcription-cli
    ```

2. 如果你的系统尚未安装 uv，请先安装。

    <details>
    <summary>点击查看 uv 安装说明</summary>

    **macOS/Linux:**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    **Windows:**
    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    </details>

<br>

3. 下载一些音频样本
    ```sh
    uv run download_audio_samples.py
    ```

2. 运行转写 CLI，并在控制台查看音频样本的转写结果。

    ```sh
    uv run transcribe --audio './audio-samples/barackobamafederalplaza.mp3' --play-audio
    ```
    通过传入 `--play-audio` 参数，转写时会在后台播放音频。


## 架构说明

这是一个 100% 本地的语音转文字 CLI，依赖 llama.cpp 在你的机器上运行。输入音频和输出文本都不会发送到任何服务器，所有处理均在本机完成。

![](./media/diagram.gif)

Python 代码会自动下载适用于你平台的 llama.cpp 构建版本，因此无需你手动处理。llama.cpp 对音频的支持仍处于实验阶段，且未完全合入主分支。基于此，Liquid AI 团队发布了支持 LFM2-Audio-1.5B 的专用 llama.cpp 构建版本，你需要使用它来运行该 CLI。

> [!NOTE]
> **支持的平台**
> 
> 当前支持：
> - android-arm64
> - macos-arm64
> - ubuntu-arm64
> - ubuntu-x64
> 
> 如果你的平台未被支持，需要等待构建版本发布。

## llama.cpp 对音频模型的支持

[llama.cpp](https://github.com/ggerganov/llama.cpp) 是一个超快、轻量的开源语言模型推理引擎，使用 C++ 编写，可在本地运行 LLM。例如，我们的 Python CLI 就是通过 llama.cpp 提供快速转写，而不是使用 `PyTorch` 或更高层的 `transformers`。

在 [examples.sh](https://github.com/Liquid4All/cookbook/blob/main/examples/audio-transcription-cli/examples.sh) 脚本中，你可以找到 3 个常见场景的 LFM2-Audio-1.5 推理示例：

- 音频转文字（也就是本 CLI 在内部做的事情）：
    ```sh
    # Audio to Speech Recognition (ASR)   
    ./llama-lfm2-audio \
        -m $CKPT/LFM2-Audio-1.5B-Q8_0.gguf \
        --mmproj $CKPT/mmproj-audioencoder-LFM2-Audio-1.5B-Q8_0.gguf \
        -mv $CKPT/audiodecoder-LFM2-Audio-1.5B-Q8_0.gguf \
        -sys "Perform ASR." \
        --audio $INPUT_WAV
    ```

- 文字转语音。
    ```sh
    # Text To Speech (TTS)
    ./llama-lfm2-audio \
        -m $CKPT/LFM2-Audio-1.5B-Q8_0.gguf \
        --mmproj $CKPT/mmproj-audioencoder-LFM2-Audio-1.5B-Q8_0.gguf \
        -mv $CKPT/audiodecoder-LFM2-Audio-1.5B-Q8_0.gguf \
        -sys "Perform TTS." \
        -p "My name is Pau Labarta Bajo and I love AI" \
        --output $OUTPUT_WAV
    ```

- 带语音风格指令的文字转语音
    ```sh
    ./llama-lfm2-audio \
        -m $CKPT/LFM2-Audio-1.5B-Q8_0.gguf \
        --mmproj $CKPT/mmproj-audioencoder-LFM2-Audio-1.5B-Q8_0.gguf \
        -mv $CKPT/audiodecoder-LFM2-Audio-1.5B-Q8_0.gguf \
        -sys "Perform TTS.
        Use the following voice: A male speaker delivers a very expressive and animated speech, with a low-pitch voice and a slightly close-sounding tone. The recording carries a slight background noise." \
        -p "What is your name man?" \
        --output $OUTPUT_WAV
    ```


## 进一步改进

当前解码文本还不够完美，原因是分块重叠以及部分句子在语法上不完整。

为了提升转写质量，可以引入文本清理模型，构建一个本地两步流程用于实时语音识别。

例如，我们可以使用：

- LFM2-Audio-1.5B 进行音频到文本提取
- LFM2-350M 进行文本清理

### 什么是 LFM2-350M？

LFM2-350M 是一个小型文本到文本模型，可用于文本清理等任务。为了在你的具体场景中达到最佳效果，需要优化系统提示词与用户提示词。

一种方式是使用我们正在开发的无代码工具 Leap Workbench，专用于此类任务。

如果你想提前体验，请加入 [Liquid AI Discord 服务器](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)，并进入 [#gpt5-level-slms](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)

## 需要帮助？
加入 Liquid AI Discord 社区并提问。

[![Discord](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)](https://discord.com/invite/liquid-ai)
