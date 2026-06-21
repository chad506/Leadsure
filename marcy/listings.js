/* ============================================
   MARCY — Magnolia, WA listings (single source of truth)
   --------------------------------------------
   SAMPLE DATA with placeholder (stock) photos. Replace with real
   listings by running scripts/fetch-marcy-listings.js with an API key
   (see that file), or wire an MLS/IDX feed.

   Fields: id, address, zip, price (whole $), beds, baths, sqft,
           type, status ('Active' | 'New'), blurb, photo (url|null)
   ============================================ */
const MARCY_LISTINGS = [
  { id: 'mag-001', address: '2820 Magnolia Blvd W', zip: '98199', price: 1495000, beds: 4, baths: 2.5, sqft: 2940, type: 'House', status: 'Active', blurb: 'Bluff-side classic with Puget Sound views', photo: 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=640&q=70' },
  { id: 'mag-002', address: '3417 33rd Ave W', zip: '98199', price: 989000, beds: 3, baths: 2, sqft: 1820, type: 'House', status: 'New', blurb: 'Updated craftsman near the Village', photo: 'https://images.unsplash.com/photo-1570129477492-45c003edd2be?auto=format&fit=crop&w=640&q=70' },
  { id: 'mag-003', address: '4124 Perkins Ln W', zip: '98199', price: 2295000, beds: 5, baths: 3.5, sqft: 3710, type: 'House', status: 'Active', blurb: 'Waterfront with private beach access', photo: 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=640&q=70' },
  { id: 'mag-004', address: '2607 Thorndyke Ave W', zip: '98199', price: 849000, beds: 2, baths: 1.5, sqft: 1440, type: 'Townhome', status: 'Active', blurb: 'Low-maintenance townhome, garage parking', photo: 'https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?auto=format&fit=crop&w=640&q=70' },
  { id: 'mag-005', address: '3232 Viewmont Way W', zip: '98199', price: 1795000, beds: 4, baths: 3, sqft: 3120, type: 'House', status: 'Active', blurb: 'Olympic Mountain views, chef’s kitchen', photo: 'https://images.unsplash.com/photo-1576941089067-2de3c901e126?auto=format&fit=crop&w=640&q=70' },
  { id: 'mag-006', address: '4032 44th Ave W', zip: '98199', price: 1150000, beds: 3, baths: 2, sqft: 2060, type: 'House', status: 'New', blurb: 'Mid-century on a quiet tree-lined street', photo: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=640&q=70' }
];
