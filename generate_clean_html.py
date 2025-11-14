#!/usr/bin/env python3
"""Generate clean index.html with proper form validation"""

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MandiGPT - AI Crop Recommendation Tool</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #2ecc71;
            --secondary-color: #3498db;
            --dark: #2c3e50;
            --light: #ecf0f1;
        }
        * {
            margin: 0; padding: 0; box-sizing: border-box;
        }
        body {
            background-color: #f8f9fa;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .hero-section {
            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
            color: white; padding: 3rem 0;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        .hero-section h1 {
            font-weight: 700; margin-bottom: 1rem; font-size: 2.5rem;
        }
        .form-section {
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            padding: 2.5rem; margin-bottom: 2rem;
        }
        .form-step {
            margin-bottom: 2rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid var(--light);
        }
        .form-step:last-child {
            border-bottom: none;
        }
        .form-step-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--dark);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .form-step-icon {
            font-size: 1.5rem;
            color: var(--primary-color);
        }
        .form-label {
            font-weight: 600;
            color: var(--dark);
            margin-bottom: 0.5rem;
        }
        .form-select, .form-control {
            border: 2px solid var(--light);
            border-radius: 8px;
            padding: 0.75rem;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        .form-select:focus, .form-control:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 0.2rem rgba(46, 204, 113, 0.25);
        }
        .btn-primary {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
            padding: 0.75rem 2rem;
            font-weight: 600;
            border-radius: 8px;
            transition: all 0.3s;
        }
        .btn-primary:hover {
            background-color: #27ae60;
            border-color: #27ae60;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3);
        }
        .loading-spinner {
            display: none;
            text-align: center;
            padding: 2rem;
        }
        .loading-spinner.show {
            display: block;
        }
        .results-section {
            display: none;
            animation: slideIn 0.5s ease-out;
        }
        .results-section.show {
            display: block;
        }
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .recommendation-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 2px solid var(--light);
            transition: all 0.3s;
        }
        .recommendation-card:hover {
            border-color: var(--primary-color);
            box-shadow: 0 4px 15px rgba(46, 204, 113, 0.2);
            transform: translateY(-3px);
        }
        .recommendation-rank {
            display: inline-block;
            width: 40px;
            height: 40px;
            background: var(--primary-color);
            color: white;
            border-radius: 50%;
            text-align: center;
            line-height: 40px;
            font-weight: 700;
            margin-right: 1rem;
        }
        .recommendation-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--dark);
        }
        .detail-item {
            background: var(--light);
            padding: 0.75rem;
            border-radius: 8px;
            text-align: center;
        }
        .detail-label {
            font-size: 0.85rem;
            color: #7f8c8d;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }
        .detail-value {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--dark);
        }
        .info-badge {
            display: inline-block;
            background: rgba(52, 152, 219, 0.1);
            color: var(--secondary-color);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.9rem;
            margin: 0.5rem 0.25rem;
            font-weight: 600;
        }
        @media (max-width: 768px) {
            .hero-section h1 {
                font-size: 2rem;
            }
            .form-section {
                padding: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="hero-section">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-7">
                    <h1><i class="fas fa-leaf"></i> MandiGPT</h1>
                    <p class="lead">AI-powered crop recommendations with real government market prices</p>
                    <p class="text-white-50">Get personalized crop recommendations based on your location, soil type, and current market data.</p>
                    <div class="info-badges" style="margin-top: 1rem;">
                        <span class="info-badge"><i class="fas fa-map-marker-alt"></i> 28 States</span>
                        <span class="info-badge"><i class="fas fa-seedling"></i> 100+ Crops</span>
                        <span class="info-badge"><i class="fas fa-sync-alt"></i> Daily Updates</span>
                    </div>
                </div>
                <div class="col-lg-5 text-center">
                    <i class="fas fa-leaf" style="font-size: 6rem; opacity: 0.3; color: white;"></i>
                </div>
            </div>
        </div>
    </div>

    <div class="container my-5">
        <div class="form-section">
            <h2><i class="fas fa-calculator"></i> Get Your Crop Recommendations</h2>
            <form id="recommendationForm">
                <div class="form-step">
                    <div class="form-step-title">
                        <i class="fas fa-map-pin form-step-icon"></i> Step 1: Select Your Location
                    </div>
                    <div class="row">
                        <div class="col-md-4 mb-3">
                            <label for="state" class="form-label">State *</label>
                            <select class="form-select" id="state" required>
                                <option value="">Select State...</option>
                                <option>Andhra Pradesh</option>
                                <option>Arunachal Pradesh</option>
                                <option>Assam</option>
                                <option>Bihar</option>
                                <option>Chhattisgarh</option>
                                <option>Goa</option>
                                <option>Gujarat</option>
                                <option>Haryana</option>
                                <option>Himachal Pradesh</option>
                                <option>Jharkhand</option>
                                <option>Karnataka</option>
                                <option>Kerala</option>
                                <option>Madhya Pradesh</option>
                                <option>Maharashtra</option>
                                <option>Manipur</option>
                                <option>Meghalaya</option>
                                <option>Mizoram</option>
                                <option>Nagaland</option>
                                <option>Odisha</option>
                                <option>Punjab</option>
                                <option>Rajasthan</option>
                                <option>Sikkim</option>
                                <option>Tamil Nadu</option>
                                <option>Telangana</option>
                                <option>Tripura</option>
                                <option>Uttar Pradesh</option>
                                <option>Uttarakhand</option>
                                <option>West Bengal</option>
                            </select>
                        </div>
                        <div class="col-md-4 mb-3">
                            <label for="district" class="form-label">District *</label>
                            <input type="text" class="form-control" id="district" placeholder="Enter district name" required>
                        </div>
                        <div class="col-md-4 mb-3">
                            <label for="market" class="form-label">Market</label>
                            <input type="text" class="form-control" id="market" placeholder="Enter market name">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="latitude" class="form-label">Latitude</label>
                            <input type="number" class="form-control" id="latitude" step="any" placeholder="e.g., 18.5204">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="longitude" class="form-label">Longitude</label>
                            <input type="number" class="form-control" id="longitude" step="any" placeholder="e.g., 73.8567">
                        </div>
                    </div>
                </div>

                <div class="form-step">
                    <div class="form-step-title">
                        <i class="fas fa-farm form-step-icon"></i> Step 2: Your Farm Profile
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="soilType" class="form-label">Soil Type *</label>
                            <select class="form-select" id="soilType" required>
                                <option value="">Select Soil Type...</option>
                                <option value="black">Black Soil</option>
                                <option value="red">Red Soil</option>
                                <option value="laterite">Laterite Soil</option>
                                <option value="mountain">Mountain Soil</option>
                                <option value="desert">Desert Soil</option>
                                <option value="alluvial">Alluvial Soil</option>
                            </select>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="season" class="form-label">Season *</label>
                            <select class="form-select" id="season" required>
                                <option value="">Select Season...</option>
                                <option value="Kharif">Kharif (Jun-Oct)</option>
                                <option value="Rabi">Rabi (Oct-Mar)</option>
                                <option value="Zaid">Zaid/Summer (Mar-Jun)</option>
                            </select>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="budget" class="form-label">Farm Budget (₹)</label>
                            <input type="number" class="form-control" id="budget" min="0" placeholder="Enter budget">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="farmSize" class="form-label">Farm Size (Acres)</label>
                            <input type="number" class="form-control" id="farmSize" min="0.1" step="0.1" placeholder="e.g., 2.5">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12 mb-3">
                            <label for="riskTolerance" class="form-label">Risk Tolerance</label>
                            <select class="form-select" id="riskTolerance">
                                <option value="Low">Low Risk</option>
                                <option value="Medium" selected>Medium Risk</option>
                                <option value="High">High Risk</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div class="form-step">
                    <div class="form-step-title">
                        <i class="fas fa-leaf form-step-icon"></i> Step 3: Choose Crops (Optional)
                    </div>
                    <label for="preferredCrops" class="form-label">Select Crops</label>
                    <select class="form-select" id="preferredCrops" multiple size="8">
                        <option>Rice</option>
                        <option>Wheat</option>
                        <option>Cotton</option>
                        <option>Sugarcane</option>
                        <option>Maize</option>
                        <option>Tomato</option>
                        <option>Onion</option>
                        <option>Potato</option>
                        <option>Groundnut</option>
                        <option>Chillies</option>
                        <option>Turmeric</option>
                        <option>Cabbage</option>
                        <option>Cauliflower</option>
                        <option>Carrot</option>
                        <option>Cucumber</option>
                    </select>
                    <small class="text-muted d-block mt-2">Hold Ctrl (Cmd on Mac) to select multiple</small>
                </div>

                <div class="row mt-4">
                    <div class="col-12">
                        <button type="submit" class="btn btn-primary btn-lg w-100">
                            <i class="fas fa-magic"></i> Get Recommendations
                        </button>
                    </div>
                </div>
            </form>
        </div>

        <div id="loadingSpinner" class="loading-spinner">
            <div class="spinner-border text-success" role="status"></div>
            <p class="mt-3"><strong>Analyzing your farm...</strong></p>
        </div>

        <div id="resultsSection" class="results-section">
            <div class="row mb-4">
                <div class="col-12"><h3><i class="fas fa-trophy"></i> Top Crop Recommendations</h3></div>
                <div id="recommendationsContainer" class="col-12"></div>
            </div>
            <div class="row mb-4">
                <div class="col-12"><h3><i class="fas fa-lightbulb"></i> Agricultural Advice</h3></div>
                <div id="adviceContainer" class="col-12"></div>
            </div>
            <div class="row">
                <div class="col-12"><h3><i class="fas fa-chart-line"></i> Market Analysis</h3></div>
                <div id="marketAnalysisContainer" class="col-12"></div>
            </div>
        </div>

        <div id="debugSection" class="mt-4" style="display: none;">
            <div class="card">
                <div class="card-header bg-dark text-white d-flex justify-content-between">
                    <h5 class="mb-0">Debug Information</h5>
                    <button type="button" class="btn btn-sm btn-outline-light" onclick="document.getElementById('debugSection').style.display='none'">Close</button>
                </div>
                <div class="card-body">
                    <div id="debugContent" class="bg-light p-3" style="max-height: 400px; overflow-y: auto;"></div>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-dark text-white py-4 mt-5">
        <div class="container text-center">
            <p class="mb-0">MandiGPT - Ministry of Agriculture & Farmers Welfare, Government of India</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function debugLog(message, data) {
            console.log(message, data);
            const debugSection = document.getElementById('debugSection');
            const debugContent = document.getElementById('debugContent');
            const timestamp = new Date().toLocaleTimeString();
            debugSection.style.display = 'block';
            const logEntry = document.createElement('div');
            logEntry.className = 'mb-2 border-bottom pb-2';
            logEntry.innerHTML = `<small class="text-muted">${timestamp}</small><div><strong>${message}</strong></div><pre style="font-size: 0.8em; margin: 0;">${JSON.stringify(data, null, 2)}</pre>`;
            debugContent.insertBefore(logEntry, debugContent.firstChild);
        }

        document.getElementById('recommendationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            document.getElementById('loadingSpinner').classList.add('show');
            document.getElementById('resultsSection').classList.remove('show');
            
            try {
                const state = document.getElementById('state').value || '';
                const district = document.getElementById('district').value || '';
                const latitude = parseFloat(document.getElementById('latitude').value) || 0;
                const longitude = parseFloat(document.getElementById('longitude').value) || 0;
                const soilTypeRaw = (document.getElementById('soilType').value || 'black').toLowerCase();
                const riskToleranceRaw = document.getElementById('riskTolerance').value || 'Medium';
                const farmSize = parseFloat(document.getElementById('farmSize').value) || 1;
                const budget = parseFloat(document.getElementById('budget').value) || 0;
                
                const soilTypeMapped = {
                    'alluvial': 'Alluvial', 'black': 'Black', 'red': 'Red',
                    'laterite': 'Laterite', 'mountain': 'Mountain', 'desert': 'Desert'
                };
                const soil_type = soilTypeMapped[soilTypeRaw] || 'Black';
                
                const location = {
                    state: state,
                    district: district,
                    latitude: latitude,
                    longitude: longitude,
                    soil_type: soil_type
                };
                debugLog('Location Data:', location);

                const selectedCrops = Array.from(document.getElementById('preferredCrops').selectedOptions).map(o => o.value);
                debugLog('Selected Crops:', selectedCrops);

                debugLog('Fetching Weather...', {url: `/api/weather/${location.state}/${location.district}?lat=${location.latitude}&lon=${location.longitude}`});
                const weatherResponse = await fetch(`/api/weather/${location.state}/${location.district}?lat=${location.latitude}&lon=${location.longitude}`);
                if (!weatherResponse.ok) throw new Error('Weather API failed');
                const weatherData = await weatherResponse.json();
                debugLog('Weather Received:', weatherData);

                debugLog('Fetching Commodity Prices...', {});
                const commodityResponse = await fetch(`/api/commodity-prices?state=${location.state}&district=${location.district}&lat=${location.latitude}&lon=${location.longitude}&crops=${selectedCrops.join(',')}`);
                if (!commodityResponse.ok) throw new Error('Commodity API failed');
                const commodityData = await commodityResponse.json();
                debugLog('Commodity Data:', commodityData);

                const data = {
                    location: location,
                    land_size: farmSize,
                    budget: budget,
                    preferred_crops: selectedCrops,
                    risk_tolerance: riskToleranceRaw,
                    weather: weatherData.weather_forecast,
                    commodity_prices: commodityData.commodity_prices
                };
                debugLog('Sending Recommendations:', data);

                const response = await fetch('/api/recommendations', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(`HTTP ${response.status}: ${JSON.stringify(errorData.detail || errorData)}`);
                }

                const result = await response.json();
                debugLog('Recommendations:', result);
                displayResults(result);
                document.getElementById('loadingSpinner').classList.remove('show');
                document.getElementById('resultsSection').classList.add('show');
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('loadingSpinner').classList.remove('show');
                alert(`Error: ${error.message}`);
                debugLog('ERROR', {message: error.message});
            }
        });

        function displayResults(result) {
            const recContainer = document.getElementById('recommendationsContainer');
            recContainer.innerHTML = '';
            if (result.recommendations && result.recommendations.length > 0) {
                result.recommendations.forEach((rec, idx) => {
                    const card = document.createElement('div');
                    card.className = 'col-md-6 mb-3';
                    card.innerHTML = `<div class="recommendation-card"><div class="d-flex"><div class="recommendation-rank">#${idx+1}</div><div><div class="recommendation-title">${rec.crop_name}</div><div class="text-success"><strong>₹${rec.market_price || 0}/q</strong></div></div></div><div class="row mt-3"><div class="col-6"><div class="detail-item"><div class="detail-label">Confidence</div><div class="detail-value">${Math.round((rec.confidence_score || 0) * 100)}%</div></div></div><div class="col-6"><div class="detail-item"><div class="detail-label">Yield</div><div class="detail-value">${rec.expected_yield || 'N/A'}</div></div></div></div><div class="detail-item mt-3"><div class="detail-value text-success">₹${rec.estimated_profit || 0}</div></div></div>`;
                    recContainer.appendChild(card);
                });
            }
            const adviceContainer = document.getElementById('adviceContainer');
            adviceContainer.innerHTML = (result.advice && result.advice.length > 0) ? result.advice.map(a => `<div class="col-md-6 mb-3"><div class="card"><div class="card-header bg-info text-white"><h6 class="mb-0">${a.title || 'Advice'}</h6></div><div class="card-body"><p>${a.description || 'N/A'}</p></div></div></div>`).join('') : '<div class="alert alert-info">No advice available</div>';
            const marketContainer = document.getElementById('marketAnalysisContainer');
            marketContainer.innerHTML = result.market_analysis ? `<div class="col-12"><div class="card"><div class="card-body"><h5>${result.market_analysis.market_sentiment || 'N/A'}</h5><p>${result.market_analysis.market_recommendation || 'N/A'}</p></div></div></div>` : '<div class="alert alert-info">No analysis available</div>';
        }
    </script>
</body>
</html>
'''

# Write to file with UTF-8 encoding
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ index.html created successfully")
print(f"📊 File size: {len(html_content)} bytes")
