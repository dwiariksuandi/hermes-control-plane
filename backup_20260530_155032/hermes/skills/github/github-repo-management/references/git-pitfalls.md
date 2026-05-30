# Git Remote & Push Pitfalls

## Remote Already Exists

`git remote add origin ...` fails if remote already configured.

**Fix:**
```bash
git remote add origin URL 2>/dev/null || git remote set-url origin URL
```

## Push Rejected: "fetch first"

Remote has commits you don't have locally.

**Fix:**
```bash
git stash -u  # or commit changes
git pull --rebase origin main
git push -u origin main
```

## Unstaged Changes Block Pull

`git pull --rebase` fails with "You have unstaged changes."

**Fix:**
```bash
git add .
git commit -m "temp checkpoint"
# or
git stash -u
```