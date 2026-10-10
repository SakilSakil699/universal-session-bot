

---

# `docs/API.md` (FINAL)

```markdown
# 🔧 API Reference

**Universal Session Bot**
Author: [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH) · [GitHub](https://github.com/SakilSakil699)

Internal API reference for developers building on top of this bot.

---

## 📦 Core Module

### `UniversalSession` — `core.universal_session`

Common denominator for all session formats.

```python
from core import UniversalSession

@dataclass
class UniversalSession:
    auth_key: bytes              # 256 bytes MTProto auth key
    dc_id: int                   # 1-5
    user_id: int
    api_id: int
    api_hash: str
    is_bot: bool = False
    test_mode: bool = False
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
