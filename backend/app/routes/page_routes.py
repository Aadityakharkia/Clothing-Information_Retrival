"""
Page Routes Blueprint
=====================
Renders Jinja2 HTML views for each frontend page.
"""

from flask import Blueprint, render_template, request, current_app
from ..services import get_ir_system

page_bp = Blueprint("pages", __name__)


def _get_stats():
    """Returns (total_docs, vocab_size) from the loaded index."""
    corpus_path = current_app.config["CORPUS_PATH"]
    ir = get_ir_system(corpus_path)
    return ir["index"].total_docs, len(ir["index"].vocabulary)


@page_bp.route("/")
def home():
    total_docs, vocab_size = _get_stats()
    return render_template(
        "search.html",
        active_page="search",
        total_docs=total_docs,
        vocab_size=vocab_size
    )


@page_bp.route("/results")
def results():
    q    = request.args.get("q", "").strip()
    mode = request.args.get("mode", "vsm").strip()
    if mode not in ("vsm", "phrase", "proximity", "semantic"):
        mode = "vsm"
    total_docs, vocab_size = _get_stats()
    return render_template(
        "results.html",
        active_page="search",
        query=q,
        mode=mode,
        initial_query=q,
        initial_mode=mode,
        total_docs=total_docs,
        vocab_size=vocab_size
    )


@page_bp.route("/tracer")
def tracer():
    total_docs, vocab_size = _get_stats()
    return render_template("tracer.html", active_page="tracer",
                           total_docs=total_docs, vocab_size=vocab_size)


@page_bp.route("/vocabulary")
def vocabulary():
    total_docs, vocab_size = _get_stats()
    return render_template("index_explorer.html", active_page="vocab",
                           total_docs=total_docs, vocab_size=vocab_size)
