# ClapApp
ClapApp was made as a fun website project where users can interact with each other by sharing a link. All the users in the same session can pick a sound from the selection available, and it will play for all the connected users.

# Access
[A live version](https://yuto3s.github.io/ClapApp/) is available. The client is hosted on [GitHub](https://github.com), the websocket server is hosted on [Heroku](https://www.heroku.com).

# Running Locally
Copy this projet locally, and cd into it.
1) Run the http server:
  `python3 -m http.server`
2) Run the websocket server:
  `python3 -m app`
3) _Optional: run tailwind to have CSS changes_:
  `npx tailwindcss -i ./client/main.css -o ./client/tailwind_main.css --watch`
  
You can then access a local version of this website at `localhost:8000`
