{{ config(
    materialized='table'
) }}

WITH daily_stats AS (
    SELECT
        event_date,
        country,
        platform,
        
        -- Basic Aggregations
        COUNT(DISTINCT user_id) as dau,
        SUM(iap_revenue) as total_iap_revenue,
        SUM(ad_revenue) as total_ad_revenue,
        SUM(match_start_count) as matches_started,
        SUM(match_end_count) as matches_ended,
        SUM(victory_count) as victories,
        SUM(defeat_count) as defeats,
        SUM(server_connection_error) as server_errors

    FROM {{ source('raw_data', 'user_metrics') }}
    GROUP BY 1, 2, 3
)

SELECT
    event_date,
    country,
    platform,
    dau,
    total_iap_revenue,
    total_ad_revenue,
    
    -- Calculated Metrics (Handling division by zero safely)
    
    -- ARPDAU: (IAP + Ad) / DAU
    CASE 
        WHEN dau > 0 THEN (total_iap_revenue + total_ad_revenue) / dau 
        ELSE 0 
    END as arpdau,

    -- Matches per DAU
    CASE 
        WHEN dau > 0 THEN matches_started / dau 
        ELSE 0 
    END as match_per_dau,

    -- Win Ratio: Victories / Matches Ended
    CASE 
        WHEN matches_ended > 0 THEN victories / matches_ended 
        ELSE 0 
    END as win_ratio,

    -- Defeat Ratio
    CASE 
        WHEN matches_ended > 0 THEN defeats / matches_ended 
        ELSE 0 
    END as defeat_ratio,

    -- Server Error per DAU
    CASE 
        WHEN dau > 0 THEN server_errors / dau 
        ELSE 0 
    END as server_error_per_dau

FROM daily_stats