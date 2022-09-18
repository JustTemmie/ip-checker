## hi

create a file named "keys.env"

and input `DISCORD=YOURDISCORDTOKENHERE`

get a token by going to <a href="https://discord.com/developers/applications">here</a>, and clicking the new application button

go into the "bot" section to the left, create a bot, give it a username and an icon if you wish, scroll down a bit and enabled the "message content intent" switch

then copy the bot token from that very same page and dump it into the keys.env file

go to the section named "OAuth2" on the left, click URL Generator, select the scope "bot", with any permissions needed, just select "Administator" if unsure

## hi again

then go into config.json and fill in the desired prefix along with your own user ID

## run the thing?!?!?!

cd into this folder, for first time setup install the dependancies by running "pip install -r requirements.txt"

then whenever you want to run the bot run the command "python3 main.py"