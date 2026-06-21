/* ============================================
   MARCY — Magnolia, WA listings (single source of truth)
   --------------------------------------------
   SAMPLE DATA — replace with your real listings, or wire an
   MLS/IDX feed later. Each card's "Show Mortgage" button feeds
   `price` into the mortgage calculator at 20% down.

   Fields: id, address, zip, price (whole $), beds, baths, sqft,
           type, status ('Active' | 'New'), blurb, photo (url|null)
   ============================================ */
const MARCY_LISTINGS = [
  { id: 'mag-001', address: '2820 Magnolia Blvd W', zip: '98199', price: 1495000, beds: 4, baths: 2.5, sqft: 2940, type: 'House', status: 'Active', blurb: 'Bluff-side classic with Puget Sound views', photo: null },
  { id: 'mag-002', address: '3417 33rd Ave W', zip: '98199', price: 989000, beds: 3, baths: 2, sqft: 1820, type: 'House', status: 'New', blurb: 'Updated craftsman near the Village', photo: null },
  { id: 'mag-003', address: '4124 Perkins Ln W', zip: '98199', price: 2295000, beds: 5, baths: 3.5, sqft: 3710, type: 'House', status: 'Active', blurb: 'Waterfront with private beach access', photo: null },
  { id: 'mag-004', address: '2607 Thorndyke Ave W', zip: '98199', price: 849000, beds: 2, baths: 1.5, sqft: 1440, type: 'Townhome', status: 'Active', blurb: 'Low-maintenance townhome, garage parking', photo: null },
  { id: 'mag-005', address: '3232 Viewmont Way W', zip: '98199', price: 1795000, beds: 4, baths: 3, sqft: 3120, type: 'House', status: 'Active', blurb: 'Olympic Mountain views, chef’s kitchen', photo: null },
  { id: 'mag-006', address: '4032 44th Ave W', zip: '98199', price: 1150000, beds: 3, baths: 2, sqft: 2060, type: 'House', status: 'New', blurb: 'Mid-century on a quiet tree-lined street', photo: null }
];
