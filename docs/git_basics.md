# Git Basics

## What is Git?

Git is a distributed version control system that tracks changes in your code. Every developer has a full copy of the repository history on their machine. It was created by Linus Torvalds in 2005 for Linux kernel development and is now the most widely used version control system in the world.

## How do I start a new repository?

Run `git init` in your project folder to create a new Git repository. This creates a hidden `.git` folder that stores all version history. Alternatively, clone an existing repository with `git clone <url>` to get a copy of a remote project.

## What is the staging area?

The staging area (also called the index) is where you prepare changes before committing them. Use `git add filename` to stage specific files, or `git add .` to stage everything. This lets you control exactly which changes go into each commit rather than committing everything at once.

## How do branches work?

A branch is a separate line of development. The default branch is usually called `main` or `master`. Create a new branch with `git branch feature-name` and switch to it with `git checkout feature-name` (or `git checkout -b feature-name` to do both at once). Branches let multiple people work on different features without interfering with each other.

## How do I merge branches?

Switch to the branch you want to merge into (e.g., `git checkout main`), then run `git merge feature-name`. If both branches modified the same lines, you get a merge conflict that you need to resolve manually by editing the conflicted files, then staging and committing the result.

## What is the difference between pull and fetch?

`git fetch` downloads new commits from the remote but does not change your working files. `git pull` does a fetch and then merges the remote changes into your current branch. Use fetch when you want to see what changed before integrating, and pull when you want to update immediately.

## How do I undo changes?

- To discard unstaged changes in a file: `git checkout -- filename`
- To unstage a file (keep changes): `git reset HEAD filename`
- To undo the last commit but keep changes: `git reset --soft HEAD~1`
- To completely undo the last commit: `git reset --hard HEAD~1` (careful - this deletes changes)
