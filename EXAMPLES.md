# Risko Platform - Quick Start Examples

## Starting the Server

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## Example Usage

### 1. Basic Risk Analysis (Python)

```python
import requests

# Analyze risk for an address
response = requests.post(
    "http://localhost:8000/api/v1/risk/analyze",
    json={"address": "Istanbul, Turkey"}
)

data = response.json()
print(f"Address: {data['address']}")
print(f"Overall Risk Score: {data['overall_risk_score']}")
print(f"Risk Level: {data['risk_level']}")
print(f"Earthquake Risk: {data['earthquake_risk']}")
print(f"Flood Risk: {data['flood_risk']}")
print(f"Fire Risk: {data['fire_risk']}")
print(f"Landslide Risk: {data['landslide_risk']}")
```

**Output:**
```
Address: Istanbul, Turkey
Overall Risk Score: 54.85
Risk Level: high
Earthquake Risk: 74.88
Flood Risk: 53.59
Fire Risk: 21.89
Landslide Risk: 47.44
```

### 2. Detailed Risk Report (Python)

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/risk/analyze/detailed",
    json={"address": "Ankara, Turkey"}
)

data = response.json()

# Print risk scores
print(f"Overall Risk: {data['risk_score']['overall_risk_score']}")

# Print recommendations
print("\nRecommendations:")
for rec in data['recommendations']:
    print(f"  - {rec['title']} (Priority: {rec['priority']})")
    
# Print analysis
print("\nAnalysis:")
for risk_type, analysis in data['analysis'].items():
    print(f"  {risk_type}: {analysis}")
```

### 3. Risk Visualization (Python)

```python
import requests
import json

response = requests.post(
    "http://localhost:8000/api/v1/risk/visualize",
    json={"address": "Izmir, Turkey"}
)

data = response.json()

# Save GeoJSON for map visualization
with open('risk_map.geojson', 'w') as f:
    json.dump(data['risk_map_data'], f, indent=2)

# Print heat map data
print("Heat Map Layers:")
for risk_type, points in data['heat_map_layers'].items():
    print(f"  {risk_type}: {len(points)} points")
```

### 4. B2B Batch Analysis (Python)

```python
import requests

headers = {
    "X-API-Key": "your-api-key-here"
}

addresses = [
    {"address": "Istanbul, Besiktas"},
    {"address": "Ankara, Cankaya"},
    {"address": "Izmir, Konak"}
]

response = requests.post(
    "http://localhost:8000/api/v1/b2b/batch-analyze",
    headers=headers,
    json=addresses
)

results = response.json()

for result in results:
    print(f"{result['address']}: Risk Level = {result['risk_level']} "
          f"(Score: {result['overall_risk_score']})")
```

### 5. Regional Statistics (Python)

```python
import requests

headers = {
    "X-API-Key": "your-api-key-here"
}

response = requests.get(
    "http://localhost:8000/api/v1/b2b/risk-statistics?region=Istanbul",
    headers=headers
)

stats = response.json()

print(f"Region: {stats['region']}")
print(f"Total Analyzed Addresses: {stats['total_analyzed_addresses']}")
print(f"Average Earthquake Risk: {stats['average_earthquake_risk']}")
print(f"Average Flood Risk: {stats['average_flood_risk']}")
print(f"High Risk %: {stats['high_risk_percentage']}")
print(f"Critical Risk %: {stats['critical_risk_percentage']}")
```

## JavaScript Examples

### Basic Risk Analysis (Node.js)

```javascript
const axios = require('axios');

async function analyzeRisk(address) {
    try {
        const response = await axios.post(
            'http://localhost:8000/api/v1/risk/analyze',
            { address: address }
        );
        
        const data = response.data;
        console.log(`Address: ${data.address}`);
        console.log(`Overall Risk: ${data.overall_risk_score}`);
        console.log(`Risk Level: ${data.risk_level}`);
        
        return data;
    } catch (error) {
        console.error('Error:', error.message);
    }
}

analyzeRisk('Istanbul, Turkey');
```

### B2B Batch Analysis (Node.js)

```javascript
const axios = require('axios');

async function batchAnalyze(addresses) {
    try {
        const response = await axios.post(
            'http://localhost:8000/api/v1/b2b/batch-analyze',
            addresses.map(addr => ({ address: addr })),
            {
                headers: {
                    'X-API-Key': 'your-api-key-here'
                }
            }
        );
        
        return response.data;
    } catch (error) {
        console.error('Error:', error.message);
    }
}

const addresses = ['Istanbul, Turkey', 'Ankara, Turkey'];
batchAnalyze(addresses).then(results => {
    results.forEach(result => {
        console.log(`${result.address}: ${result.risk_level}`);
    });
});
```

## cURL Examples

### Basic Risk Analysis

```bash
curl -X POST "http://localhost:8000/api/v1/risk/analyze" \
  -H "Content-Type: application/json" \
  -d '{"address": "Istanbul, Turkey"}'
```

### Detailed Report

```bash
curl -X POST "http://localhost:8000/api/v1/risk/analyze/detailed" \
  -H "Content-Type: application/json" \
  -d '{"address": "Ankara, Turkey"}'
```

### B2B Batch Analysis

```bash
curl -X POST "http://localhost:8000/api/v1/b2b/batch-analyze" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '[
    {"address": "Istanbul, Turkey"},
    {"address": "Ankara, Turkey"}
  ]'
```

### Regional Statistics

```bash
curl -X GET "http://localhost:8000/api/v1/b2b/risk-statistics?region=Istanbul" \
  -H "X-API-Key: your-api-key-here"
```

## Using the Interactive API Documentation

Visit http://localhost:8000/docs to access the interactive Swagger UI where you can:
1. See all available endpoints
2. Test APIs directly in the browser
3. View request/response schemas
4. Get code examples in multiple languages

## Integration with Insurance System Example

```python
import requests

class RiskoInsuranceIntegration:
    def __init__(self, api_key):
        self.base_url = "http://localhost:8000/api/v1"
        self.headers = {"X-API-Key": api_key}
    
    def calculate_premium(self, address, coverage_amount):
        """Calculate insurance premium based on risk score."""
        
        # Get risk analysis
        response = requests.post(
            f"{self.base_url}/b2b/premium-analyze",
            headers=self.headers,
            json={"address": address}
        )
        
        risk_data = response.json()
        risk_score = risk_data['risk_score']['overall_risk_score']
        
        # Calculate premium (simple example)
        base_rate = 0.01  # 1% base rate
        risk_multiplier = 1 + (risk_score / 100)
        annual_premium = coverage_amount * base_rate * risk_multiplier
        
        return {
            'address': address,
            'coverage_amount': coverage_amount,
            'annual_premium': annual_premium,
            'risk_score': risk_score,
            'risk_level': risk_data['risk_score']['risk_level'],
            'recommendations': [r['title'] for r in risk_data['recommendations'][:3]]
        }

# Usage
integration = RiskoInsuranceIntegration("your-api-key")
premium_info = integration.calculate_premium("Istanbul, Besiktas", 500000)

print(f"Property: {premium_info['address']}")
print(f"Coverage: ${premium_info['coverage_amount']:,}")
print(f"Annual Premium: ${premium_info['annual_premium']:,.2f}")
print(f"Risk Level: {premium_info['risk_level']}")
print(f"Recommendations: {', '.join(premium_info['recommendations'])}")
```

## Real Estate Platform Integration Example

```python
import requests

class RiskoRealEstateIntegration:
    def __init__(self, api_key):
        self.base_url = "http://localhost:8000/api/v1"
        self.headers = {"X-API-Key": api_key}
    
    def enrich_property_listing(self, property_data):
        """Add risk information to property listing."""
        
        response = requests.post(
            f"{self.base_url}/b2b/premium-analyze",
            headers=self.headers,
            json={
                "address": property_data['address']
            },
            params={
                "building_age": property_data.get('year_built')
            }
        )
        
        risk_data = response.json()
        
        # Add risk information to property
        property_data['risk_info'] = {
            'overall_score': risk_data['risk_score']['overall_risk_score'],
            'risk_level': risk_data['risk_score']['risk_level'],
            'earthquake_risk': risk_data['risk_score']['earthquake_risk'],
            'flood_risk': risk_data['risk_score']['flood_risk'],
            'recommendations': risk_data['recommendations'][:5]
        }
        
        return property_data

# Usage
integration = RiskoRealEstateIntegration("your-api-key")

property = {
    'id': 12345,
    'address': 'Istanbul, Kadikoy',
    'price': 1200000,
    'year_built': 1995
}

enriched_property = integration.enrich_property_listing(property)
print(f"Property {enriched_property['id']}")
print(f"Risk Level: {enriched_property['risk_info']['risk_level']}")
print(f"Risk Score: {enriched_property['risk_info']['overall_score']}")
```

## Testing

Run the test suite:

```bash
cd backend
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ -v --cov=app --cov-report=html
```

## Next Steps

1. **Get an API Key**: Contact us for B2B API access
2. **Explore the Docs**: Visit http://localhost:8000/docs
3. **Read the API Documentation**: See [API_DOCUMENTATION.md](../API_DOCUMENTATION.md)
4. **Check the Examples**: Try the code examples above
5. **Integrate**: Use our API in your application
