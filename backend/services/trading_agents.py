"""
TradingAgents integration service with Gemini models
"""
import sys
import os
from datetime import datetime, date
from typing import Dict, Any, Optional
from decimal import Decimal

# Add TradingAgents to path (will be cloned separately)
TRADING_AGENTS_PATH = os.path.join(os.path.dirname(__file__), '../../TradingAgents')
if os.path.exists(TRADING_AGENTS_PATH):
    sys.path.insert(0, TRADING_AGENTS_PATH)


class TradingAgentsService:
    """Service for interacting with TradingAgents framework"""

    def __init__(self):
        self.graph = None
        self._initialized = False

    def _initialize_graph(self):
        """Initialize TradingAgents graph with Gemini configuration"""
        if self._initialized:
            return

        try:
            from tradingagents.graph.trading_graph import TradingAgentsGraph
            from tradingagents.default_config import DEFAULT_CONFIG
        except ImportError:
            raise ImportError(
                "TradingAgents not found. Please clone the repository: "
                "git clone https://github.com/JosephTLucas/TradingAgents.git"
            )

        # Create configuration with Gemini models
        config = DEFAULT_CONFIG.copy()

        # Gemini configuration for cost optimization
        config["llm_provider"] = "google"
        config["backend_url"] = "https://generativelanguage.googleapis.com/v1beta/openai/"

        # Use Flash-Lite for analysts (cheaper, high volume)
        # Use Flash for trader and risk manager (better reasoning)
        config["quick_think_llm"] = "gemini-2.0-flash-lite"
        config["deep_think_llm"] = "gemini-2.0-flash-exp"
        config["embedding_model"] = "models/text-embedding-004"

        # Cost optimization settings
        config["max_debate_rounds"] = 1  # Reduce debate rounds to save costs
        config["online_tools"] = True  # Enable online data fetching

        # API keys (from environment)
        config["google_api_key"] = os.getenv("GOOGLE_API_KEY")
        config["alpha_vantage_api_key"] = os.getenv("ALPHA_VANTAGE_API_KEY")

        # Initialize graph
        self.graph = TradingAgentsGraph(debug=False, config=config)
        self._initialized = True

    async def analyze_stock(
        self,
        symbol: str,
        analysis_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Run TradingAgents analysis for a single stock

        Args:
            symbol: Stock ticker symbol
            analysis_date: Date for analysis (defaults to today)

        Returns:
            Dictionary with analysis results
        """
        self._initialize_graph()

        if analysis_date is None:
            analysis_date = date.today()

        # Convert date to string format expected by TradingAgents
        date_str = analysis_date.strftime("%Y-%m-%d")

        try:
            # Run the multi-agent analysis
            state, decision = self.graph.propagate(symbol.upper(), date_str)

            # Extract key information from decision
            action = self._extract_action(decision)
            confidence = self._extract_confidence(decision)
            risk_score = self._extract_risk_score(decision)
            reasoning = self._extract_reasoning(decision)

            return {
                "symbol": symbol.upper(),
                "date": analysis_date,
                "action": action,
                "confidence": Decimal(str(confidence)),
                "risk_score": Decimal(str(risk_score)),
                "reasoning": reasoning,
                "raw_decision": decision,
                "state": state  # Full agent state for debugging
            }

        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")
            raise

    def _extract_action(self, decision: Dict[str, Any]) -> str:
        """
        Extract trading action from decision

        TradingAgents may return action in different formats.
        Try multiple keys and fallback to HOLD.
        """
        # Common keys where action might be stored
        action_keys = ["action", "decision", "recommendation", "final_decision"]

        for key in action_keys:
            if key in decision:
                action = str(decision[key]).upper()
                if action in ["BUY", "SELL", "HOLD"]:
                    return action

        # Check in nested structures
        if "trader" in decision and "action" in decision["trader"]:
            action = str(decision["trader"]["action"]).upper()
            if action in ["BUY", "SELL", "HOLD"]:
                return action

        # Default to HOLD if no clear action found
        return "HOLD"

    def _extract_confidence(self, decision: Dict[str, Any]) -> float:
        """
        Extract confidence score from decision

        Confidence should be between 0 and 1.
        """
        confidence_keys = ["confidence", "confidence_score", "certainty"]

        for key in confidence_keys:
            if key in decision:
                try:
                    conf = float(decision[key])
                    # Ensure it's between 0 and 1
                    if 0 <= conf <= 1:
                        return conf
                    elif 0 <= conf <= 100:  # Convert percentage to decimal
                        return conf / 100
                except (ValueError, TypeError):
                    continue

        # Check in nested structures
        if "trader" in decision and "confidence" in decision["trader"]:
            try:
                conf = float(decision["trader"]["confidence"])
                if 0 <= conf <= 1:
                    return conf
                elif 0 <= conf <= 100:
                    return conf / 100
            except (ValueError, TypeError):
                pass

        # Default to medium confidence
        return 0.5

    def _extract_risk_score(self, decision: Dict[str, Any]) -> float:
        """
        Extract risk score from decision

        Risk score should be between 0 and 1 (0 = low risk, 1 = high risk).
        """
        risk_keys = ["risk_score", "risk", "risk_level", "volatility"]

        for key in risk_keys:
            if key in decision:
                try:
                    risk = float(decision[key])
                    if 0 <= risk <= 1:
                        return risk
                    elif 0 <= risk <= 100:
                        return risk / 100
                except (ValueError, TypeError):
                    continue

        # Check in risk manager output
        if "risk_manager" in decision and "risk_score" in decision["risk_manager"]:
            try:
                risk = float(decision["risk_manager"]["risk_score"])
                if 0 <= risk <= 1:
                    return risk
                elif 0 <= risk <= 100:
                    return risk / 100
            except (ValueError, TypeError):
                pass

        # Default to medium risk
        return 0.5

    def _extract_reasoning(self, decision: Dict[str, Any]) -> str:
        """
        Extract reasoning/explanation from decision

        Combine insights from different agents.
        """
        reasoning_parts = []

        # Common reasoning keys
        reasoning_keys = ["reasoning", "explanation", "analysis", "summary"]

        for key in reasoning_keys:
            if key in decision and decision[key]:
                reasoning_parts.append(str(decision[key]))

        # Extract agent-specific reasoning
        agent_keys = ["analyst", "researcher", "trader", "risk_manager"]
        for agent in agent_keys:
            if agent in decision:
                agent_data = decision[agent]
                if isinstance(agent_data, dict):
                    for key in reasoning_keys:
                        if key in agent_data and agent_data[key]:
                            reasoning_parts.append(f"{agent.title()}: {agent_data[key]}")

        if reasoning_parts:
            return "\n\n".join(reasoning_parts)

        # Fallback: stringify the entire decision
        return str(decision)


# Singleton instance
_trading_agents_service = None


def get_trading_agents_service() -> TradingAgentsService:
    """Get or create TradingAgents service instance"""
    global _trading_agents_service
    if _trading_agents_service is None:
        _trading_agents_service = TradingAgentsService()
    return _trading_agents_service
