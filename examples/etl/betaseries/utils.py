import os
import cceyes.config as config

headers = {
    'X-BetaSeries-Key': config.get_config('betaseries', 'key'),
    'X-BetaSeries-Version': '3.0',
    'Accept-Language': 'en',
}
