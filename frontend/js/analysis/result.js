// ========================
// RESULT PAGE LOGIC
// ========================

const Result = {
  // Display analysis results
  displayResults(results) {
    if (!results) {
      window.location.href = 'index.html';
      return;
    }

    this.displayScoreOverview(results);
    this.displayDetailedScores(results.scores);
    this.displayRecommendations(results.recommendations);
    this.displayWarnings(results.warnings);
    this.displayChart(results.scores);

    // Display resume match if available
    if (results.resumeMatch) {
      this.displayResumeMatch(results.resumeMatch);
    }
  },

  // Display score overview
  displayScoreOverview(results) {
    const overviewElement = document.getElementById('score-overview');
    if (!overviewElement) return;

    const levelClass = this.getScoreLevelClass(results.totalScore);
    const levelIcon = this.getScoreLevelIcon(results.credibilityLevel);

    overviewElement.innerHTML = `
      <div class="card card-dark text-center scale-in">
        <div style="font-size: 4rem; margin-bottom: 1rem;">${levelIcon}</div>
        <h2>Credibility Level: <span class="${levelClass}">${results.credibilityLevel}</span></h2>
        <div class="score-circle ${levelClass}" style="margin: 2rem auto;">
          <div class="score-value">${Math.round(results.totalScore)}%</div>
        </div>
        <p style="font-size: 1.1rem; margin-top: 1rem;">
          ${this.getScoreMessage(results.credibilityLevel)}
        </p>
      </div>
    `;
  },

  // Display resume match card
  displayResumeMatch(match) {
    const el = document.getElementById('resume-match');
    if (!el) return;

    const levelClass = match.score >= 80 ? 'score-high' : match.score >= 60 ? 'score-moderate' : match.score >= 40 ? 'score-low' : 'score-very-low';
    const methodText = match.method === 'semantic+keywords' ? 'Semantic + Keywords' : 'Keywords Only';

    el.innerHTML = `
      <div class="card card-dark text-center fade-in">
        <h2>Resume ↔ JD Match</h2>
        <p class="mb-1">Method: ${methodText}</p>
        <div class="score-circle ${levelClass}" style="margin: 1rem auto;">
          <div class="score-value">${Math.round(match.score)}%</div>
        </div>
        ${match.semanticScore !== undefined ? `<p>Semantic: ${Math.round(match.semanticScore)}% · Keywords: ${Math.round(match.keywordScore)}%</p>` : ''}
        ${Array.isArray(match.missingKeywords) && match.missingKeywords.length ? `
          <div class="panel mt-2">
            <h4>Suggested Missing Keywords</h4>
            <p class="mb-0">${match.missingKeywords.join(', ')}</p>
          </div>
        ` : ''}
      </div>
    `;
  },

  // Display detailed scores
  displayDetailedScores(scores) {
    const detailsElement = document.getElementById('detailed-scores');
    if (!detailsElement) return;

    const scoreCategories = [
      { name: 'Company Verification', score: scores.companyScore, icon: '🏢' },
      { name: 'Offer Quality', score: scores.offerScore, icon: '📋' },
      { name: 'Communication', score: scores.communicationScore, icon: '💬' },
      { name: 'Requirements', score: scores.requirementsScore, icon: '✅' }
    ];

    detailsElement.innerHTML = scoreCategories.map((category, index) => `
      <div class="card fade-in-up delay-${index + 1}">
        <h3 style="display: flex; align-items: center; gap: 0.5rem;">
          <span style="font-size: 1.5rem;">${category.icon}</span>
          ${category.name}
        </h3>
        <div class="progress-bar" style="margin: 1rem 0;">
          <div class="progress-fill" style="width: ${category.score}%; animation-delay: ${index * 0.2}s;"></div>
        </div>
        <p style="font-size: 1.25rem; font-weight: 600; color: ${this.getScoreColor(category.score)};">
          ${Math.round(category.score)}%
        </p>
      </div>
    `).join('');
  },

  // Display recommendations
  displayRecommendations(recommendations) {
    const recElement = document.getElementById('recommendations');
    if (!recElement) return;

    if (recommendations.length === 0) {
      recElement.innerHTML = '<div class="alert alert-success">No major concerns found!</div>';
      return;
    }

    recElement.innerHTML = `
      <div class="card card-dark fade-in">
        <h3>📌 Recommendations</h3>
        <ul style="list-style: none; padding: 0;">
          ${recommendations.map(rec => `
            <li style="padding: 0.75rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
              ${rec}
            </li>
          `).join('')}
        </ul>
      </div>
    `;
  },

  // Display warnings
  displayWarnings(warnings) {
    const warnElement = document.getElementById('warnings');
    if (!warnElement) return;

    if (warnings.length === 0) return;

    warnElement.innerHTML = warnings.map(warning => {
      const alertType = warning.includes('CRITICAL') ? 'alert-error' : 'alert-warning';
      return `<div class="alert ${alertType} scale-in">${warning}</div>`;
    }).join('');
  },

  // Display chart (simple text-based representation)
  displayChart(scores) {
    const chartElement = document.getElementById('score-chart');
    if (!chartElement) return;

    const categories = ['Company', 'Offer', 'Communication', 'Requirements'];
    const values = [
      scores.companyScore,
      scores.offerScore,
      scores.communicationScore,
      scores.requirementsScore
    ];

    chartElement.innerHTML = `
      <div class="card fade-in">
        <h3>Score Breakdown</h3>
        <div style="margin-top: 1.5rem;">
          ${categories.map((cat, i) => `
            <div style="margin-bottom: 1rem;">
              <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span>${cat}</span>
                <span style="font-weight: 600;">${Math.round(values[i])}%</span>
              </div>
              <div class="progress-bar">
                <div class="progress-fill" style="width: ${values[i]}%; animation-delay: ${i * 0.1}s;"></div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  },

  // Helper: Get score level class
  getScoreLevelClass(score) {
    if (score >= 80) return 'score-high';
    if (score >= 60) return 'score-moderate';
    if (score >= 40) return 'score-low';
    return 'score-very-low';
  },

  // Helper: Get score level icon
  getScoreLevelIcon(level) {
    const icons = {
      'HIGH': '✅',
      'MODERATE': '⚠️',
      'LOW': '⛔',
      'VERY LOW': '🚨'
    };
    return icons[level] || '❓';
  },

  // Helper: Get score message
  getScoreMessage(level) {
    const messages = {
      'HIGH': 'This internship appears to be legitimate and trustworthy.',
      'MODERATE': 'This internship has some concerns. Proceed with caution.',
      'LOW': 'This internship has multiple red flags. Investigate thoroughly.',
      'VERY LOW': 'This internship is highly suspicious. Strongly recommend avoiding.'
    };
    return messages[level] || 'Unable to determine credibility.';
  },

  // Helper: Get score color
  getScoreColor(score) {
    if (score >= 80) return '#22c55e';
    if (score >= 60) return '#f59e0b';
    if (score >= 40) return '#fb923c';
    return '#ef4444';
  }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Result;
}
