[1] Create Django Web Framework app
    [1.1] Set Up Your Environment
    [1.2] Create Project `interview` and App `app`.
        [1.2.1] Configure Settings INSTALLED_APPS 
        [1.2.2] Create BaseModel and Topic/Question Model
        [1.2.3] Create Serializers
        [1.2.4] Create Views
        [1.2.5] Configure URLs
        [1.2.6] Register Models in Admin
        [1.2.7] Create and Run Migrations
        [1.2.8] Create Superuser (admin/admin)
        [1.2.9] Apply `Authentication by JWT`
        [1.2.10] Apply `ASVS level 2`
            - corsheaders
            - token_blacklist
            - JWT token
            - Logging
        [1.2.11] Docker containerization
            - Set up docker file, docker-compose.yml file, entrypoint.sh
            - Set up Postgres Database docker
            - Set up nginx.conf 


        postgres, docker, nginx, gunicorn, wsl, redis, minio, celery, microservices


[2] Answer Interview Question
    [2.1] Python 
        [2.1.1] What is Python?
            - Python is an `object-oriented`, high-level programming language.
            - Python is an `interpreted language` because `we do not manually compile code files before running them`. However, behind the scence, Python first compiles the source code into bytecode, and then the Python Virtual Machine (PVM) interprets that bytecode at runtime.
            - High-level refer to how close a programming language is to human language rather than machine language    
    [2.2] Django REST API Framework
        [2.2.1] What is Django Framework?
            - Django is a high-level Python web framework that enables rapid development of secure and scalable web application
            - Key Value:
                - Fullstack web application
                - Follow MVT architecture 
                - Rapid development of secure and scalable app 
        [2.2.2] What is Django RESTful API?
            - A Django RESTful API is a web API built using Django and Django REST Framework (DRF) that follows `REST (Representational State Transfer) principles` to allow clients (web apps, mobile apps, other services) to communicate with a backend server using HTTP.
    [2.3] ASVS
        [2.3.1] What is ASVS?
            - ASVS (`Application security verification standard`) is a security standard pushlished by OWSAP that defines `security requirements and controls` for web applications and APIs
        [2.3.2] ASVS level
            - Level 1: 80–90% of applications, Public websites
            - Level 2: `Apps with sensitive data`, `Business-critical systems`
            - Level 3: Banking/Finance, Government systems

