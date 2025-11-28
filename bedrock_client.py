import boto3
import json
from typing import Optional, Dict, Any

class BedrockAnalyzer:
    def __init__(self, region_name='us-east-1', model_id='us.anthropic.claude-3-5-sonnet-20240620-v1:0'):
        self.region_name = region_name
        self.model_id = model_id
        self.client = boto3.client('bedrock-runtime', region_name=region_name)
    
    def analyze_data(self, prompt: str, context: Optional[str] = None, max_tokens: int = 4096) -> Dict[str, Any]:
        """Send analysis request to Claude via Bedrock"""
        try:
            full_prompt = prompt
            if context:
                full_prompt = f"Context:\n{context}\n\nQuestion:\n{prompt}"
            
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            
            if 'content' in response_body and len(response_body['content']) > 0:
                analysis_text = response_body['content'][0]['text']
                return {
                    'success': True,
                    'analysis': analysis_text,
                    'model': self.model_id
                }
            else:
                return {
                    'success': False,
                    'error': 'No content in response'
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def summarize_trends(self, data_summary: str) -> str:
        """Generate executive summary of SLOOS trends"""
        prompt = f"""Analyze the following SLOOS (Senior Loan Officer Opinion Survey) data and provide an executive summary of key trends:

{data_summary}

Please provide:
1. Overall credit conditions assessment
2. Key trends in lending standards
3. Notable changes in loan demand
4. Risk indicators and concerns
5. Forward-looking implications

Keep the summary concise and actionable for financial decision-makers."""
        
        result = self.analyze_data(prompt)
        return result.get('analysis', 'Error generating summary') if result['success'] else f"Error: {result.get('error')}"
    
    def sentiment_analysis(self, data_summary: str, loan_category: str) -> str:
        """Perform sentiment analysis on specific loan category"""
        prompt = f"""Analyze the sentiment and trends for {loan_category} based on the following SLOOS data:

{data_summary}

Provide:
1. Sentiment score (positive/neutral/negative)
2. Trend direction (tightening/stable/easing)
3. Key factors driving the sentiment
4. Comparison to other loan categories if relevant"""
        
        result = self.analyze_data(prompt)
        return result.get('analysis', 'Error generating sentiment analysis') if result['success'] else f"Error: {result.get('error')}"
    
    def custom_query(self, query: str, data_context: str) -> str:
        """Answer custom questions about SLOOS data"""
        prompt = f"""Based on the following SLOOS data, please answer this question:

Question: {query}

Data Context:
{data_context}

Provide a detailed, data-driven answer with specific insights and trends."""
        
        result = self.analyze_data(prompt)
        return result.get('analysis', 'Error processing query') if result['success'] else f"Error: {result.get('error')}"
    
    def compare_periods(self, period1_data: str, period2_data: str) -> str:
        """Compare SLOOS data between two time periods"""
        prompt = f"""Compare the following two periods of SLOOS data and identify key changes:

Period 1:
{period1_data}

Period 2:
{period2_data}

Highlight:
1. Major shifts in lending standards
2. Changes in loan demand patterns
3. Emerging risks or opportunities
4. Sector-specific trends"""
        
        result = self.analyze_data(prompt)
        return result.get('analysis', 'Error comparing periods') if result['success'] else f"Error: {result.get('error')}"
