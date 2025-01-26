from flask import Flask, request, jsonify
from competitor_analysis_agent import CompetitorAnalysisAgent

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_competitors():
    """
    Endpoint to analyze competitors.
    Expects a JSON body with a list of URLs.
    """
    data = request.json
    urls = data.get('urls', [])
    
    if not urls:
        return jsonify({'error': 'No URLs provided'}), 400
    
    agent = CompetitorAnalysisAgent(urls)
    agent.run_analysis()
    
    return jsonify({'message': 'Analysis completed successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
