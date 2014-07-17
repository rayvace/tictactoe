Tic Tac Toe
=========

An web and command line app for playing Tic Tac Toe against a computer. The computer can only win or tie. This project is built in python and javascript. The computer plays a perfect game by following the Tic Tac Toe strategy described in (Wikipedia)[http://en.wikipedia.org/wiki/Tic-tac-toe]. This program uses rules rather than the (minmax)[http://chet-weger.herokuapp.com/play_ttt/] algorithm to determine the best move.

Project Structure
=========
This project uses Flask as a lightweight web framework for receiving and respodning to API requests. The front-end uses Backbone to keep the javascript organized and LESS. You'll see that what little data there is, is persisted using SimpleCache (not meant to be used production). 

To install this project, run the following from your terminal:

```
$ git clone https://github.com/rayvace/tictactoe
```

Next you'll want to run the following:

```
$ cd tictactoe
```

Next, install virtualenv
```
$ pip install virtualenv

$ virtualenv venv

$ source venv/bin/activate
```

Finally, you'll want to install Flask
```
$ pip install Flask
```

Optionally, you can install less if you plan on making updates to the CSS.
```
$ npm install less
```

To start the server locally run the the code below from the command line and visit http://127.0.0.1:5000/ in Chrome:
```
$ python app.py
```

The figures below illustrate what you should see in your browser:

![alt Figure 1](https://raw.github.com/rayvace/tictactoe/master/static/img/fig1.png)

![alt Figure 2](https://raw.github.com/rayvace/tictactoe/master/static/img/fig2.png)

![alt Figure 3](https://raw.github.com/rayvace/tictactoe/master/static/img/fig3.png)


If you're a fan of the terminal, you can also play from the command line by running the following:
```
$ python main.py
```
