# Snapshotting and screenshotting

A website snapshot is a representation of a website at a specific point in time. Unlike a visual representation, a snapshot encapsulates the user interface elements, allowing you to open and navigate the website online or offline at a later date. Screenshots, on the other hand, lack this capacity for interactive navigation and are limited to visual inspection alone. In other words, it’s a capture of a device's point of view at a specific moment. DPULSE supports both of these methods to provide full capability for capturing target's contents. You will be prompted to select snapshotting mode during pre-scan interview:

![snap](https://github.com/user-attachments/assets/c24d297d-d52e-45e1-9770-97229abcc2ce)

## Screenshotting 

Screenshotting, as it says, is basically a process of taking screenshot of domain page. It uses selenium library and its headless browser mode in order to take screenshot. It is crucial to configrate its parameters correctly (read "Configuration file" paragraph, "Config file content" section). After scan ends, you will find screenshot of domain's main page in scan folder.

## Snapshotting: Web copy and Wayback Archive

There are two ways to make a snapshot of target domain using DPULSE. First way is a common snapshot: it saves web-page's copy as a HTML file, so it is fully interactive and contains all web elements like HTML code, DOM structure and so on. Second way is Wayback Archive snapshot. It uses Wayback Machine API in order to get all copies of a website within a certain period of time specified by user like shown below:

![snap1](https://github.com/user-attachments/assets/dd82a133-95a8-4fa4-9dc7-ed18d2768d16)

After scan ends, you will find snapshots of domain's main page in scan folder (in case of Wayback snapshot, there'll be additional folder to store all snapshots).
