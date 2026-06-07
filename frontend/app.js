// Use a relative URL so this works on any domain (Render, custom domain, localhost)
const API_URL = 'https://student-performance-model-s23t.onrender.com';
 
let extraValue = 'Yes';
 
function setExtra(val) {
  extraValue = val;
  document.getElementById('btn-yes').classList.toggle('active', val === 'Yes');
  document.getElementById('btn-no').classList.toggle('active', val === 'No');
}
 
async function predict() {
  const hours  = parseInt(document.getElementById('hours').value);
  const scores = parseInt(document.getElementById('scores').value);
  const sleep  = parseInt(document.getElementById('sleep').value);
  const papers = parseInt(document.getElementById('papers').value);
  const btn    = document.getElementById('predictBtn');
  const result = document.getElementById('result');
 
  // Validate inputs
  if (!hours || !scores || !sleep || isNaN(papers)) {
    showError('Please fill in all fields.'); return;
  }
  if (hours < 1 || hours > 9)    { showError('Hours studied must be 1–9.'); return; }
  if (scores < 40 || scores > 99) { showError('Previous score must be 40–99.'); return; }
  if (sleep < 4 || sleep > 9)    { showError('Sleep hours must be 4–9.'); return; }
  if (papers < 0 || papers > 9)  { showError('Papers practiced must be 0–9.'); return; }
 
  // Loading state
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Predicting...';
  result.className = 'result';
  result.style.display = 'none';
 
  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        hours_studied: hours,
        previous_scores: scores,
        extracurricular_activities: extraValue,
        sleep_hours: sleep,
        sample_question_papers_practiced: papers
      })
    });
 
    if (!res.ok) throw new Error('API error: ' + res.status);
    const data = await res.json();
    showSuccess(data);
 
  } catch (err) {
    showError('Connection failed. Make sure the API is running.<br/><small>' + err.message + '</small>');
 
  } finally {
    btn.disabled = false;
    btn.innerHTML = 'Predict Performance →';
  }
}
 
function showSuccess(data) {
  const result = document.getElementById('result');
  const pct = Math.min(100, Math.max(0, data.performance_index));
 
  result.className = 'result success show';
  result.innerHTML = `
    <div class="grade-badge">${data.grade}</div>
    <div class="score-label">Performance Index</div>
    <div class="score-value">${data.performance_index.toFixed(1)}</div>
    <div class="score-sub">out of 100</div>
    <div class="progress-wrap">
      <div class="progress-bar" id="pbar"></div>
    </div>
  `;
 
  setTimeout(() => {
    const bar = document.getElementById('pbar');
    if (bar) bar.style.width = pct + '%';
  }, 100);
}
 
function showError(msg) {
  const result = document.getElementById('result');
  result.className = 'result error show';
  result.innerHTML = `<p class="error-msg">⚠️ ${msg}</p>`;
}
