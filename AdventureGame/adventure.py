from time import sleep
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.progress import track

console = Console()

# Rooms map
rooms = {
    "Hall": {
        "east": "Dining Room",
        "south": "Kitchen",
        "item": "key"
    },
    "Kitchen": {
        "north": "Hall",
        "item": "monster"
    },
    "Dining Room": {
        "west": "Hall",
        "south": "Garden",
        "item": "potion"
    },
    "Garden": {
        "north": "Dining Room"
    }
}

inventory = []
current_room = "Hall"

def slow_print(text, color="white", delay=0.03):
    styled = Text()
    styled.append(text, style=color)
    for char in styled.plain:
        console.print(char, end="", style=color, justify="left", highlight=False)
        sleep(delay)
    console.print("")

def show_intro():
    console.print(Panel("🎮 Welcome to the Adventure Game! 🎮\n\nCommands:\n  go [direction]\n  get [item]\n  quit", style="bold cyan"))

def show_room():
    console.print(f"\n[bold magenta]You are in the {current_room}[/bold magenta]")
    if "item" in rooms[current_room]:
        item = rooms[current_room]["item"]
        if item == "monster":
            console.print("[bold red]A monster appears! 💀[/bold red]")
            console.print("[red]You were caught by a monster... Game Over! ❌[/red]")
            exit()
        else:
            console.print(f"[yellow]You see a {item} ✨[/yellow]")
    console.print(f"[cyan]Inventory: {inventory}[/cyan]")

def victory():
    console.print("\n[bold green]You unlocked the Garden with the key![/bold green]")
    for step in track(range(30), description="[yellow]Celebrating..."):
        sleep(0.05)
    console.print(Panel("🏆 [bold magenta]Congratulations, You Win! 🎉🌟[/bold magenta] 🏆", style="bold green"))

def main():
    global current_room
    show_intro()

    while True:
        show_room()
        move = console.input("\n>  ").lower().split()

        if len(move) == 0:
            continue

        if move[0] == "quit":
            console.print("[red]Game Over. Thanks for playing![/red]")
            break

        if move[0] == "go":
            if len(move) < 2:
                console.print("[red]Go where?[/red]")
                continue
            direction = move[1]
            if direction in rooms[current_room]:
                current_room = rooms[current_room][direction]
                if current_room == "Garden":
                    if "key" in inventory:
                        victory()
                        break
                    else:
                        console.print("[red]The Garden gate is locked. You need a key! 🔑[/red]")
                        current_room = "Dining Room"
            else:
                console.print("[red]You can't go that way![/red]")

        elif move[0] == "get":
            if "item" in rooms[current_room]:
                item = rooms[current_room]["item"]
                if len(move) > 1 and move[1] == item:
                    inventory.append(item)
                    console.print(f"[green]{item} collected! ✅[/green]")
                    del rooms[current_room]["item"]
                else:
                    console.print("[red]Get what?[/red]")
            else:
                console.print("[red]There is nothing to get here.[/red]")

        else:
            console.print("[red]Invalid command![/red]")

if __name__ == "__main__":
    console.print("[blue]Starting game...[/blue]")
    main()
