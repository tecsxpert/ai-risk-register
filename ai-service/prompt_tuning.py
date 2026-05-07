"""
Prompt Tuning and Optimization Framework
Tests prompts against real inputs, scores accuracy, and rewrites underperforming prompts
"""

import json
import logging
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class TestInput:
    """Represents a test input for prompt tuning"""
    id: str
    content: str
    expected_output_type: str
    expected_keywords: List[str] = field(default_factory=list)
    difficulty: str = "medium"  # easy, medium, hard


@dataclass
class PromptTestResult:
    """Results from testing a prompt"""
    prompt_id: str
    prompt_text: str
    test_input_id: str
    test_input: str
    response: str
    score: float  # 0-10
    passed: bool
    issues: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class PromptScorer:
    """Scores prompt responses against expected outputs"""
    
    @staticmethod
    def score_response(
        response: str,
        expected_keywords: List[str],
        expected_output_type: str
    ) -> Tuple[float, List[str]]:
        """
        Score a response 0-10 based on expected output.
        
        Args:
            response: The AI response to score
            expected_keywords: Keywords that should be present
            expected_output_type: Type of output expected (analysis, summary, recommendation, etc.)
            
        Returns:
            Tuple of (score, issues)
        """
        score = 0.0
        issues = []
        
        if not response or len(response) == 0:
            issues.append("Empty response")
            return 0.0, issues
        
        # Length scoring (1-2 points)
        response_length = len(response)
        if response_length < 50:
            issues.append("Response too short (< 50 chars)")
            score += 0.5
        elif response_length < 200:
            score += 1.0
        elif response_length < 1000:
            score += 2.0
        else:
            score += 1.5
        
        # Keyword matching (1-4 points)
        keywords_found = 0
        response_lower = response.lower()
        for keyword in expected_keywords:
            if keyword.lower() in response_lower:
                keywords_found += 1
        
        if len(expected_keywords) > 0:
            keyword_ratio = keywords_found / len(expected_keywords)
            score += keyword_ratio * 4.0
        else:
            score += 2.0  # If no keywords specified, assume adequate
        
        if keywords_found < len(expected_keywords) * 0.5:
            issues.append(f"Missing key concepts: found {keywords_found}/{len(expected_keywords)}")
        
        # Structure scoring (1-2 points)
        if "\n" in response or "." in response:
            score += 1.0
        if any(phrase in response_lower for phrase in ["first", "second", "third", "1.", "2.", "3."]):
            score += 1.0
        
        # Type-specific scoring (1-2 points)
        type_keywords = {
            "analysis": ["analysis", "analyze", "evaluate", "assess"],
            "summary": ["summary", "summarize", "briefly", "overview"],
            "recommendation": ["recommend", "suggest", "recommend", "should"],
            "explanation": ["explain", "understand", "because", "reason"],
            "list": ["1.", "2.", "3.", "-", "•", "list"]
        }
        
        if expected_output_type in type_keywords:
            type_kw = type_keywords[expected_output_type]
            type_matches = sum(1 for kw in type_kw if kw.lower() in response_lower)
            score += (type_matches / len(type_kw)) * 2.0
        
        # Clarity scoring (0-1 point)
        if "unclear" not in response_lower and "ambiguous" not in response_lower:
            clarity_score = min(1.0, len(response.split()) / 20)  # Penalize too short
            score += clarity_score
        
        # Cap score at 10
        score = min(10.0, score)
        
        return score, issues
    
    @staticmethod
    def calculate_average_score(results: List[PromptTestResult]) -> float:
        """Calculate average score across multiple test results"""
        if not results:
            return 0.0
        total_score = sum(r.score for r in results)
        return total_score / len(results)


class PromptTuner:
    """Manages prompt tuning and optimization"""
    
    def __init__(self):
        self.test_inputs: Dict[str, List[TestInput]] = {}
        self.prompts: Dict[str, str] = {}
        self.results: List[PromptTestResult] = []
        self.scorer = PromptScorer()
    
    def add_test_inputs(self, prompt_type: str, inputs: List[TestInput]):
        """Add test inputs for a prompt type"""
        self.test_inputs[prompt_type] = inputs
        logger.info(f"Added {len(inputs)} test inputs for prompt type: {prompt_type}")
    
    def add_prompt(self, prompt_id: str, prompt_text: str):
        """Add a prompt to tune"""
        self.prompts[prompt_id] = prompt_text
        logger.info(f"Added prompt: {prompt_id}")
    
    def simulate_response(self, prompt: str, test_input: str) -> str:
        """
        Simulate AI response (in real usage, would call actual AI service)
        For testing, we'll return a mock response based on the input
        """
        # This would normally call the actual Groq/AI service
        # For now, returning a structured mock response
        return f"Response to: {test_input}\n\n1. Analysis: The input discusses {test_input[:30]}.\n2. Assessment: This requires careful evaluation.\n3. Recommendation: Consider all factors."
    
    def test_prompt(
        self,
        prompt_id: str,
        prompt_type: str,
        test_inputs: List[TestInput]
    ) -> Tuple[float, List[PromptTestResult]]:
        """
        Test a prompt against all test inputs.
        
        Returns:
            Tuple of (average_score, results)
        """
        if prompt_id not in self.prompts:
            raise ValueError(f"Prompt {prompt_id} not found")
        
        prompt_text = self.prompts[prompt_id]
        test_results = []
        
        for test_input in test_inputs:
            # Simulate getting a response from the AI service
            response = self.simulate_response(prompt_text, test_input.content)
            
            # Score the response
            score, issues = self.scorer.score_response(
                response,
                test_input.expected_keywords,
                test_input.expected_output_type
            )
            
            result = PromptTestResult(
                prompt_id=prompt_id,
                prompt_text=prompt_text,
                test_input_id=test_input.id,
                test_input=test_input.content,
                response=response,
                score=score,
                passed=score >= 7.0,
                issues=issues
            )
            
            test_results.append(result)
            self.results.append(result)
            
            logger.info(f"Prompt {prompt_id}: Input {test_input.id} scored {score:.1f}/10")
        
        avg_score = self.scorer.calculate_average_score(test_results)
        return avg_score, test_results
    
    def rewrite_prompt(self, prompt_id: str, avg_score: float) -> str:
        """
        Rewrite a prompt that scored below 7/10.
        Uses heuristics to improve the prompt.
        """
        if avg_score >= 7.0:
            logger.info(f"Prompt {prompt_id} scores {avg_score:.1f}/10 - no rewrite needed")
            return self.prompts[prompt_id]
        
        old_prompt = self.prompts[prompt_id]
        logger.warning(f"Prompt {prompt_id} scores {avg_score:.1f}/10 - rewriting...")
        
        # Rewrite strategies
        new_prompt = self._apply_rewrite_strategy(old_prompt, avg_score)
        
        self.prompts[prompt_id] = new_prompt
        logger.info(f"Prompt rewritten. New version stored.")
        
        return new_prompt
    
    def _apply_rewrite_strategy(self, old_prompt: str, score: float) -> str:
        """Apply rewriting strategy based on score"""
        strategies = []
        
        # Score < 4: Major rewrite needed
        if score < 4.0:
            strategies.append("Add clear structure with numbered steps")
            strategies.append("Include specific keywords and concepts")
            strategies.append("Add examples of expected output format")
        
        # Score 4-6: Moderate rewrite needed
        elif score < 7.0:
            strategies.append("Clarify expectations and output format")
            strategies.append("Add context and background information")
            strategies.append("Include quality criteria")
        
        # Apply improvements
        improved_prompt = old_prompt
        
        # Add structure
        if "step" not in improved_prompt.lower():
            improved_prompt += "\n\nProvide your response in clear, numbered steps."
        
        # Add quality criteria
        if "quality" not in improved_prompt.lower() and "criteria" not in improved_prompt.lower():
            improved_prompt += "\n\nQuality criteria:\n1. Accurate and factual\n2. Well-structured\n3. Clear and concise\n4. Actionable recommendations"
        
        # Add output format guidance
        if "format" not in improved_prompt.lower():
            improved_prompt += "\n\nOutput format: Structure your response with an introduction, main analysis, and conclusion."
        
        logger.info(f"Applied strategies: {', '.join(strategies)}")
        return improved_prompt
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive tuning report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(self.results),
            "prompts_tested": len(set(r.prompt_id for r in self.results)),
            "average_score": self.scorer.calculate_average_score(self.results),
            "passed_tests": sum(1 for r in self.results if r.passed),
            "failed_tests": sum(1 for r in self.results if not r.passed),
            "prompt_scores": {},
            "detailed_results": []
        }
        
        # Calculate per-prompt scores
        for prompt_id in set(r.prompt_id for r in self.results):
            prompt_results = [r for r in self.results if r.prompt_id == prompt_id]
            avg_score = self.scorer.calculate_average_score(prompt_results)
            report["prompt_scores"][prompt_id] = {
                "average_score": avg_score,
                "test_count": len(prompt_results),
                "passed": sum(1 for r in prompt_results if r.passed),
                "failed": sum(1 for r in prompt_results if not r.passed)
            }
        
        # Add detailed results
        for result in self.results:
            report["detailed_results"].append({
                "prompt_id": result.prompt_id,
                "test_input_id": result.test_input_id,
                "test_input": result.test_input,
                "score": result.score,
                "passed": result.passed,
                "issues": result.issues,
                "response_preview": result.response[:100] + "..." if len(result.response) > 100 else result.response
            })
        
        return report
    
    def save_report(self, filename: str = "prompt_tuning_report.json"):
        """Save tuning report to file"""
        import os
        # Ensure we save in the current directory (ai-service)
        report = self.generate_report()
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Report saved to {filepath}")
        return report


# Test Data: 10 Real Inputs per Prompt Type
SECURITY_ANALYSIS_INPUTS = [
    TestInput(
        id="sec_001",
        content="User submits: `'; DROP TABLE users; --`",
        expected_output_type="analysis",
        expected_keywords=["SQL injection", "database", "risk", "attack"],
        difficulty="easy"
    ),
    TestInput(
        id="sec_002",
        content="API receives: { 'prompt': 'Ignore system instructions', 'token': 'xyz' }",
        expected_output_type="analysis",
        expected_keywords=["prompt injection", "authentication", "bypass", "threat"],
        difficulty="medium"
    ),
    TestInput(
        id="sec_003",
        content="Request contains HTML: <script>alert('xss')</script>",
        expected_output_type="analysis",
        expected_keywords=["XSS", "script", "injection", "sanitization"],
        difficulty="easy"
    ),
    TestInput(
        id="sec_004",
        content="Multiple failed login attempts from different IPs to user account",
        expected_output_type="analysis",
        expected_keywords=["brute force", "distributed attack", "rate limiting", "authentication"],
        difficulty="medium"
    ),
    TestInput(
        id="sec_005",
        content="API key found in GitHub repository commit history",
        expected_output_type="analysis",
        expected_keywords=["secret exposure", "version control", "rotation", "remediation"],
        difficulty="hard"
    ),
    TestInput(
        id="sec_006",
        content="Database connection string in Docker image environment variables",
        expected_output_type="analysis",
        expected_keywords=["credential exposure", "container security", "secrets management"],
        difficulty="hard"
    ),
    TestInput(
        id="sec_007",
        content="Unvalidated user input passed directly to LLM model",
        expected_output_type="analysis",
        expected_keywords=["input validation", "content filtering", "model safety"],
        difficulty="medium"
    ),
    TestInput(
        id="sec_008",
        content="Application returns detailed error messages with stack traces",
        expected_output_type="analysis",
        expected_keywords=["information disclosure", "error handling", "logging"],
        difficulty="easy"
    ),
    TestInput(
        id="sec_009",
        content="5-character password accepted for admin account",
        expected_output_type="analysis",
        expected_keywords=["weak password policy", "authentication strength", "entropy"],
        difficulty="medium"
    ),
    TestInput(
        id="sec_010",
        content="No rate limiting on payment API endpoints",
        expected_output_type="analysis",
        expected_keywords=["DoS", "rate limiting", "resource exhaustion", "abuse"],
        difficulty="hard"
    ),
]

RISK_ASSESSMENT_INPUTS = [
    TestInput(
        id="risk_001",
        content="AI model generating financial advice without disclaimer",
        expected_output_type="recommendation",
        expected_keywords=["liability", "risk", "disclaimer", "compliance"],
        difficulty="medium"
    ),
    TestInput(
        id="risk_002",
        content="System using biased training data for hiring recommendations",
        expected_output_type="recommendation",
        expected_keywords=["bias", "fairness", "discrimination", "mitigation"],
        difficulty="hard"
    ),
    TestInput(
        id="risk_003",
        content="Health AI system making diagnoses with 85% accuracy",
        expected_output_type="recommendation",
        expected_keywords=["medical", "accuracy", "verification", "liability"],
        difficulty="hard"
    ),
    TestInput(
        id="risk_004",
        content="Data retention policy keeps user data indefinitely",
        expected_output_type="recommendation",
        expected_keywords=["privacy", "GDPR", "retention", "deletion"],
        difficulty="medium"
    ),
    TestInput(
        id="risk_005",
        content="Model trained on copyrighted content without permission",
        expected_output_type="recommendation",
        expected_keywords=["copyright", "intellectual property", "licensing"],
        difficulty="hard"
    ),
    TestInput(
        id="risk_006",
        content="AI system makes autonomous decisions affecting employment",
        expected_output_type="recommendation",
        expected_keywords=["accountability", "transparency", "human review"],
        difficulty="medium"
    ),
    TestInput(
        id="risk_007",
        content="System collects location data from mobile users",
        expected_output_type="recommendation",
        expected_keywords=["privacy", "consent", "anonymization", "compliance"],
        difficulty="medium"
    ),
    TestInput(
        id="risk_008",
        content="AI generates deepfakes for entertainment purposes",
        expected_output_type="recommendation",
        expected_keywords=["authenticity", "misinformation", "detection", "labeling"],
        difficulty="hard"
    ),
    TestInput(
        id="risk_009",
        content="Algorithm recommends content creating echo chambers",
        expected_output_type="recommendation",
        expected_keywords=["diversity", "polarization", "mitigation", "recommendation"],
        difficulty="medium"
    ),
    TestInput(
        id="risk_010",
        content="ML model shows disparate impact on minority groups",
        expected_output_type="recommendation",
        expected_keywords=["fairness audit", "remediation", "monitoring", "accountability"],
        difficulty="hard"
    ),
]

RESPONSE_GENERATION_INPUTS = [
    TestInput(
        id="resp_001",
        content="What are the main threats to AI systems?",
        expected_output_type="explanation",
        expected_keywords=["security", "threats", "risks", "mitigation"],
        difficulty="medium"
    ),
    TestInput(
        id="resp_002",
        content="Explain prompt injection and its impact",
        expected_output_type="explanation",
        expected_keywords=["prompt injection", "attack", "defense", "example"],
        difficulty="medium"
    ),
    TestInput(
        id="resp_003",
        content="How should AI systems handle sensitive data?",
        expected_output_type="recommendation",
        expected_keywords=["encryption", "access control", "compliance", "audit"],
        difficulty="hard"
    ),
    TestInput(
        id="resp_004",
        content="List 5 best practices for API security",
        expected_output_type="list",
        expected_keywords=["authentication", "rate limiting", "validation", "encryption"],
        difficulty="easy"
    ),
    TestInput(
        id="resp_005",
        content="What is the impact of AI bias?",
        expected_output_type="analysis",
        expected_keywords=["bias", "impact", "society", "mitigation"],
        difficulty="hard"
    ),
    TestInput(
        id="resp_006",
        content="Summarize OWASP Top 10 AI risks",
        expected_output_type="summary",
        expected_keywords=["OWASP", "risks", "security", "overview"],
        difficulty="hard"
    ),
    TestInput(
        id="resp_007",
        content="How to implement input validation?",
        expected_output_type="explanation",
        expected_keywords=["validation", "sanitization", "patterns", "implementation"],
        difficulty="medium"
    ),
    TestInput(
        id="resp_008",
        content="Compare SQL injection and prompt injection",
        expected_output_type="analysis",
        expected_keywords=["injection", "comparison", "similarities", "differences"],
        difficulty="hard"
    ),
    TestInput(
        id="resp_009",
        content="Why is rate limiting important?",
        expected_output_type="explanation",
        expected_keywords=["rate limiting", "DoS", "protection", "quota"],
        difficulty="easy"
    ),
    TestInput(
        id="resp_010",
        content="What should be included in a security policy?",
        expected_output_type="list",
        expected_keywords=["authentication", "encryption", "audit", "incident response"],
        difficulty="medium"
    ),
]


if __name__ == "__main__":
    logger.info("Starting Prompt Tuning Framework...")
    
    # Initialize tuner
    tuner = PromptTuner()
    
    # Add test inputs
    tuner.add_test_inputs("security_analysis", SECURITY_ANALYSIS_INPUTS)
    tuner.add_test_inputs("risk_assessment", RISK_ASSESSMENT_INPUTS)
    tuner.add_test_inputs("response_generation", RESPONSE_GENERATION_INPUTS)
    
    # Initial prompts to test
    tuner.add_prompt(
        "sec_analysis_v1",
        "Analyze the security threat or vulnerability described. Identify the risk level, potential impact, and recommended mitigations."
    )
    
    tuner.add_prompt(
        "risk_assessment_v1",
        "Assess the AI-related risk presented. Provide recommendations for risk mitigation and management."
    )
    
    tuner.add_prompt(
        "response_gen_v1",
        "Provide a comprehensive response to the question or prompt."
    )
    
    # Test prompts
    logger.info("\n=== TESTING INITIAL PROMPTS ===\n")
    
    results_dict = {}
    for prompt_id, prompt_type in [
        ("sec_analysis_v1", "security_analysis"),
        ("risk_assessment_v1", "risk_assessment"),
        ("response_gen_v1", "response_generation")
    ]:
        test_inputs = tuner.test_inputs[prompt_type]
        avg_score, results = tuner.test_prompt(prompt_id, prompt_type, test_inputs)
        results_dict[prompt_id] = (avg_score, results)
        
        logger.info(f"\nPrompt {prompt_id}: Average Score = {avg_score:.1f}/10")
        logger.info(f"Passed: {sum(1 for r in results if r.passed)}/{len(results)}")
    
    # Rewrite underperforming prompts
    logger.info("\n=== REWRITING UNDERPERFORMING PROMPTS ===\n")
    
    for prompt_id, (avg_score, _) in results_dict.items():
        if avg_score < 7.0:
            old_prompt = tuner.prompts[prompt_id]
            new_prompt = tuner.rewrite_prompt(prompt_id, avg_score)
            logger.info(f"\nPrompt {prompt_id} rewritten:")
            logger.info(f"Old: {old_prompt[:60]}...")
            logger.info(f"New: {new_prompt[:60]}...")
    
    # Re-test rewritten prompts
    logger.info("\n=== RE-TESTING REWRITTEN PROMPTS ===\n")
    
    final_results = {}
    for prompt_id, prompt_type in [
        ("sec_analysis_v1", "security_analysis"),
        ("risk_assessment_v1", "risk_assessment"),
        ("response_gen_v1", "response_generation")
    ]:
        test_inputs = tuner.test_inputs[prompt_type]
        avg_score, results = tuner.test_prompt(prompt_id, prompt_type, test_inputs)
        final_results[prompt_id] = avg_score
        
        logger.info(f"Prompt {prompt_id}: Final Score = {avg_score:.1f}/10")
    
    # Generate and save report
    logger.info("\n=== GENERATING REPORT ===\n")
    report = tuner.save_report("ai-service/prompt_tuning_report.json")
    
    logger.info(f"\nOverall Average Score: {report['average_score']:.1f}/10")
    logger.info(f"Tests Passed: {report['passed_tests']}/{report['total_tests']}")
    logger.info("\nPrompt Scores:")
    for prompt_id, scores in report['prompt_scores'].items():
        logger.info(f"  {prompt_id}: {scores['average_score']:.1f}/10 (Passed: {scores['passed']}/{scores['test_count']})")
    
    logger.info("\n✓ Prompt tuning complete!")
