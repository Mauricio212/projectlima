// Modal Site Feature Audit Script
// Run this in your Modal site's browser console or as a Node.js script

const auditResults = {
  timestamp: new Date().toISOString(),
  components: [],
  pages: [],
  apiEndpoints: [],
  cssClasses: [],
  jsFiles: [],
  features: []
};

// Audit DOM structure
function auditDOMStructure() {
  console.log("=== MODAL SITE FEATURE AUDIT ===");
  
  // Find main containers
  const containers = document.querySelectorAll('[class*="container"], [class*="dashboard"], [class*="grid"], [class*="trading"]');
  console.log(`Found ${containers.length} main containers:`);
  
  containers.forEach((container, index) => {
    const classNames = container.className;
    const id = container.id;
    const children = container.children.length;
    
    console.log(`${index + 1}. Container: ${classNames} (ID: ${id}, Children: ${children})`);
    auditResults.components.push({
      type: 'container',
      className: classNames,
      id: id,
      childrenCount: children
    });
  });
}

// Audit interactive elements
function auditInteractiveElements() {
  console.log("\n=== INTERACTIVE ELEMENTS ===");
  
  // Buttons
  const buttons = document.querySelectorAll('button');
  console.log(`Found ${buttons.length} buttons:`);
  buttons.forEach((btn, index) => {
    console.log(`${index + 1}. Button: "${btn.textContent.trim()}" (Class: ${btn.className})`);
  });
  
  // Forms
  const forms = document.querySelectorAll('form');
  console.log(`\nFound ${forms.length} forms:`);
  forms.forEach((form, index) => {
    const inputs = form.querySelectorAll('input, select, textarea');
    console.log(`${index + 1}. Form with ${inputs.length} inputs (Class: ${form.className})`);
  });
  
  // Charts/Graphics
  const charts = document.querySelectorAll('[class*="chart"], [class*="graph"], canvas, svg');
  console.log(`\nFound ${charts.length} charts/graphics:`);
  charts.forEach((chart, index) => {
    console.log(`${index + 1}. Chart: ${chart.tagName} (Class: ${chart.className})`);
  });
}

// Audit current page structure
function auditPageStructure() {
  console.log("\n=== PAGE STRUCTURE ===");
  console.log(`Current URL: ${window.location.href}`);
  console.log(`Page Title: ${document.title}`);
  
  // Find navigation elements
  const navElements = document.querySelectorAll('nav, [class*="nav"], [class*="menu"]');
  console.log(`\nFound ${navElements.length} navigation elements:`);
  navElements.forEach((nav, index) => {
    const links = nav.querySelectorAll('a');
    console.log(`${index + 1}. Navigation with ${links.length} links (Class: ${nav.className})`);
  });
}

// Run audit
auditDOMStructure();
auditInteractiveElements();
auditPageStructure();

console.log("\n=== AUDIT COMPLETE ===");
console.log("Copy the above output and save it for feature extraction planning.");

