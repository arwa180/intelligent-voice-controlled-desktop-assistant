# Intelligent Voice-Controlled Desktop Automation Assistant

A Python-based offline voice assistant that understands spoken commands and automates common desktop tasks.

## Project Overview

This project was developed as the final project for the Python module of my IoT Diploma at IMT.

The main idea is to control a computer using voice commands while using offline speech recognition.

The assistant can understand spoken commands, convert them into text, execute the requested action on the computer, and provide a voice response to the user.

## Features

- Offline Speech Recognition
- Text-to-Speech
- Opening and closing applications
- Keyboard and mouse automation
- Clipboard manipulation
- Typing text using voice commands
- Opening Google Chrome
- Web searching using voice commands
- Window management
- Taking screenshots
- Displaying images
- Voice-controlled exit command

## Technologies & Libraries

### Python Standard Libraries

- os
- queue
- sys
- subprocess
- webbrowser
- time

### External Libraries

- Vosk — Offline Speech Recognition
- sounddevice — Real-time audio capture
- pyttsx3 — Text-to-Speech
- PyAutoGUI — Keyboard, mouse, and desktop automation
- Pyperclip — Clipboard management

## How It Works

The assistant follows this process:

User speaks
↓
Microphone captures the audio
↓
Vosk converts speech into text
↓
The command is processed
↓
The required desktop action is executed
↓
The assistant responds using Text-to-Speech

## Example Voice Commands

- Hello
- Open Notepad
- Open Calculator
- Close Notepad
- Open Browser
- Search Python documentation
- Type Hello World
- Copy This Text
- Read Clipboard
- Paste Clipboard
- Take Screenshot
- Minimize
- Maximize Window
- Switch Window
- Close Window
- Show Image
- Exit Assistant

## Installation

Install the required libraries using:

```bash
pip install -r requirements.txt
