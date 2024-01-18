# PeE_Helper

At the start, the bot looks for the PatchOfExile "PoE.exe" icon on the desktop and thus starts the game. Then it looks for the login window and, when found, enters the login and password, selects the selected character and starts the game session. During an active game session, the program takes photos of the game screen and scans it for known buff icons, reads the player's life amount and looks for the names of known game windows such as "INVENTORY", "ATLAS".

Based on the photo of active buffs and the player's life, the bot decides whether to use the buff, e.g. to move faster or heal. In situations where the standard of living drops below the assumed values, he uses different bottles.

The bot stops itself when it detects an open window, e.g. INVENTORY, etc., so as not to interfere with the player pressing the keys. He has to do this because some windows cover the amount of HP and visibility...

Python's weakness is Global Interpreter Lock, which does not allow background threads to spread their wings. This drastically reduces the speed of the bot. Causes button presses to get stuck. Even using Windows libraries did not help much.

I abandon the project and expose it to the world. Maybe someone will want to continue my work. The project is open source and you can take full advantage of it. The only thing I would like is for you to mention me in your project.
