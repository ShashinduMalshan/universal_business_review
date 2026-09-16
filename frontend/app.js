/**
 * OmniReview AI - Frontend Dashboard Application Logic
 */

// Global State
let sentimentChartInstance = null;
let aspectsChartInstance = null;
let currentBatchData = [];

document.addEventListener("DOMContentLoaded", () => {
  initHealthCheck();
  loadSampleButtons();
});

// 1. HEALTH CHECK & STATUS
async function initHealthCheck() {
  const statusBadge = document.getElementById("statusBadge");
  const statusText = document.getElementById("statusText");

  try {
    const res = await fetch("/api/health");
    if (res.ok) {
      const data = await res.json();
      statusBadge.className = "flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-950/40 border border-emerald-500/30 text-xs font-medium text-emerald-400";
      statusText.textContent = `API Active (${data.model_name || '3-Class ML'})`;
    } else {
      throw new Error("API error");
    }
  } catch (err) {
    statusBadge.className = "flex items-center space-x-2 px-3 py-1 rounded-full bg-rose-950/40 border border-rose-500/30 text-xs font-medium text-rose-400";
    statusText.textContent = "Offline";
  }
}

// 2. TAB SWITCHING
function switchTab(tabId) {
  document.querySelectorAll(".tab-content").forEach(el => el.classList.add("hidden"));
  document.querySelectorAll(".tab-btn").forEach(el => {
    el.classList.remove("active", "border-indigo-500", "text-indigo-400");
    el.classList.add("border-transparent", "text-slate-400");
  });

  const activeTab = document.getElementById(tabId);
  const activeBtn = document.getElementById(`btn-${tabId}`);
  if (activeTab) activeTab.classList.remove("hidden");
  if (activeBtn) {
    activeBtn.classList.add("active", "border-indigo-500", "text-indigo-400");
    activeBtn.classList.remove("border-transparent", "text-slate-400");
  }
}

// 3. LOAD QUICK TEST SAMPLES
async function loadSampleButtons() {
  const container = document.getElementById("samplePills");
  if (!container) return;

  try {
    const res = await fetch("/api/sample-reviews");
    if (res.ok) {
      const samples = await res.json();
      container.innerHTML = "";
      samples.forEach((s, idx) => {
        const btn = document.createElement("button");
        let badgeColor = "border-slate-700 bg-slate-800 text-slate-300 hover:border-indigo-500";
        if (s.expected === "Positive") badgeColor = "border-emerald-500/30 bg-emerald-500/10 text-emerald-300 hover:bg-emerald-500/20";
        if (s.expected === "Negative") badgeColor = "border-rose-500/30 bg-rose-500/10 text-rose-300 hover:bg-rose-500/20";
        if (s.expected === "Neutral") badgeColor = "border-amber-500/30 bg-amber-500/10 text-amber-300 hover:bg-amber-500/20";

        btn.className = `px-2.5 py-1 rounded-lg text-[11px] font-semibold border transition ${badgeColor}`;
        btn.textContent = `${s.expected} (${s.category || s.domain.split(' ')[0]})`;
        btn.onclick = () => {
          document.getElementById("reviewInput").value = s.text;
          document.getElementById("domainSelect").value = s.domain;
          analyzeReview();
        };
        container.appendChild(btn);
      });
    }
  } catch (err) {
    console.warn("Could not load sample reviews:", err);
  }
}

function clearInput() {
  document.getElementById("reviewInput").value = "";
  document.getElementById("resultCard").classList.add("hidden");
  document.getElementById("emptyResult").classList.remove("hidden");
}

// 4. ANALYZE SINGLE REVIEW
async function analyzeReview() {
  const text = document.getElementById("reviewInput").value.trim();
  const domain = document.getElementById("domainSelect").value;
  const analyzeBtn = document.getElementById("analyzeBtn");

  if (!text) {
    showToast("Please enter or paste a review first!", "error");
    return;
  }

  analyzeBtn.disabled = true;
  analyzeBtn.innerHTML = `<i class="fa-solid fa-spinner animate-spin"></i> <span>Analyzing...</span>`;

  try {
    const res = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ review_text: text, domain: domain })
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Prediction failed");
    }

    const data = await res.json();
    renderSingleResult(data);
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> <span>Analyze Review</span>`;
  }
}

function renderSingleResult(data) {
  document.getElementById("emptyResult").classList.add("hidden");
  const resultCard = document.getElementById("resultCard");
  resultCard.classList.remove("hidden");

  // Sentiment Badge
  const badge = document.getElementById("sentimentBadge");
  const bannerBorder = document.getElementById("bannerBorder");
  const meter = document.getElementById("circularMeter");

  if (data.sentiment === "Positive") {
    badge.className = "px-4 py-1.5 rounded-xl text-sm font-extrabold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 glow-emerald flex items-center space-x-2";
    badge.innerHTML = `<i class="fa-solid fa-circle-check"></i> <span>POSITIVE</span>`;
    bannerBorder.className = "glass-panel rounded-2xl p-6 border-l-4 border-l-emerald-500";
    meter.style.background = `conic-gradient(#10b981 ${data.confidence * 360}deg, #1f2937 0deg)`;
  } else if (data.sentiment === "Neutral") {
    badge.className = "px-4 py-1.5 rounded-xl text-sm font-extrabold bg-amber-500/20 text-amber-400 border border-amber-500/40 glow-amber flex items-center space-x-2";
    badge.innerHTML = `<i class="fa-solid fa-circle-dot"></i> <span>NEUTRAL</span>`;
    bannerBorder.className = "glass-panel rounded-2xl p-6 border-l-4 border-l-amber-500";
    meter.style.background = `conic-gradient(#f59e0b ${data.confidence * 360}deg, #1f2937 0deg)`;
  } else {
    badge.className = "px-4 py-1.5 rounded-xl text-sm font-extrabold bg-rose-500/20 text-rose-400 border border-rose-500/40 glow-rose flex items-center space-x-2";
    badge.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> <span>NEGATIVE</span>`;
    bannerBorder.className = "glass-panel rounded-2xl p-6 border-l-4 border-l-rose-500";
    meter.style.background = `conic-gradient(#f43f5e ${data.confidence * 360}deg, #1f2937 0deg)`;
  }

  // Urgency
  const urgency = document.getElementById("urgencyBadge");
  if (data.urgency_level === "Critical") {
    urgency.className = "px-3 py-1 rounded-lg text-xs font-bold bg-red-600/30 text-red-300 border border-red-500 pulse-critical";
    urgency.innerHTML = `<i class="fa-solid fa-bell mr-1"></i> Critical Alert`;
  } else if (data.urgency_level === "High") {
    urgency.className = "px-3 py-1 rounded-lg text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40";
    urgency.innerHTML = `High Priority`;
  } else {
    urgency.className = "px-3 py-1 rounded-lg text-xs font-bold bg-slate-800 text-slate-400";
    urgency.innerHTML = `Urgency: ${data.urgency_level}`;
  }

  // Confidence
  const confPct = Math.round(data.confidence * 100);
  document.getElementById("confidenceNumber").textContent = `${confPct}%`;
  document.getElementById("meterPercent").textContent = `${confPct}%`;

  // Probabilities Bar
  const pPos = Math.round((data.probabilities.Positive || 0) * 100);
  const pNeu = Math.round((data.probabilities.Neutral || 0) * 100);
  const pNeg = Math.round((data.probabilities.Negative || 0) * 100);

  document.getElementById("barPos").style.width = `${pPos}%`;
  document.getElementById("barNeu").style.width = `${pNeu}%`;
  document.getElementById("barNeg").style.width = `${pNeg}%`;
  document.getElementById("probLabels").textContent = `Pos: ${pPos}% | Neu: ${pNeu}% | Neg: ${pNeg}%`;

  // Aspects
  const aspectContainer = document.getElementById("aspectBadges");
  aspectContainer.innerHTML = "";
  data.aspects.forEach(asp => {
    const aspSpan = document.createElement("span");
    aspSpan.className = "px-2.5 py-0.5 rounded-md text-[11px] font-semibold bg-indigo-500/10 text-indigo-300 border border-indigo-500/20";
    aspSpan.textContent = asp;
    aspectContainer.appendChild(aspSpan);
  });

  // Smart Reply
  document.getElementById("smartReplyText").value = data.smart_reply || "";

  // Feature Engineering Drawer
  if (data.engineered_features) {
    document.getElementById("fChar").textContent = data.engineered_features.char_count;
    document.getElementById("fWord").textContent = data.engineered_features.word_count;
    document.getElementById("fAvgW").textContent = data.engineered_features.avg_word_length;
    document.getElementById("fExcl").textContent = data.engineered_features.exclamation_count;
    document.getElementById("fUpper").textContent = `${Math.round(data.engineered_features.uppercase_ratio * 100)}%`;
    document.getElementById("fPolarity").textContent = data.engineered_features.lexicon_polarity;
  }
}

function toggleFeatureDrawer() {
  const drawer = document.getElementById("featureDrawer");
  const icon = document.getElementById("drawerIcon");
  drawer.classList.toggle("hidden");
  icon.classList.toggle("fa-chevron-up");
  icon.classList.toggle("fa-chevron-down");
}

function copySmartReply() {
  const replyInput = document.getElementById("smartReplyText");
  replyInput.select();
  navigator.clipboard.writeText(replyInput.value);
  
  const copyBtn = document.getElementById("copyBtnText");
  copyBtn.textContent = "Copied!";
  setTimeout(() => { copyBtn.textContent = "Copy Reply"; }, 2000);
  showToast("Smart reply copied to clipboard!", "success");
}

// 5. BATCH CSV UPLOAD & DASHBOARD
async function handleCsvUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  showBatchLoading(true);

  try {
    const res = await fetch("/api/upload-csv", {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "CSV upload failed");
    }

    const data = await res.json();
    renderBatchResults(data);
    showToast(`Successfully analyzed ${data.summary.total_reviews} reviews!`, "success");
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    showBatchLoading(false);
  }
}

function loadSampleCsvBatch() {
  showBatchLoading(true);
  setTimeout(async () => {
    try {
      const sampleReviews = [
        "Consistently the top spot in town for truffle pasta. Spotless cleanliness and exceptional staff!",
        "Horrible dining experience with the burger. The freezing cold food is unacceptable. Left hungry.",
        "An ordinary experience regarding the product. It features acceptable quality and routine service.",
        "Best tech purchase of the year! Incredible battery life, crystal clear display, and fast charging.",
        "Do not buy this! Constant hardware failure and Bluetooth disconnects. Died after two weeks.",
        "The wool cardigan is soft, elegant, and fits like a dream. Top notch craftsmanship.",
        "Cheap fabric, buttons fell off immediately, and the zipper is completely jammed. Terrible.",
        "Average repair service on our plumbing. Finished on time without major issue."
      ];

      const res = await fetch("/api/predict-batch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reviews: sampleReviews })
      });

      if (!res.ok) throw new Error("Batch inference failed");
      const data = await res.json();
      renderBatchResults(data);
      showToast("Loaded sample batch successfully!", "success");
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      showBatchLoading(false);
    }
  }, 600);
}

function showBatchLoading(isLoading) {
  document.getElementById("batchLoading").classList.toggle("hidden", !isLoading);
  if (isLoading) document.getElementById("batchDashboard").classList.add("hidden");
}

function renderBatchResults(data) {
  currentBatchData = data.results || [];
  const s = data.summary;

  document.getElementById("batchDashboard").classList.remove("hidden");

  // Update KPIs
  document.getElementById("kpiTotal").textContent = s.total_reviews.toLocaleString();
  document.getElementById("kpiPos").textContent = `${s.positive_percentage}%`;
  document.getElementById("kpiNeu").textContent = `${s.neutral_percentage}%`;
  document.getElementById("kpiNeg").textContent = `${s.negative_percentage}%`;
  document.getElementById("kpiCritical").textContent = s.critical_alerts_count;
  document.getElementById("kpiAvgConf").textContent = `${s.average_confidence}%`;

  // Render Charts
  renderSentimentChart(s.positive_count, s.neutral_count, s.negative_count);
  renderAspectsChart(s.top_aspects || {});

  // Populate Table
  renderBatchTable(currentBatchData);
}

function renderSentimentChart(pos, neu, neg) {
  const ctx = document.getElementById("sentimentChart").getContext("2d");
  if (sentimentChartInstance) sentimentChartInstance.destroy();

  sentimentChartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Positive", "Neutral", "Negative"],
      datasets: [{
        data: [pos, neu, neg],
        backgroundColor: ["#10b981", "#f59e0b", "#f43f5e"],
        borderWidth: 0,
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
          labels: { color: "#94a3b8", font: { family: "Plus Jakarta Sans", size: 11 } }
        }
      },
      cutout: "70%"
    }
  });
}

function renderAspectsChart(aspectsMap) {
  const ctx = document.getElementById("aspectsChart").getContext("2d");
  if (aspectsChartInstance) aspectsChartInstance.destroy();

  const labels = Object.keys(aspectsMap);
  const values = Object.values(aspectsMap);

  aspectsChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Review Mentions",
        data: values,
        backgroundColor: "#6366f1",
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: { ticks: { color: "#94a3b8" }, grid: { color: "#1e293b" } },
        y: { ticks: { color: "#cbd5e1", font: { size: 11 } }, grid: { display: false } }
      }
    }
  });
}

function renderBatchTable(items) {
  const tbody = document.getElementById("batchTableBody");
  tbody.innerHTML = "";

  items.forEach((item, idx) => {
    const tr = document.createElement("tr");
    tr.className = "hover:bg-slate-900/60 transition";

    let badgeClass = "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20";
    if (item.sentiment === "Negative") badgeClass = "bg-rose-500/10 text-rose-400 border border-rose-500/20";
    if (item.sentiment === "Neutral") badgeClass = "bg-amber-500/10 text-amber-400 border border-amber-500/20";

    tr.innerHTML = `
      <td class="py-3 px-4 font-mono text-slate-500">${idx + 1}</td>
      <td class="py-3 px-4 text-slate-200 max-w-xs truncate" title="${item.review_text}">${item.review_text}</td>
      <td class="py-3 px-4"><span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold ${badgeClass}">${item.sentiment}</span></td>
      <td class="py-3 px-4 font-semibold text-slate-300">${Math.round(item.confidence * 100)}%</td>
      <td class="py-3 px-4 text-slate-400">${item.aspects.join(", ")}</td>
      <td class="py-3 px-4">
        <button onclick="inspectRow(${idx})" class="text-indigo-400 hover:text-indigo-300 font-semibold text-xs">
          Inspect
        </button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function filterTable() {
  const query = document.getElementById("tableSearch").value.toLowerCase();
  const filtered = currentBatchData.filter(d => 
    d.review_text.toLowerCase().includes(query) ||
    d.sentiment.toLowerCase().includes(query) ||
    d.aspects.some(a => a.toLowerCase().includes(query))
  );
  renderBatchTable(filtered);
}

function inspectRow(idx) {
  const item = currentBatchData[idx];
  if (!item) return;
  document.getElementById("reviewInput").value = item.review_text;
  switchTab("tab-live");
  renderSingleResult(item);
}

function exportResultsToCsv() {
  if (!currentBatchData.length) return;
  let csv = "Review Text,Sentiment,Confidence,Aspects,Smart Reply\n";
  currentBatchData.forEach(r => {
    csv += `"${r.review_text.replace(/"/g, '""')}","${r.sentiment}",${r.confidence},"${r.aspects.join('; ')}","${(r.smart_reply || '').replace(/"/g, '""')}"\n`;
  });

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `sentiment_analysis_report_${new Date().toISOString().slice(0,10)}.csv`;
  link.click();
  showToast("CSV report exported successfully!", "success");
}

// 6. TOAST NOTIFICATIONS
function showToast(msg, type = "success") {
  const toast = document.getElementById("toast");
  const toastMsg = document.getElementById("toastMsg");
  toastMsg.textContent = msg;

  toast.classList.remove("translate-y-20", "opacity-0");
  toast.classList.add("translate-y-0", "opacity-100");

  setTimeout(() => {
    toast.classList.remove("translate-y-0", "opacity-100");
    toast.classList.add("translate-y-20", "opacity-0");
  }, 3000);
}
