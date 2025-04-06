async function sendQuery() {
    const query = document.getElementById("queryInput").value;
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<p>Searching...</p>";
  
    try {
      const response = await fetch("http://localhost:9000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ query })
      });
  
      const data = await response.json();
  
      if (data.recommendations && data.recommendations.length > 0) {
        resultsDiv.innerHTML = data.recommendations.map((r, index) => `
          <div class="card">
            <h3>🏆 Rank ${index + 1}: ${r.Assignment_Name}</h3>
            <p>🔗 <a href="${r.Assignment_Link}" target="_blank">${r.Assignment_Link}</a></p>
            <p>🧪 Test Type: ${r.Test_Type}</p>
            <p>⏱️ Duration: ${r.Approximate_Completion_Time} mins</p>
            <p>🌐 Remote Testing: ${r.Remote_Testing_Support}</p>
            <p>📊 Adaptive/IRT: ${r.Adaptive_IRT_Support}</p>
            <p>👤 Job Levels: ${r.Job_Levels}</p>
          </div>
        `).join("");
      } else {
        resultsDiv.innerHTML = "<p>No results found.</p>";
      }
    } catch (error) {
      resultsDiv.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
    }
  }
  