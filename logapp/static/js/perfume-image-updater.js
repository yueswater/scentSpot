// Perfume Image Updater
// File: static/js/perfume-image-updater.js

(function() {
  'use strict';

  // Get default image path from data attribute
  let defaultImage = '';

  /**
   * Decode HTML entities and Unicode escapes
   */
  function decodeHTML(text) {
    const textarea = document.createElement('textarea');
    textarea.innerHTML = text;
    return textarea.value;
  }

  /**
   * Update perfume image and info when selection changes
   */
  function updatePerfumeImage() {
    const select = document.getElementById('perfume-select');
    const selectedOption = select.options[select.selectedIndex];
    const imageElement = document.getElementById('perfume-image');
    const imagePlaceholder = document.getElementById('image-placeholder');
    const titleElement = document.getElementById('perfume-title');
    const subtitleElement = document.getElementById('perfume-subtitle');

    if (selectedOption.value) {
      const perfumeImage = selectedOption.getAttribute('data-image');
      // Decode HTML entities to fix Unicode issues like \u0027
      const perfumeBrand = decodeHTML(selectedOption.getAttribute('data-brand'));
      const perfumeName = decodeHTML(selectedOption.getAttribute('data-name'));
      const perfumeCapacity = selectedOption.getAttribute('data-capacity');
      
      console.log('Selected perfume:', {
        image: perfumeImage,
        brand: perfumeBrand,
        name: perfumeName,
        capacity: perfumeCapacity
      });
      
      // Update image
      if (perfumeImage && perfumeImage !== 'None' && perfumeImage !== '') {
        imageElement.style.display = 'block';
        imagePlaceholder.style.display = 'none';
        imageElement.src = perfumeImage;
        imageElement.alt = perfumeBrand + ' - ' + perfumeName;
      } else {
        // If no image, show placeholder with gradient
        imageElement.style.display = 'block';
        imagePlaceholder.style.display = 'none';
        imageElement.src = 'https://placehold.co/400x400/e0e7ff/4f46e5?text=' + encodeURIComponent(perfumeBrand.charAt(0));
        imageElement.alt = perfumeBrand;
      }
      
      // Update title and subtitle with decoded text
      titleElement.textContent = perfumeBrand;
      subtitleElement.textContent = perfumeName + ' (' + perfumeCapacity + ' ml)';
    } else {
      // Reset to default
      console.log('Resetting to default image');
      imageElement.style.display = 'block';
      imagePlaceholder.style.display = 'none';
      imageElement.src = defaultImage;
      imageElement.alt = 'Mascot';
      titleElement.textContent = 'Our Mascot';
      subtitleElement.textContent = 'Select a perfume to see its image';
    }
  }

  /**
   * Initialize the perfume image updater
   */
  function init() {
    // Get default image from data attribute
    const container = document.getElementById('perfume-image-container');
    if (container) {
      defaultImage = container.getAttribute('data-default-image');
      console.log('Default image path:', defaultImage);
    }

    const imageElement = document.getElementById('perfume-image');
    if (!imageElement) {
      console.error('Perfume image element not found');
      return;
    }

    // Check if default image loads
    imageElement.addEventListener('load', function() {
      console.log('Image loaded successfully:', this.src);
      this.style.display = 'block';
      const placeholder = document.getElementById('image-placeholder');
      if (placeholder) {
        placeholder.style.display = 'none';
      }
    });
    
    imageElement.addEventListener('error', function() {
      console.error('Image failed to load:', this.src);
      this.style.display = 'none';
      const placeholder = document.getElementById('image-placeholder');
      if (placeholder) {
        placeholder.style.display = 'flex';
      }
    });
    
    // Bind change event to select
    const select = document.getElementById('perfume-select');
    if (select) {
      select.addEventListener('change', updatePerfumeImage);
      
      // Auto-select first perfume if only one exists
      const options = select.querySelectorAll('option[value!=""]');
      if (options.length === 1) {
        select.value = options[0].value;
        updatePerfumeImage();
      }
    } else {
      console.error('Perfume select element not found');
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose updatePerfumeImage to global scope for inline event handlers
  window.updatePerfumeImage = updatePerfumeImage;

})();