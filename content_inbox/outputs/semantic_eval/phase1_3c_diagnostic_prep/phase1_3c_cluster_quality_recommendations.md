# Phase 1.3c Cluster Quality Recommendations

## Current State

The 300-run produced only 2 effective multi-item clusters, both rated `likely_valid`. This is good for precision but may indicate over-conservative clustering.

## Findings

### cluster_c56c3a0e17404cfcafb080f8798037d2: OpenAI releases Codex Chrome extension
- Verdict: valid_event_cluster
- Issues: ['All members from same source (source_count=1)', 'All same actor — may be same_product_different_event or same_thread rather than same_event']
- Recommendation: Likely a valid event cluster but check if members are near_duplicates. If they're different tweets about same Codex launch from same source, consider folding near_duplicates and keeping one representative.

### cluster_aaa6f1924b304940a57a8b7f458afcff: DeepSeek open-sources DeepSeek-V4 Preview
- Verdict: valid_event_cluster
- Issues: ['All same actor — may be same_product_different_event or same_thread rather than same_event']
- Recommendation: Valid event cluster. Fix product extraction: 'com 1Dl' → 'DeepSeek-V4 Preview'. This cluster should be written to DB after product fix.

## Recommendations for Codex Phase 1.3c

1. **Protect valid clusters**: Both current clusters should survive any validator tightening
2. **Fix product extraction**: The DeepSeek cluster has garbage product 'com 1Dl' — fix before DB write
3. **Consider same-source near_duplicate folding**: The Codex cluster has 3 same-source items at same timestamp — could be folded to 2 if truly duplicate tweets
4. **Don't relax cluster seed rules just to increase count**: 2 good clusters is better than 5 bad ones
5. **Verify cluster formation is NOT based on**: generic AI overlap, same source alone, same actor alone, or thread_signature only
6. **Pre-write check**: Before scoped real write, confirm both clusters have correct actor/product/action fields
