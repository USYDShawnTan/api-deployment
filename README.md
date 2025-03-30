# API 部署仓库

这个仓库用于将前端和后端代码自动部署到同一个 Vercel 域名下，前端部署在根路径，后端 API 部署在 `/api` 路径前缀下。

## 自动化部署工作流

本仓库配置了自动化部署流程，当前端或后端仓库更新时会自动触发部署：

1. 前端仓库 (`USYDShawnTan/api-frontend`) 更新时触发部署
2. 后端仓库 (`USYDShawnTan/api-backend`) 更新时触发部署
3. 也可以通过此仓库的 Actions 页面手动触发部署

## 工作流程

1. 当源代码仓库收到推送时，它们会向此仓库发送一个 repository dispatch 事件
2. 此仓库的工作流会响应该事件，拉取最新代码
3. 合并前端和后端代码后部署到 Vercel

## 初始设置

### 添加必要的 Secrets

在此仓库的 Settings -> Secrets and variables -> Actions 中添加以下 secrets:

1. `PAT_TOKEN` - GitHub 个人访问令牌，需要有权访问前端和后端私有仓库
2. `VERCEL_TOKEN` - Vercel API 令牌
3. `MONGODB_URI` - MongoDB 连接字符串，格式如：`mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority`
4. `MONGODB_DB_NAME` - MongoDB 数据库名称，例如：`api_catalog`
5. `API_ACCESS_PASSWORD` - API 访问密码，用于保护 API 端点

这些环境变量在部署过程中会传递给 Vercel，确保后端能够正确连接到 MongoDB 数据库并进行身份验证。

### 前端和后端仓库设置

在前端和后端仓库中，需要添加以下文件和 secret:

1. 在 `.github/workflows/` 目录下添加 `trigger-deployment.yml` 文件
2. 添加 `PAT_TOKEN` secret

## 文件结构

```
api-deployment/
├── .github/
│   └── workflows/
│       └── deploy.yml         # 主部署工作流
├── vercel.json                # Vercel 配置文件
├── .gitignore                 # Git 忽略文件
└── README.md                  # 本说明文件
```

## 验证部署

成功部署后，您应该能够通过以下 URL 访问：

- 前端: `https://api.433200.xyz`
- 后端 API: `https://api.433200.xyz/api/api_data/?password=您的密码`
- 后端其他: `https://api.433200.xyz/api/health`

## 环境变量说明

### 后端环境变量

| 环境变量              | 说明               | 示例值                                                                         |
| --------------------- | ------------------ | ------------------------------------------------------------------------------ |
| `MONGODB_URI`         | MongoDB 连接字符串 | `mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority` |
| `MONGODB_DB_NAME`     | MongoDB 数据库名称 | `api_catalog`                                                                  |
| `API_ACCESS_PASSWORD` | API 访问密码       | `yourSecurePassword`                                                           |
| `NODE_ENV`            | 环境标识           | `production`                                                                   |

### 前端环境变量

前端应用需要知道 API 访问密码来请求数据：

| 环境变量                        | 说明         | 示例值                              |
| ------------------------------- | ------------ | ----------------------------------- |
| `REACT_APP_API_ACCESS_PASSWORD` | API 访问密码 | 与后端的 `API_ACCESS_PASSWORD` 相同 |

