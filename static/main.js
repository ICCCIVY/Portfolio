document.addEventListener('scroll', () => {
    const elements = document.querySelectorAll('.fade-in');
    const scrollPosition = window.innerHeight + window.scrollY;
  
    elements.forEach(el => {
      if (el.getBoundingClientRect().top + window.scrollY < scrollPosition - 100) {
        el.classList.add('show');
      }
    });
  });
  