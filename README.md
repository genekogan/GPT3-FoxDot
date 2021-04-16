## GPT3-FoxDot

work in progress!

Requires a [key from OpenAI](https://beta.openai.com/).

1) Install requirements 

    `pip install -r requirements.txt`

2) Install [FoxDot](https://github.com/Qirky/FoxDot) from source.

3) Download [SuperCollider](https://supercollider.github.io/) or install it from source and then [add the FoxDot quark](https://foxdot.org/installation/) to it by running `Quarks.install("FoxDot")` and recompiling the class library.

4) In the root folder, create a file called `.env` which contains the following line:

    `OPENAI_KEY=xxxxxx`

where `xxxxxx` is replaced with your API key from OpenAI.

5) Boot SuperCollider server and start FoxDot by running:

    `FoxDot.start`

6) In a terminal, run 

    `python runfoxdot.py`

This will launch the FoxDot editor.

7) In a second terminal, run 

    `python main.py`

And then click your mouse cursor onto the FoxDot editor, and wait for the main script to begin generating keystrokes to run FoxDot commands.

