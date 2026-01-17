import json
import os
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.status import Status
from src.modules.llm_client import LLMClient
from src.modules.rag_engine import RAGEngine
from src.modules.judge import Judge

console = Console()

def main():
    console.clear()
    console.print(Panel.fit("[bold blue]LLM-as-a-Judge: RAG vs Non-RAG Evaluator[/bold blue]", border_style="blue"))
    
    # Initialize
    with console.status("[bold green]Initializing system...[/bold green]"):
        llm = LLMClient()
        rag = RAGEngine()
        judge = Judge()
        time.sleep(1) # Simulated startup
    
    # 1. Input Question
    console.print("\n[bold yellow]Step 1: Input Question[/bold yellow]")
    question = Prompt.ask("Enter your question")
    if not question:
        question = "What is Retrieval-Augmented Generation?"  # Default
        console.print(f"[dim]Using default question: {question}[/dim]")

    # 2. Generate Answers
    answers = {}
    
    # Non-RAG
    with console.status("[bold cyan]Generating Non-RAG Answer...[/bold cyan]"):
        prompt_non_rag = f"Question: {question}\nAnswer the question concisely."
        answers['Non-RAG'] = llm.generate_completion(prompt_non_rag)
    
    # RAG
    with console.status("[bold magenta]Retrieving Documents & Generating RAG Answer...[/bold magenta]"):
        docs = rag.retrieve(question)
        context = rag.format_context(docs)
        prompt_rag = f"Context:\n{context}\n\nQuestion: {question}\nUsing the context above, answer the question."
        answers['RAG'] = llm.generate_completion(prompt_rag)
    
    # Display Answers
    console.print("\n[bold yellow]Step 2: Generated Answers[/bold yellow]")
    
    grid = Table.grid(expand=True, padding=1)
    grid.add_column(ratio=1)
    grid.add_column(ratio=1)
    grid.add_row(
        Panel(answers['Non-RAG'], title="[bold cyan]Non-RAG Answer[/bold cyan]"),
        Panel(f"{answers['RAG']}\n\n[dim]Docs used: {len(docs)}[/dim]", title="[bold magenta]RAG Answer[/bold magenta]")
    )
    console.print(grid)

    # 3. Evaluate
    console.print("\n[bold yellow]Step 3: AI Evaluation[/bold yellow]")
    with console.status("[bold red]Judge is evaluating...[/bold red]"):
        evaluation_result = judge.evaluate(question, answers['Non-RAG'], answers['RAG'], context)
    
    if "error" in evaluation_result:
        console.print(f"[bold red]Error in evaluation:[/bold red] {evaluation_result}")
        return

    # 4. Display Results Table
    table = Table(title="Evaluation Results")
    table.add_column("Model", style="cyan")
    table.add_column("Accuracy", justify="center")
    table.add_column("Completeness", justify="center")
    table.add_column("Relevance", justify="center")
    table.add_column("Clarity", justify="center")
    table.add_column("Grounding", justify="center")
    table.add_column("Avg Score", justify="center", style="bold green")

    eval_data = evaluation_result.get("evaluation", [])
    for item in eval_data:
        scores = item["scores"]
        table.add_row(
            item["model"],
            str(scores.get("accuracy", "-")),
            str(scores.get("completeness", "-")),
            str(scores.get("relevance", "-")),
            str(scores.get("clarity", "-")),
            str(scores.get("grounding", "N/A")),
            str(item.get("average_score", "-"))
        )
    
    console.print(table)

    # 5. Final Winner
    winner = evaluation_result.get("final_winner", "Unknown")
    reason = evaluation_result.get("reason", "No reason provided.")
    
    winner_color = "green" if winner == "RAG" else "blue"
    console.print(Panel(f"[bold]Winner:[/bold] [{winner_color}]{winner}[/{winner_color}]\n[bold]Reason:[/bold] {reason}", title="Final Verdict", border_style=winner_color))

    # 6. JSON Output (Programmatic)
    final_output = {
        "question": question,
        "answers": answers,
        "evaluation": eval_data,
        "final_winner": winner,
        "reason": reason
    }
    
    # Save code to file for "Project GUI" feel, outputting JSON to hidden file or console if requested
    # But user asked for Strict JSON Output at the end.
    
    # We will print the JSON raw at the very bottom for copy-paste utility
    console.print("\n[dim]Programmatic Output (JSON):[/dim]")
    print(json.dumps(final_output, indent=2))

if __name__ == "__main__":
    main()
