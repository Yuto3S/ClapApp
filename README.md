# ClapApp
ClapApp is a website using websockets to play sounds to all the users connected at the same time in the same session.

# Access
A live version is running at https://yuto3s.github.io/ClapApp/

# Running Locally
Copy this projet locally, and cd into it.
1) Run the http server:
  `python3 -m http.server`
2) Run the websocket server:
  `python3 -m app`
3) _Optional: run tailwind to have CSS changes_:
  `npx tailwindcss -i ./client/main.css -o ./client/tailwind_main.css --watch`
  
You can then access a local version of this website at `localhost:8000`
