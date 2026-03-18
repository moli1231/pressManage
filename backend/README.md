# Backend (Flask)

## 快速启动

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

默认超级用户（可在 `.env` 修改）：
- 手机号：`13800000000`
- 密码：`Admin@123`

## 关键命令

```bash
# 初始化数据库和超级用户
flask --app run.py init-db

# 运行测试
pytest

# 备份 SQLite
./scripts/backup_sqlite.sh pressure_gauges.db ./backups
```
