// ============================================
// FUND-DATA.JS — Shared position data
// Single source of truth for all pages
// ============================================

const SHARED_FINNHUB_KEY = 'd6kqa11r01qmopd1net0d6kqa11r01qmopd1netg';

// Bump DATA_VERSION whenever positions, costs, or prices change — invalidates all localStorage caches
const DATA_VERSION = '2026-07-13-2';

// Date when price/prevClose were last set (YYYY-MM-DD in US/Pacific)
// On a new trading day, pages auto-reset price = prevClose so Today P&L starts at $0
const PRICES_AS_OF = '2026-06-30';

// Realized P&L from closed positions (CHGG: -$449.07, RIOT: -$1,189.30, U: -$1,336.68, HPP: -$3,496.09, MDB: -$1,301.40, BXP: -$965.15, GPN: -$775.91, AXTI: -$715.96, SPG: -$774.07, DUOL: -$782.97, PL: -$1,712.79)
const SHARED_REALIZED_PNL = -13499.39;

// Sold positions
const SOLD_POSITIONS = [
  {"symbol": "CHGG", "name": "Chegg Inc", "direction": "Short", "qty": 7690, "costBasis": 0.65, "exitPrice": 0.71, "realizedPnl": -449.07, "entryDate": "Mar 4", "exitDate": "Mar 31"},
  {"symbol": "RIOT", "name": "Riot Platforms Inc", "direction": "Long", "qty": 303, "costBasis": 16.52, "exitPrice": 12.6, "realizedPnl": -1189.3, "entryDate": "Mar 4", "exitDate": "Mar 31"},
  {"symbol": "U", "name": "Unity Software Inc", "direction": "Short", "qty": 244, "costBasis": 20.52, "exitPrice": 26, "realizedPnl": -1336.68, "entryDate": "Mar 4", "exitDate": "Apr 30"},
  {"symbol": "HPP", "name": "Hudson Pacific Properties", "direction": "Short", "qty": 1244, "costBasis": 6.39, "exitPrice": 9.2, "realizedPnl": -3496.09, "entryDate": "Mar 4", "exitDate": "Apr 30"},
  {"symbol": "MDB", "name": "MongoDB Inc", "direction": "Short", "qty": 20, "costBasis": 250.37, "exitPrice": 312.08, "realizedPnl": -1301.4, "entryDate": "Mar 4", "exitDate": "May 29"},
  {"symbol": "BXP", "name": "BXP Inc", "direction": "Short", "qty": 98, "costBasis": 51.05, "exitPrice": 60.93, "realizedPnl": -965.15, "entryDate": "Mar 11", "exitDate": "May 29"},
  {"symbol": "GPN", "name": "Global Payments Inc", "direction": "Short", "qty": 78, "costBasis": 64.06, "exitPrice": 75.14, "realizedPnl": -775.91, "entryDate": "Apr 9", "exitDate": "May 29"},
  {"symbol": "AXTI", "name": "AXT Inc", "direction": "Long", "qty": 41, "costBasis": 120.85, "exitPrice": 102.93, "realizedPnl": -715.96, "entryDate": "May 13", "exitDate": "May 29"},
  {"symbol": "SPG", "name": "Simon Property Group", "direction": "Short", "qty": 26, "costBasis": 194.34, "exitPrice": 224.1, "realizedPnl": -774.07, "entryDate": "Mar 11", "exitDate": "Jun 30"},
  {"symbol": "DUOL", "name": "Duolingo Inc", "direction": "Short", "qty": 50, "costBasis": 99.7, "exitPrice": 115.35, "realizedPnl": -782.97, "entryDate": "Mar 4", "exitDate": "Jun 30"},
  {"symbol": "PL", "name": "Planet Labs PBC", "direction": "Long", "qty": 99, "costBasis": 50.5, "exitPrice": 33.2, "realizedPnl": -1712.79, "entryDate": "May 26", "exitDate": "Jun 30"}
];

// Add-on positions (March rebalance — informational only, already included in POSITIONS totals)
const ADDON_POSITIONS = [
  {"symbol": "ARM", "name": "Arm Holdings PLC", "direction": "Long", "qty": 19, "costBasis": 155.22, "entryDate": "Mar 31", "note": "Added to biggest long winner (+13.10%)"},
  {"symbol": "HPP", "name": "Hudson Pacific Properties", "direction": "Short", "qty": 534, "costBasis": 5.51, "entryDate": "Mar 31", "note": "Added to biggest short winner (+13.73%)"},
  {"symbol": "BE", "name": "Bloom Energy Corp", "direction": "Long", "qty": 15, "costBasis": 272.96, "entryDate": "Apr 30", "note": "Added to biggest April long winner"},
  {"symbol": "MRVL", "name": "Marvell Technology", "direction": "Long", "qty": 25, "costBasis": 164.88, "entryDate": "Apr 30", "note": "Added to biggest April long winner"},
  {"symbol": "MU", "name": "Micron Technology", "direction": "Long", "qty": 4, "costBasis": 923.52, "entryDate": "May 29", "note": "Added to May long winner"},
  {"symbol": "NBIS", "name": "Nebius Group", "direction": "Long", "qty": 18, "costBasis": 226.34, "entryDate": "May 29", "note": "Added to May long winner"},
  {"symbol": "ARM", "name": "Arm Holdings PLC", "direction": "Long", "qty": 19, "costBasis": 173.91, "entryDate": "May 26", "note": "Second add-on to biggest long winner"},
  {"symbol": "DELL", "name": "Dell Technologies", "direction": "Long", "qty": 10, "costBasis": 317.05, "entryDate": "May 29", "note": "Added to May long winner"},
  {"symbol": "MRVL", "name": "Marvell Technology", "direction": "Long", "qty": 14, "costBasis": 141.98, "entryDate": "Jun 30", "note": "Month-end add-on to winner"},
  {"symbol": "SNDK", "name": "SanDisk Corp", "direction": "Long", "qty": 2, "costBasis": 1252.61, "entryDate": "Jun 30", "note": "Month-end add-on to winner"},
  {"symbol": "ALAB", "name": "Astera Labs Inc", "direction": "Long", "qty": 9, "costBasis": 268.61, "entryDate": "Jun 30", "note": "Month-end add-on to winner"}
];

// Active positions — THE source of truth (65 positions)
const POSITIONS = [
  {"symbol": "BE", "name": "Bloom Energy Corp", "sector": "Energy", "industry": "Electrical Equipment & Parts", "marketCap": 69577814065, "direction": "Long", "qty": 46, "price": 302.7, "costBasis": 198.6, "prevClose": 275.01},
  {"symbol": "CBRE", "name": "CBRE Group Inc", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 40856698006, "direction": "Short", "qty": 35, "price": 134.69, "costBasis": 141.82, "prevClose": 136.09},
  {"symbol": "CORZ", "name": "Core Scientific Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 7467125258, "direction": "Long", "qty": 309, "price": 25.59, "costBasis": 16.17, "prevClose": 25.94},
  {"symbol": "CRM", "name": "Salesforce Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 133759079999, "direction": "Short", "qty": 26, "price": 156.66, "costBasis": 195.71, "prevClose": 157.93},
  {"symbol": "CRWV", "name": "CoreWeave Inc", "sector": "Technology", "industry": "Cloud Infrastructure", "marketCap": 48490291155, "direction": "Long", "qty": 62, "price": 99.54, "costBasis": 80.17, "prevClose": 95.51},
  {"symbol": "CTSH", "name": "Cognizant Technology", "sector": "Technology", "industry": "IT Services", "marketCap": 20172624315, "direction": "Short", "qty": 77, "price": 38.73, "costBasis": 64.97, "prevClose": 38.74},
  {"symbol": "CWK", "name": "Cushman & Wakefield", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 3160713833, "direction": "Short", "qty": 373, "price": 13.39, "costBasis": 13.38, "prevClose": 13.74},
  {"symbol": "FVRR", "name": "Fiverr International", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 396896013, "direction": "Short", "qty": 463, "price": 10.32, "costBasis": 10.82, "prevClose": 10.66},
  {"symbol": "INTU", "name": "Intuit Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 75211731372, "direction": "Short", "qty": 12, "price": 261, "costBasis": 437.9, "prevClose": 266.4},
  {"symbol": "LITE", "name": "Lumentum Holdings", "sector": "Technology", "industry": "Communication Equipment", "marketCap": 62396381998, "direction": "Long", "qty": 8, "price": 858.06, "costBasis": 652.68, "prevClose": 851.4},
  {"symbol": "LZ", "name": "LegalZoom.com Inc", "sector": "Technology", "industry": "Specialty Business Services", "marketCap": 1244446310, "direction": "Short", "qty": 745, "price": 6.13, "costBasis": 6.71, "prevClose": 6.11},
  {"symbol": "MU", "name": "Micron Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 1106014646269, "direction": "Long", "qty": 16, "price": 1154.29, "costBasis": 542.41, "prevClose": 1145.28},
  {"symbol": "NOW", "name": "ServiceNow Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 111082179153, "direction": "Short", "qty": 44, "price": 99.28, "costBasis": 114.35, "prevClose": 99.97},
  {"symbol": "TSM", "name": "Taiwan Semiconductor", "sector": "Technology", "industry": "Semiconductors", "marketCap": 1694640111089, "direction": "Long", "qty": 14, "price": 477.57, "costBasis": 358.83, "prevClose": 455.1},
  {"symbol": "UPWK", "name": "Upwork Inc", "sector": "Technology", "industry": "Staffing & Employment", "marketCap": 1089430056, "direction": "Short", "qty": 370, "price": 8.36, "costBasis": 13.52, "prevClose": 8.31},
  {"symbol": "VRT", "name": "Vertiv Holdings", "sector": "Industrials", "industry": "Electrical Equipment & Parts", "marketCap": 115079000000, "direction": "Long", "qty": 20, "price": 334.82, "costBasis": 251.97, "prevClose": 306.97},
  {"symbol": "WDAY", "name": "Workday Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 31312190000, "direction": "Short", "qty": 34, "price": 122.42, "costBasis": 145.57, "prevClose": 123.58},
  {"symbol": "WPP", "name": "WPP PLC", "sector": "Comm Services", "industry": "Advertising Agencies", "marketCap": 3070270000, "direction": "Short", "qty": 293, "price": 15.49, "costBasis": 17.09, "prevClose": 16.23},
  {"symbol": "WULF", "name": "TeraWulf Inc", "sector": "Technology", "industry": "Capital Markets", "marketCap": 13879870000, "direction": "Long", "qty": 320, "price": 24.7, "costBasis": 15.61, "prevClose": 25.58},
  {"symbol": "CAT", "name": "Caterpillar Inc", "sector": "Industrials", "industry": "Farm & Heavy Construction Machinery", "marketCap": 438715314805, "direction": "Long", "qty": 7, "price": 1064.9, "costBasis": 700.72, "prevClose": 1033.19},
  {"symbol": "FCG", "name": "First Trust Natural Gas ETF", "sector": "Energy", "industry": "Natural Gas ETF", "marketCap": 606577942, "direction": "Long", "qty": 174, "price": 26.61, "costBasis": 28.78, "prevClose": 26.58},
  {"symbol": "REMX", "name": "VanEck Rare Earth ETF", "sector": "Materials", "industry": "Rare Earth & Strategic Metals ETF", "marketCap": 1119500183, "direction": "Long", "qty": 54, "price": 88.5, "costBasis": 92.91, "prevClose": 86.38},
  {"symbol": "COHR", "name": "Coherent Corp", "sector": "Technology", "industry": "Scientific & Technical Instruments", "marketCap": 63484960042, "direction": "Long", "qty": 20, "price": 394.47, "costBasis": 252.4, "prevClose": 391.22},
  {"symbol": "COPX", "name": "Global X Copper Miners ETF", "sector": "Materials", "industry": "Copper Miners ETF", "marketCap": 3232889592, "direction": "Long", "qty": 62, "price": 76.97, "costBasis": 80.22, "prevClose": 75.74},
  {"symbol": "MRVL", "name": "Marvell Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 206286588744, "direction": "Long", "qty": 94, "price": 297.89, "costBasis": 118.56, "prevClose": 277.75},
  {"symbol": "PSFE", "name": "Paysafe Ltd", "sector": "Technology", "industry": "IT Services", "marketCap": 413610624, "direction": "Short", "qty": 666, "price": 7.47, "costBasis": 7.5, "prevClose": 7.37},
  {"symbol": "Z", "name": "Zillow Group Inc", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 7621850000, "direction": "Short", "qty": 113, "price": 31.52, "costBasis": 44.4, "prevClose": 31.38},
  {"symbol": "FN", "name": "Fabrinet", "sector": "Technology", "industry": "Electronic Components", "marketCap": 16880464712, "direction": "Long", "qty": 10, "price": 562.08, "costBasis": 506.94, "prevClose": 528.23},
  {"symbol": "EXPI", "name": "eXp World Holdings", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 964689386, "direction": "Short", "qty": 811, "price": 5.56, "costBasis": 6.17, "prevClose": 5.53},
  {"symbol": "NBIS", "name": "Nebius Group", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 55275017723, "direction": "Long", "qty": 71, "price": 276.17, "costBasis": 126.52, "prevClose": 261.15},
  {"symbol": "NVDA", "name": "NVIDIA Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 5105231969267, "direction": "Long", "qty": 27, "price": 200.09, "costBasis": 185.37, "prevClose": 194.97},
  {"symbol": "AMSC", "name": "American Superconductor", "sector": "Technology", "industry": "Power Infrastructure", "marketCap": 1742704473, "direction": "Long", "qty": 163, "price": 41.51, "costBasis": 30.7, "prevClose": 39.83},
  {"symbol": "CIEN", "name": "Ciena Corp", "sector": "Technology", "industry": "Communication Equipment", "marketCap": 65216259625, "direction": "Long", "qty": 14, "price": 490.56, "costBasis": 361.81, "prevClose": 478.93},
  {"symbol": "ADBE", "name": "Adobe Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 88896897563, "direction": "Short", "qty": 21, "price": 205.02, "costBasis": 245.24, "prevClose": 206.43},
  {"symbol": "ARM", "name": "Arm Holdings PLC", "sector": "Technology", "industry": "Semiconductors", "marketCap": 348853674805, "direction": "Long", "qty": 70, "price": 354.57, "costBasis": 173.91, "prevClose": 343.58},
  {"symbol": "BMBL", "name": "Bumble Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 395206480, "direction": "Short", "qty": 1429, "price": 3.2, "costBasis": 3.5, "prevClose": 3.2},
  {"symbol": "AAOI", "name": "Applied Optoelectronics", "sector": "Technology", "industry": "Semiconductors", "marketCap": 9622712586, "direction": "Long", "qty": 43, "price": 148.16, "costBasis": 115.4, "prevClose": 150.1},
  {"symbol": "AEHR", "name": "Aehr Test Systems", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 2283506263, "direction": "Long", "qty": 97, "price": 96.06, "costBasis": 51.29, "prevClose": 94.77},
  {"symbol": "TASK", "name": "TaskUs Inc", "sector": "Technology", "industry": "Information Technology Services", "marketCap": 495438098, "direction": "Short", "qty": 750, "price": 4.68, "costBasis": 6.67, "prevClose": 4.79},
  {"symbol": "TTD", "name": "The Trade Desk Inc", "sector": "Technology", "industry": "Advertising Technology", "marketCap": 9181223406, "direction": "Short", "qty": 242, "price": 18.08, "costBasis": 20.64, "prevClose": 18.65},
  {"symbol": "ACLS", "name": "Axcelis Technologies", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 4405703802, "direction": "Long", "qty": 48, "price": 189.45, "costBasis": 103.86, "prevClose": 176.13},
  {"symbol": "DELL", "name": "Dell Technologies", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 281982805992, "direction": "Long", "qty": 37, "price": 431.46, "costBasis": 244.83, "prevClose": 414.61},
  {"symbol": "GLW", "name": "Corning Inc", "sector": "Technology", "industry": "Electronic Components", "marketCap": 164287157129, "direction": "Long", "qty": 31, "price": 255.43, "costBasis": 159.77, "prevClose": 255.69},
  {"symbol": "STX", "name": "Seagate Technology", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 204124623684, "direction": "Long", "qty": 10, "price": 965, "costBasis": 497.05, "prevClose": 968.53},
  {"symbol": "AMKR", "name": "Amkor Technology", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 17467576865, "direction": "Long", "qty": 91, "price": 86.23, "costBasis": 55.01, "prevClose": 82.34},
  {"symbol": "HUT", "name": "Hut 8 Corp", "sector": "Technology", "industry": "Bitcoin Mining", "marketCap": 11509369911, "direction": "Long", "qty": 77, "price": 115.44, "costBasis": 65.16, "prevClose": 118.27},
  {"symbol": "ONTO", "name": "Onto Innovation Inc", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 15989570852, "direction": "Long", "qty": 19, "price": 378.45, "costBasis": 256.26, "prevClose": 351.45},
  {"symbol": "WDC", "name": "Western Digital Corp", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 234756110000, "direction": "Long", "qty": 15, "price": 638.72, "costBasis": 342.88, "prevClose": 651.88},
  {"symbol": "INTC", "name": "Intel Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 552055844490, "direction": "Long", "qty": 78, "price": 139.63, "costBasis": 64.47, "prevClose": 131.72},
  {"symbol": "APLD", "name": "Applied Digital Corp", "sector": "Technology", "industry": "Data Center Infrastructure", "marketCap": 8901721151, "direction": "Long", "qty": 163, "price": 37.3, "costBasis": 30.61, "prevClose": 37.77},
  {"symbol": "CRDO", "name": "Credo Technology Group Holding Ltd", "sector": "Technology", "industry": "Semiconductors", "marketCap": 48072134162, "direction": "Long", "qty": 32, "price": 271.95, "costBasis": 157.14, "prevClose": 245.68},
  {"symbol": "IREN", "name": "IREN Ltd", "sector": "Technology", "industry": "Bitcoin Mining / AI Compute", "marketCap": 14681117358, "direction": "Long", "qty": 107, "price": 45.73, "costBasis": 46.99, "prevClose": 45.91},
  {"symbol": "SNDK", "name": "SanDisk Corp", "sector": "Technology", "industry": "Data Storage", "marketCap": 283728150246, "direction": "Long", "qty": 8, "price": 2273.73, "costBasis": 999.93, "prevClose": 2050.39},
  {"symbol": "ALAB", "name": "Astera Labs Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 70786340590, "direction": "Long", "qty": 35, "price": 483.02, "costBasis": 213.08, "prevClose": 455.96},
  {"symbol": "DAVE", "name": "Dave Inc", "sector": "Technology", "industry": "Fintech", "marketCap": 5095234517, "direction": "Long", "qty": 18, "price": 372.59, "costBasis": 285.69, "prevClose": 371.62},
  {"symbol": "SITM", "name": "SiTime Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 16602021437, "direction": "Long", "qty": 10, "price": 745.56, "costBasis": 525.18, "prevClose": 710.47},
  {"symbol": "WOLF", "name": "Wolfspeed Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 2175260000, "direction": "Long", "qty": 138, "price": 48.25, "costBasis": 36.19, "prevClose": 44.24},
  {"symbol": "ON", "name": "ON Semiconductor Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 37346251983, "direction": "Long", "qty": 47, "price": 94.54, "costBasis": 105.41, "prevClose": 88.57},
  {"symbol": "AMD", "name": "Advanced Micro Devices Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 909695712140, "direction": "Long", "qty": 15, "price": 580.91, "costBasis": 343.96, "prevClose": 539.49},
  {"symbol": "FLEX", "name": "Flex Ltd", "sector": "Technology", "industry": "Electronic Manufacturing Services", "marketCap": 49755702693, "direction": "Long", "qty": 34, "price": 162.07, "costBasis": 146.38, "prevClose": 159.56},
  {"symbol": "KEEL", "name": "Keel Infrastructure", "sector": "Technology", "industry": "AI/HPC Infrastructure", "marketCap": 2807803139, "direction": "Long", "qty": 721, "price": 5.74, "costBasis": 6.94, "prevClose": 5.78, "entryDate": "2026-06-22"},
  {"symbol": "ACN", "name": "Accenture plc", "sector": "Technology", "industry": "IT Services & Consulting", "marketCap": 82752933960, "direction": "Short", "qty": 42, "price": 124.44, "costBasis": 119.76, "prevClose": 124.74, "entryDate": "2026-06-22"},
  {"symbol": "CNXC", "name": "Concentrix Corp", "sector": "Technology", "industry": "IT Services / BPO", "marketCap": 1354607381, "direction": "Short", "qty": 208, "price": 22.41, "costBasis": 23.99, "prevClose": 25.23, "entryDate": "2026-06-22"},
  {"symbol": "WIX", "name": "Wix.com Ltd", "sector": "Technology", "industry": "Website Building / Web SaaS", "marketCap": 1864190000, "direction": "Short", "qty": 112, "price": 45.37, "costBasis": 44.93, "prevClose": 44.93, "entryDate": "2026-06-30"},
  {"symbol": "GLOB", "name": "Globant SA", "sector": "Technology", "industry": "IT Services / Digital Engineering", "marketCap": 1293659475, "direction": "Short", "qty": 175, "price": 28.94, "costBasis": 28.61, "prevClose": 28.61, "entryDate": "2026-06-30"}
];
