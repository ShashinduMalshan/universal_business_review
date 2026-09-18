// OmniReview AI - Modern Frontend State & Interactive Controller

let sentimentChart = null;

// Global Toast Manager
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  const icon = type === 'success' ? '<i class="fa-solid fa-circle-check text-emerald-400"></i>' :
               type === 'error' ? '<i class="fa-solid fa-circle-xmark text-rose-400"></i>' :
               '<i class="fa-solid fa-circle-info text-indigo-400"></i>';
  toast.className = 'toast';
  toast.innerHTML = `${icon} <span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// Tab Switching with Animation
function switchTab(tabId) {
  const tabs = ['single', 'batch', 'analytics', 'history'];
  tabs.forEach(t => {
    const btn = document.getElementById(`tab${t.charAt(0).toUpperCase() + t.slice(1)}`);
    const view = document.getElementById(`view${t.charAt(0).toUpperCase() + t.slice(1)}`);
    if (t === tabId) {
      btn.className = "flex-1 py-2.5 px-4 rounded-xl font-semibold text-xs sm:text-sm text-white bg-gradient-to-r from-indigo-600 to-purple-600 shadow-md shadow-indigo-500/20 flex items-center justify-center space-x-2 transition whitespace-nowrap";
      view.classList.remove('hidden');
    } else {
      btn.className = "flex-1 py-2.5 px-4 rounded-xl font-medium text-xs sm:text-sm text-slate-400 hover:text-slate-200 hover:bg-slate-900/60 flex items-center justify-center space-x-2 transition whitespace-nowrap";
      view.classList.add('hidden');
    }
  });

  if (tabId === 'analytics') loadAnalytics();
  if (tabId === 'history') loadHistory();
}

// Single Review Sentiment Analysis
async function analyzeSingleReview() {
  const text = document.getElementById('reviewInput').value.trim();
  if (!text) {
    showToast("Please enter a customer review to analyze.", "error");
    return;
  }

  const btn = document.getElementById('analyzeBtn');
  btn.disabled = true;
  btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-2"></i> Analyzing...`;

  try {
    const response = await fetch('/api/v1/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text })
    });

    if (!response.ok) {
      throw new Error(`Inference Error: ${response.statusText}`);
    }

    const data = await response.json();
    renderSingleResult(data);
    showToast("Sentiment analysis complete!", "success");
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles mr-2"></i> <span>Analyze Sentiment</span>`;
  }
}

function renderSingleResult(data) {
  document.getElementById('resultPlaceholder').classList.add('hidden');
  document.getElementById('resultCard').classList.remove('hidden');

  // Sentiment Banner Styling
  const banner = document.getElementById('sentimentBanner');
  const label = document.getElementById('sentimentLabel');
  const icon = document.getElementById('sentimentIcon');
  const iconCont = document.getElementById('sentimentIconContainer');

  label.innerText = data.sentiment;
  document.getElementById('confidenceBadge').innerText = `${(data.confidence * 100).toFixed(1)}% Confidence`;

  if (data.sentiment === 'Positive') {
    banner.className = "p-6 rounded-3xl border bg-emerald-950/40 border-emerald-500/40 text-emerald-300 shadow-xl flex items-center justify-between";
    icon.className = "fa-solid fa-face-smile text-emerald-400";
    iconCont.className = "w-14 h-14 rounded-2xl bg-emerald-900/60 border border-emerald-500/50 flex items-center justify-center text-3xl text-emerald-300 shadow-lg shadow-emerald-900/40";
  } else if (data.sentiment === 'Neutral') {
    banner.className = "p-6 rounded-3xl border bg-amber-950/40 border-amber-500/40 text-amber-300 shadow-xl flex items-center justify-between";
    icon.className = "fa-solid fa-face-meh text-amber-400";
    iconCont.className = "w-14 h-14 rounded-2xl bg-amber-900/60 border border-amber-500/50 flex items-center justify-center text-3xl text-amber-300 shadow-lg shadow-amber-900/40";
  } else {
    banner.className = "p-6 rounded-3xl border bg-rose-950/40 border-rose-500/40 text-rose-300 shadow-xl flex items-center justify-between";
    icon.className = "fa-solid fa-face-frown text-rose-400";
    iconCont.className = "w-14 h-14 rounded-2xl bg-rose-900/60 border border-rose-500/50 flex items-center justify-center text-3xl text-rose-300 shadow-lg shadow-rose-900/40";
  }

  // Probability Bars
  const pPos = (data.probabilities.Positive * 100).toFixed(1);
  const pNeu = (data.probabilities.Neutral * 100).toFixed(1);
  const pNeg = (data.probabilities.Negative * 100).toFixed(1);

  document.getElementById('probPosText').innerText = `${pPos}%`;
  document.getElementById('probNeuText').innerText = `${pNeu}%`;
  document.getElementById('probNegText').innerText = `${pNeg}%`;

  document.getElementById('probPosBar').style.width = `${pPos}%`;
  document.getElementById('probNeuBar').style.width = `${pNeu}%`;
  document.getElementById('probNegBar').style.width = `${pNeg}%`;

  // Emotion & Tone
  document.getElementById('emotionPrimary').innerText = data.emotion.primary_emotion;
  document.getElementById('emotionConfidence').innerText = `${(data.emotion.confidence * 100).toFixed(0)}%`;
  document.getElementById('emotionTone').innerText = data.emotion.tone_tag;

  // Dispatch & Ticket
  document.getElementById('dispatchPriority').innerText = data.action_recommendation.priority_level;
  document.getElementById('dispatchDept').innerText = data.action_recommendation.assigned_department;
  document.getElementById('dispatchAction').innerText = data.action_recommendation.recommended_action;

  // Aspect Badges
  const badgeCont = document.getElementById('aspectBadgesContainer');
  badgeCont.innerHTML = '';
  data.aspect_breakdown.forEach(ab => {
    const span = document.createElement('span');
    const color = ab.sentiment === 'Positive' ? 'bg-emerald-950/80 text-emerald-300 border-emerald-700/80' :
                  ab.sentiment === 'Negative' ? 'bg-rose-950/80 text-rose-300 border-rose-700/80' :
                  'bg-slate-900 text-slate-300 border-slate-700';
    span.className = `px-3 py-1.5 rounded-xl text-xs font-semibold border ${color} flex items-center space-x-2 shadow-sm`;
    span.innerHTML = `<span>${ab.aspect}</span> <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-black/40">(${ab.polarity_score > 0 ? '+' : ''}${ab.polarity_score.toFixed(2)})</span>`;
    badgeCont.appendChild(span);
  });

  // Smart Reply
  document.getElementById('smartReplyText').innerText = data.smart_reply;
}

// Batch Processing
async function runBatchAnalysis() {
  const text = document.getElementById('batchInput').value.trim();
  if (!text) {
    showToast("Please enter at least one review per line.", "error");
    return;
  }

  const lines = text.split('\n').map(l => l.trim()).filter(l => l.length > 2);
  const btn = document.getElementById('batchRunBtn');
  btn.disabled = true;
  btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-1.5"></i> Processing...`;

  try {
    const response = await fetch('/api/v1/predict-batch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reviews: lines })
    });

    const data = await response.json();
    renderBatchResults(data);
    showToast(`Successfully analyzed ${data.total_processed} reviews!`, "success");
  } catch (err) {
    showToast(`Batch error: ${err.message}`, "error");
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<i class="fa-solid fa-play mr-1.5"></i> Process Text Lines`;
  }
}

function renderBatchResults(data) {
  document.getElementById('batchStatsCard').classList.remove('hidden');
  document.getElementById('bStatTotal').innerText = data.total_processed;
  document.getElementById('bStatPos').innerText = `${data.summary_stats.positive_percentage}%`;
  document.getElementById('bStatCsat').innerText = `${data.summary_stats.csat_score}%`;
  document.getElementById('bStatNps').innerText = `${data.summary_stats.nps_estimate > 0 ? '+' : ''}${data.summary_stats.nps_estimate}`;

  const tbody = document.getElementById('batchTableBody');
  tbody.innerHTML = '';
  data.results.forEach(r => {
    const tr = document.createElement('tr');
    const badgeColor = r.sentiment === 'Positive' ? 'text-emerald-400 bg-emerald-950/80 border-emerald-800' :
                       r.sentiment === 'Negative' ? 'text-rose-400 bg-rose-950/80 border-rose-800' :
                       'text-amber-400 bg-amber-950/80 border-amber-800';
    tr.innerHTML = `
      <td class="py-3.5 px-4 font-mono font-bold text-slate-400">${r.index}</td>
      <td class="py-3.5 px-4"><span class="px-2.5 py-1 rounded-md text-[11px] font-bold border ${badgeColor}">${r.sentiment}</span></td>
      <td class="py-3.5 px-4 font-mono font-bold">${(r.confidence * 100).toFixed(1)}%</td>
      <td class="py-3.5 px-4 text-slate-400">${r.aspects.join(', ')}</td>
      <td class="py-3.5 px-4"><span class="text-xs font-bold ${r.urgency_level === 'Critical' ? 'text-red-400 font-extrabold' : 'text-slate-400'}">${r.urgency_level}</span></td>
      <td class="py-3.5 px-4 text-slate-300 truncate max-w-xs" title="${r.review_text}">${r.review_text}</td>
    `;
    tbody.appendChild(tr);
  });
}

// Excel & CSV File Upload with Active Loading State
async function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const importBtn = document.getElementById('importBtn');
  
  if (importBtn) {
    importBtn.disabled = true;
    importBtn.classList.add('opacity-80', 'cursor-not-allowed', 'ring-2', 'ring-indigo-500');
    importBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin text-indigo-400 mr-2"></i> <span class="text-indigo-300 font-bold">Importing & Analyzing...</span>`;
  }

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/api/v1/upload-csv', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.detail || `Upload failed (${response.statusText})`);
    }
    
    const data = await response.json();
    renderBatchResults(data);
    showToast(`Imported and analyzed ${data.total_processed} reviews from file!`, "success");
  } catch (err) {
    showToast(`File Import Error: ${err.message}`, "error");
  } finally {
    if (importBtn) {
      importBtn.disabled = false;
      importBtn.classList.remove('opacity-80', 'cursor-not-allowed', 'ring-2', 'ring-indigo-500');
      importBtn.innerHTML = `<i class="fa-solid fa-file-import text-indigo-400 mr-2"></i> <span>Import & Analyze File (.csv, .xlsx)</span>`;
    }
    event.target.value = '';
  }
}

// Executive Analytics
async function loadAnalytics() {
  try {
    const response = await fetch('/api/v1/analytics/summary');
    const data = await response.json();

    document.getElementById('analyticsCsat').innerText = `${data.metrics.csat_score}%`;
    document.getElementById('analyticsGrade').innerText = `Grade: ${data.metrics.satisfaction_grade}`;
    document.getElementById('analyticsNps').innerText = `${data.metrics.nps_estimate > 0 ? '+' : ''}${data.metrics.nps_estimate}`;
    document.getElementById('analyticsTotal').innerText = data.total_reviews_analyzed;

    renderSentimentChart(data.metrics.sentiment_distribution);
    renderPainPoints(data.pain_points);
  } catch (err) {
    console.error("Analytics fetch error:", err);
  }
}

function renderSentimentChart(dist) {
  const ctx = document.getElementById('sentimentChartCanvas').getContext('2d');
  if (sentimentChart) sentimentChart.destroy();

  sentimentChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Positive', 'Neutral', 'Negative'],
      datasets: [{
        data: [dist.Positive || 0, dist.Neutral || 0, dist.Negative || 0],
        backgroundColor: ['#10b981', '#f59e0b', '#f43f5e'],
        borderWidth: 0,
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '72%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#cbd5e1', font: { size: 12, weight: 'bold' }, padding: 16 }
        }
      }
    }
  });
}

function renderPainPoints(points) {
  const cont = document.getElementById('painPointsContainer');
  cont.innerHTML = '';
  if (!points || points.length === 0) {
    cont.innerHTML = '<div class="text-xs text-slate-500 italic py-6 text-center">No pain-points detected yet.</div>';
    return;
  }

  points.slice(0, 5).forEach(p => {
    const div = document.createElement('div');
    div.className = "p-3.5 rounded-2xl bg-slate-950/80 border border-slate-800/80 flex items-center justify-between shadow-inner";
    div.innerHTML = `
      <div>
        <div class="text-xs font-bold text-slate-200">${p.aspect}</div>
        <div class="text-[11px] text-slate-400 mt-0.5">${p.negative_mentions} complaints / ${p.total_mentions} mentions</div>
      </div>
      <span class="px-3 py-1 rounded-lg text-xs font-bold ${p.negative_rate > 30 ? 'bg-rose-950/80 text-rose-300 border border-rose-800' : 'bg-slate-900 text-slate-300 border border-slate-800'}">
        ${p.negative_rate}% Risk
      </span>
    `;
    cont.appendChild(div);
  });
}

// Audit History Log
async function loadHistory() {
  try {
    const response = await fetch('/api/v1/history/?limit=50');
    const data = await response.json();
    const tbody = document.getElementById('historyTableBody');
    tbody.innerHTML = '';

    if (!data.records || data.records.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" class="py-8 text-center text-slate-500">No records found.</td></tr>';
      return;
    }

    data.records.forEach(r => {
      const tr = document.createElement('tr');
      const badgeColor = r.sentiment === 'Positive' ? 'text-emerald-400 bg-emerald-950/80 border-emerald-800' :
                         r.sentiment === 'Negative' ? 'text-rose-400 bg-rose-950/80 border-rose-800' :
                         'text-amber-400 bg-amber-950/80 border-amber-800';
      tr.innerHTML = `
        <td class="py-3.5 px-4 font-mono font-bold text-slate-400">${r.id}</td>
        <td class="py-3.5 px-4 text-slate-400 font-mono text-[11px]">${r.timestamp ? r.timestamp.slice(0, 19).replace('T', ' ') : '-'}</td>
        <td class="py-3.5 px-4"><span class="px-2.5 py-1 rounded-md text-[11px] font-bold border ${badgeColor}">${r.sentiment}</span></td>
        <td class="py-3.5 px-4 font-mono font-bold">${(r.confidence * 100).toFixed(1)}%</td>
        <td class="py-3.5 px-4 text-slate-400">${r.aspects.join(', ')}</td>
        <td class="py-3.5 px-4 text-purple-300 font-semibold">${r.emotion}</td>
        <td class="py-3.5 px-4 text-slate-300 truncate max-w-xs" title="${r.review_text}">${r.review_text}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("History fetch error:", err);
  }
}

function exportHistoryCsv() {
  window.open('/api/v1/history/export', '_blank');
  showToast("Downloading audit log CSV...", "info");
}

async function clearHistoryLog() {
  if (!confirm("Are you sure you want to clear the audit history log?")) return;
  await fetch('/api/v1/history/clear', { method: 'DELETE' });
  loadHistory();
  showToast("Audit log cleared.", "info");
}

// Preset Samples
function loadSample(type) {
  const textarea = document.getElementById('reviewInput');
  if (type === 'pos') {
    textarea.value = "I had a wonderful experience at this restaurant. The food was fresh, flavorful, and beautifully presented, and every dish we tried was delicious. The staff were friendly, attentive, and professional, making us feel very welcome throughout our visit. The atmosphere was comfortable, clean, and relaxing.";
  } else if (type === 'neu') {
    textarea.value = "The food was decent, and the service was acceptable. Nothing was particularly special, but it was an okay place for a casual meal.";
  } else if (type === 'neg') {
    textarea.value = "The food was disappointing, and the service was very slow. The staff were not friendly, and the overall experience was not worth the price.";
  } else if (type === 'crit') {
    textarea.value = "Severe food poisoning after eating the raw seafood platter! Had to visit the emergency clinic. Completely hazardous hygiene!";
  }
  updateCounters(textarea.value);
}

function clearSingleInput() {
  document.getElementById('reviewInput').value = '';
  updateCounters('');
}

function copySmartReply() {
  const text = document.getElementById('smartReplyText').innerText;
  navigator.clipboard.writeText(text);
  showToast("Smart response copied to clipboard!", "success");
}

function updateCounters(val) {
  const chars = val.length;
  const words = val.trim() ? val.trim().split(/\s+/).length : 0;
  document.getElementById('charCounter').innerText = `${chars} chars | ${words} words`;
}

document.getElementById('reviewInput').addEventListener('input', (e) => {
  updateCounters(e.target.value);
});
