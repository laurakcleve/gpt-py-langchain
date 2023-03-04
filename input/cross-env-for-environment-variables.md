---
slug: "/cross-env-for-environment-variables/"
title: "How to use environment variables in NPM scripts safely across operating systems"
date: "2021-04-20"
description: "If you've ever been stuck on `NODE_ENV is not recognized` while developing on Windows, this post is for you."
featuredImage: "../images/banner2.png"
---

If you're working with JavaScript, particularly Node, in Windows you might have come across this error before:

```bash
'NODE_ENV' is not recognized as an internal or external command,
operable program or batch file
```

The term `NODE_ENV` might be substituted with something else, but the essence of the problem is that some code is trying to set an environment variable in a non-windowsy way. The most common culprit I've seen is NPM scripts. Something that looks similar to this snippet in a `package.json` file:

```json
"scripts": {
  "build": "NODE_ENV=production webpack"
}
```

On Mac OS and Linux this is a very common way to set environment variables, but we need to make a small tweak for this to work on Windows (unless you are using Bash on Windows or another substitute).

_**Note:** You could use `--mode=production` as a flag for Webpack in particular, but this is just a general common example._

I'm going to show a couple ways to remedy this situation, but if you want my preferred solution without the extra information feel free to skip to the bottom of the article. Also, if you prefer a video I have one here:

<div class="video-container">
  <iframe width="1280" height="720" src="https://www.youtube.com/embed/t9okUDkRUDc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

## Adjusting the script only for Windows

We'll see why this isn't the best way to handle this in a moment, but just to get things running, and for general knowledge, you can get the previous script to work on Windows by changing it to this:

```json
"scripts": {
  "build": "set NODE_ENV=production& webpack"
}
```

The `build` script above has some small changes that are very important. The most obvious is the addition of the `set` keyword at the beginning of the script. This is how you set an environment variable on Windows. The second, more subtle change, is the `&` appended to the environment variable declaration.

This `&` is necessary to tell Windows we want to move on to running another command after setting the variable, very similar to the:

`npm run build && npm serve` format you commonly see in scripts.

**IMPORTANT**: It is not a mistake that there is no space between `production` and `&`. If you were to put a space there, it would set the environment variable to the string `"production "` with a space at the end.

## The problem with the Windows only way

You could stop here in many situations but you have two potential problems before you.

First, anyone using your project on a non-Windows machine essentially has the same problem you just fixed for yourself.

Second, and perhaps more impacting to you, is that any server your scripts run on are likely going to be Linux machines. This means when you deploy your code to your server, none of your scripts will run. Some people opt to just write separate scripts, which works but is a bit clunkier than the common solution, imo.

## The best of all worlds: cross-env

The most universal solve, and in my experience the most common in the JS ecosystem, is to install a package in your project:

```bash
npm i -D cross-env
```

This package allows you to use the `cross-env` command at the beginning of your scripts to make them work across various operating systems. Here's our previous script adapted:

```json
"scripts": {
  "build": "cross-env NODE_ENV=production webpack"
}
```

That's all it takes, really. You can use that on any old script in your `package.json`, and if you'd like to know more about what the package can do just head over to the <a href="https://www.npmjs.com/package/cross-env" target="_blank" rel="noopener noreferrer">cross-env package readme</a>.
