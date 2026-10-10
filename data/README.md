# 📁 Data Directory

**Universal Session Bot**
Author: [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH)

Runtime data storage — **NOT committed to Git**.

---

## 📂 Subdirectories

| Folder | Purpose |
|--------|---------|
| `sessions/` | Temporary session files during generation |
| `tdata/` | Generated Telegram Desktop tdata folders |
| `tgnet/` | Generated Android tgnet files |
| `*.db` | SQLite databases (dev only) |

---

## ⚠️ Security

- **All contents gitignored** — check root `.gitignore`
- Sessions are **encrypted** before saving to DB
- Temp files are **auto-deleted** after use
- Never commit anything from this folder

---

## 🧹 Cleanup

```bash
# Delete all runtime data
rm -rf data/* && touch data/.gitkeep
