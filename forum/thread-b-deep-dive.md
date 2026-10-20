<!--
Thread B, post 1: the deep dive. General Poker Discussion, open for replies.
Posted BEFORE Thread A, because Thread A links here.

Do not paste this file. Run   python3 forum/check.py   and paste forum/out/thread-b-deep-dive.md.
Extra template tag here:  {{coach:Card title}}  a Coach's opinion quote from coach/coach-content.md
-->

{{img:hero|Replay Suite: every hand you play on ReplayPoker, saved and explained}}

Hello everyone,

This is the home thread for **Replay Suite**: questions, bug reports, ideas, and news of each new version. The short introduction is in the showcase thread; this post is the full walkthrough, one feature at a time, with pictures. You don't need to read it all. Open the parts you are curious about.

Post 2, just below, is the **status board**: the latest version, known bugs and planned ideas. The always up to date version of it is on the website: {{site:status/}}

{{img:separator|}}

{{img:section-01|01 Installing it: Firefox, Chrome and Edge}}

**Firefox** installs from Firefox Add-ons in one click, and updates itself.

{{link-img:button-firefox|Firefox: install in one click|amo}}

**Chrome and Edge** install it by hand, because the Chrome store has not accepted it yet (it treats anything under the casino.org address as gambling, even though Replay is play money). It takes about three minutes, once.

{{link-img:button-chrome-edge|Chrome and Edge: download the latest version|latest-zip}}

[details="Show me the Chrome and Edge steps"]

1. Download the file with the button above. It is called `replay-suite-chrome.zip`.
2. **Unzip it** somewhere you will not delete later. Your Documents folder is fine. Chrome keeps using this folder, so don't move it afterwards.
3. Type `chrome://extensions` (or `edge://extensions` in Edge) in the address bar and press Enter.
4. Switch on **Developer mode**: top right in Chrome, on the left in Edge.
5. Click **Load unpacked** and choose the folder you unzipped.
6. Click the puzzle piece at the top right of the browser and pin Replay Suite so it stays visible.

{{img:shot-chrome-extensions|chrome://extensions with Developer mode on and Replay Suite loaded}}

Chrome shows a message on startup about "developer mode extensions". That is normal for anything installed this way. Click it away.

**Updating** on Chrome and Edge is by hand too, about two minutes: back up, download, unzip over the same folder, click the round reload arrow. Never click Remove, because that deletes your hands. Every step with pictures: {{site:updating/}}

[/details]

Pictures for every click, for all three browsers: {{site:install/}}

{{img:separator|}}

{{img:section-02|02 Your first day: what happens when you sit down}}

Click the Replay Suite icon at the top of your browser. The first time, it shows a short welcome.

{{img:shot-popup|One click on the icon: your library, Retro mode, and the dashboard}}

1. **Recording is on from the start.** Play as normal. Every hand you are dealt into is saved as it finishes. There is nothing to click.
2. **It can fetch the hands you have already played.** Replay keeps your last 200 hands and your tournament history. The welcome screen offers to bring those in so you don't start from zero. Say yes.

{{img:separator-thin|}}

**A note on the first week.** Numbers about other players only appear once you have seen them play enough hands. Until then the add-on shows a dash rather than guess. A number built on 8 hands is worse than no number.

{{coach:How many hands before you trust a number}}

{{img:separator|}}

{{img:section-03|03 The dashboard: every hand, and what it says about your game}}

Click the icon, then **Open Dashboard**. Left side: your sessions and tournaments. Top: the tabs. Top right: whose hands you are looking at.

{{img:shot-dashboard|The General tab: your headline numbers, your result by seat, and how your hands ended}}

**General** is the overview: how many hands, how it is going, which seats are making you chips and which are costing you. Every number is a link to the hands it was counted from.

{{coach:What "by position" is telling you}}

[details="The other tabs: Hands, Analytics, Tournaments, Range and the street tabs"]

**Hands** lists every hand, newest first. Click one to replay it. The buttons above the list narrow everything down: only tournaments, only 6-max, only the last 30 days, only hands that went to showdown, and so on.

{{img:shot-hands|Every hand in one list. Click one to replay it.}}

**Analytics** is charts: your results over time, how you did at different stack sizes, and a few things the poker books talk about. Each chart has a short line under it saying what it shows.

{{img:shot-analytics|Results over time, by stack depth and by blind level}}

{{coach:Results over time, and variance}}

**Tournaments** lists each tournament you have played, where you finished, and what it cost or paid.

{{img:shot-tournaments|Every tournament: entries, results and your best finishes}}

**Preflop, Flop, Turn and River** are the detailed numbers, street by street. You do not need them to get value from the add-on. They are there when you are curious, and every stat is one line in the glossary: {{site:glossary/}}

{{img:shot-preflop|How you play before the flop, spot by spot}}

**Range** is a grid of all 169 starting hands, shaded by how each one has done for you. Pick a group and every tab narrows to those hands.

{{img:shot-range|Pick a group of starting hands and see how they did for you}}

[/details]

**Viewing as** (top right) lets you pick any player you have shared a table with. The whole dashboard then shows their hands, as you saw them. Useful before a rematch.

{{img:shot-viewing-as|Look at any opponent's numbers from the hands you played together}}

{{img:separator|}}

{{img:section-04|04 The replayer: watch any hand again, step by step}}

Click any hand to replay it like a video: seats, stacks, the pot and the board, with the action written out on the right. Click any line to jump there.

{{img:shot-replayer|Watch any hand again, step by step, with the odds worked out}}

The **Decision** panel shows, at every step, the pot, what it costs to call, and the share of the time you need to win for that call to be worth it.

{{coach:Pot odds in one minute}}

[details="Equity, and the three ways it is worked out"]

When there is something honest to work it out from, the replayer also shows your **equity**, your chance of winning the pot:

- **Shown hand**: the opponent later showed their cards, so it can tell you your real chances on each street, before you knew.
- **A range**: pick the hands they might have had, and see your chances against those.
- **Seen with**: your chances against the hands you have actually seen this player show down before.

{{coach:Equity, and why "shown hand" matters}}

**Download as PokerStars** exports any hand for other poker software.

[/details]

{{img:separator|}}

{{img:section-05|05 The HUD: a few numbers about each opponent}}

Switch it on in Settings, HUD, **Show stats on the table**. A small badge appears under every player you have history with. Point at it and it opens up with the names of the numbers.

{{img:shot-hud|At the table: a small badge under each player you have played with}}

If you are new to this, start with three numbers:

- **VPIP**: how often this player puts chips in before the flop. 60 means they play most hands. 15 means very picky.
- **PFR**: how often they raise before the flop rather than call. A big gap between VPIP and PFR means a caller, not a raiser.
- **Hands**: how many hands the numbers are built on. Under 50, take them with a pinch of salt.

{{coach:The three numbers to start with}}

[details="Choosing what the badge shows"]

Settings, HUD. Two layouts, one for 6-max and one for full tables, because a full table has less room. Add a stat, choose its row, and the preview shows what the badge will look like.

{{img:shot-settings-hud|Choose what the badge at the table shows}}

- The badge sits behind the cards and chips, never on top of them, and never where the Fold, Call and Raise buttons are.
- It dims until you point at it.
- Your own badge is off by default (your numbers are on the dashboard). You can turn it on.

[/details]

{{img:separator|}}

{{img:section-06|06 Settings and your data: back up, restore, Retro mode}}

Click the icon, then **Settings**.

**Back up.** This is the one setting I will ask you to actually use. Your hands are stored only in your browser. If you reinstall your browser, switch computers, or clear your browsing data, they are gone, unless you have saved a backup file. It is one button: **Back up**, in the popup or in Settings, Data. Keep the file wherever you keep photos. **Restore** puts it back.

{{img:shot-settings-data|Your library, back up and restore}}

[details="Retro mode, importing, exporting and background work"]

**Retro mode** is the dark look Replay used to have. Switch it on in the popup or in Settings. It takes effect the next time you open or reload a Replay page.

**Import and Export.** Files from the older ReplayTracker tool import here. You can also export hands in PokerStars format.

**Background work.** Fetching your old hands and tournament results takes requests to Replay's servers. The add-on does this slowly on purpose, never while you are sitting at a table, and you can see what it is doing and pause it in Settings, Background.

**Delete everything** is in the Danger zone tab, in red.

[/details]

{{img:separator|}}

{{img:section-07|07 Fair play and privacy: what it sees, and what it never does}}

{{img:trust-strip|Not a bot. Never sees hidden cards. Nothing leaves your computer. Replay staff know about it.}}

**Is it cheating?** No. Everything it shows you is something you could see with your own eyes and write down with a pen: which hands a player played, what they showed at showdown, how often they raise. It does the writing for you, and the arithmetic. It never sees hidden cards and it never acts for you.

**Does it collect anything?** No. There is no account, no server, no analytics, no adverts, nothing that phones home. The only website it talks to is Replay itself, with the login you already have, to fetch your own history. The privacy policy is short: {{site:privacy/}}

**Who made it, and what does it cost?** Me, on my own time. It is free and will stay free: no premium version, no adverts. If you would like to say thanks, there is a Support button in the add-on. Entirely optional.

{{coach:Play money is still poker}}

{{img:separator|}}

{{img:section-08|08 Updates, bugs and ideas: where to find what changed}}

- **Every version**, what changed in it, and its download: {{site:versions/}}
- **Known bugs and planned ideas**: post 2 below, and always current on {{site:status/}}
- **Found a bug?** Reply here. Say which browser you use and what you were doing when it happened.
- **Have an idea?** Reply here too. Every idea gets a number on the status page, so you can follow it.

**"I installed it and nothing happened."** Reload the Replay page once. If the icon is not at the top of your browser, look under the puzzle piece (Chrome, Edge) or the extensions button (Firefox) and pin it.

**"The badge is not showing for someone."** You do not have enough hands with them yet. It appears once there is something worth saying.

**"A hand is missing."** Hands that arrive damaged (a bad connection, a page reload in the middle of a hand) are skipped rather than stored wrong. The add-on fetches them back from Replay later, when it can.

Thanks to the Replay staff for their patience with my questions, and to the players who tested early versions and told me what was wrong with them.

See you at the tables.

ThonBl7ror

<small>Replay Suite is free. It is not affiliated with ReplayPoker. [Privacy]({{site:privacy/}}) · [Website]({{site:}})</small>
