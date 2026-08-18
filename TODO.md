
## github-standard verification
- Verified 2026-08-17: branch ruleset enforced on `main` (direct push rejected,
  squash-merge PR with 0 approvals + auto-delete-branch succeeded). See
  claude-dotfiles/github-standard.md.

## Logging improvements
- update to TimedRotatingFileHandler

  like in
  @/home/guido/projects/fitted/backend/src/fitted_backend/core

  i think a folder with log files is better than a single log file.
