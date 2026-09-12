"""
REST API Routes Blueprint
=========================
Pure routing layer — parses HTTP parameters and delegates to Controllers.
"""

from flask import Blueprint, request, jsonify, current_app
from ..controllers import (
    handle_vsm_search,
    handle_positional_search,
    handle_hybrid_search,
    handle_semantic_search,
    handle_trace,
    handle_rocchio_feedback,
    handle_get_vocabulary,
    handle_autocomplete
)
from ..services import get_ir_system

api_bp = Blueprint("api", __name__, url_prefix="/api")


# ── Health ─────────────────────────────────────────────────────────────────────

@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "clothing-ir-engine",
        "version": "2.0.0"
    })


# ── Search ─────────────────────────────────────────────────────────────────────

@api_bp.route("/search/vsm", methods=["GET"])
def search_vsm():
    q           = request.args.get("q", "").strip()
    top_k       = int(request.args.get("top_k", current_app.config.get("DEFAULT_TOP_K", 10)))
    autocorrect = request.args.get("autocorrect", "true").lower() in ("true", "1", "yes")
    synonyms    = request.args.get("synonyms", "true").lower() in ("true", "1", "yes")
    corpus      = current_app.config["CORPUS_PATH"]
    return jsonify(handle_vsm_search(
        query=q,
        top_k=top_k,
        autocorrect=autocorrect,
        synonyms=synonyms,
        corpus_path=corpus
    ))


@api_bp.route("/search/positional", methods=["GET"])
def search_positional():
    q      = request.args.get("q", "").strip()
    corpus = current_app.config["CORPUS_PATH"]
    return jsonify(handle_positional_search(query=q, corpus_path=corpus))


@api_bp.route("/search/hybrid", methods=["GET"])
def search_hybrid():
    q      = request.args.get("q", "").strip()
    lam    = float(request.args.get("lambda", current_app.config.get("DEFAULT_HYBRID_LAMBDA", 0.5)))
    top_k  = int(request.args.get("top_k", current_app.config.get("DEFAULT_TOP_K", 10)))
    corpus = current_app.config["CORPUS_PATH"]
    return jsonify(handle_hybrid_search(query=q, lambda_param=lam, top_k=top_k, corpus_path=corpus))


@api_bp.route("/search/semantic", methods=["GET"])
def search_semantic():
    q      = request.args.get("q", "").strip()
    mode   = request.args.get("mode", "hybrid").strip().lower()
    alpha  = float(request.args.get("alpha", 0.5))
    top_k  = int(request.args.get("top_k", current_app.config.get("DEFAULT_TOP_K", 10)))
    corpus = current_app.config["CORPUS_PATH"]
    return jsonify(handle_semantic_search(query=q, mode=mode, alpha=alpha, top_k=top_k, corpus_path=corpus))


# ── Autocomplete / Suggestions ─────────────────────────────────────────────────

@api_bp.route("/suggest", methods=["GET"])
@api_bp.route("/autocomplete", methods=["GET"])
def suggest():
    q      = request.args.get("q", "").strip()
    limit  = int(request.args.get("limit", 8))
    corpus = current_app.config["CORPUS_PATH"]
    return jsonify(handle_autocomplete(query=q, limit=limit, corpus_path=corpus))


# ── Tracer ─────────────────────────────────────────────────────────────────────

@api_bp.route("/trace", methods=["GET"])
def trace():
    term1  = request.args.get("term1", "stretch").strip()
    term2  = request.args.get("term2", "denim").strip()
    k      = int(request.args.get("k", current_app.config.get("DEFAULT_PROXIMITY_K", 4)))
    corpus = current_app.config["CORPUS_PATH"]
    return jsonify(handle_trace(term1=term1, term2=term2, k=k, corpus_path=corpus))


# ── Relevance Feedback ─────────────────────────────────────────────────────────

@api_bp.route("/feedback", methods=["POST"])
@api_bp.route("/rocchio",  methods=["POST"])
def feedback():
    data           = request.get_json(silent=True) or {}
    query          = data.get("query", "").strip()
    relevant_ids   = data.get("relevant_doc_ids", [])
    irrelevant_ids = data.get("irrelevant_doc_ids", [])
    is_prf         = data.get("is_prf", False)
    top_k          = int(data.get("top_k", current_app.config.get("DEFAULT_TOP_K", 10)))
    corpus         = current_app.config["CORPUS_PATH"]

    if not query:
        return jsonify({"error": "Empty query"}), 400

    if is_prf and not relevant_ids:
        ir = get_ir_system(corpus)
        relevant_ids = [r["doc_id"] for r in ir["vsm"].search(query, top_k=3)]

    return jsonify(handle_rocchio_feedback(
        query=query,
        relevant_ids=relevant_ids,
        irrelevant_ids=irrelevant_ids,
        top_k=top_k,
        corpus_path=corpus
    ))


# ── Vocabulary ─────────────────────────────────────────────────────────────────

@api_bp.route("/vocabulary", methods=["GET"])
def vocabulary():
    search   = request.args.get("search", "").strip()
    page     = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))
    corpus   = current_app.config["CORPUS_PATH"]
    return jsonify(handle_get_vocabulary(corpus_path=corpus, search=search, page=page, per_page=per_page))


# ── Document Inspection ────────────────────────────────────────────────────────

@api_bp.route("/doc/<doc_id>", methods=["GET"])
def get_doc(doc_id):
    corpus = current_app.config["CORPUS_PATH"]
    ir     = get_ir_system(corpus)
    index  = ir["index"]
    if doc_id not in index.documents:
        return jsonify({"error": "Document not found"}), 404
    doc = index.documents[doc_id]
    return jsonify({
        "doc_id":           doc.doc_id,
        "category":         doc.category,
        "title":            doc.title,
        "text":             doc.text,
        "combined_text":    doc.combined_text,
        "vector_length":    round(doc.vector_length, 4),
        "term_frequencies": doc.tf_dict,
        "term_positions":   doc.positions_dict,
        "tokens": [
            {"term": t, "pos": p, "start": s, "end": e}
            for t, p, s, e in doc.tokens
        ]
    })
