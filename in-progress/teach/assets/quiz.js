/**
 * Quiz Widget — Reusable, declarative, accessible.
 *
 * Usage in HTML:
 * <div class="quiz"
 *      data-quiz='[
 *        {
 *          "question": "Question text?",
 *          "options": ["A", "B", "C", "D"],
 *          "correct": 1,
 *          "explanation": "Why B is correct.",
 *          "misconceptions": ["Picking A means X is confused with Y.", null, "Picking C means ...", "Picking D means ..."]
 *        }
 *      ]'>
 * </div>
 *
 * `misconceptions` (optional) is a parallel array to `options`: entry i
 * names the misconception that choosing option i exposes. On a wrong
 * answer, the feedback shows the diagnosis for the chosen option, so the
 * wrong pick teaches what to fix instead of just "incorrect". Use null for
 * options that carry no specific diagnosis.
 *
 * Include in <head> or end of <body>:
 *   <script src="../assets/quiz.js" defer></script>
 *
 * The script auto-discovers all .quiz elements on DOMContentLoaded.
 * Generates radio buttons + labels for keyboard accessibility and ARIA semantics.
 */

(function () {
  "use strict";

  function initQuiz(container) {
    var questions;
    try {
      questions = JSON.parse(container.dataset.quiz);
    } catch (e) {
      console.error("Quiz: invalid JSON in data-quiz", e);
      return;
    }

    var answered = new Array(questions.length).fill(false);
    var score = 0;

    // Intro
    var intro = document.createElement("p");
    intro.className = "quiz-intro";
    intro.textContent =
      "选择你认为正确的答案，提交后立即查看结果。共 " +
      questions.length +
      " 题。";
    container.appendChild(intro);

    questions.forEach(function (q, qi) {
      var qDiv = document.createElement("div");
      qDiv.className = "quiz-question";

      // Question text
      var qText = document.createElement("p");
      qText.className = "quiz-question-text";
      qText.textContent = (qi + 1) + ". " + q.question;
      qDiv.appendChild(qText);

      // Options as radio buttons
      var groupName = "quiz-q" + qi + "-" + Math.random().toString(36).slice(2, 8);

      q.options.forEach(function (opt, oi) {
        var label = document.createElement("label");
        label.className = "quiz-option";

        var input = document.createElement("input");
        input.type = "radio";
        input.name = groupName;
        input.value = String(oi);
        // Hide the radio circle — styling via .quiz-option
        input.style.marginRight = "0.5rem";
        input.style.verticalAlign = "middle";

        // Click handler
        input.addEventListener("change", function () {
          handleAnswer(qi, oi, q, qDiv, groupName);
        });

        label.appendChild(input);
        label.appendChild(document.createTextNode(String.fromCharCode(65 + oi) + ") " + opt));
        qDiv.appendChild(label);
      });

      // Feedback
      var feedback = document.createElement("div");
      feedback.className = "quiz-feedback";
      qDiv.appendChild(feedback);

      container.appendChild(qDiv);
    });

    // Score display
    var scoreDiv = document.createElement("div");
    scoreDiv.className = "quiz-score";
    container.appendChild(scoreDiv);

    function handleAnswer(qi, oi, q, qDiv, groupName) {
      if (answered[qi]) return;
      answered[qi] = true;

      var inputs = qDiv.querySelectorAll('input[type="radio"]');
      var isCorrect = oi === q.correct;
      var diagnosis =
        !isCorrect && q.misconceptions && q.misconceptions[oi]
          ? " 你的选择暴露的误解：" + q.misconceptions[oi] + "。"
          : "";

      inputs.forEach(function (input, idx) {
        input.disabled = true;
        var label = input.parentElement;

        if (idx === q.correct) {
          label.classList.add("correct");
        }
        if (idx === oi && !isCorrect) {
          label.classList.add("wrong");
        }
        label.classList.add("disabled");
      });

      if (isCorrect) score++;

      var feedback = qDiv.querySelector(".quiz-feedback");
      feedback.classList.add("visible");
      if (isCorrect) {
        feedback.classList.add("correct");
        feedback.textContent = "✓ 正确。" + (q.explanation || "");
      } else {
        feedback.classList.add("wrong");
        feedback.textContent =
          "✗ 不对。正确答案是 " +
          String.fromCharCode(65 + q.correct) +
          "。" +
          (q.explanation || "") +
          diagnosis;
      }

      // Update score if all answered
      if (answered.every(Boolean)) {
        scoreDiv.classList.add("visible");
        scoreDiv.textContent =
          "得分：" + score + " / " + questions.length;
        scoreDiv.classList.add(score === questions.length ? "pass" : "fail");
      }
    }
  }

  // Auto-init on DOMContentLoaded
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      document.querySelectorAll(".quiz").forEach(initQuiz);
    });
  } else {
    document.querySelectorAll(".quiz").forEach(initQuiz);
  }
})();
