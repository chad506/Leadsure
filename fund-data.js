// ============================================
// FUND-DATA.JS — Shared position data
// Single source of truth for all pages
// ============================================

const SHARED_FINNHUB_KEY = 'd6kqa11r01qmopd1net0d6kqa11r01qmopd1netg';

// Date when price/prevClose were last set (YYYY-MM-DD in US/Pacific)
// On a new trading day, pages auto-reset price = prevClose so Today P&L starts at $0
const PRICES_AS_OF = '2026-04-22';

// Realized P&L from closed positions (CHGG short: -$449.07, RIOT long: -$1,189.30)
const SHARED_REALIZED_PNL = -1638.37;

// Sold positions (closed end of March)
const SOLD_POSITIONS = [
  {"symbol": "CHGG", "name": "Chegg Inc", "direction": "Short", "qty": 7690, "costBasis": 0.65, "exitPrice": 0.71, "realizedPnl": -449.07, "entryDate": "Mar 4", "exitDate": "Mar 31"},
  {"symbol": "RIOT", "name": "Riot Platforms Inc", "direction": "Long", "qty": 303, "costBasis": 16.52, "exitPrice": 12.60, "realizedPnl": -1189.30, "entryDate": "Mar 4", "exitDate": "Mar 31"}
];

// Add-on positions (March rebalance — informational only, already included in POSITIONS totals)
const ADDON_POSITIONS = [
  {"symbol": "ARM", "name": "Arm Holdings PLC", "direction": "Long", "qty": 19, "costBasis": 155.22, "entryDate": "Mar 31", "note": "Added to biggest long winner (+13.10%)"},
  {"symbol": "HPP", "name": "Hudson Pacific Properties", "direction": "Short", "qty": 534, "costBasis": 5.51, "entryDate": "Mar 31", "note": "Added to biggest short winner (+13.73%)"}
];

// Active positions — THE source of truth (60 positions)
const POSITIONS = [
  {"symbol": "BE", "name": "Bloom Energy Corp", "sector": "Energy", "industry": "Electrical Equipment & Parts", "marketCap": 31512725640, "direction": "Long", "qty": 31, "price": 229.75, "costBasis": 162.62, "prevClose": 229.75},
  {"symbol": "CBRE", "name": "CBRE Group Inc", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 39213827897, "direction": "Short", "qty": 35, "price": 153.0, "costBasis": 141.82, "prevClose": 153.0},

  {"symbol": "CORZ", "name": "Core Scientific Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 4752062885, "direction": "Long", "qty": 309, "price": 21.02, "costBasis": 16.17, "prevClose": 21.02},
  {"symbol": "CRM", "name": "Salesforce Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 168013474124, "direction": "Short", "qty": 26, "price": 182.27, "costBasis": 195.71, "prevClose": 187.11},
  {"symbol": "CRWV", "name": "CoreWeave Inc", "sector": "Technology", "industry": "Cloud Infrastructure", "marketCap": 39326728332, "direction": "Long", "qty": 62, "price": 122.23, "costBasis": 80.17, "prevClose": 122.23},
  {"symbol": "CTSH", "name": "Cognizant Technology", "sector": "Technology", "industry": "IT Services", "marketCap": 28828473235, "direction": "Short", "qty": 77, "price": 58.6, "costBasis": 64.97, "prevClose": 60.45},
  {"symbol": "CWK", "name": "Cushman & Wakefield", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 2735496025, "direction": "Short", "qty": 373, "price": 14.54, "costBasis": 13.38, "prevClose": 14.54},
  {"symbol": "DUOL", "name": "Duolingo Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 4476700140, "direction": "Short", "qty": 50, "price": 104.49, "costBasis": 99.7, "prevClose": 104.49},
  {"symbol": "FVRR", "name": "Fiverr International", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 350879105, "direction": "Short", "qty": 463, "price": 10.52, "costBasis": 10.82, "prevClose": 10.52},
  {"symbol": "INTU", "name": "Intuit Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 115884452461, "direction": "Short", "qty": 12, "price": 397.18, "costBasis": 437.9, "prevClose": 404.85},
  {"symbol": "LITE", "name": "Lumentum Holdings", "sector": "Technology", "industry": "Communication Equipment", "marketCap": 50174922000, "direction": "Long", "qty": 8, "price": 866.5, "costBasis": 652.68, "prevClose": 866.5},
  {"symbol": "LZ", "name": "LegalZoom.com Inc", "sector": "Technology", "industry": "Specialty Business Services", "marketCap": 971440965, "direction": "Short", "qty": 745, "price": 6.62, "costBasis": 6.71, "prevClose": 6.62},
  {"symbol": "MDB", "name": "MongoDB Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 18927827304, "direction": "Short", "qty": 20, "price": 265.0, "costBasis": 250.37, "prevClose": 265.0},
  {"symbol": "MU", "name": "Micron Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 402847710600, "direction": "Long", "qty": 12, "price": 486.5, "costBasis": 405.19, "prevClose": 486.5},
  {"symbol": "NOW", "name": "ServiceNow Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 103982860000, "direction": "Short", "qty": 44, "price": 90.09, "costBasis": 114.35, "prevClose": 100.14},

  {"symbol": "TSM", "name": "Taiwan Semiconductor", "sector": "Technology", "industry": "Semiconductors", "marketCap": 1694640111089, "direction": "Long", "qty": 14, "price": 384.88, "costBasis": 358.83, "prevClose": 384.88},
  {"symbol": "U", "name": "Unity Software Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 8421609034, "direction": "Short", "qty": 244, "price": 25.68, "costBasis": 20.52, "prevClose": 25.68},
  {"symbol": "UPWK", "name": "Upwork Inc", "sector": "Technology", "industry": "Staffing & Employment", "marketCap": 1420218546, "direction": "Short", "qty": 370, "price": 11.34, "costBasis": 13.52, "prevClose": 11.34},
  {"symbol": "VRT", "name": "Vertiv Holdings", "sector": "Industrials", "industry": "Electrical Equipment & Parts", "marketCap": 96058879860, "direction": "Long", "qty": 20, "price": 304.53, "costBasis": 251.97, "prevClose": 312.44},
  {"symbol": "WDAY", "name": "Workday Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 32919831144, "direction": "Short", "qty": 34, "price": 119.98, "costBasis": 145.57, "prevClose": 129.16},
  {"symbol": "WPP", "name": "WPP PLC", "sector": "Comm Services", "industry": "Advertising Agencies", "marketCap": 3307478865, "direction": "Short", "qty": 293, "price": 17.78, "costBasis": 17.09, "prevClose": 18.04},
  {"symbol": "WULF", "name": "TeraWulf Inc", "sector": "Technology", "industry": "Capital Markets", "marketCap": 6314372520, "direction": "Long", "qty": 320, "price": 20.38, "costBasis": 15.61, "prevClose": 20.38},
  {"symbol": "CAT", "name": "Caterpillar Inc", "sector": "Industrials", "industry": "Farm & Heavy Construction Machinery", "marketCap": 325433009668, "direction": "Long", "qty": 7, "price": 810.95, "costBasis": 700.72, "prevClose": 810.95},
  {"symbol": "FCG", "name": "First Trust Natural Gas ETF", "sector": "Energy", "industry": "Natural Gas ETF", "marketCap": 606577942, "direction": "Long", "qty": 174, "price": 29.85, "costBasis": 28.78, "prevClose": 29.85},
  {"symbol": "REMX", "name": "VanEck Rare Earth ETF", "sector": "Materials", "industry": "Rare Earth & Strategic Metals ETF", "marketCap": 1119500183, "direction": "Long", "qty": 54, "price": 104.02, "costBasis": 92.91, "prevClose": 104.02},
  {"symbol": "COHR", "name": "Coherent Corp", "sector": "Technology", "industry": "Scientific & Technical Instruments", "marketCap": 38609869731, "direction": "Long", "qty": 20, "price": 349.0, "costBasis": 252.4, "prevClose": 349.0},
  {"symbol": "SPG", "name": "Simon Property Group", "sector": "Real Estate", "industry": "REIT - Retail", "marketCap": 58553332604, "direction": "Short", "qty": 26, "price": 201.7, "costBasis": 194.34, "prevClose": 204.76},
  {"symbol": "HPP", "name": "Hudson Pacific Properties", "sector": "Real Estate", "industry": "REIT - Office", "marketCap": 303755200, "direction": "Short", "qty": 1244, "price": 8.04, "costBasis": 6.39, "prevClose": 8.33},
  {"symbol": "COPX", "name": "Global X Copper Miners ETF", "sector": "Materials", "industry": "Copper Miners ETF", "marketCap": 3232889592, "direction": "Long", "qty": 62, "price": 84.99, "costBasis": 80.22, "prevClose": 84.99},
  {"symbol": "MRVL", "name": "Marvell Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 82953584000, "direction": "Long", "qty": 55, "price": 159.26, "costBasis": 91.54, "prevClose": 159.26},
  {"symbol": "PSFE", "name": "Paysafe Ltd", "sector": "Technology", "industry": "IT Services", "marketCap": 380404570, "direction": "Short", "qty": 666, "price": 9.19, "costBasis": 7.5, "prevClose": 9.19},
  {"symbol": "Z", "name": "Zillow Group Inc", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 9793320952, "direction": "Short", "qty": 113, "price": 45.7, "costBasis": 44.4, "prevClose": 46.17},
  {"symbol": "FN", "name": "Fabrinet", "sector": "Technology", "industry": "Electronic Components", "marketCap": 19775543448, "direction": "Long", "qty": 10, "price": 691.09, "costBasis": 506.94, "prevClose": 695.52},
  {"symbol": "BXP", "name": "BXP Inc", "sector": "Real Estate", "industry": "REIT - Office", "marketCap": 8158289470, "direction": "Short", "qty": 98, "price": 57.79, "costBasis": 51.05, "prevClose": 58.5},
  {"symbol": "EXPI", "name": "eXp World Holdings", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 964689386, "direction": "Short", "qty": 811, "price": 6.5, "costBasis": 6.17, "prevClose": 6.5},
  {"symbol": "NBIS", "name": "Nebius Group", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 24196800000, "direction": "Long", "qty": 53, "price": 156.5, "costBasis": 94.03, "prevClose": 156.55},
  {"symbol": "NVDA", "name": "NVIDIA Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 4071573854798, "direction": "Long", "qty": 27, "price": 202.26, "costBasis": 185.37, "prevClose": 202.26},
  {"symbol": "AMSC", "name": "American Superconductor", "sector": "Technology", "industry": "Power Infrastructure", "marketCap": 1605486250, "direction": "Long", "qty": 163, "price": 51.5, "costBasis": 30.7, "prevClose": 51.5},
  {"symbol": "CIEN", "name": "Ciena Corp", "sector": "Technology", "industry": "Communication Equipment", "marketCap": 56813139769, "direction": "Long", "qty": 14, "price": 495.91, "costBasis": 361.81, "prevClose": 505.93},
  {"symbol": "ADBE", "name": "Adobe Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 95729451005, "direction": "Short", "qty": 21, "price": 250.6, "costBasis": 245.24, "prevClose": 250.6},
  {"symbol": "ARM", "name": "Arm Holdings PLC", "sector": "Technology", "industry": "Semiconductors", "marketCap": 153065853750, "direction": "Long", "qty": 58, "price": 196.7, "costBasis": 136.83, "prevClose": 196.7},
  {"symbol": "BMBL", "name": "Bumble Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 354632607, "direction": "Short", "qty": 1429, "price": 4.41, "costBasis": 3.50, "prevClose": 4.47},
  {"symbol": "AAOI", "name": "Applied Optoelectronics", "sector": "Technology", "industry": "Semiconductors", "marketCap": 3500000000, "direction": "Long", "qty": 43, "price": 147.28, "costBasis": 115.40, "prevClose": 150.57},
  {"symbol": "AEHR", "name": "Aehr Test Systems", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 1500000000, "direction": "Long", "qty": 97, "price": 96.8, "costBasis": 51.29, "prevClose": 96.8},
  {"symbol": "TASK", "name": "TaskUs Inc", "sector": "Technology", "industry": "Information Technology Services", "marketCap": 440000000, "direction": "Short", "qty": 750, "price": 6.87, "costBasis": 6.67, "prevClose": 7.21},
  {"symbol": "TTD", "name": "The Trade Desk Inc", "sector": "Technology", "industry": "Advertising Technology", "marketCap": 10100000000, "direction": "Short", "qty": 242, "price": 23.35, "costBasis": 20.64, "prevClose": 23.35},
  {"symbol": "ACLS", "name": "Axcelis Technologies", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 2661324538, "direction": "Long", "qty": 48, "price": 140.0, "costBasis": 103.86, "prevClose": 140.0},
  {"symbol": "DELL", "name": "Dell Technologies", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 103344870223, "direction": "Long", "qty": 27, "price": 214.3, "costBasis": 184.71, "prevClose": 214.3},
  {"symbol": "GLW", "name": "Corning Inc", "sector": "Technology", "industry": "Electronic Components", "marketCap": 12500000000, "direction": "Long", "qty": 31, "price": 167.81, "costBasis": 159.77, "prevClose": 167.81},
  {"symbol": "STX", "name": "Seagate Technology", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 90430511640, "direction": "Long", "qty": 10, "price": 579.0, "costBasis": 497.05, "prevClose": 579.0},
  {"symbol": "AMKR", "name": "Amkor Technology", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 6800000000, "direction": "Long", "qty": 91, "price": 71.28, "costBasis": 55.01, "prevClose": 71.28},
  {"symbol": "GPN", "name": "Global Payments Inc", "sector": "Financials", "industry": "Specialty Business Services", "marketCap": 15500000000, "direction": "Short", "qty": 78, "price": 72.25, "costBasis": 64.06, "prevClose": 72.25},
  {"symbol": "HUT", "name": "Hut 8 Corp", "sector": "Technology", "industry": "Bitcoin Mining", "marketCap": 7032471710, "direction": "Long", "qty": 77, "price": 79.95, "costBasis": 65.16, "prevClose": 79.95},
  {"symbol": "ONTO", "name": "Onto Innovation Inc", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 12274494673, "direction": "Long", "qty": 19, "price": 298.8, "costBasis": 256.26, "prevClose": 298.8},
  {"symbol": "WDC", "name": "Western Digital Corp", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 114554136507, "direction": "Long", "qty": 15, "price": 391.0, "costBasis": 342.88, "prevClose": 391.0},
  {"symbol": "INTC", "name": "Intel Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 327269422127, "direction": "Long", "qty": 78, "price": 67.32, "costBasis": 64.47, "prevClose": 67.32},
  {"symbol": "APLD", "name": "Applied Digital Corp", "sector": "Technology", "industry": "Data Center Infrastructure", "marketCap": 7887239131, "direction": "Long", "qty": 163, "price": 32.3, "costBasis": 30.61, "prevClose": 32.3},
  {"symbol": "CRDO", "name": "Credo Technology Group Holding Ltd", "sector": "Technology", "industry": "Semiconductors", "marketCap": 24782692630, "direction": "Long", "qty": 32, "price": 188.0, "costBasis": 157.14, "prevClose": 188.0},
  {"symbol": "IREN", "name": "IREN Ltd", "sector": "Technology", "industry": "Bitcoin Mining / AI Compute", "marketCap": 14288868108, "direction": "Long", "qty": 107, "price": 48.05, "costBasis": 46.99, "prevClose": 48.05},
  {"symbol": "SNDK", "name": "SanDisk Corp", "sector": "Technology", "industry": "Data Storage", "marketCap": 140589924679, "direction": "Long", "qty": 6, "price": 977.23, "costBasis": 915.70, "prevClose": 977.23},
  {"symbol": "ALAB", "name": "Astera Labs Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 10500000000, "direction": "Long", "qty": 26, "price": 192.69, "costBasis": 193.86, "prevClose": 192.69},
  {"symbol": "DAVE", "name": "Dave Inc", "sector": "Technology", "industry": "Fintech", "marketCap": 1800000000, "direction": "Long", "qty": 18, "price": 281.0, "costBasis": 285.69, "prevClose": 281.0},
  {"symbol": "SITM", "name": "SiTime Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 2600000000, "direction": "Long", "qty": 10, "price": 520.71, "costBasis": 525.18, "prevClose": 523.57}
];
