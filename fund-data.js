// ============================================
// FUND-DATA.JS — Shared position data
// Single source of truth for all pages
// ============================================

const SHARED_FINNHUB_KEY = 'd6kqa11r01qmopd1net0d6kqa11r01qmopd1netg';

// Bump DATA_VERSION whenever positions, costs, or prices change — invalidates all localStorage caches
const DATA_VERSION = '2026-09-04-1';

// Date when price/prevClose were last set (YYYY-MM-DD in US/Pacific)
// On a new trading day, pages auto-reset price = prevClose so Today P&L starts at $0
const PRICES_AS_OF = '2026-09-04';

// Realized P&L from closed positions (CHGG: -$449.07, RIOT: -$1,189.30, U: -$1,336.68, HPP: -$3,496.09, MDB: -$1,301.40, BXP: -$965.15, GPN: -$775.91, AXTI: -$715.96, SPG: -$774.07, DUOL: -$782.97, PL: -$1,712.79, KEEL: -$2,141.57, ACN: -$1,954.75, WOLF: -$1,736.83, GLOB: -$1,380.86, WIX: -$3,709.56, FLEX: -$1,002.41, ON: -$1,382.23, WPP: -$2,817.22, WDAY: -$1,816.46, TASK: -$1,039.00, CWK: -$729.88, NOW: -$669.39, ADBE: -$599.03, FN: -$769.44, GLW: -$457.82, AMKR: -$638.93, IREN: -$748.51, CNXC: -$634.64, CRM: -$981.26, APLD: -$751.55, AMSC: -$440.22, REMX: -$901.62, ARM: +$3,779.27, AAOI: -$661.01, CIEN: -$785.92, ONTO: -$37.72)
const SHARED_REALIZED_PNL = -38507.95;

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
  {"symbol": "PL", "name": "Planet Labs PBC", "direction": "Long", "qty": 99, "costBasis": 50.5, "exitPrice": 33.2, "realizedPnl": -1712.79, "entryDate": "May 26", "exitDate": "Jun 30"},
  {"symbol": "KEEL", "name": "Keel Infrastructure", "direction": "Long", "qty": 721, "costBasis": 6.94, "exitPrice": 3.97, "realizedPnl": -2141.57, "entryDate": "Jun 22", "exitDate": "Jul 31"},
  {"symbol": "ACN", "name": "Accenture plc", "direction": "Short", "qty": 42, "costBasis": 119.76, "exitPrice": 166.3, "realizedPnl": -1954.75, "entryDate": "Jun 22", "exitDate": "Jul 31"},
  {"symbol": "WOLF", "name": "Wolfspeed Inc", "direction": "Long", "qty": 138, "costBasis": 36.19, "exitPrice": 23.61, "realizedPnl": -1736.83, "entryDate": "May 6", "exitDate": "Jul 31"},
  {"symbol": "GLOB", "name": "Globant SA", "direction": "Short", "qty": 175, "costBasis": 28.61, "exitPrice": 36.5, "realizedPnl": -1380.86, "entryDate": "Jun 30", "exitDate": "Jul 31"},
  {"symbol": "WIX", "name": "Wix.com Ltd", "direction": "Short", "qty": 112, "costBasis": 44.93, "exitPrice": 78.05, "realizedPnl": -3709.56, "entryDate": "Jun 30", "exitDate": "Aug 18"},
  {"symbol": "FLEX", "name": "Flex Ltd", "direction": "Long", "qty": 34, "costBasis": 146.38, "exitPrice": 116.9, "realizedPnl": -1002.41, "entryDate": "May 13", "exitDate": "Aug 19"},
  {"symbol": "ON", "name": "ON Semiconductor Corp", "direction": "Long", "qty": 47, "costBasis": 105.41, "exitPrice": 76.0, "realizedPnl": -1382.23, "entryDate": "May 6", "exitDate": "Aug 20"},
  {"symbol": "WPP", "name": "WPP PLC", "direction": "Short", "qty": 293, "costBasis": 17.09, "exitPrice": 26.71, "realizedPnl": -2817.22, "entryDate": "Mar 4", "exitDate": "Aug 20"},
  {"symbol": "WDAY", "name": "Workday Inc", "direction": "Short", "qty": 34, "costBasis": 145.57, "exitPrice": 199.0, "realizedPnl": -1816.46, "entryDate": "Mar 4", "exitDate": "Aug 20"},
  {"symbol": "TASK", "name": "TaskUs Inc", "direction": "Short", "qty": 750, "costBasis": 6.67, "exitPrice": 8.06, "realizedPnl": -1039.0, "entryDate": "Apr 7", "exitDate": "Aug 20"},
  {"symbol": "CWK", "name": "Cushman & Wakefield", "direction": "Short", "qty": 373, "costBasis": 13.38, "exitPrice": 15.34, "realizedPnl": -729.88, "entryDate": "Mar 4", "exitDate": "Aug 20"},
  {"symbol": "NOW", "name": "ServiceNow Inc", "direction": "Short", "qty": 44, "costBasis": 114.35, "exitPrice": 128.68, "realizedPnl": -669.39, "entryDate": "Mar 4", "exitDate": "Aug 20"},
  {"symbol": "ADBE", "name": "Adobe Inc", "direction": "Short", "qty": 21, "costBasis": 245.24, "exitPrice": 273.77, "realizedPnl": -599.03, "entryDate": "Mar 18", "exitDate": "Aug 20"},
  {"symbol": "FN", "name": "Fabrinet", "direction": "Long", "qty": 10, "costBasis": 506.94, "exitPrice": 430.0, "realizedPnl": -769.44, "entryDate": "Mar 11", "exitDate": "Aug 21"},
  {"symbol": "GLW", "name": "Corning Inc", "direction": "Long", "qty": 31, "costBasis": 159.77, "exitPrice": 145.0, "realizedPnl": -457.82, "entryDate": "Apr 8", "exitDate": "Aug 24"},
  {"symbol": "AMKR", "name": "Amkor Technology", "direction": "Long", "qty": 91, "costBasis": 55.01, "exitPrice": 47.99, "realizedPnl": -638.93, "entryDate": "Apr 9", "exitDate": "Aug 24"},
  {"symbol": "IREN", "name": "IREN Ltd", "direction": "Long", "qty": 107, "costBasis": 46.99, "exitPrice": 40.0, "realizedPnl": -748.51, "entryDate": "Apr 14", "exitDate": "Aug 24"},
  {"symbol": "CNXC", "name": "Concentrix Corp", "direction": "Short", "qty": 208, "costBasis": 23.99, "exitPrice": 27.04, "realizedPnl": -634.64, "entryDate": "Jun 22", "exitDate": "Sep 4"},
  {"symbol": "CRM", "name": "Salesforce Inc", "direction": "Short", "qty": 26, "costBasis": 195.71, "exitPrice": 233.45, "realizedPnl": -981.26, "entryDate": "Mar 4", "exitDate": "Sep 4"},
  {"symbol": "APLD", "name": "Applied Digital Corp", "direction": "Long", "qty": 163, "costBasis": 30.61, "exitPrice": 26.0, "realizedPnl": -751.55, "entryDate": "Apr 14", "exitDate": "Sep 4"},
  {"symbol": "AMSC", "name": "American Superconductor", "direction": "Long", "qty": 163, "costBasis": 30.7, "exitPrice": 28.0, "realizedPnl": -440.22, "entryDate": "Mar 18", "exitDate": "Sep 4"},
  {"symbol": "REMX", "name": "VanEck Rare Earth ETF", "direction": "Long", "qty": 54, "costBasis": 92.91, "exitPrice": 76.21, "realizedPnl": -901.62, "entryDate": "Mar 11", "exitDate": "Sep 4"},
  {"symbol": "ARM", "name": "Arm Holdings PLC", "direction": "Long", "qty": 70, "costBasis": 173.91, "exitPrice": 227.9, "realizedPnl": 3779.27, "entryDate": "Mar 4", "exitDate": "Sep 4"},
  {"symbol": "AAOI", "name": "Applied Optoelectronics", "direction": "Long", "qty": 43, "costBasis": 115.4, "exitPrice": 100.03, "realizedPnl": -661.01, "entryDate": "Apr 7", "exitDate": "Sep 4"},
  {"symbol": "CIEN", "name": "Ciena Corp", "direction": "Long", "qty": 14, "costBasis": 361.81, "exitPrice": 305.67, "realizedPnl": -785.92, "entryDate": "Mar 18", "exitDate": "Sep 4"},
  {"symbol": "ONTO", "name": "Onto Innovation Inc", "direction": "Long", "qty": 19, "costBasis": 256.26, "exitPrice": 254.27, "realizedPnl": -37.72, "entryDate": "Apr 10", "exitDate": "Sep 4"}
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
  {"symbol": "ALAB", "name": "Astera Labs Inc", "direction": "Long", "qty": 9, "costBasis": 268.61, "entryDate": "Jun 30", "note": "Month-end add-on to winner"},
  {"symbol": "HUT", "name": "Hut 8 Corp", "direction": "Long", "qty": 29, "costBasis": 107.63, "entryDate": "Jul 31", "note": "Month-end add-on to winner"},
  {"symbol": "STX", "name": "Seagate Technology", "direction": "Long", "qty": 4, "costBasis": 856.13, "entryDate": "Jul 31", "note": "Month-end add-on to winner"},
  {"symbol": "WDC", "name": "Western Digital Corp", "direction": "Long", "qty": 6, "costBasis": 544.84, "entryDate": "Jul 31", "note": "Month-end add-on to winner"},
  {"symbol": "DELL", "name": "Dell Technologies", "direction": "Long", "qty": 8, "costBasis": 405.37, "entryDate": "Jul 31", "note": "Month-end add-on to winner"},
  {"symbol": "SNDK", "name": "SanDisk Corp", "direction": "Long", "qty": 6, "costBasis": 1687.49, "entryDate": "Sep 4", "note": "Added to biggest storage winner (+11.9% day)"}
];

// Active positions — THE source of truth (40 positions)
const POSITIONS = [
  {"symbol": "BE", "name": "Bloom Energy Corp", "sector": "Energy", "industry": "Electrical Equipment & Parts", "marketCap": 68134483418, "direction": "Long", "qty": 46, "price": 252.87, "costBasis": 198.6, "prevClose": 235.55},
  {"symbol": "CBRE", "name": "CBRE Group Inc", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 44219598663, "direction": "Short", "qty": 35, "price": 147.85, "costBasis": 141.82, "prevClose": 148.74},
  {"symbol": "CORZ", "name": "Core Scientific Inc", "sector": "Technology", "industry": "Software - Infrastructure", "marketCap": 6476616462, "direction": "Long", "qty": 309, "price": 17.89, "costBasis": 16.17, "prevClose": 17.9},
  {"symbol": "CRWV", "name": "CoreWeave Inc", "sector": "Technology", "industry": "Cloud Infrastructure", "marketCap": 57171253900, "direction": "Long", "qty": 62, "price": 89.36, "costBasis": 80.17, "prevClose": 84.56},
  {"symbol": "CTSH", "name": "Cognizant Technology", "sector": "Technology", "industry": "IT Services", "marketCap": 26540173491, "direction": "Short", "qty": 77, "price": 62.31, "costBasis": 64.97, "prevClose": 64.64},
  {"symbol": "FVRR", "name": "Fiverr International", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 323987955, "direction": "Short", "qty": 463, "price": 9.25, "costBasis": 10.82, "prevClose": 9.2},
  {"symbol": "INTU", "name": "Intuit Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 94781936046, "direction": "Short", "qty": 12, "price": 332.7, "costBasis": 437.9, "prevClose": 344.3},
  {"symbol": "LITE", "name": "Lumentum Holdings", "sector": "Technology", "industry": "Communication Equipment", "marketCap": 71417296402, "direction": "Long", "qty": 8, "price": 881.255, "costBasis": 652.68, "prevClose": 847.37},
  {"symbol": "LZ", "name": "LegalZoom.com Inc", "sector": "Technology", "industry": "Specialty Business Services", "marketCap": 971071540, "direction": "Short", "qty": 745, "price": 6.13, "costBasis": 6.71, "prevClose": 6.4},
  {"symbol": "MU", "name": "Micron Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 1093828498426, "direction": "Long", "qty": 16, "price": 1016.59, "costBasis": 542.41, "prevClose": 958.16},
  {"symbol": "TSM", "name": "Taiwan Semiconductor", "sector": "Technology", "industry": "Semiconductors", "marketCap": 1694640111089, "direction": "Long", "qty": 14, "price": 428.91, "costBasis": 358.83, "prevClose": 417.01},
  {"symbol": "UPWK", "name": "Upwork Inc", "sector": "Technology", "industry": "Staffing & Employment", "marketCap": 1050437290, "direction": "Short", "qty": 370, "price": 8.79, "costBasis": 13.52, "prevClose": 9.19},
  {"symbol": "VRT", "name": "Vertiv Holdings", "sector": "Industrials", "industry": "Electrical Equipment & Parts", "marketCap": 93001599805, "direction": "Long", "qty": 20, "price": 280.53, "costBasis": 251.97, "prevClose": 268.83},
  {"symbol": "WULF", "name": "TeraWulf Inc", "sector": "Technology", "industry": "Capital Markets", "marketCap": 8830390000, "direction": "Long", "qty": 320, "price": 16.51, "costBasis": 15.61, "prevClose": 16.23},
  {"symbol": "CAT", "name": "Caterpillar Inc", "sector": "Industrials", "industry": "Farm & Heavy Construction Machinery", "marketCap": 394152799102, "direction": "Long", "qty": 7, "price": 813.94, "costBasis": 700.72, "prevClose": 800.14},
  {"symbol": "FCG", "name": "First Trust Natural Gas ETF", "sector": "Energy", "industry": "Natural Gas ETF", "marketCap": 606577942, "direction": "Long", "qty": 174, "price": 31.43, "costBasis": 28.78, "prevClose": 31.75},
  {"symbol": "COHR", "name": "Coherent Corp", "sector": "Technology", "industry": "Scientific & Technical Instruments", "marketCap": 63541699475, "direction": "Long", "qty": 20, "price": 281.86, "costBasis": 252.4, "prevClose": 264.41},
  {"symbol": "COPX", "name": "Global X Copper Miners ETF", "sector": "Materials", "industry": "Copper Miners ETF", "marketCap": 3232889592, "direction": "Long", "qty": 62, "price": 90.66, "costBasis": 80.22, "prevClose": 91.25},
  {"symbol": "MRVL", "name": "Marvell Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 193430522467, "direction": "Long", "qty": 94, "price": 223.55, "costBasis": 118.56, "prevClose": 208.83},
  {"symbol": "PSFE", "name": "Paysafe Ltd", "sector": "Technology", "industry": "IT Services", "marketCap": 340575280, "direction": "Short", "qty": 666, "price": 6.71, "costBasis": 7.5, "prevClose": 6.79},
  {"symbol": "Z", "name": "Zillow Group Inc", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 7729430000, "direction": "Short", "qty": 113, "price": 34.59, "costBasis": 44.4, "prevClose": 35.34},
  {"symbol": "AGNT", "name": "AGNT Inc (fka eXp World)", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 964689386, "direction": "Short", "qty": 811, "price": 4.03, "costBasis": 6.17, "prevClose": 4.04},
  {"symbol": "NBIS", "name": "Nebius Group", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 68745867916, "direction": "Long", "qty": 71, "price": 226.39, "costBasis": 126.52, "prevClose": 210.63},
  {"symbol": "NVDA", "name": "NVIDIA Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 5446936073780, "direction": "Long", "qty": 27, "price": 230.36, "costBasis": 185.37, "prevClose": 228.45},
  {"symbol": "BMBL", "name": "Bumble Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 355654637, "direction": "Short", "qty": 1429, "price": 2.9, "costBasis": 3.5, "prevClose": 2.87},
  {"symbol": "AEHR", "name": "Aehr Test Systems", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 4341781877, "direction": "Long", "qty": 97, "price": 86.26, "costBasis": 51.29, "prevClose": 76.27},
  {"symbol": "TTD", "name": "The Trade Desk Inc", "sector": "Technology", "industry": "Advertising Technology", "marketCap": 6637063326, "direction": "Short", "qty": 242, "price": 14.43, "costBasis": 20.64, "prevClose": 15.09},
  {"symbol": "ACLS", "name": "Axcelis Technologies", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 4313217503, "direction": "Long", "qty": 48, "price": 115.08, "costBasis": 103.86, "prevClose": 110.37},
  {"symbol": "DELL", "name": "Dell Technologies", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 317845718797, "direction": "Long", "qty": 45, "price": 524.14, "costBasis": 273.37, "prevClose": 516.39},
  {"symbol": "STX", "name": "Seagate Technology", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 219874643133, "direction": "Long", "qty": 14, "price": 849.28, "costBasis": 599.64, "prevClose": 798.61},
  {"symbol": "HUT", "name": "Hut 8 Corp", "sector": "Technology", "industry": "Bitcoin Mining", "marketCap": 10623733162, "direction": "Long", "qty": 106, "price": 93.545, "costBasis": 76.78, "prevClose": 88.09},
  {"symbol": "WDC", "name": "Western Digital Corp", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 183729360000, "direction": "Long", "qty": 21, "price": 467.46, "costBasis": 400.58, "prevClose": 441.57},
  {"symbol": "INTC", "name": "Intel Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 518119667902, "direction": "Long", "qty": 78, "price": 95.8, "costBasis": 64.47, "prevClose": 91.67},
  {"symbol": "CRDO", "name": "Credo Technology Group Holding Ltd", "sector": "Technology", "industry": "Semiconductors", "marketCap": 48428306258, "direction": "Long", "qty": 32, "price": 170.57, "costBasis": 157.14, "prevClose": 164.17},
  {"symbol": "SNDK", "name": "SanDisk Corp", "sector": "Technology", "industry": "Data Storage", "marketCap": 239000592508, "direction": "Long", "qty": 14, "price": 1740, "costBasis": 1294.6, "prevClose": 1554.99},
  {"symbol": "ALAB", "name": "Astera Labs Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 55718211740, "direction": "Long", "qty": 35, "price": 310.4, "costBasis": 213.08, "prevClose": 282.82},
  {"symbol": "DAVE", "name": "Dave Inc", "sector": "Technology", "industry": "Fintech", "marketCap": 4316463213, "direction": "Long", "qty": 18, "price": 380.69, "costBasis": 285.69, "prevClose": 390.86},
  {"symbol": "SITM", "name": "SiTime Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 21379002379, "direction": "Long", "qty": 10, "price": 612.09, "costBasis": 525.18, "prevClose": 574.465},
  {"symbol": "AMD", "name": "Advanced Micro Devices Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 831011403123, "direction": "Long", "qty": 15, "price": 477.57, "costBasis": 343.96, "prevClose": 456.16},
  {"symbol": "SPCX", "name": "SpaceX (Space Exploration Technologies)", "sector": "Industrials", "industry": "Space Launch & Satellite Internet", "marketCap": 2026907127240, "direction": "Long", "qty": 200, "price": 147.95, "costBasis": 147.77, "prevClose": 147.77, "entryDate": "2026-09-04"},
];
