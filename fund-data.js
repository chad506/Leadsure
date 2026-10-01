// ============================================
// FUND-DATA.JS — Shared position data
// Single source of truth for all pages
// ============================================

const SHARED_FINNHUB_KEY = 'd6kqa11r01qmopd1net0d6kqa11r01qmopd1netg';

// Bump DATA_VERSION whenever positions, costs, or prices change — invalidates all localStorage caches
const DATA_VERSION = '2026-10-01-3';

// Date when price/prevClose were last set (YYYY-MM-DD in US/Pacific)
// On a new trading day, pages auto-reset price = prevClose so Today P&L starts at $0
const PRICES_AS_OF = '2026-10-01';

// Realized P&L from closed positions (CHGG: -$449.07, RIOT: -$1,189.30, U: -$1,336.68, HPP: -$3,496.09, MDB: -$1,301.40, BXP: -$965.15, GPN: -$775.91, AXTI: -$715.96, SPG: -$774.07, DUOL: -$782.97, PL: -$1,712.79, KEEL: -$2,141.57, ACN: -$1,954.75, WOLF: -$1,736.83, GLOB: -$1,380.86, WIX: -$3,709.56, FLEX: -$1,002.41, ON: -$1,382.23, WPP: -$2,817.22, WDAY: -$1,816.46, TASK: -$1,039.00, CWK: -$729.88, NOW: -$669.39, ADBE: -$599.03, FN: -$769.44, GLW: -$457.82, AMKR: -$638.93, IREN: -$748.51, CNXC: -$634.64, CRM: -$981.26, APLD: -$751.55, AMSC: -$440.22, REMX: -$901.62, ARM: +$3,779.27, AAOI: -$661.01, CIEN: -$785.92, ONTO: -$37.72, VRT: -$71.00, WULF: -$179.30, CORZ: +$44.71)
const SHARED_REALIZED_PNL = -38713.54;

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
  {"symbol": "ONTO", "name": "Onto Innovation Inc", "direction": "Long", "qty": 19, "costBasis": 256.26, "exitPrice": 254.27, "realizedPnl": -37.72, "entryDate": "Apr 10", "exitDate": "Sep 4"},
  {"symbol": "VRT", "name": "Vertiv Holdings", "direction": "Long", "qty": 20, "costBasis": 251.97, "exitPrice": 248.42, "realizedPnl": -71.0, "entryDate": "Mar 4", "exitDate": "Oct 1"},
  {"symbol": "WULF", "name": "TeraWulf Inc", "direction": "Long", "qty": 320, "costBasis": 15.61, "exitPrice": 15.04, "realizedPnl": -179.3, "entryDate": "Mar 4", "exitDate": "Oct 1"},
  {"symbol": "CORZ", "name": "Core Scientific Inc", "direction": "Long", "qty": 309, "costBasis": 16.17, "exitPrice": 16.31, "realizedPnl": 44.71, "entryDate": "Mar 4", "exitDate": "Oct 1"}
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
  {"symbol": "MRVL", "name": "Marvell Technology", "direction": "Long", "qty": 14, "costBasis": 299.21, "entryDate": "Jun 30", "note": "Month-end add-on to winner"},
  {"symbol": "SNDK", "name": "SanDisk Corp", "direction": "Long", "qty": 2, "costBasis": 2263.37, "entryDate": "Jun 30", "note": "Month-end add-on to winner"},
  {"symbol": "ALAB", "name": "Astera Labs Inc", "direction": "Long", "qty": 9, "costBasis": 484.56, "entryDate": "Jun 30", "note": "Month-end add-on to winner"},
  {"symbol": "HUT", "name": "Hut 8 Corp", "direction": "Long", "qty": 29, "costBasis": 107.96, "entryDate": "Jul 31", "note": "Month-end add-on to winner"},
  {"symbol": "STX", "name": "Seagate Technology", "direction": "Long", "qty": 4, "costBasis": 856.13, "entryDate": "Jul 31", "note": "Month-end add-on to winner"},
  {"symbol": "WDC", "name": "Western Digital Corp", "direction": "Long", "qty": 6, "costBasis": 544.84, "entryDate": "Jul 31", "note": "Month-end add-on to winner"},
  {"symbol": "DELL", "name": "Dell Technologies", "direction": "Long", "qty": 8, "costBasis": 405.37, "entryDate": "Jul 31", "note": "Month-end add-on to winner"},
  {"symbol": "SNDK", "name": "SanDisk Corp", "direction": "Long", "qty": 6, "costBasis": 1687.49, "entryDate": "Sep 4", "note": "Added to biggest storage winner (+11.9% day)"},
  {"symbol": "MU", "name": "Micron Technology", "direction": "Long", "qty": 14, "costBasis": 1092.82, "entryDate": "Oct 1", "note": "Added to 2x winner (fill +101% vs cost)"},
  {"symbol": "AEHR", "name": "Aehr Test Systems", "direction": "Long", "qty": 53, "costBasis": 102.43, "entryDate": "Oct 1", "note": "Added to 2x winner (fill +100% vs cost)"},
  {"symbol": "DELL", "name": "Dell Technologies", "direction": "Long", "qty": 15, "costBasis": 545.05, "entryDate": "Oct 1", "note": "Added to 2x winner (fill +99% vs cost)"}
];

// Active positions — THE source of truth (37 positions)
const POSITIONS = [
  {"symbol": "BE", "name": "Bloom Energy Corp", "sector": "Energy", "industry": "Electrical Equipment & Parts", "marketCap": 78138107600, "direction": "Long", "qty": 46, "price": 275.04, "costBasis": 198.6037, "prevClose": 276.98},
  {"symbol": "CBRE", "name": "CBRE Group Inc", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 37864869360, "direction": "Short", "qty": 35, "price": 130.59, "costBasis": 141.8249, "prevClose": 128.47},
  {"symbol": "CRWV", "name": "CoreWeave Inc", "sector": "Technology", "industry": "Cloud Infrastructure", "marketCap": 46899911594, "direction": "Long", "qty": 62, "price": 87.84, "costBasis": 80.1685, "prevClose": 87.12},
  {"symbol": "CTSH", "name": "Cognizant Technology", "sector": "Technology", "industry": "IT Services", "marketCap": 25652798799, "direction": "Short", "qty": 77, "price": 61.8, "costBasis": 64.9697, "prevClose": 57.44},
  {"symbol": "FVRR", "name": "Fiverr International", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 306479941, "direction": "Short", "qty": 463, "price": 8.64, "costBasis": 10.8198, "prevClose": 8.62},
  {"symbol": "INTU", "name": "Intuit Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 72017429831, "direction": "Short", "qty": 12, "price": 283.44, "costBasis": 437.9, "prevClose": 275.71},
  {"symbol": "LITE", "name": "Lumentum Holdings", "sector": "Technology", "industry": "Communication Equipment", "marketCap": 79888164853, "direction": "Long", "qty": 8, "price": 1041.0, "costBasis": 652.6788, "prevClose": 971.26},
  {"symbol": "LZ", "name": "LegalZoom.com Inc", "sector": "Technology", "industry": "Specialty Business Services", "marketCap": 930824257, "direction": "Short", "qty": 745, "price": 5.745, "costBasis": 6.71, "prevClose": 5.61},
  {"symbol": "MU", "name": "Micron Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 1191780771655, "direction": "Long", "qty": 30, "price": 1085.55, "costBasis": 799.2807, "prevClose": 1065.11},
  {"symbol": "TSM", "name": "Taiwan Semiconductor", "sector": "Technology", "industry": "Semiconductors", "marketCap": 1694640111089, "direction": "Long", "qty": 14, "price": 458.9, "costBasis": 358.83, "prevClose": 456.19},
  {"symbol": "UPWK", "name": "Upwork Inc", "sector": "Technology", "industry": "Staffing & Employment", "marketCap": 1009106737, "direction": "Short", "qty": 370, "price": 8.355, "costBasis": 13.5248, "prevClose": 8.16},
  {"symbol": "CAT", "name": "Caterpillar Inc", "sector": "Industrials", "industry": "Farm & Heavy Construction Machinery", "marketCap": 377917101966, "direction": "Long", "qty": 7, "price": 823.45, "costBasis": 701.2083, "prevClose": 810.79},
  {"symbol": "FCG", "name": "First Trust Natural Gas ETF", "sector": "Energy", "industry": "Natural Gas ETF", "marketCap": 606577942, "direction": "Long", "qty": 174, "price": 29.07, "costBasis": 28.7799, "prevClose": 28.52},
  {"symbol": "COHR", "name": "Coherent Corp", "sector": "Technology", "industry": "Scientific & Technical Instruments", "marketCap": 54662652030, "direction": "Long", "qty": 20, "price": 317.96, "costBasis": 252.4025, "prevClose": 287.81},
  {"symbol": "COPX", "name": "Global X Copper Miners ETF", "sector": "Materials", "industry": "Copper Miners ETF", "marketCap": 3232889592, "direction": "Long", "qty": 62, "price": 83.26, "costBasis": 80.215, "prevClose": 84.7},
  {"symbol": "MRVL", "name": "Marvell Technology", "sector": "Technology", "industry": "Semiconductors", "marketCap": 222171388114, "direction": "Long", "qty": 94, "price": 267.905, "costBasis": 141.9923, "prevClose": 264.21},
  {"symbol": "PSFE", "name": "Paysafe Ltd", "sector": "Technology", "industry": "IT Services", "marketCap": 321125151, "direction": "Short", "qty": 666, "price": 5.4536, "costBasis": 7.5016, "prevClose": 5.63},
  {"symbol": "Z", "name": "Zillow Group Inc", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 7729430000, "direction": "Short", "qty": 113, "price": 27.726, "costBasis": 44.3999, "prevClose": 27.13},
  {"symbol": "AGNT", "name": "AGNT Inc (fka eXp World)", "sector": "Real Estate", "industry": "Real Estate Services", "marketCap": 594939868, "direction": "Short", "qty": 811, "price": 3.6257, "costBasis": 6.1698, "prevClose": 3.67},
  {"symbol": "NBIS", "name": "Nebius Group", "sector": "Technology", "industry": "Internet Content & Information", "marketCap": 63508100770, "direction": "Long", "qty": 71, "price": 233.58, "costBasis": 126.5225, "prevClose": 235.88},
  {"symbol": "NVDA", "name": "NVIDIA Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 5546374180490, "direction": "Long", "qty": 27, "price": 232.06, "costBasis": 185.3818, "prevClose": 228.38},
  {"symbol": "BMBL", "name": "Bumble Inc", "sector": "Technology", "industry": "Software - Application", "marketCap": 337825724, "direction": "Short", "qty": 1429, "price": 2.565, "costBasis": 3.5003, "prevClose": 2.63},
  {"symbol": "AEHR", "name": "Aehr Test Systems", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 3232641833, "direction": "Long", "qty": 150, "price": 101.25, "costBasis": 69.3595, "prevClose": 99.62},
  {"symbol": "TTD", "name": "The Trade Desk Inc", "sector": "Technology", "industry": "Advertising Technology", "marketCap": 5756037229, "direction": "Short", "qty": 242, "price": 12.185, "costBasis": 20.6395, "prevClose": 12.17},
  {"symbol": "ACLS", "name": "Axcelis Technologies", "sector": "Technology", "industry": "Semiconductor Equipment", "marketCap": 3805989106, "direction": "Long", "qty": 48, "price": 135.885, "costBasis": 103.86, "prevClose": 131.18},
  {"symbol": "DELL", "name": "Dell Technologies", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 345805852375, "direction": "Long", "qty": 60, "price": 540.0504, "costBasis": 341.0883, "prevClose": 537.95},
  {"symbol": "STX", "name": "Seagate Technology", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 209274348646, "direction": "Long", "qty": 14, "price": 933.98, "costBasis": 599.8401, "prevClose": 922.34},
  {"symbol": "HUT", "name": "Hut 8 Corp", "sector": "Technology", "industry": "Bitcoin Mining", "marketCap": 11659729346, "direction": "Long", "qty": 106, "price": 85.7, "costBasis": 76.8658, "prevClose": 86.1},
  {"symbol": "WDC", "name": "Western Digital Corp", "sector": "Technology", "industry": "Computer Hardware", "marketCap": 183729360000, "direction": "Long", "qty": 21, "price": 456.2505, "costBasis": 400.4502, "prevClose": 454.46},
  {"symbol": "INTC", "name": "Intel Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 611655263788, "direction": "Long", "qty": 78, "price": 120.72, "costBasis": 64.47, "prevClose": 120.23},
  {"symbol": "CRDO", "name": "Credo Technology Group Holding Ltd", "sector": "Technology", "industry": "Semiconductors", "marketCap": 36083949484, "direction": "Long", "qty": 32, "price": 207.71, "costBasis": 157.14, "prevClose": 194.79},
  {"symbol": "SNDK", "name": "SanDisk Corp", "sector": "Technology", "industry": "Data Storage", "marketCap": 250525855121, "direction": "Long", "qty": 14, "price": 1782.505, "costBasis": 1438.9893, "prevClose": 1739.89},
  {"symbol": "ALAB", "name": "Astera Labs Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 60471703084, "direction": "Long", "qty": 35, "price": 357.67, "costBasis": 268.6066, "prevClose": 355.97},
  {"symbol": "DAVE", "name": "Dave Inc", "sector": "Technology", "industry": "Fintech", "marketCap": 4088394963, "direction": "Long", "qty": 18, "price": 339.27, "costBasis": 285.685, "prevClose": 321.51},
  {"symbol": "SITM", "name": "SiTime Corp", "sector": "Technology", "industry": "Semiconductors", "marketCap": 19532942320, "direction": "Long", "qty": 10, "price": 683.29, "costBasis": 525.18, "prevClose": 652.03},
  {"symbol": "AMD", "name": "Advanced Micro Devices Inc", "sector": "Technology", "industry": "Semiconductors", "marketCap": 988643177619, "direction": "Long", "qty": 15, "price": 617.425, "costBasis": 343.9633, "prevClose": 611.76},
  {"symbol": "SPCX", "name": "SpaceX (Space Exploration Technologies)", "sector": "Industrials", "industry": "Space Launch & Satellite Internet", "marketCap": 1993657834927, "direction": "Long", "qty": 200, "price": 149.485, "costBasis": 147.77, "prevClose": 150.86, "entryDate": "2026-09-04"},
];
