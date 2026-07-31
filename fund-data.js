// ============================================
// FUND-DATA.JS — Shared position data
// Single source of truth for all pages
// ============================================

const SHARED_FINNHUB_KEY = 'd6kqa11r01qmopd1net0d6kqa11r01qmopd1netg';

// Bump DATA_VERSION whenever positions, costs, or prices change — invalidates all localStorage caches
const DATA_VERSION = '2026-07-31-1';

// Date when price/prevClose were last set (YYYY-MM-DD in US/Pacific)
// On a new trading day, pages auto-reset price = prevClose so Today P&L starts at $0
const PRICES_AS_OF = '2026-07-31';

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
  {"symbol": "BE", "name": "Bloom Energy Corp", "sector": "Energy", "industry": "Electrical Equipment & Parts", "marketCap": 52590828462, "direction": "Long", "qty": 46, "price": 205.81, "costBasis": 198.6, "prevClose": 207.12},
  {"symbol": "CBRE", "name": "CBRE Group Inc", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 40836203517, "direction": "Short", "qty": 35, "price": 146.81, "costBasis": 141.82, "prevClose": 149.46},
  {"symbol": "CORZ", "name": "Core Scientific Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 7231890221, "direction": "Long", "qty": 309, "price": 20.72, "costBasis": 16.17, "prevClose": 21.81},
  {"symbol": "CRM", "name": "Salesforce Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 134037542999, "direction": "Short", "qty": 26, "price": 184.02, "costBasis": 195.71, "prevClose": 180.71},
  {"symbol": "CRWV", "name": "CoreWeave Inc", "sector": "Technology", "industry": "Cloud Infrastructure", "marketCap": 39215595338, "direction": "Long", "qty": 62, "price": 71.77, "costBasis": 80.17, "prevClose": 73.9},
  {"symbol": "CTSH", "name": "Cognizant Technology", "sector": "Technology", "industry": "IT Services", "marketCap": 21537368060, "direction": "Short", "qty": 77, "price": 55.35, "costBasis": 64.97, "prevClose": 53.895},
  {"symbol": "CWK", "name": "Cushman & Wakefield", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 2980302506, "direction": "Short", "qty": 373, "price": 13.42, "costBasis": 13.38, "prevClose": 13.78},
  {"symbol": "FVRR", "name": "Fiverr International", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 376044591, "direction": "Short", "qty": 463, "price": 8.93, "costBasis": 10.82, "prevClose": 9.18},
  {"symbol": "INTU", "name": "Intuit Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 81057211775, "direction": "Short", "qty": 12, "price": 316.07, "costBasis": 437.9, "prevClose": 315.5},
  {"symbol": "LITE", "name": "Lumentum Holdings", "sector": "Technology", "industry": "Communication Equipment", "marketCap": 59360623569, "direction": "Long", "qty": 8, "price": 713.94, "costBasis": 652.68, "prevClose": 693.24},
  {"symbol": "LZ", "name": "LegalZoom.com Inc", "sector": "Technology", "industry": "Specialty Business Services", "marketCap": 1232430931, "direction": "Short", "qty": 745, "price": 7.87, "costBasis": 6.71, "prevClose": 7.86},
  {"symbol": "MU", "name": "Micron Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 1040114558292, "direction": "Long", "qty": 16, "price": 823.03, "costBasis": 542.41, "prevClose": 874.66},
  {"symbol": "NOW", "name": "ServiceNow Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 102138518738, "direction": "Short", "qty": 44, "price": 111.23, "costBasis": 114.35, "prevClose": 110.07},
  {"symbol": "TSM", "name": "Taiwan Semiconductor", "sector": "Technology", "industry": "Semiconductors", "marketCap": 1694640111089, "direction": "Long", "qty": 14, "price": 404.25, "costBasis": 358.83, "prevClose": 403.31},
  {"symbol": "UPWK", "name": "Upwork Inc", "sector": "Technology", "industry": "Staffing & Employment", "marketCap": 1090665191, "direction": "Short", "qty": 370, "price": 9.16, "costBasis": 13.52, "prevClose": 9.25},
  {"symbol": "VRT", "name": "Vertiv Holdings", "sector": "Industrials", "industry": "Electrical Equipment & Parts", "marketCap": 111529832999, "direction": "Long", "qty": 20, "price": 241.57, "costBasis": 251.97, "prevClose": 227.5},
  {"symbol": "WDAY", "name": "Workday Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 33428979095, "direction": "Short", "qty": 34, "price": 160.34, "costBasis": 145.57, "prevClose": 158.11},
  {"symbol": "WPP", "name": "WPP PLC", "sector": "Comm Services", "industry": "Advertising Agencies", "marketCap": 3070270000, "direction": "Short", "qty": 293, "price": 20.21, "costBasis": 17.09, "prevClose": 20.46},
  {"symbol": "WULF", "name": "TeraWulf Inc", "sector": "Technology", "industry": "Capital Markets", "marketCap": 13879870000, "direction": "Long", "qty": 320, "price": 17.66, "costBasis": 15.61, "prevClose": 17.82},
  {"symbol": "CAT", "name": "Caterpillar Inc", "sector": "Industrials", "industry": "Farm & Heavy Construction Machinery", "marketCap": 409381933276, "direction": "Long", "qty": 7, "price": 814.81, "costBasis": 700.72, "prevClose": 809.14},
  {"symbol": "FCG", "name": "First Trust Natural Gas ETF", "sector": "Energy", "industry": "Natural Gas ETF", "marketCap": 606577942, "direction": "Long", "qty": 174, "price": 29.35, "costBasis": 28.78, "prevClose": 28.8},
  {"symbol": "REMX", "name": "VanEck Rare Earth ETF", "sector": "Materials", "industry": "Rare Earth & Strategic Metals ETF", "marketCap": 1119500183, "direction": "Long", "qty": 54, "price": 65.97, "costBasis": 92.91, "prevClose": 66.45},
  {"symbol": "COHR", "name": "Coherent Corp", "sector": "Technology", "industry": "Scientific & Technical Instruments", "marketCap": 55246592701, "direction": "Long", "qty": 20, "price": 262.89, "costBasis": 252.4, "prevClose": 249.06},
  {"symbol": "COPX", "name": "Global X Copper Miners ETF", "sector": "Materials", "industry": "Copper Miners ETF", "marketCap": 3232889592, "direction": "Long", "qty": 62, "price": 78.86, "costBasis": 80.22, "prevClose": 79.5},
  {"symbol": "MRVL", "name": "Marvell Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 170100107715, "direction": "Long", "qty": 94, "price": 187.56, "costBasis": 118.56, "prevClose": 183.3},
  {"symbol": "PSFE", "name": "Paysafe Ltd", "sector": "Technology", "industry": "IT Services", "marketCap": 407460266, "direction": "Short", "qty": 666, "price": 8.08, "costBasis": 7.5, "prevClose": 8.47},
  {"symbol": "Z", "name": "Zillow Group Inc", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 7621850000, "direction": "Short", "qty": 113, "price": 34.06, "costBasis": 44.4, "prevClose": 33.71},
  {"symbol": "FN", "name": "Fabrinet", "sector": "Technology", "industry": "Electronic Components", "marketCap": 17056389077, "direction": "Long", "qty": 10, "price": 435.41, "costBasis": 506.94, "prevClose": 439.33},
  {"symbol": "EXPI", "name": "eXp World Holdings", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 964689386, "direction": "Short", "qty": 811, "price": 3.9, "costBasis": 6.17, "prevClose": 3.83},
  {"symbol": "NBIS", "name": "Nebius Group", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 47252403645, "direction": "Long", "qty": 71, "price": 190.41, "costBasis": 126.52, "prevClose": 188.43},
  {"symbol": "NVDA", "name": "NVIDIA Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 5005527911376, "direction": "Long", "qty": 27, "price": 200.75, "costBasis": 185.37, "prevClose": 195.04},
  {"symbol": "AMSC", "name": "American Superconductor", "sector": "Technology", "industry": "Power Infrastructure", "marketCap": 1479069631, "direction": "Long", "qty": 163, "price": 29.37, "costBasis": 30.7, "prevClose": 29.45},
  {"symbol": "CIEN", "name": "Ciena Corp", "sector": "Technology", "industry": "Communication Equipment", "marketCap": 55341527409, "direction": "Long", "qty": 14, "price": 377.05, "costBasis": 361.81, "prevClose": 372.07},
  {"symbol": "ADBE", "name": "Adobe Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 89481225242, "direction": "Short", "qty": 21, "price": 250.41, "costBasis": 245.24, "prevClose": 247.9},
  {"symbol": "ARM", "name": "Arm Holdings PLC", "sector": "Technology", "industry": "Semiconductors", "marketCap": 276650650391, "direction": "Long", "qty": 70, "price": 239.69, "costBasis": 173.91, "prevClose": 241.54},
  {"symbol": "BMBL", "name": "Bumble Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 366511620, "direction": "Short", "qty": 1429, "price": 2.85, "costBasis": 3.5, "prevClose": 2.91},
  {"symbol": "AAOI", "name": "Applied Optoelectronics", "sector": "Technology", "industry": "Semiconductors", "marketCap": 8036313271, "direction": "Long", "qty": 43, "price": 94.32, "costBasis": 115.4, "prevClose": 90.11},
  {"symbol": "AEHR", "name": "Aehr Test Systems", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 2478873555, "direction": "Long", "qty": 97, "price": 79.98, "costBasis": 51.29, "prevClose": 76.87},
  {"symbol": "TASK", "name": "TaskUs Inc", "sector": "Technology", "industry": "Information Technology Services", "marketCap": 505511702, "direction": "Short", "qty": 750, "price": 6.07, "costBasis": 6.67, "prevClose": 5.915},
  {"symbol": "TTD", "name": "The Trade Desk Inc", "sector": "Technology", "industry": "Advertising Technology", "marketCap": 8128180292, "direction": "Short", "qty": 242, "price": 18.04, "costBasis": 20.64, "prevClose": 18.28},
  {"symbol": "ACLS", "name": "Axcelis Technologies", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 4121415675, "direction": "Long", "qty": 48, "price": 130.38, "costBasis": 103.86, "prevClose": 125.21},
  {"symbol": "DELL", "name": "Dell Technologies", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 283622956265, "direction": "Long", "qty": 37, "price": 405.37, "costBasis": 244.83, "prevClose": 404.81},
  {"symbol": "GLW", "name": "Corning Inc", "sector": "Technology", "industry": "Electronic Components", "marketCap": 126212530666, "direction": "Long", "qty": 31, "price": 138.25, "costBasis": 159.77, "prevClose": 135.22},
  {"symbol": "STX", "name": "Seagate Technology", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 190973587889, "direction": "Long", "qty": 10, "price": 856.13, "costBasis": 497.05, "prevClose": 851.68},
  {"symbol": "AMKR", "name": "Amkor Technology", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 16101798206, "direction": "Long", "qty": 91, "price": 49.87, "costBasis": 55.01, "prevClose": 48.26},
  {"symbol": "HUT", "name": "Hut 8 Corp", "sector": "Technology", "industry": "Bitcoin Mining", "marketCap": 12384225762, "direction": "Long", "qty": 77, "price": 107.63, "costBasis": 65.16, "prevClose": 108.27},
  {"symbol": "ONTO", "name": "Onto Innovation Inc", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 13561090340, "direction": "Long", "qty": 19, "price": 258.58, "costBasis": 256.26, "prevClose": 250.52},
  {"symbol": "WDC", "name": "Western Digital Corp", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 179165766398, "direction": "Long", "qty": 15, "price": 544.84, "costBasis": 342.88, "prevClose": 533.04},
  {"symbol": "INTC", "name": "Intel Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 464000318466, "direction": "Long", "qty": 78, "price": 90.2, "costBasis": 64.47, "prevClose": 91.13},
  {"symbol": "APLD", "name": "Applied Digital Corp", "sector": "Technology", "industry": "Data Center Infrastructure", "marketCap": 7770073706, "direction": "Long", "qty": 163, "price": 27.39, "costBasis": 30.61, "prevClose": 27.97},
  {"symbol": "CRDO", "name": "Credo Technology Group Holding Ltd", "sector": "Technology", "industry": "Semiconductors", "marketCap": 39747761118, "direction": "Long", "qty": 32, "price": 206.99, "costBasis": 157.14, "prevClose": 201.08},
  {"symbol": "IREN", "name": "IREN Ltd", "sector": "Technology", "industry": "Bitcoin Mining / AI Compute", "marketCap": 13228706857, "direction": "Long", "qty": 107, "price": 36.8, "costBasis": 46.99, "prevClose": 38.26},
  {"symbol": "SNDK", "name": "SanDisk Corp", "sector": "Technology", "industry": "Data Storage", "marketCap": 212739845014, "direction": "Long", "qty": 8, "price": 1214.83, "costBasis": 999.93, "prevClose": 1279.96},
  {"symbol": "ALAB", "name": "Astera Labs Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 49979125930, "direction": "Long", "qty": 35, "price": 311.23, "costBasis": 213.08, "prevClose": 299.69},
  {"symbol": "DAVE", "name": "Dave Inc", "sector": "Technology", "industry": "Fintech", "marketCap": 5121425644, "direction": "Long", "qty": 18, "price": 372.69, "costBasis": 285.69, "prevClose": 377.64},
  {"symbol": "SITM", "name": "SiTime Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 14635985665, "direction": "Long", "qty": 10, "price": 535.2, "costBasis": 525.18, "prevClose": 527.87},
  {"symbol": "WOLF", "name": "Wolfspeed Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 2175260000, "direction": "Long", "qty": 138, "price": 23.62, "costBasis": 36.19, "prevClose": 23.79},
  {"symbol": "ON", "name": "ON Semiconductor Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 33785201673, "direction": "Long", "qty": 47, "price": 81.61, "costBasis": 105.41, "prevClose": 83.74},
  {"symbol": "AMD", "name": "Advanced Micro Devices Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 851091995735, "direction": "Long", "qty": 15, "price": 476.15, "costBasis": 343.96, "prevClose": 485.39},
  {"symbol": "FLEX", "name": "Flex Ltd", "sector": "Technology", "industry": "Electronic Manufacturing Services", "marketCap": 43420827169, "direction": "Long", "qty": 34, "price": 113.75, "costBasis": 146.38, "prevClose": 111.91},
  {"symbol": "KEEL", "name": "Keel Infrastructure", "sector": "Technology", "industry": "AI/HPC Infrastructure", "marketCap": 2572310031, "direction": "Long", "qty": 721, "price": 3.97, "costBasis": 6.94, "prevClose": 4.05, "entryDate": "2026-06-22"},
  {"symbol": "ACN", "name": "Accenture plc", "sector": "Technology", "industry": "IT Services & Consulting", "marketCap": 89949378325, "direction": "Short", "qty": 42, "price": 165.92, "costBasis": 119.76, "prevClose": 163.29, "entryDate": "2026-06-22"},
  {"symbol": "CNXC", "name": "Concentrix Corp", "sector": "Technology", "industry": "IT Services / BPO", "marketCap": 1357658343, "direction": "Short", "qty": 208, "price": 24.6, "costBasis": 23.99, "prevClose": 24.9, "entryDate": "2026-06-22"},
  {"symbol": "WIX", "name": "Wix.com Ltd", "sector": "Technology", "industry": "Website Building / Web SaaS", "marketCap": 1864190000, "direction": "Short", "qty": 112, "price": 55.03, "costBasis": 44.93, "prevClose": 56.68, "entryDate": "2026-06-30"},
  {"symbol": "GLOB", "name": "Globant SA", "sector": "Technology", "industry": "IT Services / Digital Engineering", "marketCap": 1351520007, "direction": "Short", "qty": 175, "price": 36.6, "costBasis": 28.61, "prevClose": 36.39, "entryDate": "2026-06-30"}
];
