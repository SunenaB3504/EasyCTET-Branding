// EasyCTET — Shared site behaviour

// ---- Countdown to exam date ----
// Single editable constant: update this if CBSE reschedules again.
const EXAM_DATE = new Date("2026-12-12T09:30:00+05:30");

function updateCountdown(){
  const el = document.getElementById("countdown");
  if(!el) return;
  const now = new Date();
  let diff = EXAM_DATE - now;
  if(diff < 0) diff = 0;
  const days = Math.floor(diff / (1000*60*60*24));
  const hours = Math.floor((diff / (1000*60*60)) % 24);
  const mins = Math.floor((diff / (1000*60)) % 60);
  const secs = Math.floor((diff / 1000) % 60);
  el.querySelector("[data-d]").textContent = days;
  el.querySelector("[data-h]").textContent = String(hours).padStart(2,"0");
  el.querySelector("[data-m]").textContent = String(mins).padStart(2,"0");
  el.querySelector("[data-s]").textContent = String(secs).padStart(2,"0");
}
setInterval(updateCountdown, 1000);
document.addEventListener("DOMContentLoaded", updateCountdown);

// ---- FAQ accordion ----
document.addEventListener("click", function(e){
  const q = e.target.closest(".faq-q");
  if(!q) return;
  const item = q.closest(".faq-item");
  item.classList.toggle("open");
});

// ---- Pricing phase (driven by pricing.json — edit that file, not this code) ----
// Phases: prelaunch -> launchFree (first N days post-approval) -> earlyBird -> standard
function computePricingPhase(cfg, now){
  const earlyBirdEnd = new Date(cfg.earlyBirdEndDate + "T23:59:59+05:30");
  if(cfg.approvedDate){
    const approved = new Date(cfg.approvedDate + "T00:00:00+05:30");
    const freeEnd = new Date(approved.getTime() + cfg.freeWindowDays*24*60*60*1000);
    if(now < freeEnd) return { phase:"launchFree", freeEnd };
  }
  if(now <= earlyBirdEnd) return { phase:"earlyBird", earlyBirdEnd };
  return { phase:"standard" };
}

function renderPricing(cfg){
  const now = new Date();
  const result = computePricingPhase(cfg, now);
  const amountEl = document.querySelector("[data-pricing-amount]");
  const noteEl = document.querySelector("[data-pricing-note]");
  const faqEl = document.querySelector("[data-faq-pricing]");
  const dateOpts = { day:"numeric", month:"long", year:"numeric", timeZone:"Asia/Kolkata" };

  let amount, note, faqText;
  if(result.phase === "launchFree"){
    const endStr = result.freeEnd.toLocaleDateString("en-IN", dateOpts);
    amount = "FREE";
    note = `Launch week only — free until ${endStr}, yours for life.`;
    faqText = `Yes — for a limited launch window (through ${endStr}) EasyCTET's full Pro Pass is completely free. Download and open the app before then, and you keep full lifetime access at no cost, ever. After the launch window, the full Pro Pass (all 5 Paper 1 subjects, 750+ questions, complete audio library, unlimited mock exams) is a one-time purchase of ₹${cfg.earlyBirdPrice} through ${new Date(cfg.earlyBirdEndDate + "T00:00:00+05:30").toLocaleDateString("en-IN", dateOpts)}, then ₹${cfg.standardPriceP1}. There are no recurring subscriptions.`;
  } else if(result.phase === "earlyBird"){
    const endStr = result.earlyBirdEnd.toLocaleDateString("en-IN", dateOpts);
    amount = `₹${cfg.earlyBirdPrice}`;
    note = `Early-bird price — through ${endStr}. One-time purchase, not a subscription.`;
    faqText = `Yes. You can practice sample questions across all 5 subjects, read introductory study guides, and preview audio masterclasses for free without registering an account. For a limited time — until ${endStr} — the full Pro Pass (all 5 Paper 1 subjects, 750+ questions, complete audio library, unlimited mock exams) is a one-time purchase of ₹${cfg.earlyBirdPrice}. After that, the price moves to ₹${cfg.standardPriceP1}. There are no recurring subscriptions.`;
  } else {
    amount = `₹${cfg.standardPriceP1}`;
    note = "One-time purchase, not a subscription.";
    faqText = `Yes. You can practice sample questions across all 5 subjects, read introductory study guides, and preview audio masterclasses for free without registering an account. The full Pro Pass (all 5 Paper 1 subjects, 750+ questions, complete audio library, unlimited mock exams) is a one-time purchase of ₹${cfg.standardPriceP1}. There are no recurring subscriptions.`;
  }

  if(amountEl) amountEl.textContent = amount;
  if(noteEl) noteEl.textContent = note;
  if(faqEl) faqEl.textContent = faqText;
}

document.addEventListener("DOMContentLoaded", function(){
  fetch("pricing.json")
    .then(function(r){ return r.json(); })
    .then(renderPricing)
    .catch(function(){ /* keep the static HTML defaults if pricing.json can't be loaded */ });
});

// ---- Mobile nav toggle (simple show/hide) ----
document.addEventListener("DOMContentLoaded", function(){
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector("nav.links");
  if(toggle && nav){
    toggle.addEventListener("click", function(){
      nav.style.display = nav.style.display === "flex" ? "none" : "flex";
      nav.style.flexDirection = "column";
      nav.style.position = "absolute";
      nav.style.top = "56px";
      nav.style.right = "20px";
      nav.style.background = "#152136";
      nav.style.border = "1px solid #1C2B45";
      nav.style.borderRadius = "10px";
      nav.style.padding = "14px 20px";
      nav.style.gap = "14px";
    });
  }
});
