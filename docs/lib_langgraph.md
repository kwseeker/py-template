# LangGraph

[LangGraph](https://langchain-ai.github.io/langgraph/) 是 LangChain 的一个扩展，是一个低级编排框架，用于构建、管理和部署长时间运行的有状态的 Agent；基于 LangChain 构建，为构建基于 LLM 的有状态、多代理应用程序提供了一个全新的范式和强大的框架支持。

LangGraph 借鉴了 **分布式系统中状态机与图计算模型** 的思想，将 AI Agent 的行为抽象成一个 **有向图（Directed Graph）**，每个节点是一个函数或模块，边代表状态转移。

## 1 参考

+ [为什么要用LangGraph](https://2048.csdn.net/68494bb97e10b149bf1f6cd4.html)
