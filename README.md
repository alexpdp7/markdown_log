# INTRODUCTION

`markdown_log` is a time tracking tool based on keeping your logs in Markdown:

* You can use your favourite text editor, keep your log in a Git repo, etc.
* You can intersperse notes between your logs

Logs are hierarchical.
Each time period recorded can have one or more task hierarchies associated, such as:

* Work / Support / Ticket 1
* Work / Development / JIRA-123
* Work / Development / Code Review

For instance, you can record a time period as the latter two; marking code review on JIRA-123.

# INSTALL

`markdown_log` is in a very early stage.
It requires [pandoc](https://pandoc.org/) to be installed.

`markdown_log` is a Python application without official releases/packages.

We recommend installing it using [pipx](https://pipxproject.github.io/pipx/):

```
$ pipx install --spec git+https://github.com/alexpdp7/markdown_log.git md_log
```

# USAGE

Check:

```
$ md_log --help
```

for a full reference.
See log.md in this directory for a complete example.

### daily-target

This command checks daily worked time against a target:

```
$ md_log daily-target log.md --target-hours=8 --filter Work
2020-12-03 8:30:00 too much 0:45:00
2020-12-04 7:15:00 too much 0:15:00
2020-12-05 9:00:00 too much 1:00:00
```

In this case, we are interested in working 8 daily hours on `Work / *` tasks.

Columns are:

* Date
* Hours worked that day on filtered tasks
* Running total

The running total starts on the last day worked, so working 9 hours results in 1 hour excess work over the 8-hour target.
The previous day we worked just 7 hours and 15 minutes, so this reduces the excess work to 15 minutes.
The first day 8 hours and 30 minutes were logged, increasing the excess work to 45 minutes.
