"""
CLI Interface for MCP Server
===========================

Command-line interface for managing and interacting with the MCP server.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table

from .config import Settings, load_settings, create_default_config_file
from .server import MCPServer
from .claude_client import ClaudeClient

app = typer.Typer(help="TW MCP Local Server - Claude 3.7 Integration")
console = Console()


@app.command()
def run(
    host: str = typer.Option("localhost", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to"),
    reload: bool = typer.Option(False, help="Enable auto-reload"),
    debug: bool = typer.Option(False, help="Enable debug mode"),
    config: str = typer.Option(".env", help="Configuration file path")
):
    """Run the MCP server."""
    try:
        # Load settings
        settings = load_settings()
        
        # Override with CLI arguments
        if host != "localhost":
            settings.host = host
        if port != 8000:
            settings.port = port
        if reload:
            settings.reload = reload
        if debug:
            settings.debug = debug
        
        console.print(Panel(
            f"Starting MCP Server\n"
            f"Host: {settings.host}\n"
            f"Port: {settings.port}\n"
            f"Debug: {settings.debug}\n"
            f"Model: {settings.claude_model}",
            title="MCP Server",
            border_style="green"
        ))
        
        # Create and run server
        server = MCPServer(settings)
        server.run()
        
    except Exception as e:
        console.print(f"[red]Error starting server: {str(e)}[/red]")
        sys.exit(1)


@app.command()
def init(
    config_path: str = typer.Option(".env", help="Path for configuration file"),
    force: bool = typer.Option(False, help="Overwrite existing config file")
):
    """Initialize a new MCP server configuration."""
    config_file = Path(config_path)
    
    if config_file.exists() and not force:
        console.print(f"[yellow]Configuration file already exists at {config_path}[/yellow]")
        console.print("Use --force to overwrite")
        return
    
    try:
        create_default_config_file(config_path)
        console.print(f"[green]Configuration file created at {config_path}[/green]")
        console.print("Please edit the file and set your ANTHROPIC_API_KEY")
        
    except Exception as e:
        console.print(f"[red]Error creating config file: {str(e)}[/red]")
        sys.exit(1)


@app.command()
def test(
    prompt: str = typer.Option("Hello, can you help me with Python?", help="Test prompt"),
    config: str = typer.Option(".env", help="Configuration file path")
):
    """Test the Claude API connection."""
    async def run_test():
        try:
            settings = load_settings()
            client = ClaudeClient(settings)
            
            console.print("[yellow]Testing Claude API connection...[/yellow]")
            
            response = await client.complete(
                prompt=prompt,
                system_prompt="You are a helpful programming assistant.",
                max_tokens=100
            )
            
            console.print(Panel(
                response.content,
                title="Claude Response",
                border_style="green"
            ))
            
            console.print(f"[green]✓ API connection successful![/green]")
            console.print(f"Model: {response.model}")
            console.print(f"Tokens used: {response.usage.get('total_tokens', 'N/A')}")
            
        except Exception as e:
            console.print(f"[red]✗ API connection failed: {str(e)}[/red]")
            sys.exit(1)
    
    asyncio.run(run_test())


@app.command()
def vibe(
    request: str = typer.Argument(..., help="Your coding request"),
    mood: str = typer.Option("supportive", help="Mood: supportive, encouraging, analytical, creative"),
    focus: str = typer.Option("general", help="Focus: general, performance, readability, architecture"),
    experience: str = typer.Option("intermediate", help="Experience level: beginner, intermediate, advanced")
):
    """Interactive vibe coding session."""
    async def run_vibe():
        try:
            settings = load_settings()
            client = ClaudeClient(settings)
            
            console.print(Panel(
                f"Vibe Coding Session\n"
                f"Mood: {mood}\n"
                f"Focus: {focus}\n"
                f"Experience: {experience}",
                title="Vibe Coder",
                border_style="blue"
            ))
            
            response = await client.vibe_code(
                request=request,
                context={
                    "mood": mood,
                    "focus": focus,
                    "experience_level": experience
                }
            )
            
            console.print(Panel(
                response.content,
                title="Vibe Coder Response",
                border_style="green"
            ))
            
        except Exception as e:
            console.print(f"[red]Error in vibe coding: {str(e)}[/red]")
            sys.exit(1)
    
    asyncio.run(run_vibe())


@app.command()
def status():
    """Check the status of the MCP server."""
    async def check_status():
        try:
            import httpx
            
            # Try to connect to the server
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/health")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    table = Table(title="MCP Server Status")
                    table.add_column("Property", style="cyan")
                    table.add_column("Value", style="green")
                    
                    table.add_row("Status", data["status"])
                    table.add_row("Version", data["version"])
                    table.add_row("Claude Status", "✓" if data["claude_status"] else "✗")
                    table.add_row("Plugins Loaded", str(data["plugins_loaded"]))
                    
                    console.print(table)
                else:
                    console.print(f"[red]Server returned status code: {response.status_code}[/red]")
                    
        except Exception as e:
            console.print(f"[red]Could not connect to server: {str(e)}[/red]")
            console.print("Make sure the server is running with 'mcp-server run'")
    
    asyncio.run(check_status())


@app.command()
def plugins():
    """List available plugins."""
    async def list_plugins():
        try:
            import httpx
            
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/plugins")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    table = Table(title="Available Plugins")
                    table.add_column("Name", style="cyan")
                    table.add_column("Version", style="green")
                    table.add_column("Status", style="yellow")
                    table.add_column("Description", style="white")
                    
                    for plugin in data["plugins"]:
                        status = "✓ Enabled" if plugin["enabled"] else "✗ Disabled"
                        table.add_row(
                            plugin["name"],
                            plugin["version"],
                            status,
                            plugin["description"]
                        )
                    
                    console.print(table)
                else:
                    console.print(f"[red]Server returned status code: {response.status_code}[/red]")
                    
        except Exception as e:
            console.print(f"[red]Could not connect to server: {str(e)}[/red]")
            console.print("Make sure the server is running with 'mcp-server run'")
    
    asyncio.run(list_plugins())


@app.command()
def analyze(
    file_path: str = typer.Argument(..., help="Path to code file to analyze"),
    language: str = typer.Option("python", help="Programming language"),
    task: str = typer.Option("analyze", help="Task: analyze, review, improve, debug")
):
    """Analyze a code file."""
    async def analyze_file():
        try:
            # Read the file
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                console.print(f"[red]File not found: {file_path}[/red]")
                sys.exit(1)
            
            with open(file_path_obj, 'r', encoding='utf-8') as f:
                code = f.read()
            
            settings = load_settings()
            client = ClaudeClient(settings)
            
            console.print(f"[yellow]Analyzing {file_path}...[/yellow]")
            
            response = await client.analyze_code(
                code=code,
                language=language,
                task=task
            )
            
            console.print(Panel(
                response.content,
                title=f"Code Analysis - {task.title()}",
                border_style="green"
            ))
            
        except Exception as e:
            console.print(f"[red]Error analyzing file: {str(e)}[/red]")
            sys.exit(1)
    
    asyncio.run(analyze_file())


@app.command()
def interactive():
    """Start an interactive vibe coding session."""
    async def run_interactive():
        try:
            settings = load_settings()
            client = ClaudeClient(settings)
            
            console.print(Panel(
                "Welcome to Interactive Vibe Coding!\n"
                "Type 'exit' to quit, 'help' for commands.",
                title="Interactive Session",
                border_style="blue"
            ))
            
            while True:
                try:
                    prompt = console.input("[cyan]vibe> [/cyan]")
                    
                    if prompt.lower() in ['exit', 'quit']:
                        console.print("[yellow]Goodbye! Happy coding! 🚀[/yellow]")
                        break
                    
                    if prompt.lower() == 'help':
                        console.print(Panel(
                            "Commands:\n"
                            "- Type your coding question or request\n"
                            "- 'exit' or 'quit' to leave\n"
                            "- 'help' for this message",
                            title="Help",
                            border_style="yellow"
                        ))
                        continue
                    
                    if not prompt.strip():
                        continue
                    
                    response = await client.vibe_code(request=prompt)
                    
                    console.print(Panel(
                        response.content,
                        title="Vibe Coder",
                        border_style="green"
                    ))
                    
                except KeyboardInterrupt:
                    console.print("\n[yellow]Goodbye! Happy coding! 🚀[/yellow]")
                    break
                except Exception as e:
                    console.print(f"[red]Error: {str(e)}[/red]")
            
        except Exception as e:
            console.print(f"[red]Error starting interactive session: {str(e)}[/red]")
            sys.exit(1)
    
    asyncio.run(run_interactive())


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()