/**
 * ResuMatch AI - Client-side Application Logic
 * Manages file uploads, extraction, analysis requests, results rendering, and UI states.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Application State
  const state = {
    resumeText: '',
    jdText: '',
    uploadedFileName: '',
    activeTab: 'upload', // 'upload' or 'paste'
    activeSkillFilter: 'all',
    currentResults: null,
    engine: localStorage.getItem('resumatch_engine') || 'local',
    geminiApiKey: localStorage.getItem('resumatch_gemini_key') || '',
    theme: localStorage.getItem('resumatch_theme') || 'dark'
  };

  // DOM Elements
  const elements = {
    // Header & Badges
    engineBadge: document.getElementById('engine-status-badge'),
    engineText: document.getElementById('engine-status-text'),
    themeToggleBtn: document.getElementById('theme-toggle-btn'),
    themeMoonIcon: document.getElementById('theme-moon-icon'),
    themeSunIcon: document.getElementById('theme-sun-icon'),
    settingsBtn: document.getElementById('settings-btn'),

    // Stepper
    step1: document.getElementById('step-nav-1'),
    step2: document.getElementById('step-nav-2'),
    step3: document.getElementById('step-nav-3'),
    step4: document.getElementById('step-nav-4'),

    // Sample buttons
    sampleFullstackBtn: document.getElementById('sample-fullstack-btn'),
    samplePmBtn: document.getElementById('sample-pm-btn'),
    sampleDsBtn: document.getElementById('sample-ds-btn'),

    // Resume Inputs
    tabUpload: document.getElementById('tab-upload'),
    tabPaste: document.getElementById('tab-paste'),
    uploadPanel: document.getElementById('upload-panel'),
    pastePanel: document.getElementById('paste-panel'),
    dropzoneArea: document.getElementById('dropzone-area'),
    fileInput: document.getElementById('file-input'),
    filePreviewCard: document.getElementById('file-preview-card'),
    previewFilename: document.getElementById('preview-filename'),
    previewFilesize: document.getElementById('preview-filesize'),
    fileRemoveBtn: document.getElementById('file-remove-btn'),
    resumeTextarea: document.getElementById('resume-textarea'),
    resumeCharCount: document.getElementById('resume-char-count'),
    resumeClearBtn: document.getElementById('resume-clear-btn'),

    // Job Description Inputs
    jdTextarea: document.getElementById('jd-textarea'),
    jdCharCount: document.getElementById('jd-char-count'),
    jdClearBtn: document.getElementById('jd-clear-btn'),

    // Action banner & buttons
    actionBanner: document.getElementById('action-banner'),
    analyzeBtn: document.getElementById('analyze-btn'),
    resetInputsBtn: document.getElementById('reset-inputs-btn'),
    bannerStatusText: document.getElementById('banner-status-text'),
    bannerStatusDesc: document.getElementById('banner-status-desc'),

    // Loading overlay
    loadingOverlay: document.getElementById('loading-overlay'),
    loadingStepText: document.getElementById('loading-step-text'),
    loadingProgressFill: document.getElementById('loading-progress-fill'),

    // Results Dashboard
    resultsSection: document.getElementById('results-section'),
    gaugeCircle: document.getElementById('gauge-circle'),
    heroScoreNum: document.getElementById('hero-score-num'),
    heroMatchBadge: document.getElementById('hero-match-badge'),
    heroScoreTitle: document.getElementById('hero-score-title'),
    heroScoreSummary: document.getElementById('hero-score-summary'),

    // Sub-scores
    valSkillMatch: document.getElementById('val-skill-match'),
    barSkillMatch: document.getElementById('bar-skill-match'),
    valSemanticMatch: document.getElementById('val-semantic-match'),
    barSemanticMatch: document.getElementById('bar-semantic-match'),
    valExpImpact: document.getElementById('val-exp-impact'),
    barExpImpact: document.getElementById('bar-exp-impact'),
    valAtsReadability: document.getElementById('val-ats-readability'),
    barAtsReadability: document.getElementById('bar-ats-readability'),

    // Stats bar
    statMatchedCount: document.getElementById('stat-matched-count'),
    statMissingCount: document.getElementById('stat-missing-count'),
    statMetricsCount: document.getElementById('stat-metrics-count'),
    statWordCount: document.getElementById('stat-word-count'),

    // Skills Matrix
    countAllSkills: document.getElementById('count-all-skills'),
    countMatchedSkills: document.getElementById('count-matched-skills'),
    countMissingSkills: document.getElementById('count-missing-skills'),
    countExtraSkills: document.getElementById('count-extra-skills'),
    skillsTagsContainer: document.getElementById('skills-tags-container'),
    skillFilterBtns: document.querySelectorAll('.skill-filter-btn'),

    // Details Lists
    strengthsContainer: document.getElementById('strengths-list-container'),
    gapsContainer: document.getElementById('gaps-list-container'),
    suggestionsContainer: document.getElementById('suggestions-list-container'),
    atsChecklistContainer: document.getElementById('ats-checklist-container'),

    // Export buttons
    copySummaryBtn: document.getElementById('copy-summary-btn'),
    downloadMarkdownBtn: document.getElementById('download-markdown-btn'),
    exportPdfBtn: document.getElementById('export-pdf-btn'),

    // Settings Modal
    settingsModal: document.getElementById('settings-modal'),
    modalCloseBtn: document.getElementById('modal-close-btn'),
    engineModeSelect: document.getElementById('engine-mode-select'),
    geminiApiKeyInput: document.getElementById('gemini-api-key-input'),
    saveSettingsBtn: document.getElementById('save-settings-btn'),
    clearKeyBtn: document.getElementById('clear-key-btn'),

    // Toast
    toastContainer: document.getElementById('toast-container')
  };

  // ==========================================================================
  // Toast Notifications
  // ==========================================================================
  function showToast(message, type = 'info', duration = 3500) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    let iconSvg = '';
    if (type === 'success') {
      iconSvg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>';
    } else if (type === 'error') {
      iconSvg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f43f5e" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>';
    } else {
      iconSvg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>';
    }

    toast.innerHTML = `${iconSvg}<span>${message}</span>`;
    elements.toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(20px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }

  // ==========================================================================
  // Theme Toggle
  // ==========================================================================
  function applyTheme(theme) {
    state.theme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('resumatch_theme', theme);

    if (theme === 'light') {
      elements.themeMoonIcon.style.display = 'none';
      elements.themeSunIcon.style.display = 'block';
    } else {
      elements.themeMoonIcon.style.display = 'block';
      elements.themeSunIcon.style.display = 'none';
    }
  }

  elements.themeToggleBtn.addEventListener('click', () => {
    applyTheme(state.theme === 'dark' ? 'light' : 'dark');
  });

  applyTheme(state.theme);

  // ==========================================================================
  // Settings & Engine Mode
  // ==========================================================================
  function updateEngineBadge() {
    if (state.engine === 'gemini' && state.geminiApiKey) {
      elements.engineBadge.classList.add('ai-mode');
      elements.engineText.textContent = 'Gemini AI Live Mode';
    } else {
      elements.engineBadge.classList.remove('ai-mode');
      elements.engineText.textContent = 'Local ATS Engine (100% Private)';
    }
  }

  function openSettingsModal() {
    elements.engineModeSelect.value = state.engine;
    elements.geminiApiKeyInput.value = state.geminiApiKey;
    elements.settingsModal.classList.add('active');
  }

  function closeSettingsModal() {
    elements.settingsModal.classList.remove('active');
  }

  elements.settingsBtn.addEventListener('click', openSettingsModal);
  elements.modalCloseBtn.addEventListener('click', closeSettingsModal);
  elements.settingsModal.addEventListener('click', (e) => {
    if (e.target === elements.settingsModal) closeSettingsModal();
  });

  elements.saveSettingsBtn.addEventListener('click', () => {
    state.engine = elements.engineModeSelect.value;
    state.geminiApiKey = elements.geminiApiKeyInput.value.trim();

    localStorage.setItem('resumatch_engine', state.engine);
    localStorage.setItem('resumatch_gemini_key', state.geminiApiKey);

    updateEngineBadge();
    closeSettingsModal();
    showToast('Engine settings updated successfully!', 'success');
  });

  elements.clearKeyBtn.addEventListener('click', () => {
    elements.geminiApiKeyInput.value = '';
    state.geminiApiKey = '';
    state.engine = 'local';
    elements.engineModeSelect.value = 'local';
    localStorage.removeItem('resumatch_gemini_key');
    localStorage.setItem('resumatch_engine', 'local');
    updateEngineBadge();
    showToast('Gemini API key cleared. Reverted to Local Engine.', 'info');
  });

  updateEngineBadge();

  // ==========================================================================
  // Stepper State Updater
  // ==========================================================================
  function updateStepper() {
    const hasResume = Boolean(state.resumeText.trim());
    const hasJd = Boolean(state.jdText.trim());

    // Step 1
    if (hasResume) {
      elements.step1.classList.remove('active');
      elements.step1.classList.add('completed');
    } else {
      elements.step1.classList.add('active');
      elements.step1.classList.remove('completed');
    }

    // Step 2
    if (hasJd) {
      elements.step2.classList.remove('active');
      elements.step2.classList.add('completed');
    } else if (hasResume) {
      elements.step2.classList.add('active');
      elements.step2.classList.remove('completed');
    } else {
      elements.step2.classList.remove('active', 'completed');
    }

    // Step 3
    if (hasResume && hasJd) {
      elements.step3.classList.add('active');
      elements.analyzeBtn.disabled = false;
      elements.bannerStatusText.textContent = 'Inputs Ready for Analysis';
      elements.bannerStatusDesc.textContent = 'Click "Analyze Resume Now" to run ATS matching and discover actionable insights.';
    } else {
      elements.step3.classList.remove('active', 'completed');
      elements.bannerStatusText.textContent = 'Awaiting Inputs';
      elements.bannerStatusDesc.textContent = 'Upload or paste your resume and job description to begin.';
    }

    // Step 4
    if (state.currentResults) {
      elements.step3.classList.add('completed');
      elements.step4.classList.add('active');
    }
  }

  // ==========================================================================
  // Text Counters
  // ==========================================================================
  function updateResumeWordCount() {
    const text = state.resumeText.trim();
    const words = text ? text.split(/\s+/).length : 0;
    const chars = text.length;
    elements.resumeCharCount.textContent = `${words.toLocaleString()} words • ${chars.toLocaleString()} characters`;
  }

  function updateJdWordCount() {
    const text = state.jdText.trim();
    const words = text ? text.split(/\s+/).length : 0;
    const chars = text.length;
    elements.jdCharCount.textContent = `${words.toLocaleString()} words • ${chars.toLocaleString()} characters`;
  }

  // ==========================================================================
  // Tab Switching (File Upload vs Paste Text)
  // ==========================================================================
  elements.tabUpload.addEventListener('click', () => {
    state.activeTab = 'upload';
    elements.tabUpload.classList.add('active');
    elements.tabPaste.classList.remove('active');
    elements.tabUpload.setAttribute('aria-selected', 'true');
    elements.tabPaste.setAttribute('aria-selected', 'false');
    elements.uploadPanel.style.display = 'block';
    elements.pastePanel.style.display = 'none';
  });

  elements.tabPaste.addEventListener('click', () => {
    state.activeTab = 'paste';
    elements.tabPaste.classList.add('active');
    elements.tabUpload.classList.remove('active');
    elements.tabPaste.setAttribute('aria-selected', 'true');
    elements.tabUpload.setAttribute('aria-selected', 'false');
    elements.pastePanel.style.display = 'flex';
    elements.uploadPanel.style.display = 'none';
    elements.resumeTextarea.focus();
  });

  elements.resumeTextarea.addEventListener('input', (e) => {
    state.resumeText = e.target.value;
    updateResumeWordCount();
    updateStepper();
  });

  elements.resumeClearBtn.addEventListener('click', () => {
    elements.resumeTextarea.value = '';
    state.resumeText = '';
    updateResumeWordCount();
    updateStepper();
    showToast('Resume text cleared', 'info');
  });

  elements.jdTextarea.addEventListener('input', (e) => {
    state.jdText = e.target.value;
    updateJdWordCount();
    updateStepper();
  });

  elements.jdClearBtn.addEventListener('click', () => {
    elements.jdTextarea.value = '';
    state.jdText = '';
    updateJdWordCount();
    updateStepper();
    showToast('Job description cleared', 'info');
  });

  // ==========================================================================
  // File Upload Handling (PDF, DOCX, TXT)
  // ==========================================================================
  elements.dropzoneArea.addEventListener('click', () => {
    elements.fileInput.click();
  });

  elements.dropzoneArea.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      elements.fileInput.click();
    }
  });

  // Drag and drop events
  ['dragenter', 'dragover'].forEach(eventName => {
    elements.dropzoneArea.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      elements.dropzoneArea.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach(eventName => {
    elements.dropzoneArea.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      elements.dropzoneArea.classList.remove('dragover');
    });
  });

  elements.dropzoneArea.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  });

  elements.fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      handleFileUpload(e.target.files[0]);
    }
  });

  async function handleFileUpload(file) {
    const validExtensions = ['.pdf', '.docx', '.txt'];
    const fileName = file.name.toLowerCase();
    const hasValidExt = validExtensions.some(ext => fileName.endsWith(ext));

    if (!hasValidExt) {
      showToast('Please upload a PDF (.pdf), Word document (.docx), or plain text (.txt) file.', 'error', 4500);
      return;
    }

    if (file.size > 16 * 1024 * 1024) {
      showToast('File exceeds the 16MB limit. Please upload a smaller document.', 'error', 4000);
      return;
    }

    // UI: Indicate uploading
    elements.dropzoneArea.style.opacity = '0.5';
    elements.dropzoneArea.style.pointerEvents = 'none';
    showToast(`Parsing ${file.name}...`, 'info');

    const formData = new FormData();
    formData.append('resume_file', file);

    try {
      const response = await fetch('/api/extract', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Failed to extract text from document.');
      }

      state.resumeText = data.text;
      state.uploadedFileName = data.filename;
      elements.resumeTextarea.value = data.text;
      updateResumeWordCount();

      // Show File Preview Card
      elements.previewFilename.textContent = data.filename;
      const sizeKb = Math.round(file.size / 1024);
      const wordCount = data.metadata.word_count || data.text.split(/\s+/).length;
      elements.previewFilesize.textContent = `${sizeKb} KB • ${wordCount.toLocaleString()} words extracted cleanly`;

      elements.dropzoneArea.style.display = 'none';
      elements.filePreviewCard.style.display = 'flex';

      showToast(`Extracted ${wordCount} words from ${data.filename}!`, 'success');
      updateStepper();

    } catch (err) {
      showToast(err.message, 'error', 6000);
    } finally {
      elements.dropzoneArea.style.opacity = '1';
      elements.dropzoneArea.style.pointerEvents = 'auto';
      elements.fileInput.value = '';
    }
  }

  elements.fileRemoveBtn.addEventListener('click', () => {
    state.resumeText = '';
    state.uploadedFileName = '';
    elements.resumeTextarea.value = '';
    updateResumeWordCount();
    elements.filePreviewCard.style.display = 'none';
    elements.dropzoneArea.style.display = 'flex';
    updateStepper();
    showToast('Uploaded resume removed.', 'info');
  });

  // ==========================================================================
  // Sample Data Loading
  // ==========================================================================
  async function loadSample(sampleId) {
    showToast(`Loading sample profile...`, 'info', 1500);

    try {
      const res = await fetch(`/api/samples/${sampleId}`);
      const data = await res.json();

      if (!res.ok || !data.success) {
        throw new Error(data.error || 'Failed to load sample.');
      }

      const sample = data.sample;

      // Populate Resume
      state.resumeText = sample.resume;
      state.uploadedFileName = `${sample.id}_resume.txt`;
      elements.resumeTextarea.value = sample.resume;
      updateResumeWordCount();

      // Show in textarea tab or file preview
      elements.tabPaste.click();

      // Populate JD
      state.jdText = sample.job_description;
      elements.jdTextarea.value = sample.job_description;
      updateJdWordCount();

      updateStepper();
      showToast(`Loaded: ${sample.title}! Ready to analyze.`, 'success', 3000);

      // Scroll smoothly down to action banner
      elements.actionBanner.scrollIntoView({ behavior: 'smooth', block: 'center' });

    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  elements.sampleFullstackBtn.addEventListener('click', () => loadSample('fullstack'));
  elements.samplePmBtn.addEventListener('click', () => loadSample('product_manager'));
  elements.sampleDsBtn.addEventListener('click', () => loadSample('data_science'));

  // ==========================================================================
  // Reset All
  // ==========================================================================
  elements.resetInputsBtn.addEventListener('click', () => {
    state.resumeText = '';
    state.jdText = '';
    state.uploadedFileName = '';
    state.currentResults = null;

    elements.resumeTextarea.value = '';
    elements.jdTextarea.value = '';
    updateResumeWordCount();
    updateJdWordCount();

    elements.filePreviewCard.style.display = 'none';
    elements.dropzoneArea.style.display = 'flex';
    elements.resultsSection.style.display = 'none';

    updateStepper();
    showToast('Reset all inputs and results.', 'info');
  });

  // ==========================================================================
  // Run Analysis Pipeline
  // ==========================================================================
  elements.analyzeBtn.addEventListener('click', async () => {
    const resume = state.resumeText.trim();
    const jd = state.jdText.trim();

    if (!resume) {
      showToast('Please upload or paste your resume first.', 'error');
      if (state.activeTab === 'upload') {
        elements.dropzoneArea.classList.add('dragover');
        setTimeout(() => elements.dropzoneArea.classList.remove('dragover'), 600);
      } else {
        elements.resumeTextarea.focus();
      }
      return;
    }

    if (!jd) {
      showToast('Please paste the target job description.', 'error');
      elements.jdTextarea.focus();
      return;
    }

    if (resume.length < 80) {
      showToast('Resume is too short. Please provide a more complete resume (at least 80 characters).', 'error');
      return;
    }

    if (jd.length < 40) {
      showToast('Job description is too short (at least 40 characters needed for ATS keyword scanning).', 'error');
      return;
    }

    // Begin Loading State
    startLoadingAnimation();

    const payload = {
      resume_text: resume,
      jd_text: jd,
      engine: state.engine,
      api_key: state.geminiApiKey
    };

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        if (data.can_fallback_to_local) {
          // Gemini failed, offer local fallback
          showToast(`Gemini API Error: ${data.error}. Retrying with Local ATS Engine...`, 'error', 4000);
          payload.engine = 'local';
          const fbRes = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          const fbData = await fbRes.json();
          if (fbData.success) {
            renderResults(fbData.result);
            return;
          }
        }
        throw new Error(data.error || 'Analysis failed. Please check inputs and try again.');
      }

      renderResults(data.result);

    } catch (err) {
      stopLoadingAnimation();
      showToast(err.message, 'error', 6000);
    }
  });

  // Animated Loading Steps
  let loadingInterval = null;
  function startLoadingAnimation() {
    elements.loadingOverlay.style.display = 'block';
    elements.resultsSection.style.display = 'none';
    elements.analyzeBtn.disabled = true;

    const steps = [
      { text: "Scanning document structure & ATS compatibility...", pct: 25 },
      { text: "Extracting core technical, leadership, and domain skills...", pct: 55 },
      { text: "Evaluating quantifiable achievements & action verbs...", pct: 80 },
      { text: "Synthesizing tailored recommendations & bullet rewrites...", pct: 95 }
    ];

    let currentStep = 0;
    elements.loadingStepText.textContent = steps[0].text;
    elements.loadingProgressFill.style.width = `${steps[0].pct}%`;

    elements.loadingOverlay.scrollIntoView({ behavior: 'smooth', block: 'center' });

    loadingInterval = setInterval(() => {
      currentStep++;
      if (currentStep < steps.length) {
        elements.loadingStepText.textContent = steps[currentStep].text;
        elements.loadingProgressFill.style.width = `${steps[currentStep].pct}%`;
      }
    }, 450);
  }

  function stopLoadingAnimation() {
    clearInterval(loadingInterval);
    elements.loadingOverlay.style.display = 'none';
    elements.analyzeBtn.disabled = false;
  }

  // ==========================================================================
  // Render Results Dashboard
  // ==========================================================================
  function renderResults(result) {
    stopLoadingAnimation();
    state.currentResults = result;

    // Show Results Section
    elements.resultsSection.style.display = 'block';

    // 1. Overall Score & Circular Gauge Animation
    const score = result.overall_score || 0;
    animateGauge(score);

    // Badge styling
    elements.heroMatchBadge.textContent = result.match_tier || 'Match';
    elements.heroMatchBadge.className = 'gauge-badge';
    if (result.tier_color === 'emerald') {
      elements.heroMatchBadge.classList.add('badge-emerald');
    } else if (result.tier_color === 'amber') {
      elements.heroMatchBadge.classList.add('badge-amber');
    } else {
      elements.heroMatchBadge.classList.add('badge-rose');
    }

    elements.heroScoreTitle = document.getElementById('hero-score-title');
    elements.heroScoreTitle.textContent = `${result.match_tier} (${score}/100)`;
    elements.heroScoreSummary.textContent = result.tier_summary || 'Analysis complete.';

    // 2. Sub-scores Meters
    const sub = result.sub_scores || {};
    renderSubscore(elements.valSkillMatch, elements.barSkillMatch, sub.skill_match || 0);
    renderSubscore(elements.valSemanticMatch, elements.barSemanticMatch, sub.semantic_relevance || 0);
    renderSubscore(elements.valExpImpact, elements.barExpImpact, sub.experience_impact || 0);
    renderSubscore(elements.valAtsReadability, elements.barAtsReadability, sub.ats_readability || 0);

    // 3. Stats Bar
    const stats = result.stats || {};
    elements.statMatchedCount.textContent = (result.skills?.matched || []).length;
    elements.statMissingCount.textContent = (result.skills?.missing || []).length;
    elements.statMetricsCount.textContent = stats.metrics_detected || 0;
    elements.statWordCount.textContent = (stats.resume_word_count || state.resumeText.split(/\s+/).length).toLocaleString();

    // 4. Skills Matrix & Counts
    const matchedSkills = result.skills?.matched || [];
    const missingSkills = result.skills?.missing || [];
    const additionalSkills = result.skills?.additional || [];

    elements.countMatchedSkills.textContent = matchedSkills.length;
    elements.countMissingSkills.textContent = missingSkills.length;
    elements.countExtraSkills.textContent = additionalSkills.length;
    elements.countAllSkills.textContent = matchedSkills.length + missingSkills.length + additionalSkills.length;

    renderSkillsList(state.activeSkillFilter);

    // 5. Strengths
    renderBulletList(elements.strengthsContainer, result.strengths || [], 'check');

    // 6. Gaps
    renderBulletList(elements.gapsContainer, result.gaps || [], 'warn');

    // 7. Actionable Suggestions
    renderSuggestionsList(result.suggestions || []);

    // 8. ATS Checklist
    renderAtsChecklist(result.ats_checklist);

    // Update Stepper
    updateStepper();

    // Smooth scroll down to results
    elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    showToast(`Analysis complete: ${score}/100 (${result.match_tier})`, 'success');
  }

  function renderSubscore(valElem, barElem, val) {
    valElem.textContent = `${val}%`;
    barElem.style.width = '0%';
    setTimeout(() => {
      barElem.style.width = `${val}%`;
    }, 100);
  }

  function animateGauge(targetScore) {
    const radius = 75;
    const circumference = 2 * Math.PI * radius; // ~471.24
    const offset = circumference - (targetScore / 100) * circumference;

    // Stroke color based on score
    let strokeColor = '#10b981'; // emerald
    if (targetScore < 55) {
      strokeColor = '#f43f5e'; // rose
    } else if (targetScore < 75) {
      strokeColor = '#f59e0b'; // amber
    }

    elements.gaugeCircle.style.stroke = strokeColor;
    elements.gaugeCircle.style.strokeDasharray = `${circumference}`;
    elements.gaugeCircle.style.strokeDashoffset = `${circumference}`;

    // Trigger transition
    setTimeout(() => {
      elements.gaugeCircle.style.strokeDashoffset = `${offset}`;
    }, 50);

    // Count up animation for number
    let current = 0;
    const duration = 1200;
    const stepTime = 20;
    const steps = duration / stepTime;
    const increment = targetScore / steps;

    const timer = setInterval(() => {
      current += increment;
      if (current >= targetScore) {
        current = targetScore;
        clearInterval(timer);
      }
      elements.heroScoreNum.textContent = Math.round(current);
    }, stepTime);
  }

  // ==========================================================================
  // Render Skills Tags with Filtering
  // ==========================================================================
  elements.skillFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      elements.skillFilterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.activeSkillFilter = btn.dataset.filter;
      renderSkillsList(state.activeSkillFilter);
    });
  });

  function renderSkillsList(filter) {
    if (!state.currentResults || !state.currentResults.skills) return;

    const matched = state.currentResults.skills.matched || [];
    const missing = state.currentResults.skills.missing || [];
    const additional = state.currentResults.skills.additional || [];

    let html = '';

    // Matched skills
    if (filter === 'all' || filter === 'matched') {
      matched.forEach(s => {
        html += `
          <div class="skill-tag matched" title="Matched in both Resume & JD">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
            <span>${escapeHtml(s.name)}</span>
            <span class="skill-badge">${s.resume_count || 1}x on resume</span>
          </div>
        `;
      });
    }

    // Missing skills
    if (filter === 'all' || filter === 'missing') {
      missing.forEach(s => {
        const isHigh = s.importance === 'High Priority';
        const tagClass = isHigh ? 'missing-high' : 'missing-rec';
        const iconSvg = isHigh
          ? '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>'
          : '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>';

        html += `
          <div class="skill-tag ${tagClass}" title="${isHigh ? 'High Priority Missing Skill' : 'Recommended Skill'}">
            ${iconSvg}
            <span>${escapeHtml(s.name)}</span>
            <span class="skill-badge">${isHigh ? 'High Priority' : 'Recommended'}</span>
          </div>
        `;
      });
    }

    // Additional skills on resume
    if (filter === 'all' || filter === 'additional') {
      additional.forEach(s => {
        html += `
          <div class="skill-tag additional" title="Bonus skill found on your resume">
            <span>${escapeHtml(s.name)}</span>
            <span class="skill-badge">Resume Extra</span>
          </div>
        `;
      });
    }

    if (!html) {
      html = '<div style="color: var(--text-muted); font-size: 0.85rem; padding: 12px;">No skills in this category.</div>';
    }

    elements.skillsTagsContainer.innerHTML = html;
  }

  // ==========================================================================
  // Render Strengths & Gaps
  // ==========================================================================
  function renderBulletList(container, items, iconType) {
    if (!items || items.length === 0) {
      container.innerHTML = '<li class="bullet-item" style="color: var(--text-muted);">None noted.</li>';
      return;
    }

    let iconSvg = '';
    if (iconType === 'check') {
      iconSvg = `
        <div class="bullet-icon check">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
        </div>
      `;
    } else {
      iconSvg = `
        <div class="bullet-icon warn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        </div>
      `;
    }

    container.innerHTML = items.map(item => `
      <li class="bullet-item">
        ${iconSvg}
        <span>${escapeHtml(item)}</span>
      </li>
    `).join('');
  }

  // ==========================================================================
  // Render Suggestions List with Priority & Examples
  // ==========================================================================
  function renderSuggestionsList(suggestions) {
    if (!suggestions || suggestions.length === 0) {
      elements.suggestionsContainer.innerHTML = '<div style="color: var(--text-muted);">No critical suggestions generated.</div>';
      return;
    }

    elements.suggestionsContainer.innerHTML = suggestions.map(s => {
      const priority = (s.priority || 'Medium').toLowerCase();
      const badgeClass = priority === 'high' ? 'priority-badge-high' : priority === 'low' ? 'priority-badge-low' : 'priority-badge-medium';
      const cardClass = `priority-${priority}`;

      const exampleBlock = s.example ? `
        <div class="suggestion-example-box">${escapeHtml(s.example)}</div>
      ` : '';

      return `
        <div class="suggestion-card ${cardClass}">
          <div class="suggestion-top">
            <div class="suggestion-title">${escapeHtml(s.title || 'Recommendation')}</div>
            <span class="suggestion-priority ${badgeClass}">${escapeHtml(s.priority || 'Medium')} Priority</span>
          </div>
          <p class="suggestion-action">${escapeHtml(s.action || '')}</p>
          ${exampleBlock}
        </div>
      `;
    }).join('');
  }

  // ==========================================================================
  // Render ATS Parse Checklist
  // ==========================================================================
  function renderAtsChecklist(checklist) {
    if (!checklist) {
      elements.atsChecklistContainer.innerHTML = '';
      return;
    }

    const items = [
      {
        label: "Contact Email Detected",
        passed: Boolean(checklist.email_present),
        help: checklist.email_present ? "Standard email format identified" : "No email detected in header"
      },
      {
        label: "Phone Number Detected",
        passed: Boolean(checklist.phone_present),
        help: checklist.phone_present ? "Phone number present" : "No phone number found"
      },
      {
        label: "LinkedIn Profile Detected",
        passed: Boolean(checklist.linkedin_present),
        help: checklist.linkedin_present ? "LinkedIn link found" : "Consider adding your LinkedIn URL"
      },
      {
        label: "Core ATS Sections Present",
        passed: (checklist.sections_found || []).length >= 4,
        help: `Found ${(checklist.sections_found || []).length} standard sections: ${(checklist.sections_found || []).join(', ')}`
      }
    ];

    elements.atsChecklistContainer.innerHTML = items.map(item => `
      <li class="bullet-item">
        <div class="bullet-icon ${item.passed ? 'check' : 'warn'}">
          ${item.passed
            ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>'
            : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>'
          }
        </div>
        <div>
          <strong>${escapeHtml(item.label)}</strong>:
          <span style="color: var(--text-secondary); font-size: 0.82rem;"> ${escapeHtml(item.help)}</span>
        </div>
      </li>
    `).join('');
  }

  // ==========================================================================
  // Export & Sharing Handlers
  // ==========================================================================
  function generateMarkdownReport() {
    if (!state.currentResults) return '';

    const r = state.currentResults;
    const sub = r.sub_scores || {};
    const matched = (r.skills?.matched || []).map(s => s.name).join(', ') || 'None';
    const missingHigh = (r.skills?.missing || []).filter(s => s.importance === 'High Priority').map(s => s.name).join(', ') || 'None';
    const missingRec = (r.skills?.missing || []).filter(s => s.importance !== 'High Priority').map(s => s.name).join(', ') || 'None';

    return `# AI Resume Match Audit Report
Generated by ResuMatch AI (${r.analysis_mode})

## Match Summary
- **Overall Score**: ${r.overall_score}/100 (${r.match_tier})
- **Summary**: ${r.tier_summary}
- **Skill Overlap Score**: ${sub.skill_match || 0}/100
- **Semantic Alignment**: ${sub.semantic_relevance || 0}/100
- **Experience & Impact**: ${sub.experience_impact || 0}/100
- **ATS Readability**: ${sub.ats_readability || 0}/100

## Skills Matrix
- **Matched Skills**: ${matched}
- **High-Priority Missing**: ${missingHigh}
- **Recommended Missing**: ${missingRec}

## Key Strengths
${(r.strengths || []).map(s => `- ${s}`).join('\n')}

## Gaps & Potential Concerns
${(r.gaps || []).map(g => `- ${g}`).join('\n')}

## Actionable Suggestions
${(r.suggestions || []).map((s, idx) => `### ${idx + 1}. [${s.priority} Priority] ${s.title}
${s.action}
${s.example ? `> ${s.example.replace(/\n/g, '\n> ')}` : ''}
`).join('\n')}

---
*Notice: ${r.disclaimer}*
`;
  }

  // Copy Summary
  elements.copySummaryBtn.addEventListener('click', async () => {
    const md = generateMarkdownReport();
    if (!md) {
      showToast('Run an analysis first before copying.', 'error');
      return;
    }

    try {
      await navigator.clipboard.writeText(md);
      showToast('Markdown summary copied to clipboard!', 'success');
    } catch (e) {
      // Fallback
      const ta = document.createElement('textarea');
      ta.value = md;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      showToast('Markdown summary copied to clipboard!', 'success');
    }
  });

  // Download Markdown File
  elements.downloadMarkdownBtn.addEventListener('click', () => {
    const md = generateMarkdownReport();
    if (!md) {
      showToast('Run an analysis first.', 'error');
      return;
    }

    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `resume_match_report_${Date.now()}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('Downloaded Markdown report.', 'success');
  });

  // Print / Save as PDF
  elements.exportPdfBtn.addEventListener('click', () => {
    if (!state.currentResults) {
      showToast('Run an analysis first before exporting.', 'error');
      return;
    }
    window.print();
  });

  // Utility: HTML Escaping
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Initialize
  updateStepper();
});
