/*
    This model aggregates raw user metrics into a daily report.
    We use safe_divide to prevent errors if DAU is zero.
*/

WITH raw_data AS (
    -- In a real scenario, you would replace this with the actual source table
    SELECT * FROM {{ source('raw_data', 'user_metrics') }}
)

SELECT
    event_date,
    country,
    platform,
    
    -- DAU (Daily Active Users)
    COUNT(DISTINCT user_id) as dau,
    
    -- Revenue
    SUM(iap_revenue) as total_iap_revenue,
    SUM(ad_revenue) as total_ad_revenue,
    
    -- ARPDAU (Total Revenue / DAU)
    SAFE_DIVIDE(SUM(iap_revenue + ad_revenue), COUNT(DISTINCT user_id)) as arpdau,
    
    -- Engagement
    SUM(match_start_count) as matches_started,
    SAFE_DIVIDE(SUM(match_start_count), COUNT(DISTINCT user_id)) as match_per_dau,
    
    -- Win/Loss Ratios
    SAFE_DIVIDE(SUM(victory_count), SUM(match_end_count)) as win_ratio,
    SAFE_DIVIDE(SUM(defeat_count), SUM(match_end_count)) as defeat_ratio,
    
    -- Technical Health
    SAFE_DIVIDE(SUM(server_connection_error), COUNT(DISTINCT user_id)) as server_error_per_dau

FROM raw_data
GROUP BY 1, 2, 3