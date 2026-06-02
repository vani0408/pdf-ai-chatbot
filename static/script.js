function previewPDF(url){

    document
    .getElementById(
        "pdfViewer"
    )
    .src = url;
}


async function uploadPDF(){

    let fileInput =
        document.getElementById(
            "pdf"
        );

    if(
        fileInput.files.length === 0
    ){
        alert(
            "Please select PDFs"
        );
        return;
    }

    let formData =
        new FormData();

    let documentList =
        document.getElementById(
            "documentList"
        );

    documentList.innerHTML = "";

    for(
        let file
        of fileInput.files
    ){

        formData.append(
            "pdfs",
            file
        );

        let fileURL =
            URL.createObjectURL(
                file
            );

        documentList.innerHTML += `
            <div class="mb-2">

                <button
                    class="btn btn-outline-primary w-100"
                    onclick="previewPDF('${fileURL}')">

                    ${file.name}

                </button>

            </div>
        `;
    }

    previewPDF(
        URL.createObjectURL(
            fileInput.files[0]
        )
    );

    let response =
        await fetch(
            "/upload",
            {
                method:"POST",
                body:formData
            }
        );

    let data =
        await response.json();

    document
    .getElementById(
        "uploadStatus"
    )
    .innerHTML = `
        <div class="alert alert-success">

            ${data.message}

        </div>
    `;
}


function clearChat(){

    document
    .getElementById(
        "chatbox"
    )
    .innerHTML = "";

    document
    .getElementById(
        "historySidebar"
    )
    .innerHTML = `
        <p class="text-muted">
            No chats yet
        </p>
    `;
}


async function downloadChat(){

    const {
        jsPDF
    } = window.jspdf;

    const doc =
        new jsPDF();

    let text =
        document
        .getElementById(
            "chatbox"
        )
        .innerText;

    doc.text(
        text,
        10,
        10
    );

    doc.save(
        "chat_history.pdf"
    );
}


async function askQuestion(){

    let question =
        document
        .getElementById(
            "question"
        )
        .value;

    if(
        question.trim() === ""
    ){
        return;
    }

    let response =
        await fetch(
            "/chat",
            {
                method:"POST",

                headers:{
                    "Content-Type":
                    "application/json"
                },

                body:JSON.stringify({
                    question:question
                })
            }
        );

    let data =
        await response.json();

    let sourceHTML = "";

    for(
        let source
        of data.sources
    ){

        sourceHTML += `
            <div>

                <strong>
                    Document:
                </strong>

                ${source.file}

                <br>

                <strong>
                    Page:
                </strong>

                ${source.page}

            </div>

            <hr>
        `;
    }

    let excerpts =
        data.excerpt.join(
            "<hr>"
        );

    let chatbox =
        document.getElementById(
            "chatbox"
        );

    chatbox.innerHTML += `
        <div class="message">

            <div class="user">
                You:
            </div>

            <div>
                ${question}
            </div>

        </div>

        <div class="message">

            <div class="bot">
                AI:
            </div>

            <div>
                ${data.answer}
            </div>

            <div class="source-box">

                <strong>
                    Sources
                </strong>

                <br><br>

                ${sourceHTML}

                <strong>
                    Relevant Excerpts
                </strong>

                <br><br>

                ${excerpts}

            </div>

        </div>
    `;

    let sidebar =
        document.getElementById(
            "historySidebar"
        );

    if(
        sidebar.innerHTML.includes(
            "No chats yet"
        )
    ){
        sidebar.innerHTML = "";
    }

    sidebar.innerHTML += `
        <div
            class="border-bottom pb-2 mb-2">

            <strong>
                Q:
            </strong>

            ${question}

        </div>
    `;

    chatbox.scrollTop =
        chatbox.scrollHeight;

    document
    .getElementById(
        "question"
    )
    .value = "";
}