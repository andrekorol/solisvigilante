import os
from lib import urlget

# Get list of Solar Cycle 24 top flares and save it in the proper directory
cycle24_dir = os.path.join("solar-cycles", "cycle24")
top_flares = urlget.download_from_url("http://www.solarham.net/top10.txt", cycle24_dir)
print(top_flares)
