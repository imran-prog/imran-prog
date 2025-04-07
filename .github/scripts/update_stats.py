import os
import re
from datetime import datetime
from collections import defaultdict
from github import Github
from dateutil import parser
from dateutil import tz

# Get environment variables
github_token = os.environ["GH_TOKEN"]
github_username = os.environ["GITHUB_USERNAME"]

# Initialize GitHub API
g = Github(github_token)
user = g.get_user(github_username)

# Get all user repositories
repos = user.get_repos()

# Initialize counters
time_of_day = {
    "morning": 0,    # 6:00 AM - 12:00 PM
    "daytime": 0,    # 12:00 PM - 6:00 PM
    "evening": 0,    # 6:00 PM - 12:00 AM
    "night": 0       # 12:00 AM - 6:00 AM
}

day_of_week = {
    "Monday": 0,
    "Tuesday": 0,
    "Wednesday": 0,
    "Thursday": 0,
    "Friday": 0,
    "Saturday": 0,
    "Sunday": 0
}

# Time zone - adjust this to your local time zone
local_tz = tz.tzlocal()

# Count commits
total_commits = 0

# Process each repository
for repo in repos:
    try:
        if repo.owner.login == github_username:  # Only process user's own repos
            commits = repo.get_commits(author=github_username)
            for commit in commits:
                commit_date = parser.parse(commit.commit.author.date.isoformat())
                # Convert to local time
                local_commit_date = commit_date.astimezone(local_tz)
                
                # Count by time of day
                hour = local_commit_date.hour
                if 6 <= hour < 12:
                    time_of_day["morning"] += 1
                elif 12 <= hour < 18:
                    time_of_day["daytime"] += 1
                elif 18 <= hour < 24:
                    time_of_day["evening"] += 1
                else:  # 0 <= hour < 6
                    time_of_day["night"] += 1
                
                # Count by day of week
                day = local_commit_date.strftime('%A')
                day_of_week[day] += 1
                
                total_commits += 1
    except Exception as e:
        print(f"Error processing repo {repo.name}: {e}")

# Calculate percentages
time_percentages = {}
for time, count in time_of_day.items():
    time_percentages[time] = round((count / total_commits) * 100, 2) if total_commits > 0 else 0

day_percentages = {}
for day, count in day_of_week.items():
    day_percentages[day] = round((count / total_commits) * 100, 2) if total_commits > 0 else 0

# Find most productive day
most_productive_day = max(day_of_week.items(), key=lambda x: x[1])[0]

# Format the stats text
time_stats = f"""**I'm a {'Night' if time_of_day['night'] > max(time_of_day['morning'], time_of_day['daytime'], time_of_day['evening']) else 'Day' if time_of_day['daytime'] > max(time_of_day['morning'], time_of_day['night'], time_of_day['evening']) else 'Morning' if time_of_day['morning'] > max(time_of_day['daytime'], time_of_day['night'], time_of_day['evening']) else 'Evening'} 🦉** 

```text
🌞 Morning    {time_of_day['morning']} commits     {'█' * (time_percentages['morning'] // 5)}{'░' * (20 - time_percentages['morning'] // 5)}   {time_percentages['morning']}% 
🌆 Daytime    {time_of_day['daytime']} commits     {'█' * (time_percentages['daytime'] // 5)}{'░' * (20 - time_percentages['daytime'] // 5)}   {time_percentages['daytime']}% 
🌃 Evening    {time_of_day['evening']} commits     {'█' * (time_percentages['evening'] // 5)}{'░' * (20 - time_percentages['evening'] // 5)}   {time_percentages['evening']}%
🌙 Night      {time_of_day['night']} commits     {'█' * (time_percentages['night'] // 5)}{'░' * (20 - time_percentages['night'] // 5)}   {time_percentages['night']}% 

```"""

day_stats = f"""📅 **I'm Most Productive on {most_productive_day}** 

```text
Monday       {day_of_week['Monday']} commits     {'█' * (day_percentages['Monday'] // 5)}{'░' * (20 - day_percentages['Monday'] // 5)}   {day_percentages['Monday']}% 
Tuesday      {day_of_week['Tuesday']} commits     {'█' * (day_percentages['Tuesday'] // 5)}{'░' * (20 - day_percentages['Tuesday'] // 5)}   {day_percentages['Tuesday']}% 
Wednesday    {day_of_week['Wednesday']} commits     {'█' * (day_percentages['Wednesday'] // 5)}{'░' * (20 - day_percentages['Wednesday'] // 5)}   {day_percentages['Wednesday']}% 
Thursday     {day_of_week['Thursday']} commits     {'█' * (day_percentages['Thursday'] // 5)}{'░' * (20 - day_percentages['Thursday'] // 5)}   {day_percentages['Thursday']}% 
Friday       {day_of_week['Friday']} commits     {'█' * (day_percentages['Friday'] // 5)}{'░' * (20 - day_percentages['Friday'] // 5)}   {day_percentages['Friday']}% 
Saturday     {day_of_week['Saturday']} commits     {'█' * (day_percentages['Saturday'] // 5)}{'░' * (20 - day_percentages['Saturday'] // 5)}   {day_percentages['Saturday']}% 
Sunday       {day_of_week['Sunday']} commits     {'█' * (day_percentages['Sunday'] // 5)}{'░' * (20 - day_percentages['Sunday'] // 5)}   {day_percentages['Sunday']}%

```"""

# Read the README file
with open('README.md', 'r', encoding='utf-8') as file:
    readme_content = file.read()

# Define start and end tags for the stats sections
start_tag = "<!--START_SECTION:waka-->"
end_tag = "<!--END_SECTION:waka-->"

# Combine stats
combined_stats = f"{time_stats}\n{day_stats}"

# Replace the content between the tags
pattern = f"{start_tag}(.*?){end_tag}"
new_content = f"{start_tag}\n{combined_stats}\n{end_tag}"
updated_readme = re.sub(pattern, new_content, readme_content, flags=re.DOTALL)

# Write the updated content back to the README file
with open('README.md', 'w', encoding='utf-8') as file:
    file.write(updated_readme)

print("GitHub stats updated successfully!")