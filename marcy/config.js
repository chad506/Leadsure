/* ============================================
   MARCY runtime config
   --------------------------------------------
   googleMapsKey: a Google Maps API key with the **Street View Static API**
   enabled. When set, each listing card shows a Google Street View photo of
   the home, built from its address. Leave '' to fall back to the `photo`
   field in listings.js (or the house-icon placeholder).

   IMPORTANT: this key is visible in the page source, so restrict it by
   HTTP referrer (leadsure.com/*) and to the Street View Static API only
   in the Google Cloud console. Street View Static has a monthly free tier.
   ============================================ */
const MARCY_CONFIG = {
  googleMapsKey: 'AIzaSyBixdEbTKyGFEiqtd3YzwRDYNVFRJ6ck04'
};
