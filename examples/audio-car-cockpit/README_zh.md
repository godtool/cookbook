# 使用 LFM2.5-Audio-1.5B 与 LFM2-1.2B-Tool 的语音与工具调用

[English](README.md) | [中文](README_zh.md)


[![Discord](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)](https://discord.com/invite/liquid-ai)

## 里面有什么？

在一个汽车座舱的模拟界面中，将 [LFM2.5-Audio-1.5B](https://huggingface.co/LiquidAI/LFM2.5-Audio-1.5B-GGUF)（TTS 和 STT 模式）与 [LFM2-1.2B-Tool](https://huggingface.co/LiquidAI/LFM2-1.2B-Tool-GGUF) 结合，让用户通过语音控制车辆功能。  
全部实时本地运行。

https://github.com/user-attachments/assets/f9b5a6fd-ed3b-4235-a856-6251441a1ada

两个模型都使用 [Llama.cpp](https://github.com/ggml-org/llama.cpp) 推理，音频模型使用自定义运行器。车载座舱（UI）使用原生 js+html+css，后端通信通过 websocket 消息完成，类似简化版的 [车载 CAN 总线](https://en.wikipedia.org/wiki/CAN_bus)。

## 快速开始

> [!NOTE]
> **支持的平台**
> 
> 当前支持：
> - macos-arm64
> - ubuntu-arm64
> - ubuntu-x64

使用方式：
```bash
# Setup python env
make setup

# Optional, if you have already llama-server in your path, you can
# symlink instead of building it
# ln -s $(which llama-server) llama-server

# Prepare the audio and tool calling models
make LFM2.5-Audio-1.5B-GGUF LFM2-1.2B-Tool-GGUF

# Launch demo
make -j2 audioserver serve
```
