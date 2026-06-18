# Research Proposal: Towards 3D Code Evolution Tensor (TAC-Graph) for Complex Agentic Software Engineering

## 1. Research Motivation (研究动机)

在当前由大型语言模型（LLMs）驱动的 Agentic Software Engineering（如 "Vibe Coding" 范式）中，Coding Agent 已经展示出处理中小型项目的强大能力。对于简单或中等复杂度的代码库，Agent 能够通过基础的代码读取工具（如文件检索、静态分析）快速构建上下文，并实现高效的代码开发与维护。

然而，**随着系统生命周期的延长，代码库不可避免地走向复杂与冗杂**——模块间交互呈指数级增长，新功能与历史包袱（废弃代码、技术债）深度纠缠。在此阶段，现有的 Coding Agent 在面临复杂的新功能注入或深层 Bug 修复时往往会遭遇瓶颈。其核心痛点在于：**传统的代码表征（如 AST 或单纯的文本序列）是静态且扁平的。** 现有的 Agent 缺乏对代码库演进的宏观全局观（Bigger Picture）**和**微观历史细节（Small Picture）的对齐能力。当 Agent 试图理解复杂系统时，目前的通用做法是依赖繁琐的 Tool Calling（如不断读取散落的文件并拼接上下文），这不仅极易导致 LLM 的 Context Window 爆炸，也无法捕捉代码“为什么被写成这样”的时间线索。

因此，建立一种全新的、能够同时追踪整体代码库在空间（拓扑结构）**与**时间（演进历史）上动态变化的表征方式，是让 Coding Agent 从“初级代码工人”走向“资深系统架构师”的必经之路。

## 2. Core Concept: 三维代码演进张量 (3D Code Evolution Tensor)

为了突破上述瓶颈，本研究提出一种全新的动态拓扑表征框架：**TAC-Graph (Temporal-Agentic-Contextual Code Graph)**。其核心思想是将代码开发建模为一个在三维空间中动态演化的张量结构：

### 2.1 维度的定义 (The Three Axes)

* **X轴（横向/时间维）：Git History (Temporal/Evolutionary)**
* **包含内容：** Commits, Bug fixes, Features, Diffs, Branches。
* **物理意义：** 代码的宏观演进历史，代表了系统的“结果”和“里程碑”。


* **Y轴（纵向/行为维）：Agent Trajectory (Behavioral/Agentic)**
* **包含内容：** Agent 的 Thought process (思维链), 读写操作 (Read/Write/Search), Bash 执行记录, Debug 试错轨迹。
* **物理意义：** 代码是如何被写出来的，代表了微观层面开发者的“动作”和“意图”。


* **Z轴（深度/空间维）：Code Structure & DSL (Spatial/Semantic)**
* **包含内容：** 抽象语法树 (AST), 数据流/控制流图 (DFG/CFG), 文件依赖关系, API 调用图。
* **物理意义：** 代码的静态拓扑和语义关联，代表了系统当前的“状态”和“领域知识”。



## 3. Research Methodology & Tasks (研究方法与下游任务)

我们可以将代码库的动态状态严格定义为一个张量 $\mathcal{T} \in \mathbb{R}^{H \times A \times S}$，其中 $H, A, S$ 分别代表历史时间、Agent 轨迹和代码空间结构。基于此框架，本研究将探索以下核心方向：

### 方向一：维度的变换与信息压缩 (Tensor Transformation & Projection)

研究如何在新表征下进行张量降维与跨维度投影：

* **演进与拓扑的融合：** 将 Git History 与 Agent Trajectory 的信息压缩并注入到 Code Structure 中，生成一种“带有历史记忆的 AST”。这使得 Agent 能够原生理解某些“不优雅但为了修复特定历史 Bug 而存在”的祖传代码。
* **跨粒度信息传输：** 在 Graph Transmission 过程中，探索使用 Temporal Graph Neural Networks (T-GNNs) 或 Graph Transformers。重点解决维度间时间粒度不对齐的挑战（如 Agent 的微观动作是秒级的，而宏观 Commit 是天级的）。

### 方向二：下游任务降维打击 (Task Untangling & Optimization)

* **Task Untangling (任务解耦)：** 在实际开发中，开发者常将 Bug 修复与新功能开发混杂在一次提交中。通过分析 TAC-Graph（特别是 Agent 意图轨迹与代码空间结构的交集），可以实现高精度的复杂 Git 提交拆分与解耦。
* **Trajectory Optimization (轨迹剪枝)：** 对比成功的 3D 子图和失败的 3D 子图，提取 Agent 在处理特定缺陷时的高效解决路径，从而指导或剪枝未来 Agent 在高维代码空间中的搜索策略。

## 4. System Implementation & Integration Modalities (落地形态与系统集成)

针对如何将庞大的 TAC-Graph 接入并增强 Coding Agent，本研究提出两种互补的落地系统形态：

### 形态 A：显式结构化检索 (Explicit Querying via Graph-QL for Code)

开发一种基于 TAC-Graph 的领域特定查询语言（DSL，类似于 GraphQL）。

* **机制：** 当 Agent 面对复杂任务时，可以主动调用该查询语言，在 3D 图中精准拉取所需的上下文。
* **优势：** 可解释性极强。Agent 可以明确执行类似 `Query(Target=AuthModule, History=Past_3_BugFixes, Agent_Trace=Failed_Attempts)` 的操作，精准获取“结构上的邻居”、“历史上的修改者”以及“过去踩过的坑”，将其序列化后作为显式 Prompt 输入，避免无效信息污染 Context。

### 形态 B：隐式表征学习映射 (Implicit Representation via Graph-VAE)

针对全量代码库上下文过载的问题，采用表征学习（Representation Learning）的方法将代码库整体“内化”到 Agent 中。

* **机制：** 训练一个图变分自编码器（Graph-VAE）或类似的图表征模型，将庞大且离散的 $\mathcal{T} \in \mathbb{R}^{H \times A \times S}$ 张量映射并压缩为一个低维的连续潜变量空间（Latent Space Embedding）。
* **优势：** 这种类似“知识蒸馏”的方法使得 Agent 无需通过繁琐的文本读取，即可直接加载对应 codebase 的连续向量特征（Soft Prompts / Prefix Tuning）。这种形态不仅绕过了 LLM Token 窗口的物理限制，还能让 Agent 像人类资深工程师一样，对整个代码库的演进脉络产生直觉性（Intuitive）的深层理解。