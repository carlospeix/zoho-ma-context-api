from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
import requests
import os
from datetime import datetime
from pathlib import Path

app = FastAPI(title="Customer Context API", version="1.0.0")

# Create static directory for widget files
static_dir = Path("static")
static_dir.mkdir(exist_ok=True)

# Enable CORS for testing (allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to Zoho domains
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Mount static files for serving widget assets
app.mount("/static", StaticFiles(directory="static"), name="static")

# Data models
class CustomerSummary(BaseModel):
    customer_id: str
    account_value: float
    risk_score: str
    support_tier: str
    last_contact: str

class SupportTicket(BaseModel):
    date: str
    issue_type: str
    priority: str
    status: str
    resolution_time: Optional[str]

class CustomerContext(BaseModel):
    summary: CustomerSummary
    recent_tickets: List[SupportTicket]
    account_info: dict

# API Endpoints
@app.get("/")
async def root():
    """Serve the main widget page for testing"""
    return HTMLResponse(content=get_widget_html(), media_type="text/html")

@app.get("/widget")
async def widget_page():
    """Alternative endpoint for the widget"""
    return HTMLResponse(content=get_widget_html(), media_type="text/html")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/customer/{customer_id}/context", response_model=CustomerContext)
async def get_customer_context(customer_id: str):
    """
    Main endpoint that aggregates customer data from multiple sources
    """
    try:
        # This is where you'll integrate with your internal systems
        summary = await fetch_customer_summary(customer_id)
        tickets = await fetch_support_history(customer_id)
        account_info = await fetch_account_info(customer_id)
        
        return CustomerContext(
            summary=summary,
            recent_tickets=tickets,
            account_info=account_info
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Internal data fetching functions
async def fetch_customer_summary(customer_id: str) -> CustomerSummary:
    """
    Fetch customer summary from your systems
    Replace with actual integration logic
    """
    # Example: Call your ERP/CRM/Database
    # response = requests.get(f"https://your-erp.com/api/customers/{customer_id}")
    
    # Mock data for now
    return CustomerSummary(
        customer_id=customer_id,
        account_value=45230.00,
        risk_score="Low",
        support_tier="Premium",
        last_contact="3 days ago"
    )

async def fetch_support_history(customer_id: str) -> List[SupportTicket]:
    """
    Fetch support ticket history
    """
    # Mock data - replace with actual data source
    return [
        SupportTicket(
            date="2025-09-15",
            issue_type="Technical Issue",
            priority="High",
            status="Resolved",
            resolution_time="4.2 hours"
        ),
        SupportTicket(
            date="2025-09-10",
            issue_type="Billing Question",
            priority="Medium",
            status="Resolved",
            resolution_time="1.8 hours"
        )
    ]

async def fetch_account_info(customer_id: str) -> dict:
    """
    Fetch additional account information
    """
    return {
        "account_manager": "Sarah Johnson",
        "implementation_date": "March 15, 2023",
        "license_count": 125,
        "contract_end_date": "March 15, 2026"
    }

def get_widget_html():
    """Return the complete widget HTML with embedded CSS and JS for testing"""
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Customer Context Widget - Test Mode</title>
    <style>
        /* Reset and base styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 14px;
            line-height: 1.4;
            color: #333;
            background-color: #f5f5f5;
            padding: 20px;
        }

        #app {
            background: white;
            padding: 16px;
            max-width: 800px;
            margin: 0 auto;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .test-header {
            background: #007bff;
            color: white;
            padding: 12px;
            margin: -16px -16px 20px -16px;
            border-radius: 8px 8px 0 0;
        }

        .test-controls {
            background: #f8f9fa;
            padding: 12px;
            margin: 20px -16px -16px -16px;
            border-radius: 0 0 8px 8px;
            border-top: 1px solid #dee2e6;
        }

        .test-controls button {
            background: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 8px;
            font-size: 13px;
        }

        .test-controls button:hover {
            background: #0056b3;
        }

        /* Widget container */
        .widget-container {
            margin-bottom: 20px;
        }

        .widget-title {
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e9ecef;
        }

        /* Summary cards layout */
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }

        .summary-card {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 6px;
            border-left: 4px solid #007bff;
            text-align: center;
        }

        .card-title {
            font-size: 11px;
            font-weight: 600;
            color: #6c757d;
            margin-bottom: 6px;
            text-transform: uppercase;
        }

        .card-value {
            font-size: 16px;
            font-weight: 700;
            color: #333;
        }

        /* Data table styles */
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 12px;
            font-size: 13px;
        }

        .data-table th {
            background-color: #f8f9fa;
            padding: 10px 8px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #dee2e6;
            color: #495057;
            font-size: 12px;
        }

        .data-table td {
            padding: 10px 8px;
            border-bottom: 1px solid #dee2e6;
        }

        .data-table tbody tr:hover {
            background-color: #f8f9fa;
        }

        /* Status indicators */
        .status {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .status.resolved { 
            background-color: #d4edda; 
            color: #155724; 
        }

        .status.active { 
            background-color: #d4edda; 
            color: #155724; 
        }

        .status.pending { 
            background-color: #fff3cd; 
            color: #856404; 
        }

        .status.inactive { 
            background-color: #f8d7da; 
            color: #721c24; 
        }

        /* Loading state */
        .loading {
            text-align: center;
            padding: 40px 20px;
            color: #6c757d;
            font-size: 14px;
        }

        /* Error state */
        .error {
            background-color: #f8d7da;
            color: #721c24;
            padding: 12px;
            border-radius: 6px;
            margin: 16px 0;
            text-align: center;
            font-size: 13px;
        }

        /* Success state for testing */
        .success {
            background-color: #d4edda;
            color: #155724;
            padding: 12px;
            border-radius: 6px;
            margin: 16px 0;
            text-align: center;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div id="app">
        <div class="test-header">
            <h2>🧪 Customer Context Widget - Test Mode</h2>
            <p>Testing the widget locally with Python API</p>
        </div>
        
        <div id="loading" class="loading">
            🔄 Loading customer context...
        </div>
        <div id="content" style="display: none;">
            <!-- Content will be populated by JavaScript -->
        </div>
        <div id="error" style="display: none;" class="error">
            Unable to load customer data. Check the console for details.
        </div>
        <div id="success" style="display: none;" class="success">
            ✅ Successfully loaded data from Python API!
        </div>

        <div class="test-controls">
            <button onclick="loadCustomerContext('TEST_CUSTOMER_123')">🔄 Reload Data</button>
            <button onclick="testErrorState()">❌ Test Error</button>
            <button onclick="showApiInfo()">📋 API Info</button>
        </div>
    </div>

    <script>
        // Configuration - automatically uses the current server
        const API_BASE_URL = window.location.origin;

        // Initialize widget on page load
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Widget initialized in test mode');
            loadCustomerContext('TEST_CUSTOMER_123');
        });

        async function loadCustomerContext(customerId) {
            try {
                showLoading();
                console.log(`Loading context for customer: ${customerId}`);
                
                // Fetch data from your Python API
                const response = await fetch(`${API_BASE_URL}/customer/${customerId}/context`);
                
                if (!response.ok) {
                    throw new Error(`API Error: ${response.status} ${response.statusText}`);
                }
                
                const contextData = await response.json();
                console.log('Received context data:', contextData);
                
                displayCustomerContext(contextData);
                showSuccess();
                
            } catch (error) {
                console.error('Error loading customer context:', error);
                showError(error.message);
            }
        }

        function displayCustomerContext(data) {
            const contentDiv = document.getElementById('content');
            
            contentDiv.innerHTML = `
                <div class="widget-container">
                    <div class="widget-title">💼 Customer Overview</div>
                    <div class="summary-cards">
                        <div class="summary-card">
                            <div class="card-title">Account Value</div>
                            <div class="card-value">${data.summary.account_value.toLocaleString()}</div>
                        </div>
                        <div class="summary-card">
                            <div class="card-title">Risk Score</div>
                            <div class="card-value" style="color: ${getRiskColor(data.summary.risk_score)}">${data.summary.risk_score}</div>
                        </div>
                        <div class="summary-card">
                            <div class="card-title">Support Tier</div>
                            <div class="card-value">${data.summary.support_tier}</div>
                        </div>
                        <div class="summary-card">
                            <div class="card-title">Last Contact</div>
                            <div class="card-value">${data.summary.last_contact}</div>
                        </div>
                    </div>
                    
                    <div class="widget-title">🎫 Recent Support History</div>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Issue Type</th>
                                <th>Priority</th>
                                <th>Status</th>
                                <th>Resolution Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${data.recent_tickets.map(ticket => `
                                <tr>
                                    <td>${ticket.date}</td>
                                    <td>${ticket.issue_type}</td>
                                    <td>${ticket.priority}</td>
                                    <td><span class="status ${ticket.status.toLowerCase()}">${ticket.status}</span></td>
                                    <td>${ticket.resolution_time || 'N/A'}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>

                    <div class="widget-title">📊 Account Information</div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                        ${Object.entries(data.account_info).map(([key, value]) => `
                            <div style="padding: 8px 0; border-bottom: 1px solid #e9ecef;">
                                <div style="font-size: 11px; color: #6c757d; margin-bottom: 4px; text-transform: uppercase; font-weight: 600;">
                                    ${key.replace('_', ' ')}
                                </div>
                                <div style="font-size: 14px; color: #333; font-weight: 500;">
                                    ${value}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
            
            hideLoading();
            contentDiv.style.display = 'block';
        }

        function getRiskColor(riskScore) {
            switch(riskScore.toLowerCase()) {
                case 'low': return '#28a745';
                case 'medium': return '#ffc107';
                case 'high': return '#dc3545';
                default: return '#333';
            }
        }

        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('content').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            document.getElementById('success').style.display = 'none';
        }

        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
        }

        function showError(message = 'Unknown error occurred') {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('success').style.display = 'none';
            const errorDiv = document.getElementById('error');
            errorDiv.innerHTML = `❌ Error: ${message}`;
            errorDiv.style.display = 'block';
        }

        function showSuccess() {
            setTimeout(() => {
                const successDiv = document.getElementById('success');
                successDiv.style.display = 'block';
                setTimeout(() => {
                    successDiv.style.display = 'none';
                }, 3000);
            }, 500);
        }

        // Test functions
        function testErrorState() {
            showError('This is a test error message');
        }

        function showApiInfo() {
            alert(`API Base URL: ${API_BASE_URL}\\n\\nAvailable endpoints:\\n• GET /health\\n• GET /customer/{id}/context\\n• GET / (this widget)`);
        }

        // Log API base URL for debugging
        console.log('API Base URL:', API_BASE_URL);
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
