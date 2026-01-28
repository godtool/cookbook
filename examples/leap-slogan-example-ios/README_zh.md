# 口号生成 iOS 应用

[English](README.md) | [中文](README_zh.md)


[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github)](https://github.com/Liquid4All/LeapSDK-Examples/tree/main/iOS/LeapSloganExample)

[![Discord](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)](https://discord.com/invite/liquid-ai)

一个简单的 iOS 应用，使用本地 AI 模型生成创意口号，无需互联网连接。

## 里面有什么？

在这个示例中，你将学习如何：
- 将 LeapSDK 集成到 iOS 项目中
- 在 iPhone 或 iPad 上本地加载并运行 AI 模型
- 实现实时流式文本生成

## 你将学到什么

在本指南结束时，你将了解：

- 如何将 LeapSDK 集成到 iOS 项目中
- 如何在 iPhone 或 iPad 上本地加载并运行 AI 模型
- 如何实现实时流式文本生成

## 架构说明

在编写代码之前，先了解我们要构建的内容。LeapSlogan 应用采用清晰的三层架构：

```
┌─────────────────────────────────┐
│      SwiftUI View Layer         │ ← 用户界面
│  (ContentView, UI Components)   │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│     ViewModel Layer             │ ← 业务逻辑
│  (SloganViewModel, @Observable) │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│      LeapSDK Layer              │ ← AI 推理
│  (ModelRunner, Conversation)    │
└─────────────────────────────────┘
```

来追踪一下用户生成口号时发生的过程：

```
1. 用户输入 "coffee shop" 并点击 Generate
   ↓
2. UI 禁用输入并显示 "Generating..."
   ↓
3. ViewModel 根据业务类型生成提示词
   ↓
4. ChatMessage 发送到 Conversation
   ↓
5. LeapSDK 开始模型推理
   ↓
6. Token 逐个流式返回
   ├─ "Wake" → UI 更新
   ├─ " up" → UI 更新
   ├─ " to" → UI 更新
   ├─ " flavor" → UI 更新
   └─ "!" → UI 更新
   ↓
7. 触发 .complete 事件
   ↓
8. UI 恢复可输入状态，显示最终口号
```

让我们开始构建应用吧！

## 环境准备

你需要：

- **Xcode 15.0+**，Swift 5.9 或更高
- **iOS 15.0+** 作为部署目标
- **真机 iOS 设备**（iPhone 或 iPad），性能最佳
  - *iOS 模拟器可用，但会明显更慢*
- 对 **SwiftUI** 与 Swift 的 async/await 有基本了解


## 步骤 1：创建新的 Xcode 项目

1. 打开 Xcode，创建一个新的 iOS App
2. 界面选择 **SwiftUI**
3. 最低部署版本设置为 **iOS 15.0**

## 步骤 2：通过 Swift Package Manager 添加 LeapSDK

LeapSDK 以 Swift Package 形式发布，集成非常方便：

1. 在 Xcode 中选择 **File → Add Package Dependencies**
2. 输入仓库地址：
   ```
   https://github.com/Liquid4All/leap-ios.git
   ```
3. 选择最新版本（0.6.0 或更新）
4. 将 **两个** Product 添加到 target：
   - ✅ `LeapSDK`
   - ✅ `LeapSDKTypes`

> **重要**：从 0.5.0 开始，必须同时添加 `LeapSDK` 和 `LeapSDKTypes`，确保运行时正确链接。

## 步骤 3：下载模型包

现在我们需要一个 AI 模型。LeapSDK 使用 **model bundle**（包含模型与配置的打包文件）：

1. 访问 [Leap 模型库](https://leap.liquid.ai/models)
2. 本教程推荐下载小模型如 **LFM2-350M**（适合移动端，约 500MB）
3. 下载对应的 `.bundle` 文件
4. 将 `.bundle` 文件拖入 Xcode 项目
5. ✅ 确认勾选 "Add to target"

你的项目结构应如下所示：
```
YourApp/
├── YourApp.swift
├── ContentView.swift
├── Models/
│   └── LFM2-350M-8da4w_output_8da8w-seq_4096.bundle  ← 你的模型
└── Assets.xcassets
```

## 步骤 4：构建 ViewModel

ViewModel 是应用的核心，负责管理模型生命周期与生成逻辑。我们按步骤来实现。

### 步骤 4.1：创建基础结构

创建一个名为 `SloganViewModel.swift` 的新 Swift 文件：

```swift
import Foundation
import SwiftUI
import LeapSDK
import Observation

@Observable
class SloganViewModel {
    // MARK: - Published State
    var isModelLoading = true
    var isGenerating = false
    var generatedSlogan = ""
    var errorMessage: String?
    
    // MARK: - Private Properties
    private var modelRunner: ModelRunner?
    private var conversation: Conversation?
    
    // MARK: - Initialization
    init() {
        // Model will be loaded when view appears
    }
}
```

**这里发生了什么？**
- `@Observable` 是 Swift 的新观察宏（iOS 17+，在 iOS 15 上也有回溯支持）
- 我们追踪四个 UI 状态：加载、生成、口号文本以及错误信息
- `ModelRunner` 和 `Conversation` 为私有属性——它们是 LeapSDK 对象

### 步骤 4.2：实现模型加载

添加模型加载函数：

```swift
// MARK: - Model Management
@MainActor
func setupModel() async {
    isModelLoading = true
    errorMessage = nil
    
    do {
        // 1. Get the model bundle URL from app bundle
        guard let modelURL = Bundle.main.url(
            forResource: "qwen-0.6b",  // Change to match your bundle name
            withExtension: "bundle"
        ) else {
            errorMessage = "Model bundle not found in app bundle"
            isModelLoading = false
            return
        }
        
        // 2. Load the model using LeapSDK
        print("Loading model from: \(modelURL.path)")
        modelRunner = try await Leap.load(url: modelURL)
        
        // 3. Create an initial conversation
        conversation = Conversation(
            modelRunner: modelRunner!,
            history: []
        )
        
        isModelLoading = false
        print("Model loaded successfully!")
        
    } catch {
        errorMessage = "Failed to load model: \(error.localizedDescription)"
        isModelLoading = false
        print("Error loading model: \(error)")
    }
}
```

**代码解读：**

1. **Bundle 查找**：在应用资源中找到模型包
2. **异步加载**：`Leap.load()` 是异步的，因为模型加载需要时间（1-5 秒）
3. **创建对话**：每次生成都需要一个 `Conversation` 记录历史
4. **错误处理**：捕获并展示加载失败信息

> **💡 提示**：模型加载是最耗时的部分。生产应用中建议提供更友好的加载界面！

### 步骤 4.3：实现口号生成

现在进入最有趣的部分——生成口号！添加如下函数：

```swift
// MARK: - Generation
@MainActor
func generateSlogan(for businessType: String) async {
    // Guard against invalid states
    guard let conversation = conversation,
          !isGenerating else { return }
    
    isGenerating = true
    generatedSlogan = ""  // Clear previous slogan
    errorMessage = nil
    
    // 1. Create the prompt
    let prompt = """
    Create a catchy, memorable slogan for a \(businessType) business. \
    Make it creative, concise, and impactful. \
    Return only the slogan, nothing else.
    """
    
    // 2. Create a chat message
    let userMessage = ChatMessage(
        role: .user,
        content: [.text(prompt)]
    )
    
    // 3. Generate response with streaming
    let stream = conversation.generateResponse(message: userMessage)
    
    // 4. Process the stream
    do {
        for await response in stream {
            switch response {
            case .chunk(let text):
                // Append each text chunk as it arrives
                generatedSlogan += text
                
            case .reasoningChunk(let reasoning):
                // Some models output reasoning - we can log it
                print("Reasoning: \(reasoning)")
                
            case .complete(let usage, let completeInfo):
                // Generation finished!
                print("✅ Generation complete!")
                print("Tokens used: \(usage.totalTokens)")
                print("Speed: \(completeInfo.stats?.tokenPerSecond ?? 0) tokens/sec")
                isGenerating = false
            }
        }
    } catch {
        errorMessage = "Generation failed: \(error.localizedDescription)"
        isGenerating = false
    }
}
```

**流式 API 解析：**

`generateResponse()` 返回一个 **AsyncStream**，会产生三类事件：

1. **`.chunk(text)`**：逐段生成的文本
   - 让 UI 看起来即时响应
   - 文本像 ChatGPT 一样逐词出现
   
2. **`.reasoningChunk(reasoning)`**：部分模型会输出“思考过程”
   - 适用于支持推理展示的模型
   
3. **`.complete(usage, info)`**：生成结束事件
   - 包含 token 使用统计
   - 包含性能指标（tokens/second）


## 步骤 5：构建用户界面

现在创建一个美观、可交互的 UI。创建或修改 `ContentView.swift`：

```swift
import SwiftUI

struct ContentView: View {
    @State private var viewModel = SloganViewModel()
    @State private var businessType = ""
    
    var body: some View {
        NavigationStack {
            ZStack {
                // Background gradient
                LinearGradient(
                    colors: [.blue.opacity(0.1), .purple.opacity(0.1)],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()
                
                VStack(spacing: 24) {
                    if viewModel.isModelLoading {
                        modelLoadingView
                    } else {
                        mainContentView
                    }
                }
                .padding()
            }
            .navigationTitle("AI Slogan Generator")
            .navigationBarTitleDisplayMode(.large)
        }
        .task {
            // Load model when view appears
            await viewModel.setupModel()
        }
    }
    
    // MARK: - Subviews
    
    private var modelLoadingView: some View {
        VStack(spacing: 20) {
            ProgressView()
                .scaleEffect(1.5)
            Text("Loading AI Model...")
                .font(.headline)
            Text("This may take a few seconds")
                .font(.caption)
                .foregroundColor(.secondary)
        }
    }
    
    private var mainContentView: some View {
        VStack(spacing: 24) {
            // Error message if any
            if let error = viewModel.errorMessage {
                errorBanner(error)
            }
            
            // Instructions
            instructionsCard
            
            // Input field
            businessTypeInput
            
            // Generate button
            generateButton
            
            // Generated slogan display
            if !viewModel.generatedSlogan.isEmpty {
                sloganResultCard
            }
            
            Spacer()
        }
    }
    
    private var instructionsCard: some View {
        VStack(alignment: .leading, spacing: 12) {
            Label("How it works", systemImage: "lightbulb.fill")
                .font(.headline)
                .foregroundColor(.blue)
            
            Text("Enter a business type and I'll generate a creative slogan using AI—completely on your device!")
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color.blue.opacity(0.1))
        .cornerRadius(12)
    }
    
    private var businessTypeInput: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Business Type")
                .font(.subheadline)
                .fontWeight(.semibold)
            
            TextField("e.g., coffee shop, tech startup, bakery", text: $businessType)
                .textFieldStyle(.roundedBorder)
                .autocapitalization(.none)
                .disabled(viewModel.isGenerating)
        }
    }
    
    private var generateButton: some View {
        Button(action: {
            Task {
                await viewModel.generateSlogan(for: businessType)
            }
        }) {
            HStack {
                if viewModel.isGenerating {
                    ProgressView()
                        .tint(.white)
                } else {
                    Image(systemName: "sparkles")
                }
                
                Text(viewModel.isGenerating ? "Generating..." : "Generate Slogan")
                    .fontWeight(.semibold)
            }
            .frame(maxWidth: .infinity)
            .padding()
            .background(
                businessType.isEmpty || viewModel.isGenerating 
                    ? Color.gray 
                    : Color.blue
            )
            .foregroundColor(.white)
            .cornerRadius(12)
        }
        .disabled(businessType.isEmpty || viewModel.isGenerating)
    }
    
    private var sloganResultCard: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Label("Your Slogan", systemImage: "quote.bubble.fill")
                    .font(.headline)
                    .foregroundColor(.purple)
                
                Spacer()
                
                // Copy button
                Button(action: {
                    UIPasteboard.general.string = viewModel.generatedSlogan
                }) {
                    Image(systemName: "doc.on.doc")
                        .foregroundColor(.blue)
                }
            }
            
            Text(viewModel.generatedSlogan)
                .font(.title3)
                .fontWeight(.medium)
                .foregroundColor(.primary)
                .padding()
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Color.purple.opacity(0.1))
                .cornerRadius(8)
        }
        .padding()
        .background(Color.white)
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 5, y: 2)
    }
    
    private func errorBanner(_ message: String) -> some View {
        HStack {
            Image(systemName: "exclamationmark.triangle.fill")
            Text(message)
                .font(.caption)
            Spacer()
        }
        .padding()
        .background(Color.red.opacity(0.1))
        .foregroundColor(.red)
        .cornerRadius(8)
    }
}

#Preview {
    ContentView()
}
```

**UI 设计亮点：**

1. **渐进式展示**：加载界面 → 主界面
2. **清晰的视觉反馈**：加载状态、禁用状态、动画
3. **友好引导**：用户一看就知道怎么用
4. **细节打磨**：渐变背景、阴影、圆角
5. **复制功能**：轻松复制生成口号


## 常见问题排查

### 问题 1："Model bundle not found"

**解决方案**：
- 检查 `.bundle` 文件是否已加入 Xcode 项目
- 确认 "Target Membership" 已勾选
- 确保代码中的 bundle 名称与实际文件名一致

### 问题 2："Failed to load model"

**解决方案**：
- 使用真机测试（模拟器不稳定）
- 确保 iOS 版本 15.0+
- 确保设备有足够存储空间（约模型大小的 2-3 倍）
- 先尝试更小的模型

### 问题 3：生成速度慢

**解决方案**：
- 使用真机（比模拟器快 10-100 倍）
- 选择更小模型（350M-1B）
- 在 GenerationOptions 中降低 `maxTokens`
- 降低温度以获得更快但更保守的输出

### 问题 4：应用启动即崩溃

**解决方案**：
- 确保添加了 `LeapSDK` 和 `LeapSDKTypes`
- 检查框架设置为 "Embed & Sign"
- 清理构建缓存（Cmd+Shift+K）
- 重启 Xcode


## 下一步

恭喜！🎉 你已经构建了一个完整的端侧 AI 应用。下面是一些拓展思路：

### 近期可做的项目

1. **LeapChat**：构建带历史记录的完整聊天界面
   - 参考 [LeapChatExample](https://github.com/Liquid4All/LeapSDK-Examples/tree/main/iOS/LeapChatExample)
   
2. **加入结构化输出**：使用 `@Generatable` 宏
   - 生成 JSON 数据结构
   - 在编译期校验输出格式

3. **实现函数调用**：让 AI 调用你的函数
   - 天气查询、计算、数据库查询
   - 参考 [函数调用指南](https://leap.liquid.ai/docs/edge-sdk/ios/function-calling)


## 需要帮助？

加入 [Liquid AI Discord 社区](https://discord.com/invite/liquid-ai) 并提问。
[![Discord](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)](https://discord.com/invite/liquid-ai)
