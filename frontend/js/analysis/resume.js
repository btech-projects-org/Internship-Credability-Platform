// ========================
// RESUME MATCHING LOGIC
// ========================

const Resume = {
  // Compute match score between resume text and job description
  async matchScore(resumeText, jdText, internshipData = {}) {
    const apiKey = (typeof window !== 'undefined' && window.HF_API_KEY) ? window.HF_API_KEY : '';

    const clean = (t) => (t || '').toLowerCase();
    const rt = clean(resumeText);
    const jt = clean(jdText);

    // Fallback keyword overlap scoring
    const keywordResult = this.keywordOverlapScore(rt, jt, internshipData);

    // If no API key, return keyword-based result
    if (!apiKey) {
      return {
        score: Math.round(keywordResult.score),
        method: 'keywords',
        missingKeywords: keywordResult.missingKeywords,
        details: 'No API key; used keyword overlap.'
      };
    }

    // Try Hugging Face embeddings for semantic similarity
    try {
      const [resumeEmb, jdEmb] = await Promise.all([
        this.fetchEmbeddings(rt, apiKey),
        this.fetchEmbeddings(jt, apiKey)
      ]);

      const semantic = this.cosineSimilarity(resumeEmb, jdEmb) * 100; // 0-100
      const combined = 0.7 * semantic + 0.3 * keywordResult.score;

      return {
        score: Math.round(Math.max(0, Math.min(100, combined))),
        method: 'semantic+keywords',
        semanticScore: Math.round(semantic),
        keywordScore: Math.round(keywordResult.score),
        missingKeywords: keywordResult.missingKeywords,
        details: 'Used HF embeddings (all-MiniLM-L6-v2) + keyword overlap.'
      };
    } catch (err) {
      console.warn('HF embeddings failed, falling back to keywords:', err);
      return {
        score: Math.round(keywordResult.score),
        method: 'keywords',
        missingKeywords: keywordResult.missingKeywords,
        details: 'HF request failed; used keyword overlap.'
      };
    }
  },

  // Fetch sentence embeddings from Hugging Face Inference API
  async fetchEmbeddings(text, apiKey) {
    const url = 'https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2';
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ inputs: text, options: { wait_for_model: true } })
    });

    if (!res.ok) {
      const msg = await res.text();
      throw new Error(`HF API error ${res.status}: ${msg}`);
    }

    const data = await res.json();
    // Response is nested arrays; flatten to 1D vector
    const vector = Array.isArray(data) ? data.flat(Infinity) : [];
    if (!vector.length) throw new Error('Invalid embedding response');
    return vector;
  },

  // Compute cosine similarity between two vectors
  cosineSimilarity(a, b) {
    const len = Math.min(a.length, b.length);
    let dot = 0, na = 0, nb = 0;
    for (let i = 0; i < len; i++) {
      const ai = a[i];
      const bi = b[i];
      dot += ai * bi;
      na += ai * ai;
      nb += bi * bi;
    }
    const denom = Math.sqrt(na) * Math.sqrt(nb) || 1;
    return dot / denom;
  },

  // Keyword overlap scoring between JD and resume (basic ATS-like)
  keywordOverlapScore(resumeText, jdText, internshipData = {}) {
    const stop = new Set(['the','and','or','for','with','a','an','to','of','in','on','at','by','from','as','is','are','be','this','that','it','you','your','our']);
    const tokenize = (t) => (t || '')
      .toLowerCase()
      .replace(/[^a-z0-9+.#/\-\s]/g, ' ')
      .split(/\s+/)
      .filter(w => w && w.length > 2 && !stop.has(w));

    const jdTokens = new Set(tokenize(jdText));
    const resumeTokens = new Set(tokenize(resumeText));

    // Boost for matching role title keywords
    const role = (internshipData.position || '').toLowerCase();
    const roleTokens = new Set(tokenize(role));

    let matchCount = 0;
    const missing = [];

    jdTokens.forEach(tok => {
      if (resumeTokens.has(tok)) matchCount++;
      else if (roleTokens.has(tok)) missing.push(tok);
    });

    const total = Math.max(jdTokens.size, 1);
    const overlapPct = (matchCount / total) * 100;

    // Small boost if role title keywords appear in resume
    let roleBoost = 0;
    roleTokens.forEach(tok => { if (resumeTokens.has(tok)) roleBoost += 1; });
    const boostPct = Math.min(roleBoost * 1.5, 10); // cap boost

    return {
      score: Math.min(100, overlapPct + boostPct),
      missingKeywords: missing.slice(0, 25)
    };
  }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Resume;
}
