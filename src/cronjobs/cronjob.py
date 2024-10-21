import time
from cronjobs.update_goal_history import check_for_updates

def process_notifications():
    """Check the notifications table for new notifications and handle them accordingly."""
    check_for_updates()

def main():
    """Main function to run all cron jobs centrally."""
    while True:
        process_notifications()
        time.sleep(10)  # Check every 10 seconds for notifications

if __name__ == "__main__":
    main()