# 教訓：驗證 push 目標與 PR base — 手打 repo 名與過期 base 的雙重陷阱

> **環境層**：此坑不限於本專案，任何用 `gh` + git remote 開 PR 的專案都可能踩到。
>
> **日期**：2026-09-29
> **關聯 PR**：品牌更名 My O! → MyO（`myo-brand-rename`）
> **狀態**：已解決

---

### 問題

將 `myo-brand-rename` 分支推送並開 PR 時，走了兩段不必要且具破壞性的彎路。

#### 1. 手打 GitHub repo 名稱驗證權限 → 打錯字 → 誤判無權限

`gh` 登入的帳號是 `ashashash001001-stack`，而 `origin` 指向另一個 owner。我先手動輸入 repo 名測試 API：

```bash
gh api repos/chungyucheung/myo-hk --jq '{full_name, permissions}'
# {"message":"Not Found","status":"404"}
```

我據此判定「帳號對此 repo 無權限」，於是新增 `fork` remote、改推自己的 fork、在 fork 上開了兩個 PR，最後才發現全部搞錯了。

實際的 owner 是 `chungyuicheung`（多一個 `i`）：

```bash
gh api repos/chungyuicheung/myo-hk --jq '.permissions.push'
# true          ← 原本就有寫入權限
```

**根本問題**：我憑記憶手打 owner 名，而不是從 `git remote get-url` 讀出。兩者只差一個字母，而 GitHub 對「不存在」與「無權存取」回傳**同一個 404**，無法從錯誤訊息分辨。

#### 2. PR base 分支落後 → diff 混入 57 個無關 commit

第一次開 PR 時，GitHub 顯示 **1,145 檔案 / 64 commits**，但我的分支實際只有 **7 commits / 459 檔案**。

原因：該 remote 的 `main` 落後本機 `main` **57 個 commit**（fork 建立後未同步）：

```bash
git ls-remote origin main   # 416a6c62  ← 本機與上游
git rev-list --count <remote>/main..main   # 57
```

PR 的 diff 是「base 到 head 的全部差異」，所以落後的 base 會把中間所有歷史變更都算進來。

修正步驟本身又踩到第二層陷阱：**即使把 base fast-forward 到位，PR 的 diff 仍不會重算**。

```bash
git push fork main:main   # 已 fast-forward，但 PR 仍顯示 1,145 檔案 / 64 commits
```

GitHub 的 PR diff 在建立時依 base 狀態計算，**不會因 base 移動而自動更新**。只能關閉 PR、刪除分支、重新推送、重開。

---

### 教訓

1. **永不手打 GitHub owner/repo 名稱。** 從 `git remote get-url` 讀，或用 `gh repo view --json nameWithOwner -q .nameWithOwner`。記憶中的字串不可信 — 兩名相似帳號只差一個字母時，人眼與記憶都不會發現。

2. **404 不代表無權限。** GitHub 對「repo 不存在」「無權存取私有 repo」「名稱打錯」回傳同一個 404。判定權限必須用**已知正確**的 repo 名，或改用不依賴 repo 名的方法。

3. **`git ls-remote` 是最可靠的權限與同步檢查**，因為它直接對 remote 詢問，不需要你輸入 repo 名。

4. **開 PR 前先確認 base 新鮮度。** base 落後會讓 diff 混入無關 commit，而且修正 base 後 PR 不會自動重算 —— 必須重建 PR，成本遠高於事先檢查。

---

### 解法

**權限與同步狀態檢查（不手打名稱）：**

```bash
# 從 remote 讀出精確 repo 路徑
for r in origin upstream; do
  echo "$r = $(git remote get-url $r)"
done

# 用讀到的路徑查權限 —— 絕不手打
gh api "repos/$(git remote get-url origin | sed 's|.*github.com/||; s|\.git$||')" \
  --jq '.permissions.push'

# 比較本地與遠端是否同步
git fetch <remote> main
git rev-list --count <remote>/main..main   # >0 代表遠端落後
```

**開 PR 前確保 base 新鮮：**

```bash
# 確認可 fast-forward（非分叉）
git merge-base --is-ancestor <remote>/main main && echo "可 fast-forward"

# 先同步 base，再推分支，最後才開 PR
git push <remote> main:main
git push <remote> <feature-branch>
gh pr create --base main --head <feature-branch>
```

**若已開錯 PR**（順序很重要，省一次重建）：

```bash
gh pr close <N> --repo <owner/repo> --comment "<說明>" --delete-branch
git push <remote> <feature-branch>   # 重新推送被刪的分支
gh pr create ...                     # 重開，diff 才會重算
```

---

### 預防

- 驗證權限一律用 `git remote get-url` 產生的路徑，不要手打。
- 看到 404 先假設「名稱可能打錯」，用 `git remote -v` 核對後再下結論。
- 開 PR 前跑 `git rev-list --count <remote>/main..main`，非 0 就先同步 base。
- 推 fork 前先確認帳號對上游的實際權限 —— 能直推上游就不要繞 fork。
- 本專案有多個 remote（`origin` = 原始 repo、`upstream` = `myo-hk/myo-hk.github.io` Pages 站），推送前務必確認目標 remote 與分支。
