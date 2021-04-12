nav = document.querySelector '.nav'

window.addEventListener 'scroll', () =>
  check = window.scrollY > nav.offsetHeight + 150
  nav.classList[if check then 'add' else 'remove'] 'active'
