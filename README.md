# 项目简介

这是一个简书服务监控工具，包含了日志记录、消息推送模块，可以进行监控任务的增删。

# 部署

## Docker Compose

您需要启动一个 MongoDB 服务，端口号为 27017

运行以下 Docker 命令：

```bash
docker network create mongodb
docker run -d -p 27017:27017 --net mongodb mongo:5.0.9
```

使用以下命令启动服务：

```bash
docker compose up -d
```

## 手动部署

您需要启动一个 MongoDB 服务，端口号为 27017，并修改 `config.yaml` 文件，将 `db_address` 改为 `localhost`。

可以使用 Poetry 安装依赖库：

```bash
poetry install --no-dev
```

或者从 `requirements.txt` 安装依赖：

```bash
pip install -r requirements.txt
```

使用以下命令启动服务：

```bash
python main.py
```
