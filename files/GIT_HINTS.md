# Authentication
## Github
Using `gh` seems to be the most practical approach to avoid playing around with TOKENS.
In this case, you authenticate the session using MFA and the session is cached while working.

```$ gh auth login```

It is also possible to use SSH and this preference is very personal.
I would recommend to use HTTPS + TOKENS especially for the great flexibility and volatility of TOKENS.

Using TOKENS you can really easily replace, revoke and work with very granular TOKENS to reduce the risks in case of a leakage.

## Gitlab
Here I also recommend to use HTTPS + TOKENS with proper permission and a reasonable expiration date.
With Gitlab, until the moment I am write this, I didn't find a similar approach as `gh auth login` for Github.
However, it is possible to use a local credential file as well documented [here](https://git-scm.com/docs/git-credential-store#_storage_format).

# Basic Stuff
## Branches
### Check the current branches
```
$ git branch
$ git branch -r
```

### Count the number of commits in a branch
```
$ git checkout <branch_name>
$ git rev-list --count HEAD ^master
```

## Remotes
### Check the remotes
```$ git remote -v```

### Remote Prune
```$ git remote prune origin```
```$ git remote prune upstream```

### Delete remote branch
```$ git push <remote> --delete <branch>```

## Fetch
### Prune while fetching
```$ git fetch -p origin```
```$ git fetch -p upstream --dry-run```
```$ git config --global fetch.prune true```

# Rebase
Interactive rebase is a powerful technique. Explore it and take advantage of this whenever you need to better organize your commits.

```$ git rebase -i HEAD~<commit number>```

`--root` means the interactive rebase will consider even the first commit.

```$ git rebase -i --root```

# Reset
Sometimes is necessary to remove one commit by whatever reason.

To reset the last commit:

```$ git reset HEAD~```

Then you can work normally with the files and commit again after the desired changes.

# Restore
Used to restore uncommitted changes in a file:

```$ git restore <file>```

# Troubleshooting
## Debug Hint
GIT_CURL_VERBOSE=1 GIT_TRACE_PACKET=1 GIT_TRACE=1 git push

# References
## Good Practices
* https://www.conventionalcommits.org/
