# 语音聊天

[English](README.md) | [中文](README_zh.md)


一个使用 LFM2-Audio-1.5B 模型生成对话音频回复的语音聊天应用。

该应用本可 100% 本地运行，但 liquid-audio 库需要 CUDA。因此模型被封装在 Modal 函数中并部署到带 CUDA 的无服务器 GPU 环境中，这样即使你（和我一样）家里没有 NVIDIA GPU，也能运行。录下你的声音，发送处理，并自动播放返回的语音回复。

## 本示例包含什么？

本示例展示如何构建一个交互式语音聊天应用，使用：

- **音频录制**：通过麦克风录音，并自动检测静音停止
- **云端处理**：使用 Modal 在云端 GPU 上运行 LFM2-Audio-1.5B
- **音频播放**：自动播放生成的语音回复

应用工作流程：
1. 从麦克风录制你的语音问题（静音自动停止）
2. 将音频上传到 Modal volume
3. 在 GPU 实例上使用 LFM2-Audio-1.5B 处理音频，生成交错的文本与音频响应
4. 下载生成的音频响应
5. 通过扬声器播放响应

模型生成的回复可以同时包含文本与音频 token，从而带来更自然的对话体验。

## 工具

本示例使用以下工具和库：

- **[liquid-audio](https://github.com/LiquidAI/liquid-audio)**：用于 LFM2-Audio 模型的 Python 库
- **[Modal](https://modal.com/)**：运行 GPU 任务的无服务器云平台
- **[PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)**：跨平台麦克风录音 I/O 库
- **[pygame](https://www.pygame.org/)**：音频播放库
- **[torchaudio](https://pytorch.org/audio/)**：PyTorch 音频处理工具
- **[rich](https://rich.readthedocs.io/)**：用于音频可视化的终端格式化库

## 如何运行

### 前置条件

1. 安装 [uv](https://github.com/astral-sh/uv)：
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. 配置 Modal：
   - 在 [modal.com](https://modal.com) 创建账号
   - 安装 Modal CLI：`uv add modal`
   - 认证：`uv run modal token new`

3. 确保终端/IDE 已获得麦克风权限

### 运行应用

1. **部署服务端**（首次或服务端代码变更时）：
   ```bash
   make deploy-server
   ```
   或直接运行：
   ```bash
   uv run modal deploy -m src.voice_chat.server
   ```

2. **运行客户端**：
   ```bash
   make run
   ```
   或直接运行：
   ```bash
   uv run modal run -m src.voice_chat.client
   ```

3. **按提示操作**：
   - 应用启动后会开始录音
   - 对着麦克风说出你的问题
   - 静音 2 秒后录音自动停止
   - 音频上传到 Modal 并处理
   - 自动下载并播放生成的语音回复

每次会话生成的音频文件会保存为本地 `answer_YYYYMMDD_HHMMSS.wav`。
