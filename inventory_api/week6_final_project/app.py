from flask import Flask, request, jsonify
from langchain_service import run_llm
from cost_utils import calculate_cost


app = Flask(__name__)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    if not data or "query" not in data or "title" not in data:
        return jsonify({
            "error": "Invalid request",
            "message": "query and title fields are required"
            
        }), 400

    query = data["query"]
    title = data["title"]

    try:
        result = run_llm(query,title)
        usage = result["usage"]

        cost = calculate_cost(
        usage["prompt_tokens"],
        usage["completion_tokens"]
        )


        return jsonify({
            "query": query,
            "title": title,
            "response": result["text"],
            "usage": result["usage"],
            "cost_usd": cost
        })

    except Exception as e:
        return jsonify({
            "error": "Failed to process request",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)


