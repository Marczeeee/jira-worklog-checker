# jira-worklog-checker

Simple script checking if users have written worklogs for the last _n_ days. If finds a day when worklogs are missing sends an email for the user.

The script uses Jira Rest Api and [Everit Worklog Query Plugin](https://github.com/everit-org/jira-worklog-query-plugin).