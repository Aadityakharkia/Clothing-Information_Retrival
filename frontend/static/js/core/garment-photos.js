/**
 * Garment Photos & Product Image Resolver
 * ========================================
 * Provides 1 distinct, high-quality, symmetrical canonical sample photo per garment type
 * for maximum visual harmony and symmetrical layout consistency.
 */

(function() {
  const CANONICAL_CATEGORY_PHOTOS = {
    'Shirt':      'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=500&q=85',
    'T-Shirt':    'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=500&q=85',
    'Jeans':      'https://images.unsplash.com/photo-1542272604-780c96856592?auto=format&fit=crop&w=500&q=85',
    'Kurta':      'https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=500&q=85',
    'Saree':      'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=500&q=85',
    'Dress':      'https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=500&q=85',
    'Hoodie':     'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=500&q=85',
    'Jacket':     'https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=500&q=85',
    'Leggings':   'https://images.unsplash.com/photo-1506629082955-511b1aa562c8?auto=format&fit=crop&w=500&q=85',
    'Sweatshirt': 'https://images.unsplash.com/photo-1578587018452-892bacefd3f2?auto=format&fit=crop&w=500&q=85'
  };

  const DEFAULT_FALLBACK = 'https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?auto=format&fit=crop&w=500&q=85';

  function getGarmentPhotoUrl(category) {
    const cat = (category || '').trim();
    return CANONICAL_CATEGORY_PHOTOS[cat] || DEFAULT_FALLBACK;
  }

  function renderGarmentThumbnail(category, title, extraClass = '') {
    const url = getGarmentPhotoUrl(category);
    const alt = (title || category || 'Garment').replace(/"/g, '&quot;');
    return `
      <div class="garment-thumb-wrap ${extraClass}">
        <img class="garment-thumb-img" 
             src="${url}" 
             alt="${alt}" 
             loading="lazy" 
             onerror="this.onerror=null; this.parentElement.classList.add('fallback-thumb'); this.style.display='none';">
        <div class="garment-fallback-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/>
          </svg>
        </div>
      </div>
    `;
  }

  window.GarmentPhotos = {
    getUrl: getGarmentPhotoUrl,
    renderThumbnail: renderGarmentThumbnail
  };
})();
