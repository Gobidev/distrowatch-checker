# distrowatch-checker
A small python scripts that checks distrowatch.com for news and sends discord webhook notifications for new ones.


## How to Run
1. Install the requirements
2. Create a SECRETS.py file containing a variable called `WEBHOOK_URL` that is set to the discord webhook you want to use for notifications.
3. Run the script periodically, I recommend cron for automation.