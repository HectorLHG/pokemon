import requests
from PIL import Image
from io import BytesIO
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.style import Style

# Crear una instancia de consola Rich
console = Console()

# Ruta al archivo de nombres y URLs
path = r"C:\Users\Hector Henriquez\Documents\mentorship\Pokemon\pokemon_names_urls.txt"
file = open(path)

name_list = []
url_list = []
for line in file:
    name_list.append(line.split(",")[0])
    url_list.append(line.split(",")[1].strip())


while True:
    console.print("\n[bold cyan]Por favor ingrese el nombre del Pokémon:[/]")
    name = input("> ").strip().lower()

    if name in name_list:
        console.print("[bold green]\n¡Pokémon encontrado!\n[/]")
        url = f"https://pokeapi.co/api/v2/pokemon/{int(name_list.index(name))+1}/"
        response = requests.get(url)
        if response.status_code == 200:
            # Datos del Pokémon
            data = response.json()
            peso = data['weight']
            altura = data['height']
            abilities = data['abilities']
            types = data['types']
            sprites = data['sprites']
            imagen_url = sprites['front_default']

            print(abilities)

            # Construir strings de habilidades y tipos
            abilities_array = [ab["ability"]["name"] for ab in abilities]
            abilities_string = ", ".join(abilities_array)
            type_string = ", ".join([tp["type"]["name"] for tp in types])

            # Mostrar información en una tabla
            table = Table(title=f"Información básica de {name.upper()}", title_style="bold magenta", title_justify="left")
            table.add_column("Atributo", style="cyan", justify="right")
            table.add_column("Valor", style="yellow", justify="left")

            table.add_row("Peso", f"{peso}")
            table.add_row("Altura", f"{altura}")
            table.add_row("Tipo(s)", type_string)
            table.add_row("Habilidades", abilities_string)
            table.add_row("URL", f"[link={url}]{url}[/link]")

            console.print(table)

            # Mostrar panel con imagen URL (puedes activar `.show()` si es necesario)
            title_color = Text(
                text=f"Imagen de [bold]{name.upper()}",
                style=Style(
                    color="blue"
                )
            )
            panel = Panel(f"[bold white]Imagen disponible en:[/] [link={imagen_url}]{imagen_url}[/link]",
                          title=title_color, title_align="left", border_style="blue")
            console.print(panel)
    else:
        console.print("[bold red]Pokémon no encontrado[/]")

    # Preguntar si desea continuar
    console.print("\n[bold yellow]¿Desea realizar otra consulta? (S/N):[/]")
    answer = input("> ").strip().upper()
    if answer != "S":
        console.print("[bold blue]\nBúsqueda finalizada. Hasta luego![/]")
        break
