# Backup Files

This folder contains legacy and backup files from refactoring.

## Files

- **chatbot_core.py.old** - Original monolithic chatbot core (before refactoring to core/ modules)
- **app.py.backup** - Original app.py before blueprint refactoring

## Purpose

These files are kept for reference and rollback purposes. They can be safely deleted once you verify the refactored version works perfectly.

## When to Delete

You can delete this folder if:

- ✅ Refactored application works without issues
- ✅ All features tested and verified
- ✅ In production for >1 month without problems

## Disk Space

Total size: ~45 KB

---

**Note:** These files are automatically ignored by git (see .gitignore)
