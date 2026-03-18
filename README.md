# 采气二厂工艺设备管理系统（前后端分离）

技术栈：
- 后端：Flask + SQLAlchemy + SQLite
- 前端：Vue3 + Vite + Element Plus

## 项目结构

- `/backend` API 服务与定时任务
- `/frontend` 管理后台页面

## 功能覆盖

- 登录鉴权（无注册）
- 角色权限（普通用户 / 管理员 / 超级用户）
- 管理员创建用户与超级用户
- 压力表 CRUD（超级用户）
- 压力表列表查询（普通用户可查看）
- 有效期自动计算
- 提醒机制（30天、15天，仅两次）
- 图片上传
- Excel 导入导出

## 启动方式

### 后端

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

前端默认代理到 `http://127.0.0.1:5000`。
