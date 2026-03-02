# claude-skills — Project Rules

## Adding or Removing Skills

When a skill is **added, removed, or renamed** in this repo, the `README.md` **must** be updated in the same commit:

1. Update the skill count in "Skills Overview"
2. Add/remove the skill row in the correct category table
3. Update the ASCII diagram (if it's an audit skill)
4. Update category skill counts in section headers (e.g. "Scaffolding & Setup (3 skills)")
5. Update **all** install scripts:
   - "Install all X skills" loop
   - "Install just the audits" loop (if audit skill)
   - Individual install commands in the `<details>` block

Never commit a new skill directory without the corresponding README update.
