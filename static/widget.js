// Initialize Zoho Widget SDK
ZOHO.embeddedApp.on("PageLoad", function (data) {
  console.log("Widget loaded for record:", data);
  loadCustomerContext(data.EntityId);
});

ZOHO.embeddedApp.init().then(() => {
  console.log("Zoho SDK initialized");
});

// Configuration
const API_BASE_URL = 'https://your-api-server.com'; // Replace with your API URL

async function loadCustomerContext(recordId) {
  try {
    showLoading();

    // Get customer ID from current record
    const customerData = await getZohoRecordData(recordId);
    const customerId = customerData.Email || recordId; // Use email or record ID

    // Fetch data from your Python API
    const response = await fetch(`${API_BASE_URL}/customer/${customerId}/context`);

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    const contextData = await response.json();
    displayCustomerContext(contextData);

  } catch (error) {
    console.error('Error loading customer context:', error);
    showError();
  }
}

async function getZohoRecordData(recordId) {
  return new Promise((resolve, reject) => {
    ZOHO.CRM.API.getRecord({
      Entity: ZOHO.CRM.UI.getEntity(),
      RecordID: recordId
    }).then((data) => {
      resolve(data.data[0]);
    }).catch(reject);
  });
}

function displayCustomerContext(data) {
  const contentDiv = document.getElementById('content');

  contentDiv.innerHTML = `
        <div class="widget-container">
            <div class="widget-title">💼 Customer Overview</div>
            <div class="summary-cards">
                <div class="summary-card">
                    <div class="card-title">Account Value</div>
                    <div class="card-value">$${data.summary.account_value.toLocaleString()}</div>
                </div>
                <div class="summary-card">
                    <div class="card-title">Risk Score</div>
                    <div class="card-value">${data.summary.risk_score}</div>
                </div>
                <div class="summary-card">
                    <div class="card-title">Support Tier</div>
                    <div class="card-value">${data.summary.support_tier}</div>
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
                    </tr>
                </thead>
                <tbody>
                    ${data.recent_tickets.map(ticket => `
                        <tr>
                            <td>${ticket.date}</td>
                            <td>${ticket.issue_type}</td>
                            <td>${ticket.priority}</td>
                            <td><span class="status ${ticket.status.toLowerCase()}">${ticket.status}</span></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;

  hideLoading();
  contentDiv.style.display = 'block';
}

function showLoading() {
  document.getElementById('loading').style.display = 'block';
  document.getElementById('content').style.display = 'none';
  document.getElementById('error').style.display = 'none';
}

function hideLoading() {
  document.getElementById('loading').style.display = 'none';
}

function showError() {
  document.getElementById('loading').style.display = 'none';
  document.getElementById('error').style.display = 'block';
}