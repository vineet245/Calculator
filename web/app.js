"use strict";
const form = document.querySelector("#calculator-form");
const first = document.querySelector("#first");
const second = document.querySelector("#second");
const result = document.querySelector("#result");
const expression = document.querySelector("#expression");
const error = document.querySelector("#error");
const submit = document.querySelector("#calculate");
let pending = null;

function clearResult() {
  if (pending) pending.abort();
  pending = null;
  submit.disabled = false;
  error.hidden = true;
  result.textContent = "—";
  expression.textContent = "गणना करने के बाद उत्तर यहाँ दिखेगा";
}

form.addEventListener("input", () => {
  clearResult();
  document.querySelector("#operation-symbol").textContent = form.elements.operation.value === "add" ? "+" : "−";
});

form.addEventListener("reset", () => {
  clearResult();
  document.querySelector("#operation-symbol").textContent = "+";
  first.focus();
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearResult();
  const a = first.value.trim();
  const b = second.value.trim();
  // Input syntax only; arithmetic and authoritative validation stay in Python.
  const numberPattern = /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/;
  if (!numberPattern.test(a) || !numberPattern.test(b)) {
    error.textContent = "कृपया सही संख्या डालें, जैसे 12, -5 या 0.75।";
    error.hidden = false;
    return;
  }
  const controller = new AbortController();
  pending = controller;
  const timeout = setTimeout(() => controller.abort(), 15000);
  submit.disabled = true;
  expression.textContent = "गणना हो रही है…";
  try {
    const response = await fetch("/api/calculate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({first: a, second: b, operation: form.elements.operation.value}),
      signal: controller.signal,
    });
    if (!response.ok) {
      throw new Error(response.status === 422
        ? "हर संख्या में अधिकतम 30 अंक और दशमलव के बाद 12 अंक रखें।"
        : "अभी गणना नहीं हो सकी। फिर से कोशिश करें।");
    }
    const data = await response.json();
    if (pending !== controller) return;
    result.textContent = data.result;
    expression.textContent = `${data.expression} =`;
  } catch (failure) {
    if (pending !== controller) return;
    expression.textContent = "गणना पूरी नहीं हुई";
    error.textContent = failure.name === "AbortError" || failure instanceof TypeError
      ? "सर्वर से संपर्क नहीं हो सका। फिर से कोशिश करें।"
      : failure.message;
    error.hidden = false;
  } finally {
    clearTimeout(timeout);
    if (pending === controller) {
      pending = null;
      submit.disabled = false;
    }
  }
});
