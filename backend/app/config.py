# 環境依存地や定数を一箇所に集約。将来の.envや設定ファイル化に備える

ALLOWED_ORIGINS = [os.getenv("BACKEND_ORIGIN", "http://localhost:5173")]
DEFAULT_ROUNDING = "round" #表示丸め込みの既定
DEFAULT_TAX_MONTH = 12 #税金の計上月
