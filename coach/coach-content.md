# Replay Suite: the coach's layer

This file holds the poker explanations for the Replay Suite documentation. Stat names are written exactly as the extension shows them. Every number given as a band is a rough guide for ReplayPoker play-money tables, not a rule.

A note on the tables these numbers come from. Replay is free chips, 6-max, 9-max and 10-max, ring games and tournaments, with 10 to 12 seconds to act and no time bank. Players see more flops and call more often than at a real-money table. Where that changes the advice, the entry says so. Do not carry cash-game numbers across as if they applied.

---

## A. Glossary

### How to read any stat on the screen

Every stat is shown as a percentage next to a small fraction, such as `31% · 14/45`. The fraction is the whole story. The number on the right is how many times this player faced that decision. The number on the left is how many times they took it. The percentage is one divided by the other. A stat with a small right-hand number is a rumour, not a fact. The reliability bar under a stat fills as that right-hand number grows.

Two words come up constantly and are worth fixing now.

**Opportunity.** A spot where the player could have done the thing. The extension only counts a decision when the player actually had it. If they were already all-in, or never faced a raise, the spot is not counted at all.

**Aggressor.** The player who made the last raise before the flop. The blinds do not count. If nobody raised, there is no aggressor that hand. Every continuation-bet stat is measured against this one player.

### Before the flop

**VPIP** (Voluntarily put money in pot)
How often this player chooses to put chips in before the flop, out of every hand they were dealt. Posting a blind does not count, and checking in the big blind does not count. 60 means they play most hands. 15 means they are very picky. At Replay, 35 to 45 is common and is not a sign of anything unusual.

**PFR** (Preflop raise)
How often this player raises before the flop, out of every hand they were dealt. Any raise counts, including a raise over a limper. Read it next to VPIP. A player at 40 VPIP and 8 PFR calls a lot and raises little. A player at 25 VPIP and 20 PFR raises nearly every hand they play. At Replay, PFR is often well below VPIP.

**RFI** (Raise first in)
When nobody has raised or called in front of them, how often this player raises rather than calling or folding. This is the cleanest measure of how they open a pot. A high number means they like to take the lead. Shown on the HUD's expanded panel by seat group as well, since a good player opens far more from the button than from under the gun.

**Limp** (Limp first in)
Same spot as RFI: nobody has entered the pot yet. How often this player calls the big blind instead of raising or folding. Limping first in is common at Replay and rare among strong players. A high number here tells you the player wants to see flops cheaply. Their raises, when they come, deserve more respect.

**OL** (Overlimp)
Somebody has already limped and nobody has raised. How often this player calls along. A high number says they follow the crowd into multiway pots. Expect many of these players at a Replay 9-max table.

**LF** (Limp then fold)
The player limped, somebody raised behind them, and they still had chips. How often they gave up. Around 30 to 60 is a rough middle. Above that, their limps are weak and a raise behind them wins the pot often. Below that, they call raises after limping, and you will see a flop against them.

**CC** (Cold call)
Somebody has raised and this player has not yet put chips in. How often they call. Calling a three-bet cold counts too. A high number, above 25 or so, is a caller who wants to see a flop with the raiser. At Replay, expect this number to run high.

**SQZ** (Squeeze)
One raise is in and at least one player has called it. How often this player re-raises. It is a strong move because two players have to fold. A number above 10 marks someone who attacks callers. Most Replay players sit near zero. Shown below 3-bet on the Preflop tab, because it is a special case of it.

**3B** (3-bet)
Exactly one raise is in. How often this player re-raises. 5 to 11 is a rough guide at 6-max, a little less at a full table. A player at 2 only re-raises with premium hands, so their re-raise means aces, kings or close. A player at 15 re-raises light and can be re-raised back.

**F3B** (Fold to 3-bet)
This player opened the pot with the first raise, somebody re-raised, and they still had chips. How often they folded. 45 to 65 is a rough middle. A high number means their opens are wide and a re-raise sends them away. A low number means they call re-raises, and you should re-raise them for value rather than as a bluff.

**C3B** (Call 3-bet)
Same spot as F3B. How often they called. Together with F3B and 4B it covers every answer to a re-raise, so the three add up to roughly 100.

**4B** (4-bet)
This player faces a re-raise, either after opening or cold, and still has chips. How often they raise again. Rare at any table. The HUD shows no colour for it because the sample never gets large enough to mean much.

**F4B** (Fold to 4-bet)
This player three-bet and somebody raised again. How often they folded. Very small samples. Treat any number here as a hint, not a read.

**C4B** (Call 4-bet)
Same spot as F4B. How often they called.

**5B** (5-bet)
This player faces a four-bet and still has chips. How often they raise again. Almost always an all-in. You will rarely see enough of these to read anything from the number.

**ATS** (Steal attempt)
The player is in the cutoff, on the button or in the small blind. Nobody has entered the pot. How often they raise. 35 to 55 is a rough middle at 6-max, a little less at 9-max or 10-max. A low number means their late raises are as strong as their early ones. A high number means they raise from late seats with many hands, and the blinds can fight back.

**FvS** (Fold to steal)
The player is in a blind and faces a first-in raise from a late seat. How often they fold. 40 to 60 is a rough middle. A player at 80 gives up their blind almost every time, so a raise from the button against them is nearly free money. A player at 25 defends often, so raise them for value.

**BD** (Defend blind)
Same spot as FvS. How often the player calls or re-raises. It is the other half of FvS, so the two add to roughly 100.

**Folded to you** (decision bar, Preflop tab)
Every time the pot was unopened when it reached this player. The bar splits those spots into Raise, Limp and Fold. The big blind checking is not shown, since that is not a choice about entering the pot.

**Facing an open** (decision bar, Preflop tab)
Every time this player's first decision came against exactly one raise. Split into 3-bet, Call and Fold.

**Facing a 3-bet** (decision bar, Preflop tab)
Every time this player opened the pot and got re-raised. Split into 4-bet, Call and Fold.

**Open sizing** (chart, Preflop tab)
When this player made the first raise, how big it was as a multiple of the big blind. Buckets run from 2 to 2.5x up to 5x and more. A player whose bar sits at 5x+ raises big. At Replay, large opens are common and often mean a strong hand.

**Re-raise sizing** (chart, Preflop tab)
When this player re-raised, how big it was compared to the raise they faced. Buckets from 2 to 2.5x up to 4x and more, plus All-in. A player who re-raises only by moving all-in tells you something about how they think about the hand.

### After the flop

The same thirteen stats exist for the flop, the turn and the river. On the HUD they carry a letter first: `F CB` is the flop continuation bet, `T CB` the turn, `R CB` the river. They are separate numbers because they are separate decisions. A player who bets nearly every flop and rarely bets the turn is telling you something.

**CB** (Continuation bet)
This player was the last raiser before the flop, and on this street nobody has bet yet. How often they bet. On the flop, 50 to 70 is a rough middle. A player at 85 bets almost every flop after raising, whether they hit or not. A player at 30 mostly checks and bets when they have something.

**Brl** (Barrel again)
Turn and river only. This player made a continuation bet on the previous street and again faces a street where nobody has bet. How often they bet again. A player who bets the flop 80 and the turn 30 gives up on the turn a lot. Calling their flop bet and seeing what they do next is a reasonable plan.

**dCB** (Delayed c-bet)
Turn and river only. This player was the raiser, checked the previous street, and now has the chance to bet. How often they do. A high number marks a player who checks the flop and bets the turn. A low number says once they check, they are done.

**FvCB** (Fold to c-bet)
The raiser bet first on this street and this player faced it with chips. How often they folded. On the flop, 35 to 50 is a rough middle. A player at 65 folds to most continuation bets, so betting the flop after raising works against them. A player at 20 almost never folds a flop, and betting without a hand is throwing chips away.

**CvCB** (Call c-bet)
Same spot as FvCB. How often they called.

**RvCB** (Raise c-bet)
Same spot as FvCB. How often they raised. 6 to 14 on the flop is a rough middle. Below 5 means a raise here is a very strong hand. Above 20 means they raise flops with draws and pairs too.

**Bet** (Bet when first)
Nobody has bet yet on this street and this player has the option. How often they bet, whoever raised before the flop. A general measure of whether this player leads out.

**Chk** (Check when first)
Same spot as Bet. How often they checked. The two add to roughly 100.

**XR** (Check-raise)
This player checked and was then bet into. How often their first answer was a raise. 6 to 14 on the flop is a rough middle. A player near zero never check-raises, so their check is an honest sign of weakness. A player at 20 or more uses the check as a trap.

**XC** (Check-call)
Same spot as XR. How often they called. A high number, above 50, is a player who checks and calls down, which is the classic Replay pattern. Bet your good hands for value against them and give up bluffing.

**XF** (Check-fold)
Same spot as XR. How often they folded. A high number means a bet after their check usually wins the pot.

**Donk** (Donk bet)
Somebody else was the raiser before the flop, nobody has bet yet, and this player bets into them. Note that this stat includes spots where the raiser has already checked, which are counted separately under Probe. So the number mixes two different situations, and the HUD shows no colour band for it. Read it as "this player leads into the raiser", and check Probe to see how much of it came after a check.

**Probe** (Probe bet)
This player is not the raiser, and the raiser has checked, either on the previous street or earlier on this one. How often this player takes the lead and bets. 40 to 60 is a rough middle. A low number means they let a checking raiser off cheaply.

**First to act on the flop** (decision bar, street tabs)
Every time this player could open the betting. Split into Bet and Check.

**After checking** (decision bar, street tabs)
Every time this player checked and was bet into. Split into Check-raise, Call and Fold.

**Facing a c-bet** (decision bar, street tabs)
Every time the raiser bet first and this player faced it. Split into Raise, Call and Fold.

**Bet sizing** (chart, street tabs)
When this player made the first bet on the street, how big it was as a share of the pot. Buckets run from under 33% up to 100% and more, plus All-in. Many Replay players bet the same size whatever they hold. Others bet small with weak hands and big with strong ones. A quick look at this chart, then at a few replayed hands, tells you which.

**Raise sizing** (chart, street tabs)
When this player raised on the street, how big the extra amount was compared to the pot after the bet they faced. Same buckets as bet sizing.

**Seen on X of Y hands** (subtitle, street tabs)
How many of this player's hands reached this street with them still in. A player who sees the flop in 60 of 100 hands sees a lot of flops.

**CB paired / CB mono / CB dry / CB wet** (C-bet by board texture, Flop tab)
The flop continuation-bet stat, split by the kind of flop. Paired means two of the three cards match. Monotone means all three are one suit. Dry means few draws are possible, such as K 7 2 with three suits. Wet means many draws are possible, such as 9 8 7 with two of a suit. Strong players bet dry flops far more often than wet ones. A player who bets every kind of flop at the same rate is not looking at the board.

**CB IP / CB OOP** (In position / Out of position, Flop tab)
The flop continuation-bet stat, split by whether the player acts last on the flop or not. Betting is easier when you act last. Most players bet more in position than out of it. If a player's OOP number is as high as their IP number, they bet on habit rather than on position.

### Showdown

**WWSF** (Won when saw flop)
Out of every hand where this player saw the flop, how often they ended up winning chips from the pot, by showdown or because everyone else folded. 43 to 50 is a rough middle. A low number, below 40, is a player who sees many flops and gives up on most of them.

**WTSD** (Went to showdown)
Out of every hand where this player saw the flop, how often they were still in at the end with at least one opponent. 26 to 34 is a rough middle. A high number, above 40, is a player who does not fold once they have seen a flop. Bet for value against them. A low number is a player who folds when pushed.

**W$SD** (Won at showdown)
Out of every showdown this player reached, how often they won. 48 to 58 is a rough middle. Read it with WTSD. A player at 45 WTSD and 40 W$SD goes to showdown a lot and loses most of them, which means they call too much. A player at 20 WTSD and 65 W$SD only goes to showdown with the goods.

**Saw the flop** (Showdown chain, Analytics tab)
Out of every hand dealt, how often this player was still in when the flop came out. The first step of the chain. The three stats above are each measured over the one before it.

**How hands ended** (General tab)
Every hand lands in exactly one of three rows. Folded means this player gave up at some point. Showdown means they went to the end with an opponent. Uncontested means everyone else folded to them. Beside each is the count and the total in big blinds. A player who loses most of their chips in the Showdown row is calling with hands that do not win often enough.

### Aggression

**AF** (Aggression factor)
After the flop, how many bets and raises this player made, divided by how many calls. Every action counts, on every street. A player at 1.0 bets and calls about equally. A player at 3.0 bets or raises three times for every call. 1.8 to 3.5 is a rough middle. Below 1.0 is a player who mainly calls. The badge caps it at 9.9, which means this player almost never calls. A dash means they have not called yet, so there is no ratio to show.

**Aggression by street** (Analytics tab and each street tab)
The same ratio, computed for the flop, the turn and the river separately. A player who is aggressive on the flop and passive on the river is common. It usually means their river bets are real.

### Tournament

**M-ratio** (Analytics tab, tournament hands only)
Your stack at the start of the hand, divided by what one full round of the table costs you in blinds and antes. An M of 10 means you can sit through ten rounds before the blinds eat your stack. It is the single most useful number for a tournament decision, because it tells you how long you can wait. Ring games have no M, since the blinds never go up.

**Harrington zones** (the coloured bands on the M-ratio chart)
Green is an M above 20. Yellow is 10 to 20. Orange is 6 to 10. Red is 1 to 6. In the green you play ordinary poker. In the yellow, hands that need to see a cheap flop start to lose value. In the orange, your main move is raising all-in first into the pot. In the red, the first reasonable hand goes all-in, and the blinds decide for you if you wait.

**Stack depth** (Analytics tab, all formats)
Your starting stack for each hand, in big blinds, grouped into four bands: 50+ BB, 25 to 50 BB, 10 to 25 BB and under 10 BB. The chart shows how you did in each band. This is different from M-ratio. It is measured in big blinds only, it ignores antes and table size, and it exists for ring games too.

### Results

**Hands**
How many hands the extension holds for this player. On the HUD badge it is the third default number. It is the ceiling for every other stat, since no stat can have a sample larger than this. Most stats have a much smaller sample, because most spots do not come up every hand.

**Net**
Chips won or lost, over the hands the extension has settled. On the General tab, the hint underneath gives the same total in big blinds and the number of hands it covers. For another player, this is only their result in hands you were both dealt into, which is not their overall record.

**BB/100** (big blinds won per 100 hands)
Net result in big blinds, divided by hands, times 100. It lets you compare a session at 50/100 with a session at 500/1000. Ring games only. In a tournament the big blind rises through the event, so a rate per 100 hands would compare nothing with nothing.

**By position** (General tab)
Big blinds won or lost from each seat, with the number of hands behind each bar. UTG is first to act, then UTG+1, UTG+2, MP, MP+1, HJ, CO, BTN, then SB and BB. Almost every player loses from the blinds and wins most from the button. What matters is the size of each.

**Results over time** (Analytics tab)
Your running total in big blinds, one point per hand, in the order the hands were played. Click a point to open that hand in the replayer.

**Starting hands** (Analytics tab and Range tab)
A 13 by 13 grid, one cell for each of the 169 possible starting hands. Suited hands sit above the diagonal, pairs on it, offsuit hands below. Blue is a hand you have won with, red one you have lost with, empty means never played. Hover a cell to see the count and the total.

**Range width** (Range tab)
The share of all 1,326 possible two-card holdings your selection covers. Pairs have 6 ways to be dealt, suited hands 4, offsuit hands 12, so a selection of 20 cells can be a wide range or a narrow one.

**General and SP** (HUD badge)
General is every hand the extension holds for the player. SP is only the hands that match the table you are at now: same number of seats, and bounty tournaments kept apart from everything else. The badge shows SP only when every stat on it has a big enough sample there. Otherwise it shows General and says so.

---

## B. Coach's opinion cards

### Card: Why bother recording hands

You already remember the hand where your aces got cracked. You do not remember the forty hands where you called a raise from the small blind and quietly lost a few chips each time. Memory keeps the dramatic hands and drops the expensive ones. A record keeps all of them, with the same weight. That is the whole reason to do this. It is not about playing like a professional. It is about seeing your own game the way an honest friend at your shoulder would see it, and noticing the one or two habits that cost the most. Record for a week before you look at anything. Then look.

### Card: The three numbers to start with

The badge shows three things by default: VPIP, PFR and the hand count. Read them in reverse. The hand count first, because it tells you whether to believe the other two. Under 30 hands, treat them as a first impression. VPIP next: how many hands does this player enter? At Replay, 40 is normal. 60 is loose. 20 is tight for these tables. Then PFR: of the hands they play, do they raise or call? A big gap between VPIP and PFR, say 45 and 8, is a caller. A small gap, say 25 and 20, is a raiser. That one comparison tells you more than any other single number on the badge.

### Card: How many hands before you trust a number

Every stat has its own floor, the smallest sample before the extension will show it at all. VPIP needs about 15 hands. Fold to 3-bet needs 12 times of actually being re-raised after opening, which can take 300 hands to collect. The reliability bar under each stat fills from the floor up, and reads full at several times the floor. An empty bar is a hint. A full bar is a read. Between the two, ask whether the number would surprise you if it moved ten points. If it would, wait. Sample size is the only honest defence against being fooled by a player's last three hands.

### Card: Reading a very loose player

A badge like VPIP 62, PFR 10, WTSD 45 describes a player who enters most pots, mostly by calling, and does not fold once they have seen a flop. Bluffing them is expensive. Value betting them is where your chips come from. Bet your good pairs and better on every street and size those bets larger than you would against anyone else, because they are paying to see your hand. Do not slow-play. They will call anyway. The one thing to respect is a raise from them, especially on the turn or river, because a player who calls everything only raises when they have it. Check their XR and RvCB to confirm.

### Card: Reading a very tight player

A badge like VPIP 14, PFR 11, F3B 75 describes a player who waits for good cards, raises when they get them and lets go when re-raised. Their raise means a real hand, so fold hands you would call with against anyone else. Their fold rate is the opportunity. Raise their blinds from the button. Re-raise their opens when you have position, because F3B 75 says they give up three times in four. After the flop, if they check, bet. They rarely check strong hands. Tight players at Replay are less common than loose ones, and they are often the ones who have been playing a long time. Respect their bets and attack their folds.

### Card: What "by position" is telling you

The chart on the General tab shows big blinds won or lost from each seat. Nearly everyone loses from the small blind and the big blind. That is the price of the blinds. You paid before you saw your cards, and you act first on every later street. The useful question is how much. If the blinds lose more than the button wins, the blinds are calling too many raises. The button should be your best seat, because you act last on every street. If it is not, look at your hands from there. Under the gun (UTG) should be close to even or a little positive, because you are supposed to enter only with strong hands.

### Card: What BB/100 means and why we use it

Chips won tells you the result. It does not tell you the rate, and it cannot compare a session at 50/100 blinds with a session at 500/1000. BB/100 fixes that. Take your net in big blinds, divide by the hands, multiply by 100. Now every ring session is on the same scale. A winning Replay player might run 10 to 20 BB/100 over a large sample, because the calls are looser than at a real-money table. Do not read anything from a few hundred hands. The rate swings wildly before a few thousand. It is ring-only, because a tournament's big blind keeps rising, so a rate per 100 hands would mean nothing there.

### Card: Which hands are worth replaying

Not the big wins. You already know how those went. Replay three kinds of hands. First, the big losses, and ask one question: was there a street where a fold would have saved most of it? Second, the hands where you called on the river and lost, because that is where most chips leave a Replay stack. Third, the medium pots you won without a showdown, because those show you which bets worked. Use the stat filters. Click a stat on any street tab, choose "Only where you took it", and the Hands tab shows exactly those spots. Ten hands chosen that way teach more than a hundred scrolled through.

### Card: Pot odds in one minute

The Decision panel shows four lines. Pot is what is in the middle. To call is what it costs to stay. Equity needed is the share of the time you must win for that call to break even. If the pot is 600 and the call is 200, you put in 200 to win 800, so you need to win one time in four, or 25 percent. Compare that to how often your hand wins. A flush draw on the flop wins about 35 percent by the river, so it clears 25. SPR is the stack divided by the pot. Below 3, you are usually committed with a good pair. Above 10, you can wait.

### Card: Equity, and why "shown hand" matters

Equity is your chance of winning the pot if all the cards were dealt out. It only means something against a specific set of opponent cards. The panel offers three ways to fill that in. "Shown hand" uses the cards the opponent turned over at showdown, so it invents nothing. But on the flop you did not know those cards. The panel says "hindsight" for that reason. "A range" is your own guess at what they might hold, and you can see what you assumed. "Seen with" builds a range from what this player has shown in your archive, which is slanted toward strong hands, since weak ones get folded before showdown. Use it with care.

### Card: Results over time, and variance

The curve on the Analytics tab is your running total, one point per hand. Look at its shape, not one point. A gentle upward slope with bumps is a winning player having a normal week. A steep drop is usually two or three big pots. Click the point to open the hand. Variance is the word for the swings that happen even when you play well. At Replay, with loose calls and big pots, the swings are larger than at a tight table. A few hundred hands can show a loss for a good player and a win for a poor one. Judge yourself over thousands of hands, and judge each decision in the replayer, not by how it ended.

### Card: Stack depth: why the same hand plays differently at 12 BB and 80 BB

With 12 big blinds, ace-jack is a hand you push all-in with before the flop and never see the flop with. With 80 big blinds, the same hand is a call or a modest raise, and the decisions come after the flop. Small pairs go the other way. At 80 BB they are worth a call to try for a set, because the pot can grow large if you hit. At 12 BB there is no room for that. The Stack depth chart shows your result in four bands, from 50+ BB down to under 10 BB. If one band is bleeding, click it, and every tab narrows to those hands.

### Card: M-ratio for tournament players

M is your stack divided by the cost of one full round of blinds and antes. It answers the only tournament question that matters: how long can I wait? The chart bands it the way Dan Harrington did. Green, above 20, is normal poker. Yellow, 10 to 20, is when you stop calling raises with hands that need a cheap flop. Orange, 6 to 10, is when the raise-and-fold game ends and your main move is all-in first into the pot. Red, under 6, means the next reasonable hand goes in. At Replay, players sit in the yellow and orange far longer than they should, calling and hoping. Watch your own colour and act before it turns.

### Card: Aggression factor, what it is and is not

AF is bets plus raises, divided by calls, after the flop. It is a ratio, not a percentage. A 2.0 means this player bets or raises twice for every call. What it tells you is style: does this player push or follow? What it does not tell you is how often they bet. A player who checks nine times and bets once, never calling, has an AF of infinity and the badge shows 9.9. Read it with the Bet and Chk stats on each street. A low AF, under 1.0, at a Replay table is a calling station. Value bet them and stop bluffing. A high AF with a low VPIP is a player who bets when they have it.

### Card: The Range tab: what a 13 by 13 grid shows

The grid has 169 cells, one for every starting hand that plays the same way. Pairs run down the diagonal from AA to 22. Suited hands sit above it, offsuit hands below. Suited means both cards in one suit. K9s is the cell for a king and a nine of the same suit. Each cell is shaded by how you have done with that hand, blue for won, red for lost, empty for never dealt. Click cells, or drag across them, to build a selection. Range width tells you what share of all possible holdings that is. Then apply it, and every tab shows only hands where you held one of those. Try selecting your red cells and asking why.

### Card: Play money is still poker

The cards do not know the chips are free. A flush still beats a straight, a raise still asks the same question, and the pot odds are the same arithmetic. What changes is the people. Replay players call more, see more flops and fold less on the river, because losing costs nothing but chips that come back tomorrow. That makes some real-money advice wrong here. Bluffing works less. Value betting works more. Thin folds matter less than thin calls. Studying your play-money hands teaches you how the game works and how you actually behave under a clock. Both carry over. The habits you build here are the habits you will bring anywhere.

---

## C. Spoken lines for two videos

### Video segment: the HUD, what the badge is telling you

Next to each player, you will see a small badge with three numbers. The first is VPIP. That is how often this player puts chips in before the flop, out of every hand they are dealt. The second is PFR, how often they raise. The third is the hand count, how many hands we have on them.

Start with the hand count. Under thirty, treat the rest as a first impression.

Now look at the two percentages together. Here is a player at 58 and 7. They enter most pots and almost never raise. That is a caller. Bet your good hands against them and do not bother bluffing.

Here is another at 16 and 13. They play few hands and raise most of the ones they play. When this player raises, believe them. When they fold, which they do a lot, take the pot.

Click the badge and it opens. Under each stat there is a small bar. That is the reliability bar. It fills as the sample grows. An empty bar is a rumour. A full bar is a read.

### Video segment: the stats tabs in three minutes

Open the dashboard and start on General. Across the top are your headline numbers. Look at VPIP and PFR first, then Net. Below them, the chart by position. You will lose from the blinds. Everyone does. The question is whether the button pays for it.

Now click Flop. The three bars at the top are your decisions. First to act, after checking, and facing a continuation bet. Under those, each stat shows a percentage and a fraction. The fraction is the sample. Click any stat, and you can filter the Hands tab to the exact hands behind it. That is the fastest way from a number to a lesson.

Last, Analytics. The curve at the top is your result over time. Look at the shape, not the wiggles. Below it, stack depth, which tells you where the chips come from. If you play tournaments, the M-ratio chart shows how much time you had, in colours.

Three tabs, three questions. Who am I? Where does it happen? And is it working?
