// ============================================
// FUND-DATA.JS — Shared position data
// Single source of truth for all pages
// ============================================

const SHARED_FINNHUB_KEY = 'd6kqa11r01qmopd1net0d6kqa11r01qmopd1netg';

// Date when price/prevClose were last set (YYYY-MM-DD in US/Pacific)
// On a new trading day, pages auto-reset price = prevClose so Today P&L starts at $0
const PRICES_AS_OF = '2026-05-13';

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
  {"symbol": "BE", "name": "Bloom Energy Corp", "sector": "Energy", "industry": "Electrical Equipment & Parts", "marketCap": 31512725640, "direction": "Long", "qty": 46, "price": 288.95, "costBasis": 198.60, "prevClose": 280.69},
  {"symbol": "CBRE", "name": "CBRE Group Inc", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 39213827897, "direction": "Short", "qty": 35, "price": 140.32, "costBasis": 141.82, "prevClose": 144.06},
  {"symbol": "CORZ", "name": "Core Scientific Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 4752062885, "direction": "Long", "qty": 309, "price": 23.45, "costBasis": 16.17, "prevClose": 22.79},
  {"symbol": "CRM", "name": "Salesforce Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 168013474124, "direction": "Short", "qty": 26, "price": 166.11, "costBasis": 195.71, "prevClose": 171.31},
  {"symbol": "CRWV", "name": "CoreWeave Inc", "sector": "Technology", "industry": "Cloud Infrastructure", "marketCap": 39326728332, "direction": "Long", "qty": 62, "price": 110.32, "costBasis": 80.17, "prevClose": 107.75},
  {"symbol": "CTSH", "name": "Cognizant Technology", "sector": "Technology", "industry": "IT Services", "marketCap": 28828473235, "direction": "Short", "qty": 77, "price": 45.55, "costBasis": 64.97, "prevClose": 47.73},
  {"symbol": "CWK", "name": "Cushman & Wakefield", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 2735496025, "direction": "Short", "qty": 373, "price": 12.93, "costBasis": 13.38, "prevClose": 13.35},
  {"symbol": "DUOL", "name": "Duolingo Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 4476700140, "direction": "Short", "qty": 50, "price": 104.21, "costBasis": 99.7, "prevClose": 106.01},
  {"symbol": "FVRR", "name": "Fiverr International", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 350879105, "direction": "Short", "qty": 463, "price": 10.63, "costBasis": 10.82, "prevClose": 10.91},
  {"symbol": "INTU", "name": "Intuit Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 115884452461, "direction": "Short", "qty": 12, "price": 377.03, "costBasis": 437.9, "prevClose": 387.74},
  {"symbol": "LITE", "name": "Lumentum Holdings", "sector": "Technology", "industry": "Communication Equipment", "marketCap": 50174922000, "direction": "Long", "qty": 8, "price": 1021.52, "costBasis": 652.68, "prevClose": 992.37},
  {"symbol": "LZ", "name": "LegalZoom.com Inc", "sector": "Technology", "industry": "Specialty Business Services", "marketCap": 971440965, "direction": "Short", "qty": 745, "price": 5.69, "costBasis": 6.71, "prevClose": 6.16},
  {"symbol": "MDB", "name": "MongoDB Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 18927827304, "direction": "Short", "qty": 20, "price": 301.41, "costBasis": 250.37, "prevClose": 308.72},
  {"symbol": "MU", "name": "Micron Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 402847710600, "direction": "Long", "qty": 12, "price": 788.76, "costBasis": 405.19, "prevClose": 766.58},
  {"symbol": "NOW", "name": "ServiceNow Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 103982860000, "direction": "Short", "qty": 44, "price": 86.87, "costBasis": 114.35, "prevClose": 89.0},
  {"symbol": "TSM", "name": "Taiwan Semiconductor", "sector": "Technology", "industry": "Semiconductors", "marketCap": 1694640111089, "direction": "Long", "qty": 14, "price": 397.27, "costBasis": 358.83, "prevClose": 397.28},
  {"symbol": "UPWK", "name": "Upwork Inc", "sector": "Technology", "industry": "Staffing & Employment", "marketCap": 1420218546, "direction": "Short", "qty": 370, "price": 8.48, "costBasis": 13.52, "prevClose": 8.35},
  {"symbol": "VRT", "name": "Vertiv Holdings", "sector": "Industrials", "industry": "Electrical Equipment & Parts", "marketCap": 96058879860, "direction": "Long", "qty": 20, "price": 369.35, "costBasis": 251.97, "prevClose": 367.13},
  {"symbol": "WDAY", "name": "Workday Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 32919831144, "direction": "Short", "qty": 34, "price": 113.06, "costBasis": 145.57, "prevClose": 118.62},
  {"symbol": "WPP", "name": "WPP PLC", "sector": "Comm Services", "industry": "Advertising Agencies", "marketCap": 3307478865, "direction": "Short", "qty": 293, "price": 17.24, "costBasis": 17.09, "prevClose": 17.46},
  {"symbol": "WULF", "name": "TeraWulf Inc", "sector": "Technology", "industry": "Capital Markets", "marketCap": 6314372520, "direction": "Long", "qty": 320, "price": 22.82, "costBasis": 15.61, "prevClose": 22.8},
  {"symbol": "CAT", "name": "Caterpillar Inc", "sector": "Industrials", "industry": "Farm & Heavy Construction Machinery", "marketCap": 325433009668, "direction": "Long", "qty": 7, "price": 903.15, "costBasis": 700.72, "prevClose": 912.14},
  {"symbol": "FCG", "name": "First Trust Natural Gas ETF", "sector": "Energy", "industry": "Natural Gas ETF", "marketCap": 606577942, "direction": "Long", "qty": 174, "price": 29.51, "costBasis": 28.78, "prevClose": 29.79},
  {"symbol": "REMX", "name": "VanEck Rare Earth ETF", "sector": "Materials", "industry": "Rare Earth & Strategic Metals ETF", "marketCap": 1119500183, "direction": "Long", "qty": 54, "price": 106.59, "costBasis": 92.91, "prevClose": 108.03},
  {"symbol": "COHR", "name": "Coherent Corp", "sector": "Technology", "industry": "Scientific & Technical Instruments", "marketCap": 38609869731, "direction": "Long", "qty": 20, "price": 397.19, "costBasis": 252.4, "prevClose": 374.01},
  {"symbol": "SPG", "name": "Simon Property Group", "sector": "Real Estate", "industry": "REIT - Retail", "marketCap": 58553332604, "direction": "Short", "qty": 26, "price": 202.66, "costBasis": 194.34, "prevClose": 205.66},
  {"symbol": "COPX", "name": "Global X Copper Miners ETF", "sector": "Materials", "industry": "Copper Miners ETF", "marketCap": 3232889592, "direction": "Long", "qty": 62, "price": 92.17, "costBasis": 80.22, "prevClose": 90.77},
  {"symbol": "MRVL", "name": "Marvell Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 82953584000, "direction": "Long", "qty": 80, "price": 174.83, "costBasis": 114.46, "prevClose": 164.5},
  {"symbol": "PSFE", "name": "Paysafe Ltd", "sector": "Technology", "industry": "IT Services", "marketCap": 380404570, "direction": "Short", "qty": 666, "price": 9.23, "costBasis": 7.5, "prevClose": 8.69},
  {"symbol": "Z", "name": "Zillow Group Inc", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 9793320952, "direction": "Short", "qty": 113, "price": 39.17, "costBasis": 44.4, "prevClose": 39.63},
  {"symbol": "FN", "name": "Fabrinet", "sector": "Technology", "industry": "Electronic Components", "marketCap": 19775543448, "direction": "Long", "qty": 10, "price": 675.41, "costBasis": 506.94, "prevClose": 634.48},
  {"symbol": "BXP", "name": "BXP Inc", "sector": "Real Estate", "industry": "REIT - Office", "marketCap": 8158289470, "direction": "Short", "qty": 98, "price": 58.21, "costBasis": 51.05, "prevClose": 59.01},
  {"symbol": "EXPI", "name": "eXp World Holdings", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 964689386, "direction": "Short", "qty": 811, "price": 5.215, "costBasis": 6.17, "prevClose": 6.04},
  {"symbol": "NBIS", "name": "Nebius Group", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 24196800000, "direction": "Long", "qty": 53, "price": 205.57, "costBasis": 94.03, "prevClose": 179.11},
  {"symbol": "NVDA", "name": "NVIDIA Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 4071573854798, "direction": "Long", "qty": 27, "price": 226.78, "costBasis": 185.37, "prevClose": 220.78},
  {"symbol": "AMSC", "name": "American Superconductor", "sector": "Technology", "industry": "Power Infrastructure", "marketCap": 1605486250, "direction": "Long", "qty": 163, "price": 53.95, "costBasis": 30.7, "prevClose": 54.51},
  {"symbol": "CIEN", "name": "Ciena Corp", "sector": "Technology", "industry": "Communication Equipment", "marketCap": 56813139769, "direction": "Long", "qty": 14, "price": 573.19, "costBasis": 361.81, "prevClose": 577.15},
  {"symbol": "ADBE", "name": "Adobe Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 95729451005, "direction": "Short", "qty": 21, "price": 233.92, "costBasis": 245.24, "prevClose": 240.83},
  {"symbol": "ARM", "name": "Arm Holdings PLC", "sector": "Technology", "industry": "Semiconductors", "marketCap": 153065853750, "direction": "Long", "qty": 58, "price": 216.03, "costBasis": 136.83, "prevClose": 207.92},
  {"symbol": "BMBL", "name": "Bumble Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 354632607, "direction": "Short", "qty": 1429, "price": 3.36, "costBasis": 3.50, "prevClose": 3.36},
  {"symbol": "AAOI", "name": "Applied Optoelectronics", "sector": "Technology", "industry": "Semiconductors", "marketCap": 3500000000, "direction": "Long", "qty": 43, "price": 204.23, "costBasis": 115.40, "prevClose": 188.28},
  {"symbol": "AEHR", "name": "Aehr Test Systems", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 1500000000, "direction": "Long", "qty": 97, "price": 95.78, "costBasis": 51.29, "prevClose": 96.72},
  {"symbol": "TASK", "name": "TaskUs Inc", "sector": "Technology", "industry": "Information Technology Services", "marketCap": 440000000, "direction": "Short", "qty": 750, "price": 5.64, "costBasis": 6.67, "prevClose": 5.82},
  {"symbol": "TTD", "name": "The Trade Desk Inc", "sector": "Technology", "industry": "Advertising Technology", "marketCap": 10100000000, "direction": "Short", "qty": 242, "price": 20.19, "costBasis": 20.64, "prevClose": 21.14},
  {"symbol": "ACLS", "name": "Axcelis Technologies", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 2661324538, "direction": "Long", "qty": 48, "price": 161.15, "costBasis": 103.86, "prevClose": 161.64},
  {"symbol": "DELL", "name": "Dell Technologies", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 103344870223, "direction": "Long", "qty": 27, "price": 240.41, "costBasis": 184.71, "prevClose": 238.94},
  {"symbol": "GLW", "name": "Corning Inc", "sector": "Technology", "industry": "Electronic Components", "marketCap": 12500000000, "direction": "Long", "qty": 31, "price": 201.6, "costBasis": 159.77, "prevClose": 198.24},
  {"symbol": "STX", "name": "Seagate Technology", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 90430511640, "direction": "Long", "qty": 10, "price": 808.76, "costBasis": 497.05, "prevClose": 808.795},
  {"symbol": "AMKR", "name": "Amkor Technology", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 6800000000, "direction": "Long", "qty": 91, "price": 73.96, "costBasis": 55.01, "prevClose": 73.45},
  {"symbol": "GPN", "name": "Global Payments Inc", "sector": "Financials", "industry": "Specialty Business Services", "marketCap": 15500000000, "direction": "Short", "qty": 78, "price": 66.44, "costBasis": 64.06, "prevClose": 68.61},
  {"symbol": "HUT", "name": "Hut 8 Corp", "sector": "Technology", "industry": "Bitcoin Mining", "marketCap": 7032471710, "direction": "Long", "qty": 77, "price": 105.31, "costBasis": 65.16, "prevClose": 107.31},
  {"symbol": "ONTO", "name": "Onto Innovation Inc", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 12274494673, "direction": "Long", "qty": 19, "price": 276.47, "costBasis": 256.26, "prevClose": 277.94},
  {"symbol": "WDC", "name": "Western Digital Corp", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 114554136507, "direction": "Long", "qty": 15, "price": 487.13, "costBasis": 342.88, "prevClose": 488.74},
  {"symbol": "INTC", "name": "Intel Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 327269422127, "direction": "Long", "qty": 78, "price": 119.76, "costBasis": 64.47, "prevClose": 120.61},
  {"symbol": "APLD", "name": "Applied Digital Corp", "sector": "Technology", "industry": "Data Center Infrastructure", "marketCap": 7887239131, "direction": "Long", "qty": 163, "price": 43.93, "costBasis": 30.61, "prevClose": 43.93},
  {"symbol": "CRDO", "name": "Credo Technology Group Holding Ltd", "sector": "Technology", "industry": "Semiconductors", "marketCap": 24782692630, "direction": "Long", "qty": 32, "price": 186.92, "costBasis": 157.14, "prevClose": 198.57},
  {"symbol": "IREN", "name": "IREN Ltd", "sector": "Technology", "industry": "Bitcoin Mining / AI Compute", "marketCap": 14288868108, "direction": "Long", "qty": 107, "price": 53.85, "costBasis": 46.99, "prevClose": 56.56},
  {"symbol": "SNDK", "name": "SanDisk Corp", "sector": "Technology", "industry": "Data Storage", "marketCap": 140589924679, "direction": "Long", "qty": 6, "price": 1418.56, "costBasis": 915.70, "prevClose": 1452.02},
  {"symbol": "ALAB", "name": "Astera Labs Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 10500000000, "direction": "Long", "qty": 26, "price": 216.57, "costBasis": 193.86, "prevClose": 204.42},
  {"symbol": "DAVE", "name": "Dave Inc", "sector": "Technology", "industry": "Fintech", "marketCap": 1800000000, "direction": "Long", "qty": 18, "price": 237.65, "costBasis": 285.69, "prevClose": 242.25},
  {"symbol": "SITM", "name": "SiTime Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 2600000000, "direction": "Long", "qty": 10, "price": 823.3, "costBasis": 525.18, "prevClose": 847.19},
  {"symbol": "WOLF", "name": "Wolfspeed Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 4700000000, "direction": "Long", "qty": 138, "price": 63.8, "costBasis": 36.19, "prevClose": 53.72},
  {"symbol": "ON", "name": "ON Semiconductor Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 22900000000, "direction": "Long", "qty": 47, "price": 113.6, "costBasis": 105.41, "prevClose": 104.11},
  {"symbol": "AMD", "name": "Advanced Micro Devices Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 683000000000, "direction": "Long", "qty": 15, "price": 445.14, "costBasis": 343.96, "prevClose": 448.29},
  {"symbol": "AXTI", "name": "AXT Inc", "sector": "Technology", "industry": "Compound Semiconductor Substrates", "marketCap": 12000000000, "direction": "Long", "qty": 41, "price": 118.4, "costBasis": 120.85, "prevClose": 122.9},
  {"symbol": "FLEX", "name": "Flex Ltd", "sector": "Technology", "industry": "Electronic Manufacturing Services", "marketCap": 65700000000, "direction": "Long", "qty": 34, "price": 145.64, "costBasis": 146.38, "prevClose": 139.69}
];
