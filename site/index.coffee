grid = document.querySelector '.grid'
masonry = new Masonry grid,
  itemSelector: '.grid-item'
  columnWidth: 320
imagesLoaded(grid).on 'progress', => masonry.layout()
