// ============================================
// FUND-DATA.JS — Shared position data
// Single source of truth for all pages
// ============================================

const SHARED_FINNHUB_KEY = 'd6kqa11r01qmopd1net0d6kqa11r01qmopd1netg';

// Bump DATA_VERSION whenever positions, costs, or prices change — invalidates all localStorage caches
const DATA_VERSION = '2026-06-04-1';

// Date when price/prevClose were last set (YYYY-MM-DD in US/Pacific)
// On a new trading day, pages auto-reset price = prevClose so Today P&L starts at $0
const PRICES_AS_OF = '2026-05-30';

// Realized P&L from closed positions (CHGG: -$449.07, RIOT: -$1,189.30, U: -$1,336.68, HPP: -$3,496.09, MDB: -$1,301.40, BXP: -$965.15, GPN: -$775.91, AXTI: -$715.96)
const SHARED_REALIZED_PNL = -10229.56;

// Sold positions
const SOLD_POSITIONS = [
  {"symbol": "CHGG", "name": "Chegg Inc", "direction": "Short", "qty": 7690, "costBasis": 0.65, "exitPrice": 0.71, "realizedPnl": -449.07, "entryDate": "Mar 4", "exitDate": "Mar 31"},
  {"symbol": "RIOT", "name": "Riot Platforms Inc", "direction": "Long", "qty": 303, "costBasis": 16.52, "exitPrice": 12.60, "realizedPnl": -1189.30, "entryDate": "Mar 4", "exitDate": "Mar 31"},
  {"symbol": "U", "name": "Unity Software Inc", "direction": "Short", "qty": 244, "costBasis": 20.52, "exitPrice": 26.00, "realizedPnl": -1336.68, "entryDate": "Mar 4", "exitDate": "Apr 30"},
  {"symbol": "HPP", "name": "Hudson Pacific Properties", "direction": "Short", "qty": 1244, "costBasis": 6.39, "exitPrice": 9.20, "realizedPnl": -3496.09, "entryDate": "Mar 4", "exitDate": "Apr 30"},
  {"symbol": "MDB", "name": "MongoDB Inc", "direction": "Short", "qty": 20, "costBasis": 250.37, "exitPrice": 312.08, "realizedPnl": -1301.40, "entryDate": "Mar 4", "exitDate": "May 29"},
  {"symbol": "BXP", "name": "BXP Inc", "direction": "Short", "qty": 98, "costBasis": 51.05, "exitPrice": 60.93, "realizedPnl": -965.15, "entryDate": "Mar 11", "exitDate": "May 29"},
  {"symbol": "GPN", "name": "Global Payments Inc", "direction": "Short", "qty": 78, "costBasis": 64.06, "exitPrice": 75.14, "realizedPnl": -775.91, "entryDate": "Apr 9", "exitDate": "May 29"},
  {"symbol": "AXTI", "name": "AXT Inc", "direction": "Long", "qty": 41, "costBasis": 120.85, "exitPrice": 102.93, "realizedPnl": -715.96, "entryDate": "May 13", "exitDate": "May 29"}
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
  {"symbol": "DELL", "name": "Dell Technologies", "direction": "Long", "qty": 10, "costBasis": 317.05, "entryDate": "May 29", "note": "Added to May long winner"}
];

// Active positions — THE source of truth (63 positions)
const POSITIONS = [
  {"symbol": "BE", "name": "Bloom Energy Corp", "sector": "Energy", "industry": "Electrical Equipment & Parts", "marketCap": 77798245119, "direction": "Long", "qty": 46, "price": 285.02, "costBasis": 198.60, "prevClose": 290.01},
  {"symbol": "CBRE", "name": "CBRE Group Inc", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 36496659964, "direction": "Short", "qty": 35, "price": 125.06, "costBasis": 141.82, "prevClose": 126.42},
  {"symbol": "CORZ", "name": "Core Scientific Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 9075624999, "direction": "Long", "qty": 309, "price": 26.86, "costBasis": 16.17, "prevClose": 27.76},
  {"symbol": "CRM", "name": "Salesforce Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 171662405482, "direction": "Short", "qty": 26, "price": 191.12, "costBasis": 195.71, "prevClose": 176.17},
  {"symbol": "CRWV", "name": "CoreWeave Inc", "sector": "Technology", "industry": "Cloud Infrastructure", "marketCap": 68098090464, "direction": "Long", "qty": 62, "price": 109.55, "costBasis": 80.17, "prevClose": 106.86},
  {"symbol": "CTSH", "name": "Cognizant Technology", "sector": "Technology", "industry": "IT Services", "marketCap": 27086379784, "direction": "Short", "qty": 77, "price": 55.78, "costBasis": 64.97, "prevClose": 53.85},
  {"symbol": "CWK", "name": "Cushman & Wakefield", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 2938128253, "direction": "Short", "qty": 373, "price": 12.45, "costBasis": 13.38, "prevClose": 12.76},
  {"symbol": "DUOL", "name": "Duolingo Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 5496590417, "direction": "Short", "qty": 50, "price": 111.38, "costBasis": 99.7, "prevClose": 108.67},
  {"symbol": "FVRR", "name": "Fiverr International", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 411635799, "direction": "Short", "qty": 463, "price": 11, "costBasis": 10.82, "prevClose": 11},
  {"symbol": "INTU", "name": "Intuit Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 96766444272, "direction": "Short", "qty": 12, "price": 331.55, "costBasis": 437.9, "prevClose": 313},
  {"symbol": "LITE", "name": "Lumentum Holdings", "sector": "Technology", "industry": "Communication Equipment", "marketCap": 70409004571, "direction": "Long", "qty": 8, "price": 854.98, "costBasis": 652.68, "prevClose": 860.62},
  {"symbol": "LZ", "name": "LegalZoom.com Inc", "sector": "Technology", "industry": "Specialty Business Services", "marketCap": 1146607070, "direction": "Short", "qty": 745, "price": 6.3, "costBasis": 6.71, "prevClose": 6.29},  {"symbol": "MU", "name": "Micron Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 1167768566100, "direction": "Long", "qty": 16, "price": 971.02, "costBasis": 542.41, "prevClose": 923.52},
  {"symbol": "NOW", "name": "ServiceNow Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 140113505718, "direction": "Short", "qty": 44, "price": 124.39, "costBasis": 114.35, "prevClose": 108.73},
  {"symbol": "TSM", "name": "Taiwan Semiconductor", "sector": "Technology", "industry": "Semiconductors", "marketCap": 1694640111089, "direction": "Long", "qty": 14, "price": 418.47, "costBasis": 358.83, "prevClose": 424.86},
  {"symbol": "UPWK", "name": "Upwork Inc", "sector": "Technology", "industry": "Staffing & Employment", "marketCap": 1089430000, "direction": "Short", "qty": 370, "price": 8.83, "costBasis": 13.52, "prevClose": 8.59},
  {"symbol": "VRT", "name": "Vertiv Holdings", "sector": "Industrials", "industry": "Electrical Equipment & Parts", "marketCap": 121266990000, "direction": "Long", "qty": 20, "price": 315.73, "costBasis": 251.97, "prevClose": 314.18},
  {"symbol": "WDAY", "name": "Workday Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 36108930000, "direction": "Short", "qty": 34, "price": 146.21, "costBasis": 145.57, "prevClose": 130.01},
  {"symbol": "WPP", "name": "WPP PLC", "sector": "Comm Services", "industry": "Advertising Agencies", "marketCap": 3035390000, "direction": "Short", "qty": 293, "price": 18.61, "costBasis": 17.09, "prevClose": 18.78},
  {"symbol": "WULF", "name": "TeraWulf Inc", "sector": "Technology", "industry": "Capital Markets", "marketCap": 12665810000, "direction": "Long", "qty": 320, "price": 25.57, "costBasis": 15.61, "prevClose": 26.395},
  {"symbol": "CAT", "name": "Caterpillar Inc", "sector": "Industrials", "industry": "Farm & Heavy Construction Machinery", "marketCap": 398616852802, "direction": "Long", "qty": 7, "price": 875.89, "costBasis": 700.72, "prevClose": 887.67},
  {"symbol": "FCG", "name": "First Trust Natural Gas ETF", "sector": "Energy", "industry": "Natural Gas ETF", "marketCap": 606577942, "direction": "Long", "qty": 174, "price": 28.53, "costBasis": 28.78, "prevClose": 28.8},
  {"symbol": "REMX", "name": "VanEck Rare Earth ETF", "sector": "Materials", "industry": "Rare Earth & Strategic Metals ETF", "marketCap": 1119500183, "direction": "Long", "qty": 54, "price": 99.65, "costBasis": 92.91, "prevClose": 101.5},
  {"symbol": "COHR", "name": "Coherent Corp", "sector": "Technology", "industry": "Scientific & Technical Instruments", "marketCap": 70997512371, "direction": "Long", "qty": 20, "price": 361.49, "costBasis": 252.4, "prevClose": 376.95},
  {"symbol": "SPG", "name": "Simon Property Group", "sector": "Real Estate", "industry": "REIT - Retail", "marketCap": 65731946639, "direction": "Short", "qty": 26, "price": 204.93, "costBasis": 194.34, "prevClose": 206.77},
  {"symbol": "COPX", "name": "Global X Copper Miners ETF", "sector": "Materials", "industry": "Copper Miners ETF", "marketCap": 3232889592, "direction": "Long", "qty": 62, "price": 88.16, "costBasis": 80.22, "prevClose": 88.44},
  {"symbol": "MRVL", "name": "Marvell Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 191957361321, "direction": "Long", "qty": 80, "price": 205.02, "costBasis": 114.46, "prevClose": 204.83},
  {"symbol": "PSFE", "name": "Paysafe Ltd", "sector": "Technology", "industry": "IT Services", "marketCap": 413610903, "direction": "Short", "qty": 666, "price": 7.74, "costBasis": 7.5, "prevClose": 7.65},
  {"symbol": "Z", "name": "Zillow Group Inc", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 8025550000, "direction": "Short", "qty": 113, "price": 35.01, "costBasis": 44.4, "prevClose": 35.44},
  {"symbol": "FN", "name": "Fabrinet", "sector": "Technology", "industry": "Electronic Components", "marketCap": 22298995209, "direction": "Long", "qty": 10, "price": 654.18, "costBasis": 506.94, "prevClose": 667.95},  {"symbol": "EXPI", "name": "eXp World Holdings", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 964689386, "direction": "Short", "qty": 811, "price": 4.92, "costBasis": 6.17, "prevClose": 4.88},
  {"symbol": "NBIS", "name": "Nebius Group", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 66564056056, "direction": "Long", "qty": 71, "price": 231.11, "costBasis": 126.52, "prevClose": 226.34},
  {"symbol": "NVDA", "name": "NVIDIA Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 5429511984304, "direction": "Long", "qty": 27, "price": 211.16, "costBasis": 185.37, "prevClose": 214.25},
  {"symbol": "AMSC", "name": "American Superconductor", "sector": "Technology", "industry": "Power Infrastructure", "marketCap": 2439570875, "direction": "Long", "qty": 163, "price": 50.96, "costBasis": 30.7, "prevClose": 51.33},
  {"symbol": "CIEN", "name": "Ciena Corp", "sector": "Technology", "industry": "Communication Equipment", "marketCap": 80541952581, "direction": "Long", "qty": 14, "price": 580.25, "costBasis": 361.81, "prevClose": 570.18},
  {"symbol": "ADBE", "name": "Adobe Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 110762925693, "direction": "Short", "qty": 21, "price": 259.23, "costBasis": 245.24, "prevClose": 241.44},
  {"symbol": "ARM", "name": "Arm Holdings PLC", "sector": "Technology", "industry": "Semiconductors", "marketCap": 375900569092, "direction": "Long", "qty": 70, "price": 353.31, "costBasis": 173.91, "prevClose": 335.27},
  {"symbol": "BMBL", "name": "Bumble Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 419988424, "direction": "Short", "qty": 1429, "price": 3.18, "costBasis": 3.50, "prevClose": 3.26},
  {"symbol": "AAOI", "name": "Applied Optoelectronics", "sector": "Technology", "industry": "Semiconductors", "marketCap": 14898674955, "direction": "Long", "qty": 43, "price": 158.43, "costBasis": 115.40, "prevClose": 169.02},
  {"symbol": "AEHR", "name": "Aehr Test Systems", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 2944653763, "direction": "Long", "qty": 97, "price": 92.35, "costBasis": 51.29, "prevClose": 99.99},
  {"symbol": "TASK", "name": "TaskUs Inc", "sector": "Technology", "industry": "Information Technology Services", "marketCap": 579690044, "direction": "Short", "qty": 750, "price": 6.34, "costBasis": 6.67, "prevClose": 6.31},
  {"symbol": "TTD", "name": "The Trade Desk Inc", "sector": "Technology", "industry": "Advertising Technology", "marketCap": 10915924331, "direction": "Short", "qty": 242, "price": 21.57, "costBasis": 20.64, "prevClose": 21.15},
  {"symbol": "ACLS", "name": "Axcelis Technologies", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 4622992786, "direction": "Long", "qty": 48, "price": 150.43, "costBasis": 103.86, "prevClose": 155.55},
  {"symbol": "DELL", "name": "Dell Technologies", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 304003720655, "direction": "Long", "qty": 37, "price": 420.93, "costBasis": 244.83, "prevClose": 317.05},
  {"symbol": "GLW", "name": "Corning Inc", "sector": "Technology", "industry": "Electronic Components", "marketCap": 152074705405, "direction": "Long", "qty": 31, "price": 181.18, "costBasis": 159.77, "prevClose": 182.97},
  {"symbol": "STX", "name": "Seagate Technology", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 206573195215, "direction": "Long", "qty": 10, "price": 879.82, "costBasis": 497.05, "prevClose": 880.72},
  {"symbol": "AMKR", "name": "Amkor Technology", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 18032760750, "direction": "Long", "qty": 91, "price": 69.58, "costBasis": 55.01, "prevClose": 70.58},  {"symbol": "HUT", "name": "Hut 8 Corp", "sector": "Technology", "industry": "Bitcoin Mining", "marketCap": 14905208312, "direction": "Long", "qty": 77, "price": 124.85, "costBasis": 65.16, "prevClose": 124.24},
  {"symbol": "ONTO", "name": "Onto Innovation Inc", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 12719926424, "direction": "Long", "qty": 19, "price": 258.26, "costBasis": 256.26, "prevClose": 258.81},
  {"symbol": "WDC", "name": "Western Digital Corp", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 183098590000, "direction": "Long", "qty": 15, "price": 531.23, "costBasis": 342.88, "prevClose": 531.18},
  {"symbol": "INTC", "name": "Intel Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 549492581462, "direction": "Long", "qty": 78, "price": 114.7, "costBasis": 64.47, "prevClose": 120.89},
  {"symbol": "APLD", "name": "Applied Digital Corp", "sector": "Technology", "industry": "Data Center Infrastructure", "marketCap": 13699790974, "direction": "Long", "qty": 163, "price": 47.29, "costBasis": 30.61, "prevClose": 49.65},
  {"symbol": "CRDO", "name": "Credo Technology Group Holding Ltd", "sector": "Technology", "industry": "Semiconductors", "marketCap": 41704130293, "direction": "Long", "qty": 32, "price": 236.05, "costBasis": 157.14, "prevClose": 222.35},
  {"symbol": "IREN", "name": "IREN Ltd", "sector": "Technology", "industry": "Bitcoin Mining / AI Compute", "marketCap": 23313499825, "direction": "Long", "qty": 107, "price": 63.56, "costBasis": 46.99, "prevClose": 64.05},
  {"symbol": "SNDK", "name": "SanDisk Corp", "sector": "Technology", "industry": "Data Storage", "marketCap": 260849756084, "direction": "Long", "qty": 6, "price": 1695, "costBasis": 915.70, "prevClose": 1641.64},
  {"symbol": "ALAB", "name": "Astera Labs Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 54865969684, "direction": "Long", "qty": 26, "price": 342.87, "costBasis": 193.86, "prevClose": 349.17},
  {"symbol": "DAVE", "name": "Dave Inc", "sector": "Technology", "industry": "Fintech", "marketCap": 3592537489, "direction": "Long", "qty": 18, "price": 282.58, "costBasis": 285.69, "prevClose": 268.82},
  {"symbol": "SITM", "name": "SiTime Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 17554135968, "direction": "Long", "qty": 10, "price": 710.22, "costBasis": 525.18, "prevClose": 729.51},
  {"symbol": "WOLF", "name": "Wolfspeed Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 2865540000, "direction": "Long", "qty": 138, "price": 59.3, "costBasis": 36.19, "prevClose": 65.05},
  {"symbol": "ON", "name": "ON Semiconductor Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 47388935810, "direction": "Long", "qty": 47, "price": 120.64, "costBasis": 105.41, "prevClose": 123.77},
  {"symbol": "AMD", "name": "Advanced Micro Devices Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 831818237555, "direction": "Long", "qty": 15, "price": 516.12, "costBasis": 343.96, "prevClose": 518.09},  {"symbol": "FLEX", "name": "Flex Ltd", "sector": "Technology", "industry": "Electronic Manufacturing Services", "marketCap": 54227596933, "direction": "Long", "qty": 34, "price": 150.8, "costBasis": 146.38, "prevClose": 144.85},
  {"symbol": "PL", "name": "Planet Labs PBC", "sector": "Technology", "industry": "Satellite Earth Observation / Space Data Infrastructure", "marketCap": 16082082738, "direction": "Long", "qty": 99, "price": 51.16, "costBasis": 50.50, "prevClose": 51.4, "entryDate": "2026-05-26"}
];
