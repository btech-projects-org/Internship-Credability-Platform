// ========================
// INTERNSHIP ANALYSIS LOGIC
// ========================

const Analysis = {
  // Analyze internship credibility
  analyzeInternship(data) {
    const scores = {
      companyScore: this.calculateCompanyScore(data),
      offerScore: this.calculateOfferScore(data),
      communicationScore: this.calculateCommunicationScore(data),
      requirementsScore: this.calculateRequirementsScore(data)
    };

    const totalScore = (
      scores.companyScore +
      scores.offerScore +
      scores.communicationScore +
      scores.requirementsScore
    ) / 4;

    const credibilityLevel = this.getCredibilityLevel(totalScore);
    const recommendations = this.generateRecommendations(scores, data);
    const warnings = this.generateWarnings(scores, data);

    return {
      scores,
      totalScore,
      credibilityLevel,
      recommendations,
      warnings,
      timestamp: new Date().toISOString()
    };
  },

  // Calculate company credibility score
  calculateCompanyScore(data) {
    let score = 0;

    // Company website exists and is valid
    if (data.companyWebsite && Validation.isValidURL(data.companyWebsite)) {
      score += 25;
    }

    // Company email domain matches website
    if (data.contactEmail && data.companyWebsite) {
      const emailDomain = data.contactEmail.split('@')[1];
      const websiteDomain = data.companyWebsite.replace(/^https?:\/\//, '').replace(/^www\./, '').split('/')[0];
      if (emailDomain === websiteDomain) {
        score += 25;
      }
    }

    // Company has social media presence
    if (data.hasLinkedIn) score += 15;
    if (data.hasGlassdoor) score += 15;

    // Company is registered
    if (data.isRegistered) score += 20;

    return Math.min(score, 100);
  },

  // Calculate offer details score
  calculateOfferScore(data) {
    let score = 50; // Base score

    // Red flags reduce score
    if (data.requiresPayment) score -= 30;
    if (data.noJobDescription) score -= 20;
    if (data.unrealisticSalary) score -= 15;
    if (data.immediateStart) score -= 10;
    if (data.noContract) score -= 25;

    return Math.max(score, 0);
  },

  // Calculate communication score
  calculateCommunicationScore(data) {
    let score = 50; // Base score

    // Professional communication adds points
    if (data.professionalEmail) score += 20;
    if (data.detailedJobDescription) score += 15;
    if (data.clearTimeline) score += 15;

    // Red flags reduce score
    if (data.pressureToDecide) score -= 25;
    if (data.vagueResponses) score -= 20;
    if (data.multipleFollowups) score -= 10;

    return Math.max(Math.min(score, 100), 0);
  },

  // Calculate requirements score
  calculateRequirementsScore(data) {
    let score = 50; // Base score

    // Reasonable requirements add points
    if (data.reasonableSkills) score += 20;
    if (data.clearExpectations) score += 15;
    if (data.mentionedTraining) score += 15;

    // Unusual requirements reduce score
    if (data.requestsPersonalInfo) score -= 30;
    if (data.requestsBankDetails) score -= 40;
    if (data.unusualRequirements) score -= 20;

    return Math.max(Math.min(score, 100), 0);
  },

  // Get credibility level based on total score
  getCredibilityLevel(score) {
    if (score >= 80) return 'HIGH';
    if (score >= 60) return 'MODERATE';
    if (score >= 40) return 'LOW';
    return 'VERY LOW';
  },

  // Generate recommendations
  generateRecommendations(scores, data) {
    const recommendations = [];

    if (scores.companyScore < 60) {
      recommendations.push('Verify company registration and legitimacy');
      recommendations.push('Research company reviews on Glassdoor and LinkedIn');
    }

    if (scores.offerScore < 60) {
      recommendations.push('Request a detailed written contract');
      recommendations.push('Clarify all terms and conditions before accepting');
    }

    if (scores.communicationScore < 60) {
      recommendations.push('Ask for clarification on vague points');
      recommendations.push('Request official company email communication');
    }

    if (scores.requirementsScore < 60) {
      recommendations.push('Never share bank details or personal documents upfront');
      recommendations.push('Question any unusual requirements');
    }

    if (data.requiresPayment) {
      recommendations.push('⚠️ NEVER pay for an internship opportunity');
    }

    return recommendations;
  },

  // Generate warnings
  generateWarnings(scores, data) {
    const warnings = [];

    if (data.requiresPayment) {
      warnings.push('🚨 CRITICAL: Payment required - Likely a SCAM');
    }

    if (data.requestsBankDetails) {
      warnings.push('🚨 CRITICAL: Bank details requested - Do NOT share');
    }

    if (scores.totalScore < 40) {
      warnings.push('⚠️ HIGH RISK: Multiple red flags detected');
    }

    if (data.noContract) {
      warnings.push('⚠️ WARNING: No written contract mentioned');
    }

    if (data.pressureToDecide) {
      warnings.push('⚠️ WARNING: Pressure tactics being used');
    }

    return warnings;
  }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Analysis;
}
