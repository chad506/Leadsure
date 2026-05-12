// ============================================
// FUND-DATA.JS — Shared position data
// Single source of truth for all pages
// ============================================

const SHARED_FINNHUB_KEY = 'd6kqa11r01qmopd1net0d6kqa11r01qmopd1netg';

// Date when price/prevClose were last set (YYYY-MM-DD in US/Pacific)
// On a new trading day, pages auto-reset price = prevClose so Today P&L starts at $0
const PRICES_AS_OF = '2026-05-11';

// Realized P&L from closed positions (CHGG: -$449.07, RIOT: -$1,189.30, U: -$1,336.68, HPP: -$3,496.09)
const SHARED_REALIZED_PNL = -6471.14;

// Sold positions (closed end of March)
const SOLD_POSITIONS = [
  {"symbol": "CHGG", "name": "Chegg Inc", "direction": "Short", "qty": 7690, "costBasis": 0.65, "exitPrice": 0.71, "realizedPnl": -449.07, "entryDate": "Mar 4", "exitDate": "Mar 31"},
  {"symbol": "RIOT", "name": "Riot Platforms Inc", "direction": "Long", "qty": 303, "costBasis": 16.52, "exitPrice": 12.60, "realizedPnl": -1189.30, "entryDate": "Mar 4", "exitDate": "Mar 31"},
  {"symbol": "U", "name": "Unity Software Inc", "direction": "Short", "qty": 244, "costBasis": 20.52, "exitPrice": 26.00, "realizedPnl": -1336.68, "entryDate": "Mar 4", "exitDate": "Apr 30"},
  {"symbol": "HPP", "name": "Hudson Pacific Properties", "direction": "Short", "qty": 1244, "costBasis": 6.39, "exitPrice": 9.20, "realizedPnl": -3496.09, "entryDate": "Mar 4", "exitDate": "Apr 30"}
];

// Add-on positions (March rebalance — informational only, already included in POSITIONS totals)
const ADDON_POSITIONS = [
  {"symbol": "ARM", "name": "Arm Holdings PLC", "direction": "Long", "qty": 19, "costBasis": 155.22, "entryDate": "Mar 31", "note": "Added to biggest long winner (+13.10%)"},
  {"symbol": "HPP", "name": "Hudson Pacific Properties", "direction": "Short", "qty": 534, "costBasis": 5.51, "entryDate": "Mar 31", "note": "Added to biggest short winner (+13.73%)"},
  {"symbol": "BE", "name": "Bloom Energy Corp", "direction": "Long", "qty": 15, "costBasis": 272.96, "entryDate": "Apr 30", "note": "Added to biggest April long winner"},
  {"symbol": "MRVL", "name": "Marvell Technology", "direction": "Long", "qty": 25, "costBasis": 164.88, "entryDate": "Apr 30", "note": "Added to biggest April long winner"}
];

// Active positions — THE source of truth (61 positions)
const POSITIONS = [
  {"symbol": "BE", "name": "Bloom Energy Corp", "sector": "Energy", "industry": "Electrical Equipment & Parts", "marketCap": 31512725640, "direction": "Long", "qty": 46, "price": 275.88, "costBasis": 198.60, "prevClose": 283.92},
  {"symbol": "CBRE", "name": "CBRE Group Inc", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 39213827897, "direction": "Short", "qty": 35, "price": 142.93, "costBasis": 141.82, "prevClose": 146.11},
  {"symbol": "CORZ", "name": "Core Scientific Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 4752062885, "direction": "Long", "qty": 309, "price": 21.92, "costBasis": 16.17, "prevClose": 22.95},
  {"symbol": "CRM", "name": "Salesforce Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 168013474124, "direction": "Short", "qty": 26, "price": 175.12, "costBasis": 195.71, "prevClose": 177.49},
  {"symbol": "CRWV", "name": "CoreWeave Inc", "sector": "Technology", "industry": "Cloud Infrastructure", "marketCap": 39326728332, "direction": "Long", "qty": 62, "price": 103.82, "costBasis": 80.17, "prevClose": 114.7},
  {"symbol": "CTSH", "name": "Cognizant Technology", "sector": "Technology", "industry": "IT Services", "marketCap": 28828473235, "direction": "Short", "qty": 77, "price": 48.54, "costBasis": 64.97, "prevClose": 49.25},
  {"symbol": "CWK", "name": "Cushman & Wakefield", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 2735496025, "direction": "Short", "qty": 373, "price": 13.4, "costBasis": 13.38, "prevClose": 13.76},
  {"symbol": "DUOL", "name": "Duolingo Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 4476700140, "direction": "Short", "qty": 50, "price": 107.66, "costBasis": 99.7, "prevClose": 105.15},
  {"symbol": "FVRR", "name": "Fiverr International", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 350879105, "direction": "Short", "qty": 463, "price": 10.95, "costBasis": 10.82, "prevClose": 11.05},
  {"symbol": "INTU", "name": "Intuit Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 115884452461, "direction": "Short", "qty": 12, "price": 394.27, "costBasis": 437.9, "prevClose": 393.29},
  {"symbol": "LITE", "name": "Lumentum Holdings", "sector": "Technology", "industry": "Communication Equipment", "marketCap": 50174922000, "direction": "Long", "qty": 8, "price": 978.36, "costBasis": 652.68, "prevClose": 1053.09},
  {"symbol": "LZ", "name": "LegalZoom.com Inc", "sector": "Technology", "industry": "Specialty Business Services", "marketCap": 971440965, "direction": "Short", "qty": 745, "price": 6.28, "costBasis": 6.71, "prevClose": 6.1},
  {"symbol": "MDB", "name": "MongoDB Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 18927827304, "direction": "Short", "qty": 20, "price": 313.92, "costBasis": 250.37, "prevClose": 294.65},
  {"symbol": "MU", "name": "Micron Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 402847710600, "direction": "Long", "qty": 12, "price": 739.32, "costBasis": 405.19, "prevClose": 795.33},
  {"symbol": "NOW", "name": "ServiceNow Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 103982860000, "direction": "Short", "qty": 44, "price": 90.42, "costBasis": 114.35, "prevClose": 91.49},
  {"symbol": "TSM", "name": "Taiwan Semiconductor", "sector": "Technology", "industry": "Semiconductors", "marketCap": 1694640111089, "direction": "Long", "qty": 14, "price": 388.76, "costBasis": 358.83, "prevClose": 404.54},
  {"symbol": "UPWK", "name": "Upwork Inc", "sector": "Technology", "industry": "Staffing & Employment", "marketCap": 1420218546, "direction": "Short", "qty": 370, "price": 8.49, "costBasis": 13.52, "prevClose": 8.81},
  {"symbol": "VRT", "name": "Vertiv Holdings", "sector": "Industrials", "industry": "Electrical Equipment & Parts", "marketCap": 96058879860, "direction": "Long", "qty": 20, "price": 352.58, "costBasis": 251.97, "prevClose": 367.92},
  {"symbol": "WDAY", "name": "Workday Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 32919831144, "direction": "Short", "qty": 34, "price": 121.51, "costBasis": 145.57, "prevClose": 121.42},
  {"symbol": "WPP", "name": "WPP PLC", "sector": "Comm Services", "industry": "Advertising Agencies", "marketCap": 3307478865, "direction": "Short", "qty": 293, "price": 17.49, "costBasis": 17.09, "prevClose": 17.9},
  {"symbol": "WULF", "name": "TeraWulf Inc", "sector": "Technology", "industry": "Capital Markets", "marketCap": 6314372520, "direction": "Long", "qty": 320, "price": 22.11, "costBasis": 15.61, "prevClose": 23.37},
  {"symbol": "CAT", "name": "Caterpillar Inc", "sector": "Industrials", "industry": "Farm & Heavy Construction Machinery", "marketCap": 325433009668, "direction": "Long", "qty": 7, "price": 898.63, "costBasis": 700.72, "prevClose": 926.79},
  {"symbol": "FCG", "name": "First Trust Natural Gas ETF", "sector": "Energy", "industry": "Natural Gas ETF", "marketCap": 606577942, "direction": "Long", "qty": 174, "price": 29.62, "costBasis": 28.78, "prevClose": 29.58},
  {"symbol": "REMX", "name": "VanEck Rare Earth ETF", "sector": "Materials", "industry": "Rare Earth & Strategic Metals ETF", "marketCap": 1119500183, "direction": "Long", "qty": 54, "price": 104.52, "costBasis": 92.91, "prevClose": 109.53},
  {"symbol": "COHR", "name": "Coherent Corp", "sector": "Technology", "industry": "Scientific & Technical Instruments", "marketCap": 38609869731, "direction": "Long", "qty": 20, "price": 361.47, "costBasis": 252.4, "prevClose": 379.69},
  {"symbol": "SPG", "name": "Simon Property Group", "sector": "Real Estate", "industry": "REIT - Retail", "marketCap": 58553332604, "direction": "Short", "qty": 26, "price": 205.36, "costBasis": 194.34, "prevClose": 201.0},
  {"symbol": "COPX", "name": "Global X Copper Miners ETF", "sector": "Materials", "industry": "Copper Miners ETF", "marketCap": 3232889592, "direction": "Long", "qty": 62, "price": 86.5, "costBasis": 80.22, "prevClose": 87.59},
  {"symbol": "MRVL", "name": "Marvell Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 82953584000, "direction": "Long", "qty": 80, "price": 160.84, "costBasis": 114.46, "prevClose": 170.84},
  {"symbol": "PSFE", "name": "Paysafe Ltd", "sector": "Technology", "industry": "IT Services", "marketCap": 380404570, "direction": "Short", "qty": 666, "price": 8.78, "costBasis": 7.5, "prevClose": 8.72},
  {"symbol": "Z", "name": "Zillow Group Inc", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 9793320952, "direction": "Short", "qty": 113, "price": 39.87, "costBasis": 44.4, "prevClose": 40.44},
  {"symbol": "FN", "name": "Fabrinet", "sector": "Technology", "industry": "Electronic Components", "marketCap": 19775543448, "direction": "Long", "qty": 10, "price": 613.26, "costBasis": 506.94, "prevClose": 649.53},
  {"symbol": "BXP", "name": "BXP Inc", "sector": "Real Estate", "industry": "REIT - Office", "marketCap": 8158289470, "direction": "Short", "qty": 98, "price": 58.78, "costBasis": 51.05, "prevClose": 58.94},
  {"symbol": "EXPI", "name": "eXp World Holdings", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 964689386, "direction": "Short", "qty": 811, "price": 6.04, "costBasis": 6.17, "prevClose": 6.6},
  {"symbol": "NBIS", "name": "Nebius Group", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 24196800000, "direction": "Long", "qty": 53, "price": 176.56, "costBasis": 94.03, "prevClose": 186.1},
  {"symbol": "NVDA", "name": "NVIDIA Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 4071573854798, "direction": "Long", "qty": 27, "price": 216.76, "costBasis": 185.37, "prevClose": 219.44},
  {"symbol": "AMSC", "name": "American Superconductor", "sector": "Technology", "industry": "Power Infrastructure", "marketCap": 1605486250, "direction": "Long", "qty": 163, "price": 53.49, "costBasis": 30.7, "prevClose": 58.72},
  {"symbol": "CIEN", "name": "Ciena Corp", "sector": "Technology", "industry": "Communication Equipment", "marketCap": 56813139769, "direction": "Long", "qty": 14, "price": 558.17, "costBasis": 361.81, "prevClose": 581.47},
  {"symbol": "ADBE", "name": "Adobe Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 95729451005, "direction": "Short", "qty": 21, "price": 244.04, "costBasis": 245.24, "prevClose": 246.15},
  {"symbol": "ARM", "name": "Arm Holdings PLC", "sector": "Technology", "industry": "Semiconductors", "marketCap": 153065853750, "direction": "Long", "qty": 58, "price": 205.03, "costBasis": 136.83, "prevClose": 212.65},
  {"symbol": "BMBL", "name": "Bumble Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 354632607, "direction": "Short", "qty": 1429, "price": 3.44, "costBasis": 3.50, "prevClose": 3.29},
  {"symbol": "AAOI", "name": "Applied Optoelectronics", "sector": "Technology", "industry": "Semiconductors", "marketCap": 3500000000, "direction": "Long", "qty": 43, "price": 187.37, "costBasis": 115.40, "prevClose": 184.9},
  {"symbol": "AEHR", "name": "Aehr Test Systems", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 1500000000, "direction": "Long", "qty": 97, "price": 93.52, "costBasis": 51.29, "prevClose": 104.56},
  {"symbol": "TASK", "name": "TaskUs Inc", "sector": "Technology", "industry": "Information Technology Services", "marketCap": 440000000, "direction": "Short", "qty": 750, "price": 5.85, "costBasis": 6.67, "prevClose": 5.85},
  {"symbol": "TTD", "name": "The Trade Desk Inc", "sector": "Technology", "industry": "Advertising Technology", "marketCap": 10100000000, "direction": "Short", "qty": 242, "price": 21.62, "costBasis": 20.64, "prevClose": 21.52},
  {"symbol": "ACLS", "name": "Axcelis Technologies", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 2661324538, "direction": "Long", "qty": 48, "price": 153.83, "costBasis": 103.86, "prevClose": 165.08},
  {"symbol": "DELL", "name": "Dell Technologies", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 103344870223, "direction": "Long", "qty": 27, "price": 232.03, "costBasis": 184.71, "prevClose": 247.04},
  {"symbol": "GLW", "name": "Corning Inc", "sector": "Technology", "industry": "Electronic Components", "marketCap": 12500000000, "direction": "Long", "qty": 31, "price": 194.34, "costBasis": 159.77, "prevClose": 207.39},
  {"symbol": "STX", "name": "Seagate Technology", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 90430511640, "direction": "Long", "qty": 10, "price": 784.48, "costBasis": 497.05, "prevClose": 834.01},
  {"symbol": "AMKR", "name": "Amkor Technology", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 6800000000, "direction": "Long", "qty": 91, "price": 70.96, "costBasis": 55.01, "prevClose": 76.69},
  {"symbol": "GPN", "name": "Global Payments Inc", "sector": "Financials", "industry": "Specialty Business Services", "marketCap": 15500000000, "direction": "Short", "qty": 78, "price": 68.08, "costBasis": 64.06, "prevClose": 68.77},
  {"symbol": "HUT", "name": "Hut 8 Corp", "sector": "Technology", "industry": "Bitcoin Mining", "marketCap": 7032471710, "direction": "Long", "qty": 77, "price": 98.3, "costBasis": 65.16, "prevClose": 102.19},
  {"symbol": "ONTO", "name": "Onto Innovation Inc", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 12274494673, "direction": "Long", "qty": 19, "price": 273.75, "costBasis": 256.26, "prevClose": 287.52},
  {"symbol": "WDC", "name": "Western Digital Corp", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 114554136507, "direction": "Long", "qty": 15, "price": 484.99, "costBasis": 342.88, "prevClose": 515.83},
  {"symbol": "INTC", "name": "Intel Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 327269422127, "direction": "Long", "qty": 78, "price": 117.69, "costBasis": 64.47, "prevClose": 129.44},
  {"symbol": "APLD", "name": "Applied Digital Corp", "sector": "Technology", "industry": "Data Center Infrastructure", "marketCap": 7887239131, "direction": "Long", "qty": 163, "price": 42.16, "costBasis": 30.61, "prevClose": 44.59},
  {"symbol": "CRDO", "name": "Credo Technology Group Holding Ltd", "sector": "Technology", "industry": "Semiconductors", "marketCap": 24782692630, "direction": "Long", "qty": 32, "price": 191.59, "costBasis": 157.14, "prevClose": 210.22},
  {"symbol": "IREN", "name": "IREN Ltd", "sector": "Technology", "industry": "Bitcoin Mining / AI Compute", "marketCap": 14288868108, "direction": "Long", "qty": 107, "price": 53.89, "costBasis": 46.99, "prevClose": 55.15},
  {"symbol": "SNDK", "name": "SanDisk Corp", "sector": "Technology", "industry": "Data Storage", "marketCap": 140589924679, "direction": "Long", "qty": 6, "price": 1406.28, "costBasis": 915.70, "prevClose": 1547.56},
  {"symbol": "ALAB", "name": "Astera Labs Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 10500000000, "direction": "Long", "qty": 26, "price": 198.56, "costBasis": 193.86, "prevClose": 207.35},
  {"symbol": "DAVE", "name": "Dave Inc", "sector": "Technology", "industry": "Fintech", "marketCap": 1800000000, "direction": "Long", "qty": 18, "price": 242.05, "costBasis": 285.69, "prevClose": 249.42},
  {"symbol": "SITM", "name": "SiTime Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 2600000000, "direction": "Long", "qty": 10, "price": 818.11, "costBasis": 525.18, "prevClose": 901.48},
  {"symbol": "WOLF", "name": "Wolfspeed Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 4700000000, "direction": "Long", "qty": 138, "price": 46.68, "costBasis": 36.19, "prevClose": 50.31},
  {"symbol": "ON", "name": "ON Semiconductor Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 22900000000, "direction": "Long", "qty": 47, "price": 99.42, "costBasis": 105.41, "prevClose": 107.24},
  {"symbol": "AMD", "name": "Advanced Micro Devices Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 683000000000, "direction": "Long", "qty": 15, "price": 438.22, "costBasis": 343.96, "prevClose": 458.79}
];
