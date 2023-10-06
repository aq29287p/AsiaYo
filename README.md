# AsiaYo API

## 系統需求
### Ubuntu
- Version: `22.04`
### Python
- Version: >= `3.10`

### 建立 python virtual environment
在 project 目錄下執行下面的 command

```bash
# 創建虛擬環境 venv
python3 -m venv venv
# 進入虛擬環境 venv
. venv/bin/activate
```

### 安裝 dependency
```bash
pip install -r requirements.txt
```

### 設定檔 Config
複製 `config/sample_api_config.py` 到 `config/api_config.py`，接著修改 `config/api_config.py` 配置內容
