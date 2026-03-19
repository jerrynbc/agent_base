# Docker 构建与部署指南

本文档总结了构建和部署 Docker 容器的经验，帮助您在不同环境中快速构建和运行应用。

## 一、Dockerfile 构建经验

### 1. 基础镜像选择
- **选择轻量级基础镜像**：使用 `python:3.11-slim` 等轻量级镜像，减少镜像体积
- **使用镜像加速源**：使用 `docker.1ms.run` 等加速源，提高拉取速度
- **指定具体版本**：避免使用 `latest` 标签，确保构建的可重复性

### 2. 系统依赖安装
- **按需安装依赖**：只安装应用必需的系统依赖
- **清理缓存**：安装后删除 `apt` 缓存，减少镜像体积
- **合并命令**：使用 `&&` 合并多个命令，减少镜像层数

### 3. 项目文件复制
- **合理组织文件**：根据项目结构合理安排复制顺序
- **使用 .dockerignore**：创建 `.dockerignore` 文件，排除不需要复制的文件（如 `venv`、`.git` 等）

### 4. Python 依赖安装
- **使用 --no-cache-dir**：避免缓存包，减少镜像体积
- **使用 requirements.txt**：统一管理依赖，确保版本一致性
- **考虑使用虚拟环境**：在容器内创建虚拟环境，隔离依赖

### 5. 环境变量配置
- **设置必要的环境变量**：如 `COZE_PROJECT_TYPE` 等
- **使用 .env 文件**：对于敏感信息，使用环境变量文件管理

### 6. 启动命令定义
- **指定明确的启动命令**：如 `python src/main.py -m http -p 5000`
- **使用 CMD 而非 ENTRYPOINT**：提供更大的灵活性

## 二、docker-compose 配置经验

### 1. 服务配置
- **合理设置服务名称**：使用有意义的服务名称
- **指定构建上下文**：如 `build: .`
- **配置端口映射**：根据需要映射容器端口到主机

### 2. 网络配置
- **使用默认网络**：对于简单应用，使用 docker-compose 默认网络
- **配置自定义网络**：对于复杂应用，创建自定义网络

### 3. 卷挂载
- **挂载代码目录**：如 `- .:/app`，方便开发时修改代码
- **挂载数据卷**：对于需要持久化的数据，使用数据卷

### 4. 环境变量
- **在 docker-compose.yml 中设置环境变量**：如 `COZE_PROJECT_TYPE=agent`
- **使用环境变量文件**：通过 `env_file` 指定环境变量文件

## 三、构建与运行命令

### 1. 构建镜像
```bash
# 使用 docker build 命令构建镜像
docker build -t prd_agent .

# 使用 docker-compose 构建
docker-compose build
```

### 2. 运行容器
```bash
# 使用 docker run 命令运行容器
docker run -p 5001:5000 --env COZE_PROJECT_TYPE=agent prd_agent

# 使用 docker-compose 运行
docker-compose up

# 后台运行
docker-compose up -d
```

### 3. 停止和删除容器
```bash
# 停止容器
docker-compose down

# 停止并删除镜像
docker-compose down --rmi all
```

## 四、常见问题与解决方案

### 1. 端口占用
- **问题**：容器端口映射失败，提示端口已被占用
- **解决方案**：修改 `docker-compose.yml` 中的端口映射，使用未被占用的端口

### 2. 网络连接问题
- **问题**：构建时无法拉取镜像或安装依赖
- **解决方案**：
  - 使用镜像加速源
  - 配置代理：`export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890`

### 3. 依赖安装失败
- **问题**：pip 安装依赖时失败
- **解决方案**：
  - 检查网络连接
  - 确保 requirements.txt 中的依赖版本兼容
  - 尝试使用国内 pip 源

### 4. 容器启动失败
- **问题**：容器启动后立即退出
- **解决方案**：
  - 查看容器日志：`docker logs <container_id>`
  - 检查启动命令是否正确
  - 确保依赖已正确安装

## 五、最佳实践

### 1. 镜像优化
- **多层构建**：使用多阶段构建减少最终镜像体积
- **清理缓存**：定期清理无用的镜像和容器
- **使用 Alpine 镜像**：对于更轻量级的应用，使用 Alpine 基础镜像

### 2. 安全性
- **避免使用 root 用户**：在容器中创建非 root 用户
- **定期更新基础镜像**：及时更新基础镜像以修复安全漏洞
- **扫描镜像**：使用工具扫描镜像中的安全漏洞

### 3. 部署策略
- **使用 CI/CD**：集成 CI/CD 流程，自动化构建和部署
- **使用容器编排工具**：对于生产环境，使用 Kubernetes 等容器编排工具
- **监控和日志**：配置容器监控和日志收集

### 4. 开发与生产环境
- **分离开发和生产配置**：使用不同的配置文件
- **使用环境变量**：通过环境变量区分不同环境
- **测试环境**：在部署到生产环境前，在测试环境验证

## 六、本项目构建示例

### 1. Dockerfile
```dockerfile
FROM docker.1ms.run/python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV COZE_PROJECT_TYPE=agent

# 定义启动命令
CMD ["python", "src/main.py", "-m", "flow"]
```

### 2. docker-compose.yml
```yaml
services:
  prd_agent:
    build: .
    ports:
      - "5001:5000"
    environment:
      - COZE_PROJECT_TYPE=agent
    volumes:
      - .:/app
    command: python src/main.py -m http -p 5000
```

### 3. 构建和运行步骤
1. **构建镜像**：`docker-compose build`
2. **启动容器**：`docker-compose up`
3. **访问服务**：http://localhost:5001/health
4. **停止容器**：`docker-compose down`

## 七、总结

通过合理的 Dockerfile 设计和 docker-compose 配置，可以快速构建和部署应用，提高开发和部署效率。在不同环境中，只需复制 Dockerfile 和 docker-compose.yml 文件，即可快速构建和运行应用，实现环境的一致性和可移植性。