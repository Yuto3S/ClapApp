# ClapApp
ClapApp was made as a fun website project where users can interact with each other by sharing a link. Through websockets, connections are kept open with the server and people can invite each other.

Broadcasters are able to send and read messages, while listeners can only read.


# Access
[A live version](https://yuto3s.github.io/ClapApp/) is available. The client is hosted on [GitHub](https://github.com), the websocket server is hosted on [Render](https://render.com).
# Running Locally
This project requires `python>=3.10` to run correctly. You can check your local version by using `python --version`.

Open your favorite terminal and `cd` to the repo where you want to get ClapApp, and execute those commands one by one:
```
$ git clone https://github.com/Yuto3S/ClapApp
$ cd ClapApp
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
$ python -m http.server
```
While keeping this open, start a new terminal window and `cd` into the ClapApp repo once again
```
$ python -m app
```
You can now access https://localhost:8000 to see your local website running, and you can open tabs in multiple browsers using the broadcaster/receiver links to play with the sounds and websockets.

_Optional: in yet another terminal window, you can see the CSS changes by running tailwind: (you might have to install the package)_
```
$ npx tailwindcss -i ./client/main.css -o ./client/tailwind_main.css --watch
```
