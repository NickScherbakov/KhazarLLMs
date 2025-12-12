# KhazarLLMs 🌟

> 🌐 **语言:** [English](../../README.md) | [العربية](../ar/README.md) | [中文](README.md) | [Русский](../ru/README.md)

**集体创造力管理的LLM集合系统**

> 🌐 **[着陆页](../../docs/i18n/zh/index.html)** | 📚 **[文档 (English)](../../USAGE_GUIDE.md)** | 💻 **[示例](../../examples/)**

受米洛拉德·帕维奇的《哈扎尔辞典》及其对多重视角探索的启发，KhazarLLMs编排具有独特个性和角色的AI智能体集合，协作完成创造性任务。就像《哈扎尔辞典》的复调结构，多种声音讲述相互关联的故事，该系统汇集不同的AI视角，从多个角度探索想法。

## 🎭 理念

在《哈扎尔辞典》中，真理不是从单一视角产生，而是从许多声音的相互作用中产生 - 基督教、伊斯兰教和犹太教来源讲述重叠但不同的故事。类似地，KhazarLLMs相信最具创造性和洞察力的解决方案源于多个AI视角的碰撞和综合，每个都有自己的角色和个性：

- **梦想家** - 生成狂野、无限的创造性愿景
- **批评家** - 以敏锐的洞察力和建设性挑战进行分析
- **综合者** - 将分散的想法编织成连贯的整体
- **哲学家** - 探索深层含义和更广泛的背景
- **反叛者** - 挑战假设并打破常规
- **建筑师** - 将想法结构化并组织成可实现的形式
- **诗人** - 增添美感和情感共鸣

## ✨ 特性

- 🤖 **多个智能体角色** - 每个都有独特的创造性角色和个性
- 🎯 **灵活编排** - 顺序、并行、辩论和共识模式
- 🔄 **迭代改进** - 多轮对话以发展想法
- 💾 **会话管理** - 保存和查看创造性会话
- 🎨 **提供商无关** - 与OpenAI、Anthropic或模拟模式一起工作
- 🛠️ **CLI和Python API** - 通过命令行使用或集成到您的代码中

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/NickScherbakov/KhazarLLMs.git
cd KhazarLLMs

# 安装依赖
pip install -r requirements.txt

# 可选：设置API密钥
cp .env.example .env
# 用您的API密钥编辑.env
```

### 基本用法

```python
import asyncio
from khazar_llms.agents.personas import DreamerAgent, CriticAgent, SynthesizerAgent
from khazar_llms.orchestration.ensemble import Ensemble
from khazar_llms.orchestration.session import CreativeSession

async def main():
    # 创建智能体
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
        SynthesizerAgent(provider="mock"),
    ]
    
    # 创建集合
    ensemble = Ensemble(agents=agents, max_iterations=3)
    
    # 运行创造性会话
    session = CreativeSession(ensemble)
    results = await session.run("设计一种新的沟通形式")
    
    # 查看结果
    for msg in results["conversation"]:
        print(f"{msg.sender}: {msg.content}")

asyncio.run(main())
```

### CLI用法

```bash
# 获取帮助
python -m khazar_llms.cli info

# 列出可用的智能体
python -m khazar_llms.cli list-agents

# 运行创造性任务
python -m khazar_llms.cli create-task "想象一个存在于多个维度的图书馆"

# 使用带特定智能体的并行模式
python -m khazar_llms.cli --mode parallel --agents dreamer rebel poet create-task "创建一种新的乐器"

# 使用真实的LLM提供商
python -m khazar_llms.cli --provider openai create-task "设计未来的教育系统"
```

## 📖 示例

有关详细示例，请参见 `examples/` 目录：

- `basic_ensemble.py` - 基本集合创建和执行
- `parallel_debate.py` - 高级编排模式

运行示例：
```bash
python examples/basic_ensemble.py
python examples/parallel_debate.py
```

## 🏗️ 架构

### 核心组件

1. **智能体** (`khazar_llms/agents/`)
   - 具有记忆和响应逻辑的基础智能体类
   - 具有独特系统提示的专业角色
   - 用于多个提供商的LLM客户端抽象

2. **编排** (`khazar_llms/orchestration/`)
   - 用于协调智能体的集合管理
   - 用于运行和保存协作的会话管理
   - 多种对话模式（顺序、并行、辩论、共识）

3. **工具** (`khazar_llms/utils/`)
   - 具有提供商抽象的LLM客户端
   - 用于无API成本测试的模拟提供商

## 🎨 对话模式

- **顺序** - 智能体依次响应，基于先前的响应
- **并行** - 所有智能体同时响应相同的上下文
- **辩论** - 智能体进行结构化的来回交流
- **共识** - 智能体明确地朝着达成一致和综合努力

## 🧪 开发

### 运行测试

```bash
pytest tests/
```

### 代码格式化

```bash
black khazar_llms/
flake8 khazar_llms/
```

## 🌈 使用案例

- **创意写作** - 从多个叙事视角生成故事
- **产品设计** - 通过不同视角探索产品想法
- **问题解决** - 从多个角度处理复杂问题
- **艺术与诗歌** - 创建多层次的艺术作品
- **哲学** - 通过对话探索哲学问题
- **教育** - 通过多种解释方法学习主题

## 🤝 贡献

欢迎贡献！这个项目是集体AI创造力的实验。随时：

- 添加新的智能体角色
- 实现新的编排模式
- 改进对话动态
- 添加可视化工具
- 创建新示例

有关更多详细信息，请参阅我们的[贡献指南](CONTRIBUTING.md)。

## 🌐 着陆页

该项目的专业着陆页可在 `docs/` 目录中找到。要查看它：

```bash
# 直接在浏览器中打开
open docs/i18n/zh/index.html

# 或使用本地服务器提供服务
cd docs
python -m http.server 8000
# 访问 http://localhost:8000
```

### 部署着陆页

您可以将着陆页部署到GitHub Pages、Netlify或Vercel。有关部署说明，请参阅[docs/README.md](../../docs/README.md)。

## 📜 许可证

MIT许可证 - 有关详细信息，请参阅LICENSE文件

## 🙏 致谢

- 灵感来自米洛拉德·帕维奇的《哈扎尔辞典》
- 建立在出色的LLM提供商的基础上
- 献给所有探索AI集合创造潜力的人

---

*"哈扎尔人是一个从历史中消失的民族，只留下碎片和相互矛盾的记载。从这些碎片中，我们可以想象无限的故事。同样，从不同的AI视角，无限的创造可能性应运而生。"*
