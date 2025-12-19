\# PKI-Based 2FA System (Dockerized FastAPI)



\## Overview

This project implements a PKI-backed Two-Factor Authentication (2FA) system using FastAPI and Docker.  

It supports secure seed decryption using RSA private keys and time-based OTP generation and verification.



---



\## Features

\- RSA-based encrypted seed decryption

\- Persistent seed storage inside container

\- TOTP generation (RFC 6238)

\- TOTP verification with ±30s tolerance

\- Fully containerized using Docker \& Docker Compose



---



\## API Endpoints



\### POST /decrypt-seed

Decrypts a base64-encoded encrypted seed using the student private key and stores it.



\*\*Request Body\*\*

```json

{

&nbsp; "encrypted\_seed": "<base64\_string>"

}



Response



{ "status": "ok" }



GET /generate-2fa



Generates the current TOTP code from the stored seed.



Response



{

&nbsp; "code": "123456",

&nbsp; "valid\_for": 30

}



POST /verify-2fa



Verifies a submitted TOTP code with ±1 time window tolerance.



Request Body



{

&nbsp; "code": "123456"

}





Response



{

&nbsp; "valid": true

}



Setup Instructions

Prerequisites



Docker



Docker Compose



Build \& Run

docker-compose build

docker-compose up





The API will be available at:



http://localhost:8080





Swagger UI:



http://localhost:8080/docs

