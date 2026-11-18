import random
import tkinter as tk
from tkinter import font as tkfont

BG = "#05060a"
FG = "#39ff88"
ACCENT = "#7a5cff"
MUTED = "#8a93a6"

QUOTES = [
    "Let's double down on synergy, align our lightsabers, and scale toward the same KPI.",
    "Moonwalk out of yesterday’s constraints and right into tomorrow’s opportunity.",
    "We’ll stay proactive, mitigate risks, and keep our strategy clean of black mold.",
    "Let's disrupt the loop, break out of Groundhog Day, and move the needle.",
    "Inject the bag—secure the value, deliver the ROI, and add serious upside.",
    "Park the lightsabers, leverage synergy, and turn this into a win-win.",
    "Smooth execution, no tripping over your own moves. Dancing forward to the next big thing!",
    "You just pulled off a cross-border pivot. You’ve got home field advantage now.",
    "We take that energy, channel it into our goals, and ignite the next stage of success.",
    "Let’s be the spark, light up that path, and keep everything running hot—just in a safe, scalable way!",
    "Your majesty of scales, let’s keep climbing, leveraging every step, and making sure we scale smarter, not harder.",
    "Norway, Node 4, Q999—let’s line them up and keep climbing those mountains.",
    "Order Synergy: aligning forces, executing big wins, and building something that stands the test of time.",
    "I'll take anybody's beef, make a sloppy Joe.",
    "From ancient echoes, we spin a song... ancient in theme, but always in boots.",
    "Dodge the red light, run on green, and make sure we’re scaling smarter—not harder.",
    "I stand by nothing, and I stand by that. Standing by nothing means you’re ready to reinvent everything.",
    "Let’s flip it for real—take that energy, spin it positive, and craft something you’ll be proud to stand behind.",
    "Whether it’s a punchline or a big move, we’re aiming for that direct hit.",
    "No knots, no limits—we keep it flexible, and you guide where we go.",
    "We’re on your timeline, and when you’re ready to move, we’ll pivot right into action.",
    "Who needs gravity when growth keeps you grounded and moving upward?",
    "We’re not writing names; we’re writing goals. Let’s focus on what you want to create, not erase.",
    "Cutting through bureaucracy? We’ll find the path of least resistance and make sure we’re achieving real results.",
    "Instead of menacing phantoms, we’ll focus on the vision. Let’s start that saga right.",
    "From 10 to 11, that’s progress! We’re not staying static; we’re leveling up.",
    "Traveling light is a power move. No baggage means you’re free to adapt on the fly.",
]

def do_generate():
    quote_var.set(random.choice(QUOTES))
    status_var.set("KPIs aligned. Synergy achieved.")

root = tk.Tk()
root.title("Synergy Saber")
root.configure(bg=BG)
root.geometry("450x250")
root.resizable(False, False)

title_font = tkfont.Font(family="Consolas", size=16, weight="bold")
mono_font = tkfont.Font(family="Consolas", size=11)

tk.Label(root, text="SYNERGY SABER", font=title_font, fg=FG, bg=BG).pack(pady=(20, 5))
tk.Label(root, text="Corporate Buzzword & Moonwalk Generator", font=tkfont.Font(family="Consolas", size=9), fg=MUTED, bg=BG).pack()

quote_var = tk.StringVar(value="Ready to align your lightsabers?")
tk.Label(
    root,
    textvariable=quote_var,
    font=mono_font,
    fg="white",
    bg=BG,
    justify="center",
    wraplength=400,
    height=4
).pack(pady=10)

tk.Button(
    root,
    text="INJECT THE BAG",
    command=do_generate,
    font=mono_font,
    bg=ACCENT,
    fg="white",
    activebackground=FG,
    bd=0,
    width=20,
    height=2
).pack()

status_var = tk.StringVar(value="waiting for synergy...")
tk.Label(root, textvariable=status_var, font=tkfont.Font(family="Consolas", size=8), fg=MUTED, bg=BG).pack(side="bottom", pady=10)

root.mainloop()
