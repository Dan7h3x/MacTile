#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
import subprocess

# Layouts
from libqtile import backend, bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, DropDown, Group, Key, Match, ScratchPad, Screen
from libqtile.lazy import lazy

# Startup ------------------------------


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~")
    subprocess.Popen([home + "/.config/qtile/autostart.sh"])


# Key Bindings ------------------------------

# The mod key for the default config is 'mod4', which is typically bound to the "Super" keys,
# which are things like the windows key and the mac command key.
mod = "mod4"
alt = "mod1"
# Scripts/Apps Variables
home = os.path.expanduser("~")
terminal = "alacritty"
terminalfloat = "kitty"
music_player = "termmusic"
brightness = "brightness"
volume = "volume"
screenshot = "takeshot"
file_manager = "pcmanfm"
text_editor = "kitty -e nvim"
web_browser = "brave-browser-nightly"
notify_cmd = "dunstify -u low -h string:x-dunst-stack-tag:qtileconfig"

colors = {
    "glass": "afafff26",
    "glass2": "afafff60",
    "black": "#000000",
    "red": "#FF3131",
    "white": "#ffffff",
    "purple": "#9457EB",
    "magenta": "#E23DA5",
    "blue": "#4D4DFF",
    "orange": "#F6890A",
}


# resize functions
def resize(qtile, direction):
    layout = qtile.current_layout
    child = layout.current
    parent = child.parent

    while parent:
        if child in parent.children:
            layout_all = False

            if (direction == "left" and parent.split_horizontal) or (
                direction == "up" and not parent.split_horizontal
            ):
                parent.split_ratio = max(5, parent.split_ratio - layout.grow_amount)
                layout_all = True
            elif (direction == "right" and parent.split_horizontal) or (
                direction == "down" and not parent.split_horizontal
            ):
                parent.split_ratio = min(95, parent.split_ratio + layout.grow_amount)
                layout_all = True

            if layout_all:
                layout.group.layout_all()
                break

        child = parent
        parent = child.parent


@lazy.function
def resize_left(qtile):
    current = qtile.current_layout.name
    layout = qtile.current_layout
    if current == "bsp":
        resize(qtile, "left")
    elif current == "columns":
        layout.cmd_grow_left()


@lazy.function
def resize_right(qtile):
    current = qtile.current_layout.name
    layout = qtile.current_layout
    if current == "bsp":
        resize(qtile, "right")
    elif current == "columns":
        layout.cmd_grow_right()


@lazy.function
def resize_up(qtile):
    current = qtile.current_layout.name
    layout = qtile.current_layout
    if current == "bsp":
        resize(qtile, "up")
    elif current == "columns":
        layout.cmd_grow_up()


@lazy.function
def resize_down(qtile):
    current = qtile.current_layout.name
    layout = qtile.current_layout
    if current == "bsp":
        resize(qtile, "down")
    elif current == "columns":
        layout.cmd_grow_down()


ScratchGroups = (
    ScratchPad(
        "SPD",
        dropdowns=[
            # Drop down terminal with tmux session
            DropDown(
                "term",
                terminal,
                opacity=0.9,
                x=0.2,
                y=0.012,
                width=0.65,
                height=0.45,
                on_focus_lost_hide=False,
                warp_pointer=False,
            ),
            # Another terminal exclusively for music player
            DropDown(
                "music",
                terminal + " -e ncmpcpp",
                opacity=0.95,
                x=0.64,
                y=0.25,
                width=0.35,
                height=0.55,
                on_focus_lost_hide=False,
                warp_pointer=False,
            ),
        ],
    ),
)


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Terminal --
    Key(
        [mod], "Return", lazy.spawn(terminal), desc="Launch terminal with qtile configs"
    ),
    Key(
        [mod, "shift"],
        "Return",
        lazy.spawn(terminalfloat),
        desc="Launch floating terminal with qtile configs",
    ),
    # GUI Apps --
    Key([mod, "shift"], "f", lazy.spawn(file_manager), desc="Launch file manager"),
    Key([mod, "shift"], "e", lazy.spawn(text_editor), desc="Launch text editor"),
    Key([mod, "shift"], "w", lazy.spawn(web_browser), desc="Launch web browser"),
    # CLI Apps --
    Key(
        ["control", "mod1"],
        "v",
        lazy.spawn(terminalfloat + " -e nvim"),
        desc="Open vim in qtile's terminal",
    ),
    Key(
        ["control", "mod1"],
        "r",
        lazy.spawn(terminalfloat + " -e ranger"),
        desc="Open ranger in qtile's terminal",
    ),
    Key(
        ["control", "mod1"],
        "h",
        lazy.spawn(terminalfloat + " -e gotop"),
        desc="Open htop in qtile's terminal",
    ),
    Key(
        ["control", "mod1"],
        "m",
        lazy.spawn(terminalfloat + " -e ncmpcpp"),
        desc="Open ncmpcpp in qtile's terminal",
    ),
    # Rofi Applets --
    Key(
        ["mod1"],
        "F1",
        lazy.spawn("launcher"),
        desc="Run application launcher",
    ),
    Key(
        [mod],
        "x",
        lazy.spawn("powermenu"),
        desc="Run powermenu applet",
    ),
    # Function keys : Brightness --
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn(brightness + " --inc"),
        desc="Increase display brightness",
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn(brightness + " --dec"),
        desc="Decrease display brightness",
    ),
    # Function keys : Volume --
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn(volume + " --inc"),
        desc="Raise speaker volume",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn(volume + " --dec"),
        desc="Lower speaker volume",
    ),
    Key([], "XF86AudioMute", lazy.spawn(volume + " --toggle"), desc="Toggle mute"),
    Key(
        [],
        "XF86AudioMicMute",
        lazy.spawn(volume + " --toggle-mic"),
        desc="Toggle mute for mic",
    ),
    # Function keys : Media --
    Key([], "XF86AudioNext", lazy.spawn("mpc next"), desc="Next track"),
    Key([], "XF86AudioPrev", lazy.spawn("mpc prev"), desc="Previous track"),
    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle"), desc="Toggle play/pause"),
    Key([], "XF86AudioStop", lazy.spawn("mpc stop"), desc="Stop playing"),
    # Screenshots --
    Key([], "Print", lazy.spawn(screenshot + " --area"), desc="Take Screenshot"),
    Key(
        ["control"],
        "Print",
        lazy.spawn(screenshot + " --in5"),
        desc="Take Screenshot in 5 seconds",
    ),
    Key(
        ["shift"],
        "Print",
        lazy.spawn(screenshot + " --in10"),
        desc="Take Screenshot in 10 seconds",
    ),
    Key(
        ["control", "shift"],
        "Print",
        lazy.spawn(screenshot + " --win"),
        desc="Take Screenshot of active window",
    ),
    Key(
        [mod],
        "Print",
        lazy.spawn(screenshot + " --area"),
        desc="Take Screenshot of selected area",
    ),
    # Misc --
    Key([mod], "p", lazy.spawn("toggle_eww"), desc="Run colorpicker"),
    Key([mod], "m", lazy.spawn("toggle_music"), desc="Run colorpicker"),
    # Key([mod], "p", lazy.spawn("toggle_eww"), desc="Run colorpicker"),
    Key(
        ["mod1", "control"],
        "l",
        lazy.spawn("sh lock.sh"),
        desc="Run lockscreen",
    ),
    # WM Specific --
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "k", lazy.spawn("keys.sh"), desc="Keybindings"),
    # Control Qtile
    Key(
        [mod, "control"],
        "r",
        lazy.reload_config(),
        lazy.spawn(notify_cmd + ' "Configuration Reloaded!"'),
        desc="Reload the config",
    ),
    Key(
        [mod, "control"],
        "s",
        lazy.restart(),
        lazy.spawn(notify_cmd + ' "Restarting Qtile..."'),
        desc="Restart Qtile",
    ),
    Key(
        [mod, "control"],
        "q",
        lazy.shutdown(),
        lazy.spawn(notify_cmd + ' "Exiting Qtile..."'),
        desc="Shutdown Qtile",
    ),
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([alt], "Left", resize_left, desc="Resize window left"),
    Key([alt], "Right", resize_right, desc="Resize window Right"),
    Key([alt], "Up", resize_up, desc="Resize windows upward"),
    Key([alt], "Down", resize_down, desc="Resize windows downward"),
    Key([alt], "n", lazy.layout.normalize(), desc="Normalize window size ratios"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"],
        "Left",
        lazy.layout.shuffle_left(),
        desc="Move window to the left",
    ),
    Key(
        [mod, "shift"],
        "Right",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key(
        [mod, "control"],
        "Left",
        lazy.layout.grow_left(),
        desc="Grow window to the left",
    ),
    Key(
        [mod, "control"],
        "Right",
        lazy.layout.grow_right(),
        desc="Grow window to the right",
    ),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key(
        [mod, "control"],
        "Return",
        lazy.layout.normalize(),
        desc="Reset all window sizes",
    ),
    # Toggle floating and fullscreen
    Key(
        [mod],
        "space",
        lazy.window.toggle_floating(),
        desc="Put the focused window to/from floating mode",
    ),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Put the focused window to/from fullscreen mode",
    ),
    # Go to next/prev group
    Key(
        [mod, "mod1"],
        "Right",
        lazy.screen.next_group(),
        desc="Move to the group on the right",
    ),
    Key(
        [mod, "mod1"],
        "Left",
        lazy.screen.prev_group(),
        desc="Move to the group on the left",
    ),
    # Back-n-forth groups
    Key([mod], "b", lazy.screen.toggle_group(), desc="Move to the last visited group"),
    # Change focus to other window
    Key([mod], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    # Toggle between different layouts as defined below
    Key([mod, "shift"], "space", lazy.next_layout(), desc="Toggle between layouts"),
    # Increase the space for master window at the expense of slave windows
    Key(
        [mod],
        "equal",
        lazy.layout.increase_ratio(),
        desc="Increase the space for master window",
    ),
    # Decrease the space for master window in the advantage of slave windows
    Key(
        [mod],
        "minus",
        lazy.layout.decrease_ratio(),
        desc="Decrease the space for master window",
    ),
    # Toggle between split and unsplit sides of stack.
    Key(
        [mod, "shift"],
        "s",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "comma", lazy.group["SPD"].dropdown_toggle("term")),
    Key([mod], "period", lazy.group["SPD"].dropdown_toggle("music")),
    # Modes: Reize
    # Modes: Layouts
]


def show_keys():
    key_help = ""
    for i in range(0, len(keys)):
        k = keys[i]
        if not isinstance(k, Key):
            continue
        mods = ""

        for m in k.modifiers:
            if m == "mod4":
                mods += "Super + "
            else:
                mods += m.capitalize() + " + "

        if len(k.key) > 1:
            mods += k.key.capitalize()
        else:
            mods += k.key

        key_help += "{:<25} {}".format(
            mods, k.desc + ("\n" if i != len(keys) - 1 else "")
        )

    return key_help


keys.extend(
    [
        Key(
            [mod],
            "a",
            lazy.spawn(
                "sh -c 'echo \""
                + show_keys()
                + '" | rofi -dmenu -theme ~/.config/rofi/hotkeys.rasi -i -p ""\''
            ),
            desc="Print keyboard bindings",
        ),
    ]
)

## Mouse Bindings ------------------------------

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

## Groups ------------------------------
groups = [Group(i) for i in "1234567"]
for i in groups:
    keys.extend(
        [
            # mod + number of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + number of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )
groups.append(ScratchGroups[0])
## Layouts ------------------------------
var_bg_color = colors["white"]
var_active_bg_color = colors["glass"]
var_active_fg_color = colors["purple"]
var_inactive_bg_color = colors["glass"]
var_inactive_fg_color = colors["orange"]
var_urgent_bg_color = colors["glass"]
var_urgent_fg_color = colors["blue"]
var_section_fg_color = "#EBCB8B"
var_active_color = "#bd93f9"
var_normal_color = "#6272a4"
var_border_width = 2
var_margin = [2, 2, 2, 2]
var_gap_top = 26
var_gap_bottom = 30
var_gap_left = 2
var_gap_right = 2
var_font_name = "JetBrainsMono Nerd Font"

layouts = [
    # Extension of the Stack layout
    # Layout inspired by bspwm
    layout.Bsp(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_on_single=False,
        border_width=var_border_width,
        fair=True,
        grow_amount=1,
        lower_right=False,
        margin=var_margin,
        margin_on_single=None,
        ratio=1.5,
        wrap_clients=False,
    ),
    layout.Columns(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_on_single=False,
        border_width=var_border_width,
        fair=False,
        grow_amount=10,
        insert_position=0,
        margin=var_margin,
        margin_on_single=None,
        num_columns=2,
        split=True,
        wrap_focus_columns=True,
        wrap_focus_rows=True,
        wrap_focus_stacks=True,
    ),
    # This layout divides the screen into a matrix of equally sized cells and places one window in each cell.
    layout.Matrix(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        columns=2,
        margin=var_margin,
    ),
    # Maximized layout
    layout.Max(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        margin=0,
    ),
    # Emulate the behavior of XMonad's default tiling scheme.
    layout.MonadTall(
        align=0,
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        change_ratio=0.05,
        change_size=20,
        margin=0,
        max_ratio=0.75,
        min_ratio=0.25,
        min_secondary_size=85,
        new_client_position="after_current",
        ratio=0.5,
        single_border_width=None,
        single_margin=None,
    ),
    # Emulate the behavior of XMonad's ThreeColumns layout.
    layout.MonadThreeCol(
        align=0,
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        change_ratio=0.05,
        change_size=20,
        main_centered=True,
        margin=0,
        max_ratio=0.75,
        min_ratio=0.25,
        min_secondary_size=85,
        new_client_position="top",
        ratio=0.5,
        single_border_width=None,
        single_margin=None,
    ),
    # Emulate the behavior of XMonad's horizontal tiling scheme.
    layout.MonadWide(
        align=0,
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        change_ratio=0.05,
        change_size=20,
        margin=0,
        max_ratio=0.75,
        min_ratio=0.25,
        min_secondary_size=85,
        new_client_position="after_current",
        ratio=0.5,
        single_border_width=None,
        single_margin=None,
    ),
    # Tries to tile all windows in the width/height ratio passed in
    layout.RatioTile(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        fancy=False,
        margin=var_margin,
        ratio=1.618,
        ratio_increment=0.1,
    ),
    # This layout cuts piece of screen_rect and places a single window on that piece, and delegates other window placement to other layout
    layout.Slice(match=None, side="left", width=256),
    # A mathematical layout, Renders windows in a spiral form by splitting the screen based on a selected ratio.
    layout.Spiral(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        clockwise=True,
        main_pane="left",
        main_pane_ratio=None,
        margin=0,
        new_client_position="top",
        ratio=0.6180469715698392,
        ratio_increment=0.1,
    ),
    # A layout composed of stacks of windows
    layout.Stack(
        autosplit=False,
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        fair=False,
        margin=var_margin,
        num_stacks=2,
    ),
    # A layout with two stacks of windows dividing the screen
    layout.Tile(
        add_after_last=False,
        add_on_top=True,
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_on_single=False,
        border_width=var_border_width,
        expand=True,
        margin=var_margin,
        margin_on_single=None,
        master_length=1,
        master_match=None,
        max_ratio=0.85,
        min_ratio=0.15,
        ratio=0.618,
        ratio_increment=0.05,
        shift_windows=False,
    ),
    # This layout works just like Max but displays tree of the windows at the left border of the screen_rect, which allows you to overview all opened windows.
    layout.TreeTab(
        active_bg=colors["black"],
        active_fg=var_active_fg_color,
        bg_color=colors["glass"],
        border_width=var_border_width,
        font=var_font_name,
        fontshadow=None,
        fontsize=14,
        inactive_bg=var_inactive_bg_color,
        inactive_fg=var_inactive_fg_color,
        level_shift=0,
        margin_left=0,
        margin_y=0,
        padding_left=10,
        padding_x=10,
        padding_y=10,
        panel_width=100,
        place_right=False,
        previous_on_rm=False,
        section_bottom=0,
        section_fg=var_section_fg_color,
        section_fontsize=14,
        section_left=10,
        section_padding=10,
        section_top=10,
        sections=["Default"],
        urgent_bg=var_urgent_bg_color,
        urgent_fg=var_urgent_fg_color,
        vspace=5,
    ),
    # Tiling layout that works nice on vertically mounted monitors
    layout.VerticalTile(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        margin=var_margin,
    ),
    # A layout with single active windows, and few other previews at the right
    layout.Zoomy(
        columnwidth=300,
        margin=var_margin,
        property_big="1.0",
        property_name="ZOOM",
        property_small="0.1",
    ),
    # Floating layout, which does nothing with windows but handles focus order
    layout.Floating(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        fullscreen_border_width=0,
        max_border_width=2,
    ),
]


## Screens ------------------------------
def apps():
    qtile.cmd_spawn("launcher")


def powermenu():
    qtile.cmd_spawn("powermenu")


def search():
    qtile.cmd_spawn("fsearch")


def ranger():
    qtile.cmd_spawn(terminalfloat + " -e ranger")


def pacseek():
    qtile.cmd_spawn(terminalfloat + " -e pacseek")


def nmtui():
    qtile.cmd_spawn("nmgui")


def cal():
    qtile.cmd_spawn("galendae -c" + home + "/.config/qtile/cal.conf")


def dash():
    qtile.cmd_spawn("toggle_eww")


def update():
    qtile.cmd_spawn(terminalfloat + " -e yay")


screens = [
    Screen(
        top=bar.Bar(
            widgets=[
                widget.Spacer(
                    length=-4,
                    background=None,
                ),
                widget.Image(
                    filename="~/.config/qtile/IconsNew/apple.png",
                    margin=2,
                    background=None,
                    opacity=1.0,
                    mouse_callbacks={"Button1": apps, "Button3": dash},
                ),
                widget.Sep(
                    background=colors["glass"],
                    foreground=colors["magenta"],
                    size_percent=100,
                ),
                widget.GroupBox(
                    font="SFMono Nerd Font Bold",
                    fontsize=14,
                    borderwidth=2,
                    highlight_method="line",
                    active=colors["orange"],
                    block_highlight_text_color=colors["white"],
                    highlight_color=colors["glass"],
                    inactive=colors["glass"],
                    foreground=colors["purple"],
                    background=colors["glass"],
                    this_current_screen_border=colors["red"],
                    this_screen_border=colors["blue"],
                    other_current_screen_border=colors["red"],
                    other_screen_border=colors["magenta"],
                    urgent_border=colors["red"],
                    rounded=True,
                    hide_unused=True,
                    disable_drag=True,
                    margin_y=2,
                    margin_x=0,
                ),
                widget.Sep(
                    background=colors["glass"],
                    foreground=colors["magenta"],
                    size_percent=100,
                ),
                # widget.Image(
                #     filename="~/.config/qtile/IconsNew/vertical.png",
                #     background=colors["white"],
                #     margin=-3,
                #     padding=-2,
                # ),
                # widget.Spacer(
                #     length=-5,
                #     background=colors["glass"],
                # ),
                widget.CurrentLayoutIcon(
                    background=colors["glass"], foreground=colors["orange"]
                ),
                widget.CurrentLayout(
                    background=colors["glass"],
                    foreground=colors["orange"],
                    fmt="{}",
                    font="SFMono Nerd Font Bold",
                    fontsize=13,
                ),
                widget.Sep(
                    background=colors["glass"],
                    foreground=colors["magenta"],
                    size_percent=100,
                ),
                widget.Image(
                    filename="~/.config/qtile/IconsNew/search.png",
                    margin=0,
                    background=colors["glass"],
                    padding=2,
                    mouse_callbacks={"Button1": search},
                ),
                widget.Image(
                    filename="~/.config/qtile/IconsNew/folder.png",
                    margin=0,
                    background=colors["glass"],
                    mouse_callbacks={"Button1": ranger},
                ),
                widget.Image(
                    filename="~/.config/qtile/IconsNew/packages.png",
                    margin=0,
                    background=colors["glass"],
                    mouse_callbacks={"Button1": pacseek},
                ),
                widget.Sep(
                    background=colors["glass"],
                    foreground=colors["magenta"],
                    size_percent=100,
                ),
                widget.TaskList(
                    background=colors["glass"],
                    border=colors["purple"],
                    borderwidth=2,
                    fontsize=13,
                    margin=0,
                    font="SFMono Nerd Font Bold",
                    icon_size=20,
                    highlight_method="border",
                    max_title_width=295,
                ),
                widget.Sep(
                    background=colors["glass"],
                    foreground=colors["magenta"],
                    size_percent=100,
                ),
                widget.Image(
                    filename="~/.config/qtile/IconsNew/time.png",
                    margin=0,
                    background=colors["glass"],
                ),
                widget.Pomodoro(
                    background=colors["glass"],
                    color_active=colors["blue"],
                    color_break=colors["orange"],
                    color_inactive=colors["white"],
                    fmt="{}",
                    prefix_inactive="Pomo",
                    font="SFMono Nerd Font Bold",
                    fontsize=12,
                    length_long_break=10,
                    length_pomodori=30,
                    length_short_break=5,
                ),
                widget.Image(
                    filename="~/.config/qtile/IconsNew/headphones.png",
                    margin=0,
                    background=colors["glass"],
                ),
                widget.Mpd2(
                    background=colors["glass"],
                    foreground=colors["white"],
                    fmt="{}",
                    mouse_buttons={1: "toggle", 3: "stop", 4: "previous", 5: "next"},
                    font="SFMono Nerd Font Bold",
                    fontsize=13,
                    max_chars=24,
                    status_format="{title}",
                    scroll=True,
                    width=300,
                ),
                # widget.Image(
                #     filename="~/.config/qtile/IconsNew/vertical.png",
                #     background=colors["glass"],
                # ),
                # widget.Spacer(
                #     length=-8,
                #     background=colors["glass"],
                # ),
                widget.Sep(
                    background=colors["glass"],
                    foreground=colors["magenta"],
                    size_percent=100,
                ),
                widget.Spacer(
                    length=-1,
                    background=colors["glass"],
                ),
                widget.Systray(
                    background=colors["glass"],
                    icon_size=25,
                    padding=10,
                ),
                widget.Sep(
                    background=colors["glass"],
                    foreground=colors["magenta"],
                    size_percent=100,
                ),
                widget.Image(
                    filename="~/.config/qtile/IconsNew/update.png",
                    background=colors["glass"],
                    margin=0,
                ),
                widget.CheckUpdates(
                    background=colors["glass"],
                    foreground=colors["white"],
                    colour_have_updates=colors["blue"],
                    colour_no_updates=colors["white"],
                    font="SFMono Nerd Font Bold",
                    distro="Arch_yay",
                    display_format="Ups: {updates}",
                    fmt="{}",
                    initial_text="-",
                    no_update_string="Up2Date",
                    mouse_callbacks={"Button1": update},
                    fontsize=13,
                ),
                widget.Image(
                    filename="~/.config/qtile/IconsNew/weather.png",
                    background=colors["glass"],
                    margin=0,
                ),
                widget.Wttr(
                    background=colors["glass"],
                    foreground=colors["white"],
                    location={},
                    format="%t(%f)",
                    font="SFMono Nerd Font Bold",
                    fontsize=13,
                ),
                widget.Spacer(
                    length=4,
                    background=colors["glass"],
                ),
                widget.Image(
                    filename="~/.config/qtile/IconsNew/wifi.png",
                    background=colors["glass"],
                    margin=2,
                ),
                widget.Wlan(
                    background=colors["glass"],
                    interface="wlp2s0",
                    format="{essid}{percent:2.0%}",
                    disconnected_message="Off",
                    foreground=colors["white"],
                    font="SFMono Nerd Font Bold",
                    fontsize=13,
                    scroll=True,
                    scroll_repeat=True,
                    scroll_interval=0.1,
                    scroll_step=1,
                    max_chars=10,
                    update_interval=1,
                    mouse_callbacks={"Button1": nmtui},
                    padding=-1,
                ),
                widget.Net(
                    interface="wlp2s0",
                    format="{down:1.2f}{down_suffix:<0}",
                    background=colors["glass"],
                    foreground=colors["magenta"],
                    font="SFMono Nerd Font Bold",
                    fontsize=14,
                    prefix="k",
                    mouse_callbacks={"Button1": nmtui},
                ),
                widget.Image(
                    background=colors["glass"],
                    filename="~/.config/qtile/IconsNew/ssd.png",
                    margin=1,
                ),
                widget.DF(
                    background=colors["glass"],
                    foreground=colors["blue"],
                    format="{uf}|{r:.0f}%",
                    measure="G",
                    font="SFMono Nerd Font Bold",
                    fontsize=14,
                    partition="/",
                    visible_on_warn=False,
                    warn_space=20,
                ),
                widget.Image(
                    filename="~/.config/qtile/IconsNew/memory.png",
                    background=colors["glass"],
                    margin=1,
                ),
                widget.Memory(
                    background=colors["glass"],
                    format="{MemUsed: .0f}{mm}",
                    foreground=colors["white"],
                    font="SFMono Nerd Font Bold",
                    fontsize=13,
                    update_interval=3,
                ),
                widget.BatteryIcon(
                    theme_path="~/.config/qtile/IconsNew/Battery/",
                    background=colors["glass"],
                    scale=1,
                ),
                widget.Battery(
                    font="SFMono Nerd Font Bold",
                    background=colors["glass"],
                    foreground=colors["white"],
                    format="{percent:2.0%}",
                    fontsize=13,
                ),
                widget.Image(
                    filename="~/.config/qtile/IconsNew/light.png",
                    background=colors["glass"],
                    margin=-2,
                ),
                widget.Backlight(
                    background=colors["glass"],
                    foreground=colors["white"],
                    padding=-1,
                    backlight_name="amdgpu_bl1",
                    change_command="brightness",
                    fmt="{}",
                    font="SFMono Nerd Font Bold",
                    format="{percent:2.0%}",
                ),
                widget.Spacer(
                    length=5,
                    background=colors["glass"],
                ),
                widget.Volume(
                    font="JetBrainsMono Nerd Font",
                    theme_path="~/.config/qtile/IconsNew/Volume/",
                    margin=2,
                    padding=-1,
                    fmt="{}",
                    emoji=False,
                    fontsize=13,
                    background=colors["glass"],
                    foreground=colors["white"],
                    volume_app="volume",
                ),
                widget.Image(
                    filename="~/.config/qtile/IconsNew/clock.png",
                    background=colors["glass"],
                    margin_y=-2,
                    margin_x=-2,
                ),
                widget.Clock(
                    format="%I:%M %p",
                    background=colors["glass"],
                    foreground=colors["white"],
                    font="SFMono Nerd Font Bold",
                    fontsize=13,
                    mouse_callbacks={"Button1": cal},
                ),
                widget.Image(
                    filename="~/.config/qtile/IconsNew/logout.png",
                    margin=-2,
                    background=colors["glass"],
                    mouse_callbacks={"Button1": powermenu},
                ),
            ],
            size=25,
            border_color=colors["glass"],
            border_width=[0, 4, 0, 4],
            margin=[0, 0, 0, 0],
            background=colors["glass"],
        ),
    ),
]
## General Configuration Variables ------------------------------

# If a window requests to be fullscreen, it is automatically fullscreened.
# Set this to false if you only want windows to be fullscreen if you ask them to be.
auto_fullscreen = False

# When clicked, should the window be brought to the front or not.
# If this is set to "floating_only", only floating windows will get affected (This sets the X Stack Mode to Above.)
bring_front_click = False

# If true, the cursor follows the focus as directed by the keyboard, warping to the center of the focused window.
# When switching focus between screens, If there are no windows in the screen, the cursor will warp to the center of the screen.
cursor_warp = False

# A function which generates group binding hotkeys. It takes a single argument, the DGroups object, and can use that to set up dynamic key bindings.
# A sample implementation is available in 'libqtile/dgroups.py' called `simple_key_binder()`, which will bind groups to "mod+shift+0-10" by default.
dgroups_key_binder = None

# A list of Rule objects which can send windows to various groups based on matching criteria.
dgroups_app_rules = []  # type: list


# The default floating layout to use. This allows you to set custom floating rules among other things if you wish.
floating_layout = layout.Floating(
    border_focus=var_active_color,
    border_normal=var_normal_color,
    border_width=var_border_width,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="matplotlib"),
        Match(wm_class="Lxappearance"),
        Match(wm_class="Pavucontrol|Xfce4-power-manager-settings"),
        Match(wm_class="Xfce4-power-manager-settings"),
        Match(wm_class="feh|Viewnior|Mpv"),
        Match(wm_class="Kvantum Manager|qt5ct"),
        Match(title="branchdialog"),
        Match(wm_class="Fsearch"),
        Match(wm_class="TelegramDesktop"),
        Match(wm_class="Bluetooth|bluetooth"),
        Match(wm_class="Windscribe2"),
        Match(wm_class="MATLAB R2018b|matlab r2018b"),
        Match(wm_class="Blueman-manager"),
        Match(wm_class="kitty"),
    ],
)

# Behavior of the _NET_ACTIVATE_WINDOW message sent by applications
#
# urgent: urgent flag is set for the window
# focus: automatically focus the window
# smart: automatically focus if the window is in the current group
# never: never automatically focus any window that requests it
focus_on_window_activation = "smart"

# Controls whether or not focus follows the mouse around as it moves across windows in a layout.
follow_mouse_focus = True

# Default settings for bar widgets.
widget_defaults = dict(
    font="JetBrainsMono Nerd Font", fontsize=13, padding=5, background="#00000000"
)

# Same as `widget_defaults`, Default settings for extensions.
extension_defaults = widget_defaults.copy()

# Controls whether or not to automatically reconfigure screens when there are changes in randr output configuration.
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
