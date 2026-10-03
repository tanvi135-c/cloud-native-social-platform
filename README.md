# Cloud-Native Social Discussion Platform

A Reddit-inspired social discussion platform built to demonstrate
full-stack development, containerization, Kubernetes orchestration, and
infrastructure monitoring.

Users can register and log in, create discussion posts, comment, and
vote. The application is containerized with Docker and deployed to
Kubernetes using Minikube, with NGINX Ingress for routing and
Prometheus/Grafana for monitoring.

## Features

-   User registration and login with JWT-based authentication
-   Create, view, update, and delete discussion posts
-   Comment on posts
-   Upvote and downvote posts
-   PostgreSQL persistence
-   Responsive web interface
-   Dockerized frontend and backend
-   Kubernetes Deployments and Services
-   NGINX Ingress routing
-   Prometheus and Grafana monitoring

## Technology Stack

  Layer            Technologies
  ---------------- ------------------------------
  Frontend         HTML, CSS, JavaScript, NGINX
  Backend          Python, FastAPI
  Authentication   JWT, bcrypt
  Database         PostgreSQL
  Containers       Docker, Docker Compose
  Orchestration    Kubernetes, Minikube
  Routing          NGINX Ingress Controller
  Monitoring       Prometheus, Grafana
  Source control   Git, GitHub

## Architecture

``` text
                         Browser
                            |
                            v
                     NGINX Ingress
                       /       \
                      /         \
                     v           v
                 Frontend      FastAPI
                  (NGINX)        |
                                 v
                             PostgreSQL

               Kubernetes metrics and state
                           |
                           v
                       Prometheus
                           |
                           v
                        Grafana
```

## Repository Structure

``` text
cloud-native-social-platform/
├── backend/
│   ├── app/
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── create-post.html
│   ├── post.html
│   ├── app.js
│   └── style.css
├── k8s/
│   ├── backend.yaml
│   ├── frontend.yaml
│   ├── postgres.yaml
│   └── ingress.yaml
├── docker-compose.yml
└── README.md
```

*The exact filenames in your `k8s/` directory may differ depending on
how you organized your manifests.*

## Run Locally

### Prerequisites

-   Python 3.12 or later
-   PostgreSQL
-   Node-free static frontend (served with Python's HTTP server)
-   Docker Desktop (for container-based execution)
-   `kubectl`, Minikube, and Helm (for Kubernetes and monitoring)

### 1. Configure the backend

Open a terminal in the project directory, then:

``` bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/` and configure your local database
URL:

``` env
DATABASE_URL=postgresql://localhost/social_platform
```

Make sure PostgreSQL is running and the `social_platform` database
exists.

Start the API:

``` bash
uvicorn app.main:app --reload --port 8002
```

API base URL: `http://127.0.0.1:8002`

Interactive API documentation: `http://127.0.0.1:8002/docs`

Database health check: `http://127.0.0.1:8002/test-db`

### 2. Run the frontend

In a separate terminal:

``` bash
cd frontend
python3 -m http.server 5500
```

Open `http://127.0.0.1:5500` in your browser.

If your frontend is configured to call the Docker backend on port
`8000`, update its API base URL to match the backend URL you are using
locally. The backend CORS configuration must allow the frontend origin.

## Run with Docker Compose

From the repository root:

``` bash
docker compose up --build
```

To stop the services:

``` bash
docker compose down
```

To stop services and remove the Compose database volume (this deletes
persisted database data):

``` bash
docker compose down -v
```

The Compose setup exposes the backend on port `8000` and PostgreSQL on
port `5432`. The frontend exposure depends on the ports configured in
your Compose file.

## Deploy to Kubernetes with Minikube

### Prerequisites

Start Docker Desktop, then start Minikube:

``` bash
minikube start
```

If your Kubernetes manifests reference locally built images, build them
in Minikube's Docker environment:

``` bash
eval "$(minikube docker-env)"
docker build -t cloud-native-social-platform-backend:latest ./backend
docker build -t cloud-native-social-platform-frontend:latest ./frontend
```

Apply your manifests from the project root (adjust filenames if yours
differ):

``` bash
kubectl apply -f k8s/
```

Check resources:

``` bash
kubectl get pods
kubectl get services
kubectl get ingress
```

If the Ingress controller is not enabled, enable it:

``` bash
minikube addons enable ingress
```

On macOS with the Minikube Docker driver, the forwarding terminal must
remain open while you access the service. You can obtain a local URL
with:

``` bash
minikube service ingress-nginx-controller -n ingress-nginx --url
```

Open the first HTTP URL returned by the command. Keep that terminal
running.

## Monitoring with Prometheus and Grafana

The project uses the `kube-prometheus-stack` Helm chart to deploy
Prometheus, Grafana, Alertmanager, and Kubernetes metrics components.

Add and update the chart repository:

``` bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

Install the monitoring stack:

``` bash
helm install monitoring prometheus-community/kube-prometheus-stack
```

Check the pods:

``` bash
kubectl get pods
```

Forward Grafana to localhost:

``` bash
kubectl port-forward service/monitoring-grafana 3000:80
```

Open `http://127.0.0.1:3000`.

Retrieve the generated Grafana admin password:

``` bash
kubectl get secret monitoring-grafana \
  -o jsonpath="{.data.admin-password}" | base64 --decode
```

The default username is `admin`. Use the password returned by the
command. Prometheus is provisioned as a data source by the chart.

## API Overview

  ---------------------------------------------------------------------------------------
  Method            Endpoint                          Purpose           Authentication
  ----------------- --------------------------------- ----------------- -----------------
  `POST`            `/api/register`                   Register a user   No

  `POST`            `/api/login`                      Log in and        No
                                                      receive a token   

  `GET`             `/api/posts`                      List posts        No

  `GET`             `/api/posts/{post_id}`            Get a post        No

  `POST`            `/api/posts`                      Create a post     Yes

  `PUT`             `/api/posts/{post_id}`            Update your own   Yes
                                                      post              

  `DELETE`          `/api/posts/{post_id}`            Delete your own   Yes
                                                      post              

  `POST`            `/api/posts/{post_id}/comments`   Add a comment     Yes

  `GET`             `/api/posts/{post_id}/comments`   List comments     No

  `POST`            `/api/posts/{post_id}/vote`       Upvote (`1`) or   Yes
                                                      downvote (`-1`)   

  `GET`             `/api/posts/{post_id}/votes`      Get vote totals   No
  ---------------------------------------------------------------------------------------

The API prefix shown above reflects the Kubernetes Ingress
configuration. If running the backend directly, check the routes
configured in `backend/app/main.py`.

## Security Notes

-   Do not commit `.env` files, credentials, private keys, or Kubernetes
    secrets.
-   Replace development JWT secrets before any production deployment.
-   Use strong, unique database credentials outside local development.
-   Configure HTTPS and production-grade secret management before
    exposing the application publicly.

## Current Status and Future Improvements

Implemented: - Core social platform functionality - Docker
containerization - Kubernetes deployment on Minikube - Ingress-based
routing - Prometheus/Grafana monitoring - GitHub source repository

Planned improvements: - Automated CI/CD pipeline (GitLab CI/CD or GitHub
Actions) - Push versioned images to a container registry - Automated
Kubernetes deployment from the pipeline - Production deployment on AWS
EKS - Automated tests and application-specific metrics

## Author

**Tanvi Shendge**

Computer Science and Engineering \| Cloud Computing (AWS)
