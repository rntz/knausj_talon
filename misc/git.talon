tag: terminal
and tag: user.git
-
# Standard commands
git add patch: "git add . -p "
git add: "git add "
git add everything | git [add] update: "git add -u "
git bisect: "git bisect "
git blame: "git blame "
git branch: "git branch "
git remote branches: "git branch --remote\n"
git branch <user.word>: "git branch {word}"
git checkout master: "git checkout master "
git checkout <user.optional_word>: "git checkout {optional_word}"
git cherry pick <user.optional_word>: "git cherry-pick {optional_word}"
git cherry pick continue: "git cherry-pick --continue "
git cherry pick abort: "git cherry-pick --abort "
git cherry pick skip: "git cherry-pick --skip "
git clone: "git clone "
git commit: "git commit "
git commit amend: "git commit --amend "
git commit message <user.text>: "git commit -m '{text}'"
git commit message$:
  insert("git commit -m ''")
  key(left)
git diff (colour|color) words: "git diff --color-words "
(get|git) diff <user.optional_text>: "git diff {optional_text}"
(get|git) diff (cached | cashed): "git diff --cached "
git fetch: "git fetch "
git fetch <user.word>: "git fetch {word}"
git fetch prune: "git fetch --prune "
git in it: "git init "
git log all: "git log "
git log all changes: "git log -c "
git log: "git log "
git log changes: "git log -c "
git merge: "git merge "
git merge <user.word>: "git merge {word}"
git merge abort: "git merge --abort "
git move: "git mv "
git new branch: "git checkout -b "
git (new branch tracking | check out tracking): "git checkout -t "
git pull: "git pull "
git pull origin: "git pull origin "
git pull rebase: "git pull --rebase "
git pull fast forward: "git pull --ff-only "
git pull <user.word>: "git pull {word} "
(get|git) push: "git push "
(get|git) push origin: "git push origin "
(get|git) push up stream origin: "git push -u origin"
(get|git) push <user.word>: "git push {word} "
(get|git) push tags: "git push --tags "
git rebase: "git rebase "
git rebase continue: "git rebase --continue"
git rebase skip: "git rebase --skip"
git remove: "git rm "
git (remove|delete) branch: "git branch -d "
git (remove|delete) remote branch: "git push --delete origin "
git reset: "git reset "
git reset soft: "git reset --soft "
git reset hard: "git reset --hard "
git restore: "git restore "
git restore staged: "git restore --staged "
git remote show origin: "git remote show origin "
git remote add <word>: "git remote add {word} "
git remote: "git remote "
git show: "git show "
git stash pop: "git stash pop "
git stash: "git stash "
git stash apply: "git stash apply "
git stash list: "git stash list "
git stash show: "git stash show"
git status: "git status\n"
git submodule add:  "git submodule add "
git tag: "git tag "

# Convenience
git edit config: "git config --local -e "

git clone clipboard:
  insert("git clone ")
  edit.paste()
  key(enter)
git diff highlighted:
    edit.copy()
    insert("git diff ")
    edit.paste()
    key(enter)
git diff clipboard:
    insert("git diff ")
    edit.paste()
    key(enter)
git add highlighted:
    edit.copy()
    insert("git add ")
    edit.paste()
    key(enter)
git add clipboard:
    insert("git add ")
    edit.paste()
    key(enter)
git commit highlighted:
    edit.copy()
    insert("git add ")
    edit.paste()
    insert("\ngit commit\n")
