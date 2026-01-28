<h1 align="center">Liquid AI Cookbook</h1>
<p align="center"><em>使用 Liquid AI 模型与 Liquid Edge AI 平台构建</em></p>
<p align="center"><a href="./README.md">English</a> | <a href="./README_zh.md">中文</a></p>

<p align="center">
    🌊 <a href="https://docs.liquid.ai/"><b>Liquid 文档</b></a>&nbsp&nbsp | &nbsp&nbsp🤗 <a href="https://huggingface.co/LiquidAI">Hugging Face</a>&nbsp&nbsp | &nbsp&nbsp🚀 <a href="https://leap.liquid.ai">Liquid Edge AI 平台</a>
</p>
<p align="center">
    <a href="https://discord.com/invite/liquid-ai"><img src="https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white" alt="Join Discord"></a>&nbsp&nbsp</a>
</p>


## 欢迎开发者！👋

本仓库包含使用 Liquid AI 开源权重模型（LFM）和开源 LEAP SDK 构建的 **示例**、**教程** 与 **应用**。

无论你是想定制模型、部署到笔记本或端侧设备，还是构建完整应用，都能在这里找到入门资源。

## 术语对照（EN ⇄ 中文）

| English | 中文 |
|---|---|
| fine-tuning | 微调 |
| inference | 推理 |
| structured generation | 结构化生成 |
| tool calling | 工具调用 |
| edge devices | 端侧设备 |

## 你在找什么？🔍

- [本地 AI 应用示例 🤖](#本地-ai-应用示例) 展示 LFM 模型家族的能力。
- [微调笔记本与示例 🎯](./finetuning/README.md) 提升 LFM2 模型在特定场景下的性能。
- [部署到 iOS 与 Android 设备 📱](#部署到-ios-与-android-设备) 使用 LEAP SDK。

- [端到端教程 📚](#端到端教程) 覆盖从数据采集、评估、微调到部署的完整流程。

- [社区构建的示例 🌟](#社区构建的示例) 展示 Liquid AI 模型的更多可能性。

- [每月 60 分钟技术深潜：高效 AI 全面解析](#录播：60-分钟技术深潜高效-ai-全专题) 详见 [Liquid Discord 社区](https://discord.com/invite/liquid-ai)。

## 本地 AI 应用示例

| 名称 | 是什么？ |
|-------|-----------|
| 🧾 [**invoice-parser**](./examples/invoice-parser/README.md) | 使用 LFM2-VL-3B 从发票 PDF 中提取结构化数据的 Python CLI |
| 🎙️ [**audio-transcription-cli**](./examples/audio-transcription-cli/) | 使用 llama.cpp 与 LFM2-Audio-1.5B 进行实时语音转文字的 Python CLI |
| ✈️ [**flight-search-assistant**](./examples/flight-search-assistant/README.md) | 使用具备工具调用的 LFM2.5-1.2B-Thinking 帮你查找并预订机票的 Python CLI |
| 🚗 [**audio-car-cockpit**](./examples/audio-car-cockpit/README.md) | 结合 LFM2.5-Audio-1.5B（TTS/STT）与 LFM2-1.2B-Tool 的语音车载座舱演示，支持本地实时推理 |


## 部署到 iOS 与 Android 设备

[LEAP Edge SDK](https://leap.liquid.ai/docs/edge-sdk/overview) 是我们用于在移动设备上运行 LFM2 模型的原生框架。

Edge SDK 为 Android（Kotlin）与 iOS（Swift）编写，目标是让小语言模型部署像调用云端 LLM API 一样简单，面向所有应用开发者。

### Android

| 示例 | 描述 |
|---------|-------------|
| [LeapChat](https://github.com/Liquid4All/LeapSDK-Examples/tree/main/Android/LeapChat) | 具备实时 token 流、持久消息记录与现代聊天 UI（气泡与输入指示）的综合聊天应用 |
| [SloganApp](./examples/leap-slogan-example-ios/README.md) | 单轮营销文案生成。UI 使用 Android Views 实现。 |
| [ShareAI](https://github.com/Liquid4All/LeapSDK-Examples/tree/main/Android/ShareAI) | 网站摘要生成器 |
| [Recipe Generator](https://github.com/Liquid4All/LeapSDK-Examples/tree/main/Android/RecipeGenerator) | 使用 LEAP SDK 的结构化输出生成 |
| [Visual Language Model example](https://github.com/Liquid4All/LeapSDK-Examples/tree/main/Android/VLMExample) | 视觉语言模型示例 |

### iOS

| 示例 | 描述 |
|---------|-------------|
| [LeapChat](https://github.com/Liquid4All/LeapSDK-Examples/tree/main/iOS/LeapChatExample) | 展示 LeapSDK 高级特性的综合聊天应用，包括实时流式输出、对话管理与现代 UI 组件。 |
| [LeapSloganExample](https://github.com/Liquid4All/LeapSDK-Examples/tree/main/iOS/LeapChatExample) | 用于文本生成的基础 LeapSDK 集成示例，SwiftUI 应用。 |
| [Recipe Generator](https://github.com/Liquid4All/LeapSDK-Examples/tree/main/iOS/RecipeGenerator) | 结构化输出生成 |
| [Audio demo](https://github.com/Liquid4All/LeapSDK-Examples/tree/main/iOS/LeapAudioDemo) | 使用 LeapSDK 进行端侧 AI 推理的音频输入/输出 SwiftUI 示例。 |



## 端到端教程

从设置到部署的完整端到端教程。

| 教程 | 仓库 |
|----------|------------|
| 端侧设备上超快且高精度的图像分类 | [▶️ 前往仓库](https://github.com/Paulescu/image-classification-with-local-vlms) ![GitHub Repo stars](https://img.shields.io/github/stars/Paulescu/image-classification-with-local-vlms) |
| 使用小型本地大语言模型构建国际象棋游戏 | [▶️ 前往仓库](https://github.com/Paulescu/chess-game) ![GitHub Repo stars](https://img.shields.io/github/stars/Paulescu/chess-game) |


## 社区构建的示例

展示 Liquid 模型实际应用的成品项目。

| 项目 | 仓库 |
|---------|------------|
| TranslatorLens：离线翻译相机 | [▶️ 前往仓库](https://github.com/linmx0130/TranslatorLens) ![GitHub Repo stars](https://img.shields.io/github/stars/linmx0130/TranslatorLens) |
| Food Images Fine-tuning | [▶️ 前往仓库](https://github.com/benitomartin/food-images-finetuning) ![GitHub Repo stars](https://img.shields.io/github/stars/benitomartin/food-images-finetuning) |
| Meeting Intelligence CLI | [▶️ 前往仓库](https://github.com/chintan-projects/meeting-prompter) ![GitHub Repo stars](https://img.shields.io/github/stars/chintan-projects/meeting-prompter) |
| Private Doc Q&A：结合 RAG 与语音输入的端侧文档问答 | [▶️ 前往仓库](https://github.com/chintan-projects/private-doc-qa) ![GitHub Repo stars](https://img.shields.io/github/stars/chintan-projects/private-doc-qa) |
| Photo Triage Agent：使用 LFM 视觉模型清理私有照片库 | [▶️ 前往仓库](https://github.com/chintan-projects/photo-triage-agent) ![GitHub Repo stars](https://img.shields.io/github/stars/chintan-projects/photo-triage-agent) | 
| LFM-Scholar：可检索与引用论文的自动化文献综述代理 | [▶️ 前往仓库](https://github.com/gyunggyung/LFM-Scholar) ![GitHub Repo stars](https://img.shields.io/github/stars/gyunggyung/LFM-Scholar) |
| LFM2-KoEn-Tuning：面向韩英翻译的 LFM2 1.2B 微调模型 | [▶️ 前往仓库](https://github.com/gyunggyung/LFM2-KoEn-Tuning) ![GitHub Repo stars](https://img.shields.io/github/stars/gyunggyung/LFM2-KoEn-Tuning) |
| Private Summarizer：100% 本地文本摘要，支持多语言 | [▶️ 前往仓库](https://github.com/Private-Intelligence/private_summarizer) ![GitHub Repo stars](https://img.shields.io/github/stars/Private-Intelligence/private_summarizer) |

## 录播：60 分钟技术深潜（高效 AI 全专题）

| 日期 | 主题 |
|---------|------------|
| 2025-11-06 | [▶️ 微调 LFM2-VL 用于图像分类](https://www.youtube.com/watch?v=00IK9apncCg) |
| 2025-11-27 | [▶️ 使用 LFM2-Audio 构建 100% 本地语音转文字 CLI](https://www.youtube.com/watch?v=yeu077gPmCA) |
| 2025-12-26 | [▶️ 使用 GRPO 与 OpenEnv 微调 LFM2-350M 用于浏览器控制](https://www.youtube.com/watch?v=gKQ08yee3Lw) |
| 2026-01-22 | [▶️ 基于 LFM2.5-VL-1.6B 与 WebGPU 的本地视频字幕生成](https://www.youtube.com/watch?v=xsWARHFoA3E) |


想参与下一场活动？加入 [Liquid Discord 社区](https://discord.com/invite/liquid-ai) 并进入 `#live-events` 频道！

## 贡献

欢迎贡献！

- 在 `社区构建的示例` 部分提交 PR 并附上你的项目 GitHub 仓库链接。


## 支持 💬

- 📖 [Liquid AI 文档](https://docs.liquid.ai/)
- 💬 [加入我们的 Discord 社区](https://discord.com/invite/liquid-ai)
