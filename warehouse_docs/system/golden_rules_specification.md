# Golden Rules Specification

## FIX-1: Token Selection Validation
- **Purpose**: Ensure only validated tokens enter the trading pipeline
- **Implementation**: `fix_1_token_selector.py`
- **Validation**: Minimum volume, market cap, and liquidity requirements
- **Status**: Active

## FIX-2: ROI Calculation Standards  
- **Purpose**: Standardized return on investment calculations
- **Implementation**: `fix_2_token_roi_generator.py`
- **Validation**: Risk-adjusted returns with ATR integration
- **Status**: Active

## FIX-3: Risk Management Filter
- **Purpose**: Filter high-risk positions before execution
- **Implementation**: `fix_3_roi_filter.py`
- **Validation**: Maximum position size and correlation limits
- **Status**: Active

## FIX-4: Decision Generation Logic
- **Purpose**: Automated trading decision framework
- **Implementation**: `fix_4_decision_generator.py`
- **Validation**: Multi-factor scoring with human oversight
- **Status**: Active

## FIX-5: Live Price Validation
- **Purpose**: Real-time price verification before trades
- **Implementation**: `fix_5_live_price_validator.py`
- **Validation**: Cross-exchange price validation
- **Status**: Active

## FIX-6: Grid Configuration Safety
- **Purpose**: Grid bot parameter validation
- **Implementation**: Grid hold verification system
- **Validation**: Risk limits and position sizing
- **Status**: Active

*Last Updated: $(date)*
*Compliance Status: All rules enforced*
