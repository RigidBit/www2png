# WWW2PNG .env Setup

The following code goes in the `.env` file within the root folder.

Be sure to replace all the unpopulated values below with their correct values.

The `.env` file should never be committed!

```
FLASK_SECRET_KEY="<SECRET>"
SELENIUM_TIMEOUT=30
IMGUR_CLIENT_ID="<SECRET>"
IMGUR_CLIENT_SECRET="<SECRET>"
POSTGRESQL_HOST="127.0.0.1"
POSTGRESQL_PORT=5432
POSTGRESQL_USER="www2png"
POSTGRESQL_PASS="<SECRET>"
POSTGRESQL_DB="www2png"
RIGIDBIT_API_KEY="<SECRET>"
RIGIDBIT_BASE_URL="http://localhost:8000"
RIGIDBIT_PROOF_DELAY=60
WWW2PNG_BASE_URL="http://192.168.0.1:5000"
WWW2PNG_IMAGE_DIR="static/image"
WWW2PNG_PROCESSING_THREADS=10
WWW2PNG_PROCESSING_TTR=120
WWW2PNG_PRUNE_LOOP_DELAY=5
WWW2PNG_STYLE_DIR="static/style"
WWW2PNG_SCREENSHOT_DIR="data"
WWW2PNG_SCREENSHOT_PRUNE_DELAY=120
WWW2PNG_SCREENSHOT_SETTINGS_DEFAULT='{"maxResolution": "1980x10800", "minResolution": "1x1", "resolution": "1366x768",  "full_page": false, "fullPageMaxLoops": 3, "delay": 0,  "maxDelay": 10}'
WWW2PNG_UNVERIFIED_USER_PRUNE_DELAY=120
WWW2PNG_VERBOSE=true
GREENSTALK_HOST="127.0.0.1"
GREENSTALK_PORT=11300
GREENSTALK_TUBE_QUEUE="www2png-queue"
GREENSTALK_TUBE_ACTIONS="www2png-actions"
SMTP_HOST="email-smtp.us-east-1.amazonaws.com"
SMTP_PORT=587
SMTP_USER="<SECRET>"
SMTP_PASS="<SECRET>"
SMTP_SENDER="WWW2PNG <noreply@www2png.com>"
```