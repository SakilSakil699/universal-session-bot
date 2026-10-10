# 🛠️ Utils Module

**Universal Session Bot**
Author: [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH) · [GitHub](https://github.com/SakilSakil699)

Helper utilities — validators, logger, rate limiter, files.

---

## 📂 Files

| File | Purpose |
|------|---------|
| `__init__.py` | Package exports |
| `validators.py` | Phone, OTP, session, file validation |
| `logger.py` | Colored console + rotating file logs |
| `rate_limit.py` | Sliding-window rate limiter |
| `file_handler.py` | Safe download/upload helpers |

---

## 💻 Usage

### Validators

```python
from utils import Validators

Validators.is_valid_phone("+919876543210")    # True
Validators.is_valid_otp("1 2 3 4 5")          # True
Validators.is_valid_username("@Sakil")        # False (too short)
Validators.mask_phone("+919876543210")        # +91****3210
