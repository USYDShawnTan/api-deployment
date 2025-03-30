# API 部署仓库

这个仓库用于将前端和后端代码自动部署到同一个 Vercel 域名下，前端部署在根路径，后端 API 部署在 `/api` 路径前缀下。

## 自动化部署工作流

本仓库配置了自动化部署流程，当前端或后端仓库更新时会自动触发部署：

1. 前端仓库 (`USYDShawnTan/api-frontend`) 更新时触发部署
2. 后端仓库 (`USYDShawnTan/api-backend`) 更新时触发部署
3. 也可以通过此仓库的 Actions 页面手动触发部署，自动也行

## 工作流程

1. 当源代码仓库收到推送时，它们会向此仓库发送一个 repository dispatch 事件
2. 此仓库的工作流会响应该事件，拉取最新代码
3. 合并前端和后端代码后部署到 Vercel

## 仓库结构

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

API_ACCESS_PASSWORD

BACKEND_REPO

FRONTEND_REPO

MONGODB_DB_NAME

MONGODB_URI

PAT_TOKEN

REACT_APP_API_URL

VERCEL_ORG_ID

VERCEL_PROJECT_ID

VERCEL_TOKEN
