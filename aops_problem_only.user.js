// ==UserScript==
// @name         AoPS AMC Problem Only
// @namespace    https://github.com/czw831024/AMC
// @version      1.1.0
// @description  Hide solutions on AMC problem pages until requested.
// @match        https://artofproblemsolving.com/wiki/*
// @run-at       document-idle
// @grant        none
// ==/UserScript==

(() => {
  'use strict';

  const url = new URL(window.location.href);
  const pageName = url.searchParams.get('title') || decodeURIComponent(url.pathname);
  if (!/AMC_[^/]*_Problems\/Problem_\d+/.test(pageName)) return;

  const article = document.querySelector('#mw-content-text .mw-parser-output');
  if (!article) return;

  const headings = [...article.querySelectorAll('h2')];
  const problemHeadingIndex = headings.findIndex(
    (heading) => heading.textContent.trim() === 'Problem'
  );
  const solutionsHeading = headings[problemHeadingIndex + 1];
  if (problemHeadingIndex < 0 || !solutionsHeading) return;

  const hiddenElements = [];
  for (let element = solutionsHeading; element; element = element.nextElementSibling) {
    hiddenElements.push(element);
  }
  const contents = article.querySelector(':scope > #toc, :scope > .toc');
  if (contents) contents.hidden = true;
  for (const element of hiddenElements) element.hidden = true;

  const button = document.createElement('button');
  button.type = 'button';
  button.textContent = 'Show Solutions';
  button.setAttribute('aria-expanded', 'false');
  Object.assign(button.style, {
    display: 'block',
    margin: '24px 0',
    padding: '10px 18px',
    border: '1px solid #1675a9',
    borderRadius: '6px',
    background: '#1675a9',
    color: '#fff',
    font: '600 16px system-ui, sans-serif',
    cursor: 'pointer'
  });

  button.addEventListener('click', () => {
    if (contents) contents.hidden = false;
    for (const element of hiddenElements) element.hidden = false;
    button.remove();
  });

  solutionsHeading.parentElement.insertBefore(button, solutionsHeading);
})();
