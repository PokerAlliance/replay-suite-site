# Settings and your data

Click the icon, then <kbd>Settings</kbd>. Settings opens in its own tab with six sections: Data, Appearance, Recording, Background, HUD, Danger zone.

<!-- VIDEO: V4 Deep dive, chapters "Back up, restore, import" to "Retro, recording, danger zone" -->

## Back up

!!! careful "Read this one"
    Your hands are stored only in your browser, on this computer. If you reinstall the browser, switch computers, or clear your browsing data, they are gone. Unless you have a backup file.

1. Click the icon, then <kbd>Back up</kbd>. (Also in Settings, Data.)
2. The browser saves one file, named like `replay-suite-backup-2026-09-21.rsb.gz`.
3. Keep it wherever you keep photos. That is all.

The add-on reminds you in the popup when you have played a lot since the last backup. One click, done.

<!-- SHOT: popup-backup-reminder.png -->

## Restore

Restore puts a backup file back, for example on a new computer.

It **replaces** everything currently stored, so the add-on shows you what is about to be replaced and asks you to type `REPLACE` before it goes ahead. It also saves a copy of the current data first, so a mistake can be undone.

## Import

Import **merges** hands from a file into what you already have. Nothing is replaced, and the same hand is never stored twice.

If you used the older ReplayTracker tool, its exported files go in here.

## Export for other trackers

Writes your hands in PokerStars hand-history format, which most poker software reads. Export everything, one session, or one hand from the replayer.

## Recover from ReplayPoker

Fetches hands and tournament results from Replay's own history pages. It is the same thing the welcome screen offered. Run it again any time, for example after a bad connection lost a few hands.

## Background

The add-on does some work when you are not at a table: bringing in old hands, checking tournament results, fetching skipped hands. This section shows what is running now and lets you pause it.

The slider is how hard the add-on is allowed to work Replay's servers. Slow is the default and it is the polite setting. Faster is allowed, and the page tells you what it costs.

<!-- SHOT: options-background.png -->

## Appearance

**Retro mode** is the dark look Replay used to have. On or off, takes effect at once, no reload.

<!-- SHOT: retro-before-after.png -->

## Recording

**Record hands automatically** is on from the start. Turn it off if you want to play without saving for a while. Everything already saved stays.

## HUD

Everything about the badge at the table. It has its own page: [The HUD](hud.md).

## Danger zone

**Delete everything** removes every hand, session, tournament and setting from this browser. Two clicks. It cannot be undone, which is what backups are for.

Uninstalling the add-on also removes its data.

## Support

The add-on is free and stays free. <kbd>Support</kbd> in the popup opens a small screen with links for saying thanks and for sending feedback. They are ordinary links. Nothing is loaded from those sites unless you go there.
