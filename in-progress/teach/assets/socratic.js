/**
 * Socratic Recall Widget — free-recall question with hint and reference answer.
 *
 * The retrieval-practice stage before the quiz: the learner answers from
 * memory first (effortful retrieval builds storage strength), may open a
 * hint that points to source clues, then checks the reference answer —
 * which must resolve the question, not pose another one.
 *
 * Usage in HTML:
 * <div class="socratic"
 *      data-socratic='[
 *        {
 *          "question": "Why does X happen?",
 *          "hint": "Recall the token-count part of the attention cost.",
 *          "answer": "Because attention scores grow with the square of sequence length..."
 *        }
 *      ]'>
 * </div>
 *
 * Include in <head> or end of <body>:
 *   <script src="../assets/socratic.js" defer></script>
 *
 * The script auto-discovers all .socratic elements on DOMContentLoaded.
 * Reveal is one-way: once hint/answer is shown it stays visible.
 */

(function () {
  "use strict";

  function initSocratic(container) {
    var items;
    try {
      items = JSON.parse(container.dataset.socratic);
    } catch (e) {
      console.error("Socratic: invalid JSON in data-socratic", e);
      return;
    }

    var intro = document.createElement("p");
    intro.className = "socratic-intro";
    intro.textContent =
      "先不看提示，从记忆里作答（口头或写下要点），再展开参考答案核对。共 " +
      items.length +
      " 题。";
    container.appendChild(intro);

    items.forEach(function (item, ii) {
      var itDiv = document.createElement("div");
      itDiv.className = "socratic-item";

      var qText = document.createElement("p");
      qText.className = "socratic-question";
      qText.textContent = (ii + 1) + ". " + item.question;
      itDiv.appendChild(qText);

      var controls = document.createElement("div");
      controls.className = "socratic-controls";
      itDiv.appendChild(controls);

      // Hint (optional) — revealed once, then stays
      if (item.hint) {
        var hintDiv = document.createElement("div");
        hintDiv.className = "socratic-hint";
        hintDiv.id = "socratic-hint-" + ii + "-" + Math.random().toString(36).slice(2, 8);
        hintDiv.textContent = item.hint;
        itDiv.appendChild(hintDiv);

        var hintBtn = document.createElement("button");
        hintBtn.type = "button";
        hintBtn.className = "socratic-btn";
        hintBtn.textContent = "提示 Hint";
        hintBtn.setAttribute("aria-expanded", "false");
        hintBtn.setAttribute("aria-controls", hintDiv.id);
        hintBtn.addEventListener("click", function () {
          hintDiv.classList.add("visible");
          hintBtn.setAttribute("aria-expanded", "true");
          hintBtn.remove();
        });
        controls.appendChild(hintBtn);
      }

      // Reference answer — must resolve the question outright
      var ansDiv = document.createElement("div");
      ansDiv.className = "socratic-answer";
      ansDiv.id = "socratic-answer-" + ii + "-" + Math.random().toString(36).slice(2, 8);
      ansDiv.textContent = item.answer;
      itDiv.appendChild(ansDiv);

      var ansBtn = document.createElement("button");
      ansBtn.type = "button";
      ansBtn.className = "socratic-btn";
      ansBtn.textContent = "参考答案 Answer";
      ansBtn.setAttribute("aria-expanded", "false");
      ansBtn.setAttribute("aria-controls", ansDiv.id);
      ansBtn.addEventListener("click", function () {
        ansDiv.classList.add("visible");
        ansBtn.setAttribute("aria-expanded", "true");
        ansBtn.remove();
      });
      controls.appendChild(ansBtn);

      container.appendChild(itDiv);
    });
  }

  // Auto-init on DOMContentLoaded
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      document.querySelectorAll(".socratic").forEach(initSocratic);
    });
  } else {
    document.querySelectorAll(".socratic").forEach(initSocratic);
  }
})();
