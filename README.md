# LangChain智能体应用

这是一个基于LangChain的智能体应用，使用Flask作为前端，支持对接第三方模型和输入提示词。

## 功能特点

- **模型配置**：支持配置API地址、API密钥、模型名称、温度等参数
- **长上下文交互**：支持与AI进行长上下文的对话交互
- **Markdown渲染**：支持实时渲染Markdown格式的回复
- **流式输出**：AI回复以流式方式逐字显示，提升用户体验
- **抽屉式配置面板**：可收起/展开的配置面板，节省空间
- **Docker部署**：支持使用Docker容器运行，方便快速部署

## 技术栈

- **后端**：Python、Flask、LangChain
- **前端**：HTML、Tailwind CSS、JavaScript
- **部署**：Docker、Docker Compose

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/jerrynbc/agent_base.git
cd agent_base
```

### 2. 构建和运行

使用Docker Compose构建和运行应用：

```bash
docker-compose build
docker-compose up
```

### 3. 访问应用

在浏览器中访问：http://localhost:5003

## 配置说明

1. **API地址**：输入第三方模型的API地址，如https://api.openai.com/v1
2. **API密钥**：输入访问API所需的密钥
3. **模型**：输入模型名称，如gpt-3.5-turbo、doubao-seed-1.6等
4. **温度**：设置生成文本的随机性，范围0-2
5. **最大令牌数**：设置生成文本的最大长度
6. **系统提示词**：设置AI的系统提示词，定义AI的角色和行为

## 项目结构

```
base_agent/
├── src/
│   ├── app.py          # Flask应用主文件
│   ├── agent.py        # LangChain智能体实现
│   └── config.py       # 配置文件
├── templates/
│   └── index.html      # 前端界面
├── requirements.txt    # 依赖文件
├── Dockerfile          # Docker构建文件
└── docker-compose.yml  # Docker编排配置
```

## 开发说明

由于使用了卷挂载，修改代码后无需重新构建镜像即可看到更改效果。

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License