/*
 * Modal
 *
 * Pico.css - https://picocss.com
 * Copyright 2019-2024 - Licensed under MIT
 */

// Config
const isOpenClass = "modal-is-open";
const openingClass = "modal-is-opening";
const closingClass = "modal-is-closing";
const scrollbarWidthCssVar = "--pico-scrollbar-width";
const animationDuration = 400; // ms
let visibleModal = null;

// Toggle modal
const toggleModal = (event) => {
  event.preventDefault();
  const modal = document.getElementById(event.currentTarget.dataset.target);
  if (!modal) return;
  modal && (modal.open ? closeModal(modal) : openModal(modal));
};

// Open modal
const openModal = (modal) => {
  const { documentElement: html } = document;
  const scrollbarWidth = getScrollbarWidth();
  if (scrollbarWidth) {
    html.style.setProperty(scrollbarWidthCssVar, `${scrollbarWidth}px`);
  }
  html.classList.add(isOpenClass, openingClass);
  setTimeout(() => {
    visibleModal = modal;
    html.classList.remove(openingClass);
  }, animationDuration);
  modal.showModal();
};

// Close modal
const closeModal = (modal) => {
  visibleModal = null;
  const { documentElement: html } = document;
  html.classList.add(closingClass);
  setTimeout(() => {
    html.classList.remove(closingClass, isOpenClass);
    html.style.removeProperty(scrollbarWidthCssVar);
    modal.close();
  }, animationDuration);
};

// Close with a click outside
document.addEventListener("click", (event) => {
  if (visibleModal === null) return;
  const modalContent = visibleModal.querySelector("article");
  const isClickInside = modalContent.contains(event.target);
  !isClickInside && closeModal(visibleModal);
});

// Close with Esc key
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && visibleModal) {
    closeModal(visibleModal);
  }
});

// Get scrollbar width
const getScrollbarWidth = () => {
  const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
  return scrollbarWidth;
};

// Is scrollbar visible
const isScrollbarVisible = () => {
  return document.body.scrollHeight > screen.height;
};

// from https://github.com/RWDevelopment/theme_switch?tab=readme-ov-file

let isLight = true
const html = document.documentElement
const switchTheme = document.getElementById('theme_switcher')
const os_default = '<i class="fa fa-lightbulb-o"></i>'
const sun = '<i class="fa fa-sun-o"></i>'
const moon = '<i class="fa fa-moon-o"></i>'

document.addEventListener('DOMContentLoaded', () => {
  switchTheme.innerHTML = os_default
  isLight = !window.matchMedia('(prefers-color-scheme: dark)').matches; 
  html.setAttribute('data-theme', isLight ? "light" : "dark")
  switchTheme.setAttribute('data-tooltip', isLight ? "ludicrous mode" : "hacker mode")
})

switchTheme.addEventListener('click', (e)=> {
  e.preventDefault()
  isLight = !isLight
  html.setAttribute('data-theme', isLight? 'light':'dark')
  switchTheme.innerHTML = isLight? sun : moon
  switchTheme.setAttribute('data-tooltip', isLight ? "ludicrous mode" : "hacker mode")
  removeTooltip()
})

const removeTooltip = (timeInt = 500) => {
  setTimeout(()=>{
    switchTheme.blur()
  },timeInt)
}
