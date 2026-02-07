const questionInput = document.getElementById('question');
const submitBtn = document.getElementById('submitBtn');
const responseSection = document.getElementById('responseSection');
const responseContent = document.getElementById('responseContent');
const ticketList = document.getElementById('ticketList');

submitBtn.addEventListener('click', handleSubmit);
questionInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        handleSubmit();
    }
});

function handleSubmit() {
    const question = questionInput.value.trim();
    
    if (!question) {
        alert('Please enter a question');
        return;
    }

    // Show loading state
    submitBtn.disabled = true;
    submitBtn.textContent = 'Processing...';
    responseSection.classList.add('visible');
    responseContent.innerHTML = '<div class="loading">Analyzing your question</div>';
    ticketList.innerHTML = '';

    // Make API call to Flask backend
    fetch('/api/question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question: question
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Display the response
        const responseData = {
            answer: data.answer,
            tickets: data.tickets || [] // If your backend returns tickets, otherwise empty array
        };
        displayResponse(responseData);
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit Query';
    })
    .catch(error => {
        console.error('Error:', error);
        responseContent.innerHTML = '<div style="color: #dc3545;">An error occurred while processing your request. Please try again.</div>';
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit Query';
    });
}

function displayResponse(data) {
    let answer = data.answer;
    let tickets = data.tickets || [];
    
    // Extract ticket numbers from the answer text
    const ticketPattern = /(Relevant ticket numbers:)\s*\n?\s*(?:\d+\.\s*)?(IT-\d+(?:\s*,?\s*\n?\s*(?:\d+\.\s*)?IT-\d+)*)/gi;
    const ticketMatches = answer.match(ticketPattern);
    console.log("TICKET MATCHES: ", ticketMatches);
    
    if (ticketMatches) {
        // Extract individual ticket IDs
        const ticketIds = [];
        ticketMatches.forEach(match => {
            const ids = match.match(/IT-\d+/g);
            if (ids) {
                ticketIds.push(...ids);
            }
        });
        
        // Remove the ticket section from the answer
        answer = answer.replace(/(Relevant ticket numbers:)\s*\n?\s*(?:\d+\.\s*)?(IT-\d+(?:\s*,?\s*\n?\s*(?:\d+\.\s*)?IT-\d+)*)/gi, '').trim();
        
        // Create ticket objects from the extracted IDs
        ticketIds.forEach(id => {
            tickets.push({
                id: id,
                title: "Related incident",
                url: `#ticket-${id}`,
                date: new Date().toISOString().split('T')[0]
            });
        });
    }

    console.log("Tickets after extraction: ", tickets);
    
    // Convert **text** to <strong>text</strong> for bold formatting
    answer = answer.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert newlines to <br> tags for proper line breaks
    answer = answer.replace(/\n/g, '<br>');
    
    // Display answer with HTML rendering
    responseContent.innerHTML = answer;

    // Display related tickets
    if (tickets && tickets.length > 0) {
        ticketList.innerHTML = tickets.map(ticket => `
            <li class="ticket-item">
                <a href="${ticket.url}" class="ticket-link">${ticket.id}: ${ticket.title}</a>
                <div class="ticket-meta">${ticket.date}</div>
            </li>
        `).join('');
    } else {
        ticketList.innerHTML = '<li class="ticket-item" style="border: none;">No related tickets found</li>';
    }
}