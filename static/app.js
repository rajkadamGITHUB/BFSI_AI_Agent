const messages =
    document.getElementById("messages");

const questionList =
    document.getElementById("questionList");

let allQuestions = [];

let chatHistory = [];


/* LOAD QUESTIONS */

async function loadQuestions() {

    try {

        const response =
            await fetch("/questions");

        if (!response.ok) {
            throw new Error("Failed to load questions");
        }

        const data =
            await response.json();

        allQuestions = data.questions;

        renderQuestions(allQuestions);

    } catch (error) {

        questionList.innerHTML = `
            <div class="loading">
                ❌ Unable to load banking questions.
            </div>
        `;

        console.error(error);
    }
}


/* DISPLAY QUESTIONS */

function renderQuestions(questions) {

    questionList.innerHTML = "";

    if (questions.length === 0) {

        questionList.innerHTML = `
            <div class="loading">
                No questions available.
            </div>
        `;

        return;
    }

    questions.forEach(question => {

        const button =
            document.createElement("button");

        button.className =
            "question-button";

        button.textContent =
            question.question;

        button.onclick =
            () => sendQuestion(question);

        questionList.appendChild(button);
    });
}


/* FILTER */

function filterQuestions(category, selectedButton) {

    document
        .querySelectorAll(".category")
        .forEach(button => {

            button.classList.remove("active");

        });


    selectedButton.classList.add("active");


    if (category === "all") {

        renderQuestions(allQuestions);

        return;
    }


    const filtered =
        allQuestions.filter(
            question =>
                question.category === category
        );


    renderQuestions(filtered);
}


/* SEND QUESTION */

async function sendQuestion(question) {

    removeWelcome();

    addMessage(
        question.question,
        "user"
    );

    disableQuestions(true);


    const loadingMessage =
        addLoadingMessage();


    try {

        const response =
            await fetch("/chat", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    question_id:
                        question.id,

                    history:
                        chatHistory

                })

            });


        const data =
            await response.json();


        removeLoadingMessage(
            loadingMessage
        );


        if (!response.ok) {

            addMessage(
                data.detail ||
                "Something went wrong.",
                "ai"
            );

            return;
        }


        addMessage(
            data.answer,
            "ai"
        );


        chatHistory.push({

            role: "user",

            content:
                question.question

        });


        chatHistory.push({

            role: "assistant",

            content:
                data.answer

        });


    } catch (error) {

        removeLoadingMessage(
            loadingMessage
        );

        addMessage(
            "Unable to connect to the AI service.",
            "ai"
        );

        console.error(error);

    } finally {

        disableQuestions(false);
    }
}


/* ADD MESSAGE */

function addMessage(text, sender) {

    const message =
        document.createElement("div");

    message.className =
        sender === "user"
            ? "message user-message"
            : "message ai-message";


    const avatar =
        document.createElement("div");

    avatar.className =
        sender === "user"
            ? "avatar user-avatar"
            : "avatar ai-avatar";


    avatar.textContent =
        sender === "user"
            ? "👤"
            : "🤖";


    const content =
        document.createElement("div");

    content.className =
        "message-content";


    content.textContent = text;


    message.appendChild(avatar);

    message.appendChild(content);


    messages.appendChild(message);


    messages.scrollTop =
        messages.scrollHeight;
}


/* LOADING MESSAGE */

function addLoadingMessage() {

    const message =
        document.createElement("div");

    message.className =
        "message ai-message";


    message.innerHTML = `
        <div class="avatar ai-avatar">
            🤖
        </div>

        <div class="message-content typing-indicator" role="status" aria-label="Reviewing your BFSI question">
            <span>BFSI</span>
            <span class="typing-dots" aria-hidden="true"><i></i><i></i><i></i></span>
        </div>
    `;


    messages.appendChild(message);

    messages.scrollTop =
        messages.scrollHeight;


    return message;
}


/* REMOVE LOADING */

function removeLoadingMessage(element) {

    if (element &&
        element.parentNode) {

        element.parentNode.removeChild(
            element
        );
    }
}


/* REMOVE WELCOME */

function removeWelcome() {

    const welcome =
        document.getElementById("welcome");

    if (welcome) {
        welcome.remove();
    }
}


/* DISABLE QUESTIONS */

function disableQuestions(disabled) {

    document
        .querySelectorAll(".question-button")
        .forEach(button => {

            button.disabled =
                disabled;

        });
}


/* NEW CHAT */

function newChat() {

    chatHistory = [];

    messages.innerHTML = `
        <div id="welcome" class="welcome">

            <div class="welcome-icon">
                🤖
            </div>

            <h2>
                How can I help you today?
            </h2>

            <p>
                Select a banking question below
                to get started.
            </p>

            <div class="welcome-info">

                <div>
                    <span>🔐</span>
                    <strong>Secure</strong>
                </div>

                <div>
                    <span>⚡</span>
                    <strong>Fast</strong>
                </div>

                <div>
                    <span>🏦</span>
                    <strong>BFSI Focused</strong>
                </div>

            </div>

        </div>
    `;
}


/* START */

loadQuestions();
