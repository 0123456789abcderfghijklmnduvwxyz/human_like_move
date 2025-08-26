# human_like_move
Moves your mouse kinda like a human not really tho, its probably detectable but for the account automation tasks i've done it was good enough. Its fully vibe coded, so if something doesnt work or you want to change something go on lmarena.ai and just ask GPT-5-high for help cause i aint helping you.

Here are some values it gave me for diffrent distances, you can test it out yourself. If you want to find a specific point on your screen, so that you can move to it, screenshot your entire screen and go on https://imageonline.io/find-coordinates-of-image/, cause im too broke to buy photoshop and Gen-P doesnt work anymore i had to use that one, anyways here are the values: 

Big move (~400–1200 px): curvature=0.15–0.25, jitter=0.05–0.12, jitter_px_cap=16–24, jitter_decay=0.8–1.0, jitter_cycles=(1.5, 3.0).

Short move (<80 px): jitter=0.12–0.25, jitter_min_px=1–2 px, jitter_px_cap=8–12, jitter_cycles=(2.0, 4.0).

Also you should set the FPS to 1000 or so, it doesnt really matter i think, it just makes everything smoother and it didnt have any impact on my performance. Here are some example calls i used in my code if you need some, you just have to change the x and y coords:

human_like_move(x=random.randint(846, 1059), y=random.randint(541, 557), duration=random.uniform(0.3, 0.9), fps=1000, curvature=0.1, jitter=0.18, jitter_min_px=1, jitter_px_cap=9, jitter_cycles=(2.0, 4.0), jitter_decay=0.9)

human_like_move(x=random.randint(838, 1061), y=random.randint(461, 481), duration=random.uniform(0.7, 2.2), fps=1000, curvature=0.19, jitter=0.09, jitter_px_cap=15, jitter_min_px=1, jitter_cycles=(1.5, 3.0), jitter_decay=0.85)
