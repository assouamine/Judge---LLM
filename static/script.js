// Main JavaScript for LLM-as-a-Judge Interface
// Neo-Brutalist Design Edition

document.addEventListener('DOMContentLoaded', function () {
    // ========================================
    // MAIN FUNCTIONALITY
    // ========================================
    const questionInput = document.getElementById('questionInput');
    const evaluateBtn = document.getElementById('evaluateBtn');
    const loadingState = document.getElementById('loadingState');
    const resultsSection = document.getElementById('resultsSection');
    const copyJsonBtn = document.getElementById('copyJsonBtn');

    // Evaluate button click handler
    evaluateBtn.addEventListener('click', async function () {
        const question = questionInput.value.trim();

        if (!question) {
            alert('Please enter a question!');
            return;
        }

        // Show loading, hide results
        loadingState.classList.remove('hidden');
        resultsSection.classList.add('hidden');
        evaluateBtn.disabled = true;

        try {
            const response = await fetch('/evaluate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question })
            });

            if (!response.ok) {
                throw new Error('Evaluation failed');
            }

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            alert('Error: ' + error.message);
            console.error('Error:', error);
            loadingState.classList.add('hidden');
        } finally {
            evaluateBtn.disabled = false;
        }
    });

    // Copy JSON button
    copyJsonBtn.addEventListener('click', function () {
        const jsonText = document.getElementById('jsonOutput').textContent;
        navigator.clipboard.writeText(jsonText).then(function () {
            const originalText = copyJsonBtn.innerHTML;
            copyJsonBtn.innerHTML = 'COPIED';
            setTimeout(function () {
                copyJsonBtn.innerHTML = originalText;
            }, 2000);
        });
    });

    // Allow Enter key to submit (Ctrl+Enter for newline)
    questionInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey) {
            e.preventDefault();
            evaluateBtn.click();
        }
    });

    function displayResults(data) {
        // Stop loading
        loadingState.classList.add('hidden');
        
        // Show results section
        resultsSection.classList.remove('hidden');

        // Scroll to results
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);

        // Display answers
        document.getElementById('nonRagAnswer').textContent = data.answers.non_rag;
        document.getElementById('ragAnswer').textContent = data.answers.rag;
        document.getElementById('docsCount').textContent = data.answers.docs_used;

        // Display evaluation scores
        const evaluation = data.evaluation.evaluation || [];
        const tableBody = document.getElementById('scoresTableBody');
        tableBody.innerHTML = '';

        evaluation.forEach(item => {
            const row = document.createElement('tr');
            
            // Highlight winner row style if needed (or just keep it simple)
            const isWinner = item.model === data.evaluation.final_winner;
            row.style.fontWeight = isWinner ? 'bold' : 'normal';

            row.innerHTML = `
                <td style="border-right: 2px solid #000;">${item.model}</td>
                <td class="score-cell">${item.scores.accuracy || '-'}</td>
                <td class="score-cell">${item.scores.completeness || '-'}</td>
                <td class="score-cell">${item.scores.relevance || '-'}</td>
                <td class="score-cell">${item.scores.clarity || '-'}</td>
                <td class="score-cell">${item.scores.grounding || 'N/A'}</td>
                <td class="score-cell" style="background: #000; color: #fff;">${item.average_score.toFixed(1)}</td>
            `;

            tableBody.appendChild(row);

            // Store justification
            if (item.model === 'Non-RAG') {
                document.getElementById('nonRagJustification').textContent = item.justification;
            } else {
                document.getElementById('ragJustification').textContent = item.justification;
            }
        });

        // Display winner
        const winner = data.evaluation.final_winner;
        const reason = data.evaluation.reason;

        document.getElementById('winnerName').textContent = winner;
        document.getElementById('winnerReason').textContent = reason;

        // Display JSON output
        const jsonOutput = {
            question: data.question,
            answers: data.answers,
            evaluation: data.evaluation
        };

        document.getElementById('jsonOutput').textContent = JSON.stringify(jsonOutput, null, 2);
    }
});
