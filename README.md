# web_logger

Get your log through the web. Why having a web logger rather than a native
interface?

- Remote access (although it works perfectly locally)
- UI customization (if you are confortable with CSS)

This application was built to run smoothly on a Raspberry Pi, however it has
been designed on a platform agnostic way.

### Getting started

You need `Python 3.5+` to run this package.

#### Browser support

A banner pops in on browsers which don't support the needed feature. Also, it
has been developed for those browsers:

- Chrome 62+

> On Windows the HTTP server is quite instable, you may need to reload the page
> (press F5) if the logger get stuck before getting ready.

Please specify your browser path to the API.

```python
from web_logger import Logger, LoggerException

def demo(logger):
    logger.log("Logger ready")

Logger("/path/to/browser", onReady=demo)
```

**Note:** Currently the python script needs to run on the `www` directory
containing the interface files. However it is enough for the purpose of my
projects so I don't plan to fix this. If this behavior upsets you, you are very
welcome to submit a fix.

To customize the interface, you can copy all the files in another directory
specific to your project, you can do versioning on this folder and use this
folder as the working directory.

#### API

Please see the `demo.py` file to see an example.

```python
logger = Logger(
        browser_path, # if None or none provided, Logger will start in remote mode
        http_port=3000, # TCP port to use for the HTTP server
        ws_port=3001, # TCP port to use for the WebSocket server
        onReady=lambda _: None, # callback for when logger is ready
    )
# the Logger constructor will block the thread until logger.stop is called
# or the browser is closed if run in local mode

# All methods should be called after the onReady callback has been called
try:
    logger.defineNewMenu(menu) # defines the menu items and action to be displayed on top of the logger
    logger.printMessage(message) # logs a message on the HTML interface
    logger.printMessage(message, audioFile="/audio.mp3") # logs a message on the HTML interface and play the audio
except LoggerException:
    print("Logger was not ready or has already terminated")
    pass
```

##### Audio files

You have the ability to play audio sound on the interface by specifying a
`audioFile` argument. Check what are the supported audio formats for the browser
you want to use.

**N.B.:** The path to audio file will be sent to the browser and therefore need
to be relative to the root of the HTTP server. The root of the HTTP server can
be set by changing the current directory. Because of HTTP specification, you
cannot access the parent directory of the HTTP root folder.
