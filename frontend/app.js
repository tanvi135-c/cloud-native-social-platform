const API_URL = "/api";


// =========================================================
// AUTH HELPERS
// =========================================================

function getToken() {
    return localStorage.getItem("access_token");
}


function isLoggedIn() {
    return !!getToken();
}


function logout() {

    localStorage.removeItem("access_token");

    window.location.href = "login.html";
}


// =========================================================
// SIDEBAR USER
// =========================================================

function updateSidebar() {

    const usernameElement =
        document.getElementById("sidebar-username");

    if (!usernameElement) {
        return;
    }

    if (isLoggedIn()) {

        usernameElement.textContent = "Tanvi";

        const status =
            document.getElementById("sidebar-status");

        if (status) {
            status.textContent = "Online";
        }

    } else {

        usernameElement.textContent = "Guest";

    }
}


// =========================================================
// LOAD POSTS
// =========================================================

async function loadPosts() {

    const container =
        document.getElementById("posts-container");

    if (!container) {
        return;
    }

    try {

        const response =
            await fetch(`${API_URL}/posts`);

        if (!response.ok) {
            throw new Error("Unable to load posts");
        }

        const posts =
            await response.json();

        const count =
            document.getElementById("discussion-count");

        if (count) {
            count.textContent = posts.length;
        }

        if (posts.length === 0) {

            container.innerHTML = `
                <div class="post-card">
                    <p class="post-content">
                        No discussions yet.
                        Be the first to start one!
                    </p>
                </div>
            `;

            return;
        }

        container.innerHTML = "";

        posts.forEach(post => {

            const element =
                document.createElement("div");

            element.className = "post-card";

            element.innerHTML = `

                <div class="post-header">

                    <div class="post-avatar">
                        U${post.user_id}
                    </div>

                    <div class="post-author">

                        <strong>
                            User ${post.user_id}
                        </strong>

                        <span>
                            Community member
                        </span>

                    </div>

                </div>


                <h3>
                    ${escapeHtml(post.title)}
                </h3>


                <p class="post-content">
                    ${escapeHtml(post.content)}
                </p>


                <div class="post-actions">

                    <button
                        class="action-btn"
                        onclick="vote(${post.id}, 1)">

                        👍 Upvote

                    </button>


                    <button
                        class="action-btn"
                        onclick="vote(${post.id}, -1)">

                        👎 Downvote

                    </button>


                    <a
                        href="post.html?id=${post.id}"
                        class="view-post">

                        View discussion →

                    </a>

                </div>

            `;

            container.appendChild(element);

        });

    } catch (error) {

        container.innerHTML = `
            <div class="post-card">
                <p class="post-content">
                    Unable to connect to the backend.
                    Make sure Docker is running.
                </p>
            </div>
        `;

        console.error(error);
    }
}


// =========================================================
// LOGIN
// =========================================================

const loginForm =
    document.getElementById("login-form");

if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const email =
                document.getElementById("login-email").value;

            const password =
                document.getElementById("login-password").value;

            const message =
                document.getElementById("login-message");

            message.textContent = "Logging in...";

            try {

                const response =
                    await fetch(`${API_URL}/login`, {

                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            email: email,
                            password: password
                        })

                    });


                const data =
                    await response.json();


                if (!response.ok) {

                    message.textContent =
                        data.detail || "Login failed.";

                    return;
                }


                localStorage.setItem(
                    "access_token",
                    data.access_token
                );


                message.textContent =
                    "Login successful!";


                setTimeout(() => {

                    window.location.href =
                        "index.html";

                }, 500);


            } catch (error) {

                message.textContent =
                    "Unable to connect to server.";

                console.error(error);
            }

        }
    );
}


// =========================================================
// REGISTER
// =========================================================

const registerForm =
    document.getElementById("register-form");

if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const username =
                document.getElementById(
                    "register-username"
                ).value;

            const email =
                document.getElementById(
                    "register-email"
                ).value;

            const password =
                document.getElementById(
                    "register-password"
                ).value;

            const message =
                document.getElementById(
                    "register-message"
                );

            message.textContent =
                "Creating account...";


            try {

                const response =
                    await fetch(
                        `${API_URL}/register`,
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                username,
                                email,
                                password
                            })

                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    message.textContent =
                        data.detail ||
                        "Registration failed.";

                    return;
                }


                message.textContent =
                    "Account created successfully!";


                setTimeout(() => {

                    window.location.href =
                        "login.html";

                }, 700);


            } catch (error) {

                message.textContent =
                    "Unable to connect to server.";

                console.error(error);
            }

        }
    );
}


// =========================================================
// CREATE POST
// =========================================================

const createPostForm =
    document.getElementById(
        "create-post-form"
    );

if (createPostForm) {

    createPostForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const token = getToken();


            if (!token) {

                window.location.href =
                    "login.html";

                return;
            }


            const title =
                document.getElementById(
                    "post-title"
                ).value;

            const content =
                document.getElementById(
                    "post-content"
                ).value;

            const message =
                document.getElementById(
                    "post-message"
                );


            message.textContent =
                "Publishing...";


            try {

                const response =
                    await fetch(
                        `${API_URL}/posts`,
                        {

                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/json",

                                "Authorization":
                                    `Bearer ${token}`

                            },

                            body: JSON.stringify({
                                title,
                                content
                            })

                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    message.textContent =
                        data.detail ||
                        "Unable to create post.";

                    return;
                }


                message.textContent =
                    "Discussion published!";


                setTimeout(() => {

                    window.location.href =
                        `post.html?id=${data.id}`;

                }, 600);


            } catch (error) {

                message.textContent =
                    "Unable to connect to server.";

                console.error(error);
            }

        }
    );
}


// =========================================================
// VOTE
// =========================================================

async function vote(postId, value) {

    const token = getToken();


    if (!token) {

        alert(
            "Please login before voting."
        );

        window.location.href =
            "login.html";

        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/posts/${postId}/vote`,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Authorization":
                            `Bearer ${token}`

                    },

                    body: JSON.stringify({
                        value
                    })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                data.detail ||
                "Unable to record vote."
            );

            return;
        }


        alert("Vote recorded successfully!");


    } catch (error) {

        console.error(error);

        alert(
            "Unable to connect to server."
        );
    }
}


// =========================================================
// SINGLE POST
// =========================================================

async function loadSinglePost() {

    const container =
        document.getElementById(
            "single-post-container"
        );


    if (!container) {
        return;
    }


    const params =
        new URLSearchParams(
            window.location.search
        );


    const postId =
        params.get("id");


    if (!postId) {

        container.innerHTML =
            "<p>Post not found.</p>";

        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/posts/${postId}`
            );


        if (!response.ok) {
            throw new Error("Post not found");
        }


        const post =
            await response.json();


        container.innerHTML = `

            <article class="post-card">

                <div class="post-header">

                    <div class="post-avatar">
                        U${post.user_id}
                    </div>

                    <div class="post-author">

                        <strong>
                            User ${post.user_id}
                        </strong>

                        <span>
                            Community member
                        </span>

                    </div>

                </div>


                <h3>
                    ${escapeHtml(post.title)}
                </h3>


                <p class="post-content">
                    ${escapeHtml(post.content)}
                </p>


                <div class="post-actions">

                    <button
                        class="action-btn"
                        onclick="vote(${post.id}, 1)">

                        👍 Upvote

                    </button>


                    <button
                        class="action-btn"
                        onclick="vote(${post.id}, -1)">

                        👎 Downvote

                    </button>

                </div>

            </article>

        `;


        loadComments(postId);


    } catch (error) {

        container.innerHTML = `
            <div class="post-card">
                <p class="post-content">
                    Unable to load this discussion.
                </p>
            </div>
        `;

        console.error(error);
    }
}


// =========================================================
// COMMENTS
// =========================================================

async function loadComments(postId) {

    const container =
        document.getElementById(
            "comments-container"
        );


    if (!container) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/posts/${postId}/comments`
            );


        const comments =
            await response.json();


        if (comments.length === 0) {

            container.innerHTML = `
                <div class="comment">
                    <p class="comment-text">
                        No comments yet.
                        Start the conversation!
                    </p>
                </div>
            `;

            return;
        }


        container.innerHTML = "";


        comments.forEach(comment => {

            const element =
                document.createElement("div");

            element.className = "comment";


            element.innerHTML = `

                <div class="comment-user">
                    User ${comment.user_id}
                </div>

                <p class="comment-text">
                    ${escapeHtml(comment.content)}
                </p>

            `;


            container.appendChild(element);

        });


    } catch (error) {

        console.error(error);

    }
}


// =========================================================
// ADD COMMENT
// =========================================================

const commentForm =
    document.getElementById(
        "comment-form"
    );


if (commentForm) {

    commentForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const token =
                getToken();


            if (!token) {

                alert(
                    "Please login to comment."
                );

                window.location.href =
                    "login.html";

                return;
            }


            const params =
                new URLSearchParams(
                    window.location.search
                );


            const postId =
                params.get("id");


            const content =
                document.getElementById(
                    "comment-content"
                ).value;


            try {

                const response =
                    await fetch(
                        `${API_URL}/posts/${postId}/comments`,
                        {

                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/json",

                                "Authorization":
                                    `Bearer ${token}`

                            },

                            body: JSON.stringify({
                                content
                            })

                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    alert(
                        data.detail ||
                        "Unable to add comment."
                    );

                    return;
                }


                document.getElementById(
                    "comment-content"
                ).value = "";


                loadComments(postId);


            } catch (error) {

                console.error(error);

                alert(
                    "Unable to connect to server."
                );
            }

        }
    );
}


// =========================================================
// DASHBOARD
// =========================================================

async function loadDashboard() {

    const container =
        document.getElementById(
            "dashboard-posts"
        );


    if (!container) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/posts`
            );


        const posts =
            await response.json();


        const count =
            document.getElementById(
                "dashboard-post-count"
            );


        if (count) {
            count.textContent =
                posts.length;
        }


        const apiStatus =
            document.getElementById(
                "api-status"
            );


        if (apiStatus) {

            apiStatus.textContent =
                response.ok
                    ? "Online"
                    : "Offline";
        }


        if (posts.length === 0) {

            container.innerHTML =
                `<p class="loading">
                    No discussions yet.
                </p>`;

            return;
        }


        container.innerHTML = "";


        posts.slice(0, 5).forEach(post => {

            const element =
                document.createElement("div");


            element.className =
                "post-card";


            element.innerHTML = `

                <h3>
                    ${escapeHtml(post.title)}
                </h3>

                <p class="post-content">
                    ${escapeHtml(post.content)}
                </p>

                <div class="post-actions">

                    <a
                        href="post.html?id=${post.id}"
                        class="view-post">

                        Open discussion →

                    </a>

                </div>

            `;


            container.appendChild(element);

        });


    } catch (error) {

        const apiStatus =
            document.getElementById(
                "api-status"
            );


        if (apiStatus) {
            apiStatus.textContent =
                "Offline";
        }


        console.error(error);
    }
}


// =========================================================
// HTML SECURITY
// =========================================================

function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent =
        text;

    return div.innerHTML;
}


// =========================================================
// INITIALIZE
// =========================================================

updateSidebar();

loadPosts();

loadSinglePost();

loadDashboard();