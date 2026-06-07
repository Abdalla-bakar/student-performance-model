const API_URL = 'https://student-performance-model-s23t.onrender.com/predict';
 
let extraValue = 'Yes';
 
function setExtra(val) {
  extraValue = val;
  document.getElementById('btn-yes').classList.toggle('active', val === 'Yes');
  document.getElementById('btn-no').classList.toggle('active', val === 'No');
}
 
async function predict() {
  const hoursRaw  = document.getElementById('hours').value;
  const scoresRaw = document.getElementById('scores').value;
  const sleepRaw  = document.getElementById('sleep').value;
  const papersRaw = document.getElementById('papers').value;
 
  const hours  = parseInt(hoursRaw);
  const scores = parseInt(scoresRaw);
  const sleep  = parseInt(sleepRaw);
  const papers = parseInt(papersRaw);
 
  const btn    = document.getElementById('predictBtn');
  const result = document.getElementById('result');
 
  // BUG FIX: use .trim() === '' to check empty, NOT falsy check
  // because !papers would block papers=0 which is a valid value
  if (hoursRaw.trim() === '' || scoresRaw.trim() === '' || sleepRaw.trim() === '' || papersRaw.trim() === '') {
    showError('Please fill in all fields.'); return;
  }
  if (isNaN(hours) || isNaN(scores) || isNaN(sleep) || isNaN(papers)) {
    showError('Please enter valid numbers.'); return;
  }
  if (hours < 1 || hours > 9)     { showError('Hours studied must be 1–9.'); return; }
  if (scores < 40 || scores > 99) { showError('Previous score must be 40–99.'); return; }
  if (sleep < 4 || sleep > 9)     { showError('Sleep hours must be 4–9.'); return; }
  if (papers < 0 || papers > 9)   { showError('Papers practiced must be 0–9.'); return; }
 
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
 
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || 'API error: ' + res.status);
    }
    const data = await res.json();
    showSuccess(data);
 
  } catch (err) {
    showError('Request failed: ' + err.message);
  } finally {
    btn.disabled = false;
    btn.innerHTML = 'Predict Performance →';
  }
}
 
function showSuccess(data) {
  const result = document.getElementById('result');
  const pct = Math.min(100, Math.max(0, data.performance_index));
 
  result.className = 'result success show';
  result.style.display = '';
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
  result.style.display = '';
  result.innerHTML = `<p class="error-msg">⚠️ ${msg}</p>`;
}