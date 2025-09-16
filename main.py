from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, SpinnerColumn
from rich.text import Text
from rich.table import Table
from rich import box
from rich.style import Style
import subprocess
import time
import os

console = Console()

# Ulepszony pixel art dla LegendaryOS z bardziej szczegółowym designem (raw string)
PIXEL_ART = r"""
 _                              _                   ___  ____
| |    ___  __ _  ___ _ __   __| | __ _ _ __ _   _ / _ \/ ___|
| |   / _ \/ _` |/ _ \ '_ \ / _` |/ _` | '__| | | | | | \___ \
| |__|  __/ (_| |  __/ | | | (_| | (_| | |  | |_| | |_| |___) |
|_____\___|\__, |\___|_| |_|\__,_|\__,_|_|   \__, |\___/|____/
           |___/                             |___/
"""

def display_welcome():
    """Wyświetla animowany ekran powitalny z przejściami kolorów."""
    console.clear()
    colors = ["bright_red", "bright_magenta", "bright_blue", "bright_cyan", "bright_yellow", "bright_green", "bright_white"]
    for i in range(5):  # Wolniejsza animacja z przejściami kolorów
        console.print(Panel(
            Text(PIXEL_ART, style=f"bold {colors[i % len(colors)]} on black", justify="center"),
            title="[blink italic]Update-System dla LegendaryOS[/blink italic]",
            subtitle="v2.2.0 | Pixel Art Edition",
            border_style=Style(color=colors[(i + 1) % len(colors)], bgcolor="grey0"),
            box=box.ASCII_DOUBLE_HEAD,
            padding=(1, 2),
            expand=False
        ))
        console.print(f"[{colors[i % len(colors)]}][beep][/]")
        time.sleep(0.25)  # Wolniejsza animacja dla lepszego efektu
        console.clear()

    # Końcowy ekran powitalny
    console.print(Panel(
        Text(PIXEL_ART, style="bold bright_magenta on black", justify="center"),
        title="Update-System dla LegendaryOS",
        subtitle="v2.2.0 | Pixel Art Edition",
        border_style="bold bright_cyan",
        box=box.ASCII_DOUBLE_HEAD,
        padding=(1, 2),
        expand=False
    ))
    console.print("[bright_cyan][beep beep][/bright_cyan]\n")

def run_command(command, description, sudo=False):
    """Uruchamia polecenie i wyświetla postęp z ulepszonym stylem."""
    current_color = colors[0]
    console.print(f"\n[bold {current_color}]{description}[/bold {current_color}]")
    with Progress(
        SpinnerColumn(spinner_name="dots", style="bright_yellow"),
        TextColumn("[progress.description]{task.description}", style="bold white on black"),
        BarColumn(bar_width=None, style="bright_cyan"),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task("Wykonywanie...", total=100)
        try:
            if sudo:
                command = ["sudo"] + command
            process = subprocess.run(command, check=True, capture_output=True, text=True, timeout=300)
            for i in range(100):
                progress.update(task, advance=1)
                time.sleep(0.02)  # Symulacja postępu
            console.print(f"[bright_green]Sukces: {description} zakończono pomyślnie![/bright_green]")
            console.print("[bright_yellow][beep][/bright_yellow]")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[bright_red]Błąd w {description}: {e.stderr}[/bright_red]")
            console.print("[bright_red][error beep][/bright_red]")
            return False
        except subprocess.TimeoutExpired:
            console.print(f"[bright_red]Błąd: Przekroczono limit czasu dla {description}[/bright_red]")
            console.print("[bright_red][error beep][/bright_red]")
            return False
        except Exception as e:
            console.print(f"[bright_red]Nieoczekiwany błąd w {description}: {str(e)}[/bright_red]")
            console.print("[bright_red][error beep][/bright_red]")
            return False

def display_summary(successful, failed):
    """Wyświetla podsumowanie aktualizacji w formie stylizowanej tabeli."""
    table = Table(
        title="Podsumowanie aktualizacji LegendaryOS",
        box=box.ROUNDED,
        style="bold bright_cyan",
        title_style="bold bright_magenta",
        show_lines=True
    )
    table.add_column("Status", style="bold", justify="center", width=10)
    table.add_column("Opis", style="white", width=40)
    table.add_column("Szczegóły", style="dim white", width=50)
    for desc in successful:
        table.add_row("[bright_green]Sukces[/bright_green]", desc, "Zakończono bez błędów")
    for desc in failed:
        table.add_row("[bright_red]Błąd[/bright_red]", desc, "Sprawdź logi dla szczegółów")
    console.print("\n")
    console.print(table)
    console.print("[bright_yellow][beep beep beep][/bright_yellow]")

def main():
    global colors
    colors = ["bright_red", "bright_magenta", "bright_blue", "bright_cyan", "bright_yellow", "bright_green", "bright_white"]
    display_welcome()

    # Lista aktualizacji
    updates = [
        (["zypper", "update"], "Aktualizacja repozytoriów Zypper", True),
        (["flatpak", "update", "-y"], "Aktualizacja Flatpaka", False),
        (["fwupdmgr", "refresh"], "Odświeżanie firmware", True),
        (["fwupdmgr", "update"], "Instalacja aktualizacji firmware", True),
        (["/usr/share/LegendaryOS/scripts/update-legendaryos.sh"], "Aktualizacja LegendaryOS", True),
    ]

    successful = []
    failed = []

    # Wykonanie aktualizacji z dynamicznymi kolorami
    for idx, (cmd, desc, sudo) in enumerate(updates):
        if cmd[0].endswith("update-legendaryos.sh") and not os.path.exists(cmd[0]):
            console.print(f"[bright_red]Błąd: Skrypt {cmd[0]} nie istnieje![/bright_red]")
            console.print(f"[{colors[idx % len(colors)]}][error beep][/]")
            failed.append(desc)
            continue
        if run_command(cmd, desc, sudo):
            successful.append(desc)
        else:
            failed.append(desc)

    # Wyświetlenie podsumowania
    display_summary(successful, failed)

    console.print(Panel(
        Text("Aktualizacja systemu LegendaryOS zakończona!", style="bold bright_green on black", justify="center"),
        border_style="bold bright_green",
        box=box.DOUBLE_EDGE,
        padding=(1, 2),
        expand=False
    ))
    console.print("[bright_green][final beep][/bright_green]\n")

if __name__ == "__main__":
    main()
