# Trello-Raspberry-Pi-Zero-API
API to display your Trello Boards on a Raspberry PI using the Bonnet OLED display

![](https://github.com/abhinuvpitale/Trello-Raspberry-Pi-Zero-API/blob/master/docs/raspitrello.gif)


I have always needed a to-do list on my desk!

Sticky notes can't be updated whenever and wherever I want
And all the apps that are out there don't stay continuously on my desk reminding what *to do.*

So I created this sweet little todo list synced to my Trello To-Do List Boards which can help me focus and browse my tasks from my desk!

## Requirements

1. Raspberry Pi Zero W
2. Bonnet OLED 128*32 board
3. Trello Dev Account

## How to?

1. Setup your Raspberry Pi along with the Bonnet OLED using this [link].(https://learn.adafruit.com/adafruit-128x64-oled-bonnet-for-raspberry-pi/overview)
2. Create a `keys.dat` file with the following syntax

```
KEY
TOKEN
BOARD
```

3. List of your boards can be found using this [link](https://trello.readme.io/docs/api-introduction#section--a-name-boards-boards-a-)

4. Run the `raspiTrello.py` to start

## TODO::

- Create a script to scrape boardnames to ease Setup
- Mark/Unmark items on the list
