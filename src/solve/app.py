import json

def lambda_handler(event, context):
    # Handle preflight OPTIONS request
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': ''
        }
    
    try:
        body = json.loads(event['body'])
        matrix = body['matrix']
        
        # Calculate determinant with step-by-step breakdown using ijk notation
        # Matrix elements: [i][j][k] pattern
        # Positive terms: aei + bfg + cdh (left to right diagonals)
        # Negative terms: ceg + afh + bdi (right to left diagonals)
        
        a, b, c = matrix[0]  # i=0
        d, e, f = matrix[1]  # i=1
        g, h, i = matrix[2]  # i=2
        
        # Positive terms (left to right)
        pos1 = a * e * i  # a₀₀ * e₁₁ * i₂₂
        pos2 = b * f * g  # b₀₁ * f₁₂ * g₂₀
        pos3 = c * d * h  # c₀₂ * d₁₀ * h₂₁
        positive = pos1 + pos2 + pos3
        
        # Negative terms (right to left)
        neg1 = c * e * g  # c₀₂ * e₁₁ * g₂₀
        neg2 = a * f * h  # a₀₀ * f₁₂ * h₂₁
        neg3 = b * d * i  # b₀₁ * d₁₀ * i₂₂
        negative = neg1 + neg2 + neg3
        
        det = positive - negative
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'determinant': det,
                'calculation': f"Positive: {a}×{e}×{i} + {b}×{f}×{g} + {c}×{d}×{h} | Negative: {c}×{e}×{g} + {a}×{f}×{h} + {b}×{d}×{i}",
                'steps': f"({pos1} + {pos2} + {pos3}) - ({neg1} + {neg2} + {neg3}) = {positive} - {negative} = {det}"
            })
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(e)})
        }
