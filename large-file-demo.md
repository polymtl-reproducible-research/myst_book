# The problem with large files in Git

Here are some commands to illustrate the shell, and git's handling of small
versus large files.

```sh
# First, go to https://github.com/new to create a new dummy repository with
# a `README.md` file. For my demo, I used my account `mguaypaq` and the repo
# name `demo-ing8100`. Let's save these two pieces of information in some
# shell variables.
USER=mguaypaq
REPO=demo-ing8100

# The command `mktemp -d` creates a clean temporary directory where we can
# experiment. It outputs the full path to this directory, so we can directly
# go there by giving the output to the `cd` command.
cd $(mktemp -d)

# If you want information about a shell command, a good source is to look at
# its manual page, using the `man` command (use arrow keys or pgup/pgdn to
# scroll, and type the letter q to quit). For shell builtin commands like
# `cd` or `printf` or control flow keywords like `if`, `for`, `while`, the
# online manual https://www.gnu.org/software/bash/manual/bash.html is easier.
man mktemp

# We're going to make several clones of the repository to illustrate some
# potential interactions with collaborators, called `clone-1`, `clone-2`, etc.
git clone "git@github.com:${USER}/${REPO}" clone-1
cd clone-1

# First, let's create 20,000 small text files (which git can easily handle),
# nested inside 20 folders (so we don't have to see all of them at once).

# The command `seq` outputs a range of numbers, which is useful for looping,
# or for generating sequential filenames. With the option `seq -w`, it will
# prefix small numbers with enough zeros to make them equal width, which is
# convenient.
# We use `mkdir` in the outer loop to create each directory, and `echo` with
# some output redirection to create each file in the inner loop.
for x in $(seq -w 1 20); do
  mkdir "folder-${x}"
  for y in $(seq -w 0 999); do
    echo "some text with ${x} and ${y} in it" >"folder-${x}/file-${y}.txt"
  done
done
cat folder-17/file-029.txt

# Using `time` before a command is a convenient way to get the shell to check
# how long the command takes. Even though there are 20,000 files, these `git`
# commands are pretty quick.
time git add .
time git commit -m 'Add 20k small files'
time git push  # fast

# It's also pretty quick for a new collaborator to get a copy of the repo.
cd ..
time git clone "git@github.com:${USER}/${REPO}" clone-2  # fast
cd clone-2
ls

# Now let's add a single large file (20 megabytes of random data), and see
# `git` become slower for some operations.
# The special file `/dev/urandom` is an infinite source of random bytes, and
# the `head` command reads the start of it (usually it shows the first 10 lines
# of text, but here we ask it for 20M bytes of data).
cd ../clone-1
head --bytes 20M /dev/urandom >big-file.dat
time git add big-file.dat
time git commit -m 'Add a single 20M file'
time git push  # slow

# This is also slow for collaborators the first time they pull the changes.
cd ../clone-2
time git pull  # slow
ls

# And it's also slow for new collaborators when they first clone the repo.
cd ..
time git clone "git@github.com:${USER}/${REPO}" clone-3  # slow
cd clone-3
ls

# If we simply delete the file from the original repo, it doesn't really solve
# the problem...
cd ../clone-1
git rm big-file.dat
git commit -m 'Oops, delete the large file'
time git push  # fast

# This will be a quick update for existing collaborators...
cd ../clone-2
time git pull  # fast

cd ../clone-3
time git pull  # fast

# But it will still be slow for new collaborators!
cd ..
time git clone "git@github.com:${USER}/${REPO}" clone-4  # slow
cd clone-4
ls

# To fix the problem, we need to forcefully remove all the commits which
# contain the large file from git's history. This can be tricky to do, and
# it also comes with some headaches for existing collaborators.
# In this simplified example, we can do it by just removing the last 2 commits
# from the current branch.
cd ../clone-1
git reset --hard HEAD~2
git push  # fails
git push --force  # succeeds

# Now things are fast again for new collaborators.
cd ..
time git clone "git@github.com:${USER}/${REPO}" clone-5  # fast
cd clone-5
ls

# But existing collaborators will accidentally restore the removed history
# if they're not aware and careful!
cd ../clone-2
git pull  # this won't remove any commits
git push  # this will re-push the removed commits to the server

# These difficulties can be mitigated by using protected branches, but you
# will still have to communicate with and help all existing collaborators.
# It's much better to avoid committing large files in the first place.
```
