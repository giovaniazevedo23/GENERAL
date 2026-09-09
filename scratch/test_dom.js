const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = `
<html><body>
<button class="theme-btn" data-theme="default">
  <div class="theme-ring"></div>
</button>
<button class="theme-btn" data-theme="superhero">
  <div class="theme-ring"></div>
</button>
</body></html>
`;

const dom = new JSDOM(html);
const document = dom.window.document;

function setTheme(themeId) {
    document.querySelectorAll('.theme-btn').forEach(btn => {
      let ringDiv = btn.querySelector('.theme-ring');
      if (ringDiv) {
        if (btn.dataset.theme === themeId || (themeId === 'default' && btn.dataset.theme === 'default')) {
          ringDiv.classList.add('ring-4', 'ring-blue-500', 'ring-offset-2', 'ring-offset-slate-900');
        } else {
          ringDiv.classList.remove('ring-4', 'ring-blue-500', 'ring-offset-2', 'ring-offset-slate-900');
        }
      }
    });
}

setTheme('default');
console.log("After default:");
console.log("Default classes:", document.querySelector('[data-theme="default"] .theme-ring').className);
console.log("Superhero classes:", document.querySelector('[data-theme="superhero"] .theme-ring').className);

setTheme('superhero');
console.log("After superhero:");
console.log("Default classes:", document.querySelector('[data-theme="default"] .theme-ring').className);
console.log("Superhero classes:", document.querySelector('[data-theme="superhero"] .theme-ring').className);
